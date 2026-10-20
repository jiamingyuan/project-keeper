"""Behavioral checks in isolated temporary projects; no live project mutation."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "project_keeper.py"
spec = importlib.util.spec_from_file_location("keeper", SCRIPT)
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)


def sample_body(action, text):
    return pk.format_log(action, {title: text for title in pk.log_fields(action)})


class KeeperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="project-keeper-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        pk.init(self.root, "样例项目")

    def get(self, rel):
        return pk.read(self.root, rel)

    def set(self, rel, value):
        pk.write(self.root, rel, value)

    def ready(self, v="V1.0"):
        pk.create_version(self.root, v, "样例项目")
        for name in pk.VERSION_DOCS[1:]:
            pk.scaffold(self.root, v, "样例项目", name)
        self.root.joinpath("app.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
        self.root.joinpath("test_app.py").write_text("from app import add\nassert add(1, 2) == 3\n", encoding="utf-8")
        req = self.get(v + "/requirements.md").replace("待确认：用户判断交付满足要求的标准。", "add(1, 2) 返回 3。")
        self.set(v + "/requirements.md", req)
        self.set(v + "/spec.md", self.get(v + "/spec.md").replace("状态：draft，尚不能据此执行。", "状态：ready；样例任务实现 add。"))
        result = subprocess.run([sys.executable, "test_app.py"], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.set(v + "/test-results.md", self.get(v + "/test-results.md") + "\n### 样例批次\n\n实际执行 python test_app.py，exit=0；add(1,2)=3。\n")
        pk.record(self.root, v, "code", "code-" + v, sample_body("code-execute", "样例实现和开发验证完成"), ["app.py", "test_app.py"])
        pk.record(self.root, v, "test", "test-" + v, sample_body("test-execute", "实际测试退出码 0；完整输出见测试结果"))
        return v

    def proposal(self, v="V1.0", changed=True):
        updates = {}
        for rel in (v + "/requirements.md", "project-brief.md", "architecture.md", "roadmap.md"):
            before = self.get(rel)
            after = before
            if rel == v + "/requirements.md":
                after = before.replace("尚未完成。关闭时记录交付、用户验收及依据、遗留与延期项、操作记录入口。", "交付 add；无本轮遗留；用户已确认。")
            elif changed:
                after += "\n样例版本已验证的描述变化。\n"
            updates[rel] = {"before_sha256": pk.digest(before), "after": after}
        return {"acceptance": {"confirmed": True, "statement": "我验收通过了", "source": "样例用户输入"},
                "roadmap_sources": {"todo": {"statement": "请将样例任务状态更新为已验证", "source": "样例用户输入"}} if changed else {},
                "summary": "按实际样例交付同步，未声明部署", "updates": updates}

    def close(self, v="V1.0", op="close-1", changed=True):
        pk.prepare(self.root, v, op, self.proposal(v, changed))
        return pk.apply_close(self.root, v, op)

    def test_init_incomplete_and_reserved_config(self):
        self.assertIn("待确认", self.get("project-brief.md"))
        self.assertTrue(all(not l.strip() or l.startswith("#") for l in self.get("config.toml").splitlines()))
        self.assertEqual(pk.states(self.root), {})
        self.assertTrue(pk.validate(self.root)["valid"])

    def test_reinit_preserves_existing_content(self):
        self.set("project-brief.md", "已有用户文档")
        result = pk.init(self.root, "另一个名字")
        self.assertEqual(self.get("project-brief.md"), "已有用户文档")
        self.assertIn("project-brief.md", result["reused"])

    def test_discovery_and_nested_ambiguity(self):
        nested = self.root / "src"
        nested.mkdir()
        self.assertEqual(pk.root_path(cwd=nested), self.root)
        pk.init(nested, "nested")
        with self.assertRaises(pk.KeeperError):
            pk.root_path(cwd=nested)
        self.assertEqual(pk.root_path(str(nested)), nested)

    def test_project_isolation(self):
        other = self.root / "other"
        other.mkdir()
        pk.init(other, "other")
        before = pk.read(other, "log.md")
        pk.append_log(self.root, "a", "project-update", sample_body("project-update", "only first"))
        self.assertEqual(pk.read(other, "log.md"), before)

    def test_paths_and_symlinks_rejected(self):
        for value in ("../escape.md", "/tmp/escape.md", "V1.0/../../escape", "x\\y"):
            with self.assertRaises(pk.KeeperError):
                pk.path(self.root, value)
        outside = self.root / "outside"
        outside.mkdir()
        self.root.joinpath("pjkp", "linked").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(pk.KeeperError):
            self.set("linked/a.md", "bad")
        self.assertFalse((outside / "a.md").exists())

    def test_pjkp_root_symlink_rejected(self):
        other = self.root / "other"
        other.mkdir()
        (other / "pjkp").symlink_to(self.root / "pjkp", target_is_directory=True)
        with self.assertRaises(pk.KeeperError):
            pk.root_path(other)

    def test_version_creation_staged_and_resume(self):
        result = pk.create_version(self.root, "V0.1", "样例")
        self.assertTrue(result["created"])
        self.assertFalse(pk.path(self.root, "V0.1/spec.md").exists())
        before = self.get("V0.1/requirements.md")
        self.assertFalse(pk.create_version(self.root, "V0.1", "样例")["created"])
        self.assertEqual(before, self.get("V0.1/requirements.md"))
        for version in ("v1.0", "V01.0", "V1.0/../V2.0", "V1.2.3"):
            with self.assertRaises(pk.KeeperError):
                pk.create_version(self.root, version, "样例")

    def test_stage_validation(self):
        pk.create_version(self.root, "V1.0", "样例")
        self.assertTrue(pk.validate(self.root, "V1.0")["valid"])
        self.assertFalse(pk.validate(self.root, "V1.0", "plan")["valid"])
        for name in ("spec.md", "test-plan.md"):
            pk.scaffold(self.root, "V1.0", "样例", name)
        self.assertTrue(pk.validate(self.root, "V1.0", "plan")["valid"])
        self.assertFalse(pk.validate(self.root, "V1.0", "close")["valid"])

    def test_log_idempotence_and_correction(self):
        body = sample_body("project-update", "- a\n- b")
        self.assertTrue(pk.append_log(self.root, "e1", "project-update", body)["appended"])
        before = self.get("log.md")
        self.assertFalse(pk.append_log(self.root, "e1", "project-update", body)["appended"])
        self.assertEqual(before, self.get("log.md"))
        with self.assertRaises(pk.KeeperError):
            pk.append_log(self.root, "e1", "project-update", sample_body("project-update", "不同结果"))
        pk.append_log(self.root, "e2", "correction", sample_body("correction", "更正 e1"), parent="e1")
        self.assertTrue(self.get("log.md").startswith(before))
        self.assertTrue(pk.validate(self.root)["valid"])

    def test_context_returns_navigation_not_bodies(self):
        data = pk.inventory(self.root)
        self.assertFalse(any("text" in f for f in data["files"]))
        self.assertEqual({f["path"] for f in data["files"]}, {"pjkp/" + f for f in (*pk.PROJECT_DOCS, "config.toml")})
        text = "# A\n\n## B\nkeep\n```\n## C\n```\n\n## D\nother\n"
        self.assertIn("## C", pk.section(text, "B"))
        self.assertNotIn("other", pk.section(text, "B"))

    def test_record_and_real_sample_test(self):
        self.ready()
        self.assertEqual(pk.readiness(self.root, "V1.0"), [])
        self.assertEqual(pk.get_state(self.get("V1.0/requirements.md"))["phase"], "awaiting-acceptance")
        self.assertTrue(pk.validate(self.root, "V1.0", "test")["valid"])

    def test_changed_requirements_invalidate_execution(self):
        self.ready()
        self.set("V1.0/requirements.md", self.get("V1.0/requirements.md").replace("返回 3", "返回 4"))
        self.assertTrue(pk.readiness(self.root, "V1.0"))
        with self.assertRaises(pk.KeeperError):
            self.close()

    def test_changed_code_invalidates_test_and_close(self):
        self.ready()
        (self.root / "app.py").write_text("def add(a,b): return 0\n")
        self.assertTrue(any("实现" in x for x in pk.readiness(self.root, "V1.0")))
        with self.assertRaises(pk.KeeperError):
            self.close()

    def test_new_code_record_invalidates_old_test(self):
        self.ready()
        pk.record(self.root, "V1.0", "code", "code-second", sample_body("code-execute", "重新核查"), ["app.py", "test_app.py"])
        self.assertIsNone(pk.get_state(self.get("V1.0/requirements.md"))["test"])

    def test_cannot_reuse_record_id_for_changed_basis(self):
        self.ready()
        self.set("V1.0/spec.md", self.get("V1.0/spec.md") + "\n变化\n")
        with self.assertRaises(pk.KeeperError):
            pk.record(self.root, "V1.0", "code", "code-V1.0", sample_body("code-execute", "新结果"), ["app.py"])

    def test_no_acceptance_no_close(self):
        self.ready()
        proposal = self.proposal()
        proposal["acceptance"]["confirmed"] = False
        with self.assertRaises(pk.KeeperError):
            pk.prepare(self.root, "V1.0", "close-1", proposal)
        self.assertIsNone(pk.get_state(self.get("V1.0/requirements.md"))["closed_by"])

    def test_no_execution_cannot_close_with_confirmation(self):
        pk.create_version(self.root, "V1.0", "样例")
        with self.assertRaises(pk.KeeperError):
            pk.prepare(self.root, "V1.0", "close-1", self.proposal())

    def test_stale_proposal_rejected(self):
        self.ready()
        proposal = self.proposal()
        self.set("roadmap.md", self.get("roadmap.md") + "\n新工作\n")
        with self.assertRaises(pk.KeeperError):
            pk.prepare(self.root, "V1.0", "close-1", proposal)

    def test_close_and_undo_preserve_code_tests_and_history(self):
        self.ready()
        source = (self.root / "app.py").read_bytes()
        tests = self.get("V1.0/test-results.md")
        brief = self.get("project-brief.md")
        self.assertEqual(self.close()["status"], "applied")
        closed_log = self.get("log.md")
        op = pk.load_operation(self.root, "V1.0", "close-1")
        self.assertIn("用户验收", op["files"]["V1.0/requirements.md"]["after"])
        result = pk.undo_close(self.root, "V1.0", "close-1", "用户要求重新打开")
        self.assertEqual(result["status"], "undone")
        self.assertEqual(brief, self.get("project-brief.md"))
        self.assertEqual(tests, self.get("V1.0/test-results.md"))
        self.assertEqual(source, (self.root / "app.py").read_bytes())
        self.assertTrue(self.get("log.md").startswith(closed_log))
        self.assertIn("最近完成版本：暂无", self.get("index.md"))
        self.assertTrue(pk.validate(self.root, "V1.0", "test")["valid"])

    def test_repeat_apply_does_not_overwrite_later_edits(self):
        self.ready()
        self.close()
        self.set("architecture.md", self.get("architecture.md") + "\n新的用户编辑\n")
        changed = self.get("architecture.md")
        before_log = self.get("log.md")
        pk.apply_close(self.root, "V1.0", "close-1")
        self.assertEqual(changed, self.get("architecture.md"))
        self.assertEqual(before_log, self.get("log.md"))

    def test_partial_close_and_resume(self):
        self.ready()
        pk.prepare(self.root, "V1.0", "close-1", self.proposal())
        before = self.get("roadmap.md")
        self.set("roadmap.md", before + "\n并发修改\n")
        self.assertEqual(pk.apply_close(self.root, "V1.0", "close-1")["status"], "partial")
        self.assertIn("并发修改", self.get("roadmap.md"))
        self.set("roadmap.md", before)  # fixture simulates user resolving the conflict
        self.assertEqual(pk.apply_close(self.root, "V1.0", "close-1")["status"], "applied")

    def test_close_process_interruption_resume(self):
        self.ready()
        pk.prepare(self.root, "V1.0", "close-1", self.proposal())
        real_write = pk.write
        def interrupt(root, rel, text, expected=None):
            if rel == "architecture.md":
                raise OSError("simulated interruption")
            return real_write(root, rel, text, expected)
        with patch.object(pk, "write", interrupt):
            with self.assertRaises(OSError):
                pk.apply_close(self.root, "V1.0", "close-1")
        self.assertEqual(pk.operation_status(self.root, "V1.0", "close-1")["status"], "applying")
        self.assertEqual(pk.apply_close(self.root, "V1.0", "close-1")["status"], "applied")

    def test_post_prepare_implementation_change_stops_apply(self):
        self.ready()
        pk.prepare(self.root, "V1.0", "close-1", self.proposal())
        (self.root / "app.py").write_text("changed\n")
        with self.assertRaises(pk.KeeperError):
            pk.apply_close(self.root, "V1.0", "close-1")

    def test_undo_conflict_resolution_preserves_new_work(self):
        self.ready()
        brief_before = self.get("project-brief.md")
        self.close()
        self.set("project-brief.md", self.get("project-brief.md") + "\n后续独立能力\n")
        changed = self.get("project-brief.md")
        result = pk.undo_close(self.root, "V1.0", "close-1", "重开")
        self.assertEqual(result["status"], "undo-partial")
        self.assertEqual(changed, self.get("project-brief.md"))
        merged = brief_before + "\n后续独立能力\n"
        pk.resolve_undo(self.root, "V1.0", "close-1", {"project-brief.md": {"current_sha256": pk.digest(changed), "merged": merged, "reason": "保留独立能力，仅撤销本次摘要"}})
        self.assertEqual(pk.undo_close(self.root, "V1.0", "close-1", "完成合并")["status"], "undone")
        self.assertEqual(merged, self.get("project-brief.md"))

    def test_repeated_undo_and_reclose(self):
        self.ready()
        self.close()
        pk.undo_close(self.root, "V1.0", "close-1", "重开")
        before = self.get("log.md")
        self.assertTrue(pk.undo_close(self.root, "V1.0", "close-1", "重复")["already_undone"])
        self.assertEqual(before, self.get("log.md"))
        self.close(op="close-2")
        pk.undo_close(self.root, "V1.0", "close-1", "旧撤销")
        self.assertEqual(pk.get_state(self.get("V1.0/requirements.md"))["closed_by"], "close-2")

    def test_index_preserves_other_versions_and_manual_notes(self):
        self.ready()
        self.close()
        pk.create_version(self.root, "V1.1", "样例")
        self.set("index.md", self.get("index.md") + "\n额外用户记录\n")
        pk.undo_close(self.root, "V1.0", "close-1", "重开")
        self.assertIn("V1.1", self.get("index.md"))
        self.assertIn("额外用户记录", self.get("index.md"))

    def test_later_closure_requires_semantic_review(self):
        self.ready("V1.0")
        self.close("V1.0", "close-1")
        self.ready("V1.1")
        self.close("V1.1", "close-2", changed=False)
        result = pk.undo_close(self.root, "V1.0", "close-1", "重开旧版")
        self.assertIn("project-brief.md", result["conflicts"])
        self.assertIn("最近完成版本：V1.1", self.get("index.md"))

    def test_malicious_operation_target_and_corrupt_snapshot_rejected(self):
        self.ready()
        pk.prepare(self.root, "V1.0", "close-1", self.proposal())
        op = pk.load_operation(self.root, "V1.0", "close-1")
        op["files"]["../app.py"] = op["files"].pop("architecture.md")
        pk.save_operation(self.root, op)
        with self.assertRaises(pk.KeeperError):
            pk.apply_close(self.root, "V1.0", "close-1")

    def test_lock_and_cli_readonly(self):
        with pk.lock(self.root):
            with self.assertRaises(pk.KeeperError):
                with pk.lock(self.root):
                    pass
        log = self.get("log.md")
        result = subprocess.run([sys.executable, str(SCRIPT), "--project", str(self.root), "context"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["initialized"])
        self.assertEqual(log, self.get("log.md"))

    def test_undo_recovers_after_document_write_before_journal_save(self):
        self.ready()
        self.close()
        real_write = pk.write
        def interrupt(root, rel, text, expected=None):
            real_write(root, rel, text, expected)
            if rel == "V1.0/requirements.md":
                raise OSError("after target write")
        with patch.object(pk, "write", interrupt):
            with self.assertRaises(OSError):
                pk.undo_close(self.root, "V1.0", "close-1", "模拟中断")
        self.assertEqual(pk.undo_close(self.root, "V1.0", "close-1", "恢复")["status"], "undone")

    def test_undo_repairs_missing_completion_log(self):
        self.ready()
        self.close()
        with patch.object(pk, "append_log", side_effect=OSError("log interrupted")):
            with self.assertRaises(OSError):
                pk.undo_close(self.root, "V1.0", "close-1", "重开")
        self.assertEqual(pk.load_operation(self.root, "V1.0", "close-1")["status"], "undone")
        before = self.get("log.md")
        pk.undo_close(self.root, "V1.0", "close-1", "恢复")
        self.assertGreater(len(self.get("log.md")), len(before))
        after = self.get("log.md")
        pk.undo_close(self.root, "V1.0", "close-1", "重复")
        self.assertEqual(after, self.get("log.md"))

    def test_close_repairs_missing_completion_log(self):
        self.ready()
        pk.prepare(self.root, "V1.0", "close-1", self.proposal())
        with patch.object(pk, "append_log", side_effect=OSError("log interrupted")):
            with self.assertRaises(OSError):
                pk.apply_close(self.root, "V1.0", "close-1")
        pk.apply_close(self.root, "V1.0", "close-1")
        actions = [m["action"] for m, _ in pk.log_entries(self.get("log.md"))]
        self.assertEqual(actions.count("version-close"), 1)
        self.assertEqual(actions.count("project-update"), 1)

    def test_operation_path_symlink_rejected(self):
        self.ready()
        outside = self.root / "outside"
        outside.mkdir()
        pk.path(self.root, "V1.0/.operations").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(pk.KeeperError):
            pk.prepare(self.root, "V1.0", "close-1", self.proposal())
        self.assertEqual(list(outside.iterdir()), [])

    def test_closed_version_cannot_continue_without_undo(self):
        self.ready()
        self.close()
        with self.assertRaises(pk.KeeperError):
            pk.create_version(self.root, "V1.0", "样例")
        with self.assertRaises(pk.KeeperError):
            pk.scaffold(self.root, "V1.0", "样例", "spec.md")

    def test_test_failure_evidence_not_rewritten_by_acceptance(self):
        self.ready()
        rel = "V1.0/test-results.md"
        self.set(rel, self.get(rel) + "\n### 补充批次\n失败：外部依赖不可用；未执行：集成测试。\n")
        pk.record(self.root, "V1.0", "test", "test-second", sample_body("test-execute", "测试已执行，存在失败和未覆盖项"))
        evidence = self.get(rel)
        self.close()
        self.assertEqual(evidence, self.get(rel))
        self.assertIn("失败", evidence)

    def test_planning_question_roundtrip_and_invalidated_test_plan(self):
        self.ready()
        req = "V1.0/requirements.md"
        self.set(req, self.get(req).replace("## 已确认决定与开放问题", "## 已确认决定与开放问题\n\n新问题：是否支持负数？影响验收，等待用户。"))
        self.assertIn("是否支持负数", pk.section(self.get(req), "已确认决定与开放问题"))
        self.assertTrue(pk.readiness(self.root, "V1.0"))
        self.set("V1.0/test-plan.md", self.get("V1.0/test-plan.md") + "\n待重审：负数覆盖\n")
        self.assertFalse(pk.validate(self.root, "V1.0", "close")["valid"])

    def test_stale_merge_rejected(self):
        self.ready()
        self.close()
        self.set("architecture.md", self.get("architecture.md") + "\n后续编辑\n")
        pk.undo_close(self.root, "V1.0", "close-1", "重开")
        old = self.get("architecture.md")
        self.set("architecture.md", old + "\n再次编辑\n")
        with self.assertRaises(pk.KeeperError):
            pk.resolve_undo(self.root, "V1.0", "close-1", {"architecture.md": {"current_sha256": pk.digest(old), "merged": old, "reason": "合并"}})

    def test_noninit_write_cannot_initialize_project(self):
        other = self.root / "not-adopted"
        other.mkdir()
        result = subprocess.run([sys.executable, str(SCRIPT), "--project", str(other), "sync-index"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((other / "pjkp").exists())

    def test_skill_links_and_template_placeholders(self):
        import re
        skill = SCRIPT.parents[1]
        for doc in [skill / "SKILL.md", *sorted((skill / "references").glob("*.md"))]:
            for target in re.findall(r"\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
                if "://" not in target and not target.startswith("#"):
                    self.assertTrue((doc.parent / target.split("#", 1)[0]).exists(), (doc.name, target))
        self.assertNotIn("[TODO:", (skill / "SKILL.md").read_text(encoding="utf-8"))

    def test_navigation_only_expands_requested_version(self):
        for v in ("V1.0", "V1.1"):
            pk.create_version(self.root, v, "样例")
        pk.append_log(self.root, "history-1", "project-update", sample_body("project-update", "历史原文保留"))
        default = pk.inventory(self.root)
        selected = pk.inventory(self.root, "V1.1")
        all_versions = pk.inventory(self.root, all_versions=True)
        self.assertFalse(any("/V1." in f["path"] for f in default["files"]))
        self.assertFalse(any("/V1.0/" in f["path"] for f in selected["files"]))
        self.assertTrue(any("/V1.1/" in f["path"] for f in selected["files"]))
        self.assertTrue(any("/V1.0/" in f["path"] for f in all_versions["files"]))
        self.assertEqual(len(next(f for f in default["files"] if f["path"] == "pjkp/log.md")["headings"]), 1)
        self.assertIn("历史原文保留", self.get("log.md"))

    def test_requirement_folder_identity_validation(self):
        pk.create_version(self.root, "V1.0", "样例")
        text = self.get("V1.0/requirements.md")
        state = pk.get_state(text)
        state["version"] = "V2.0"
        self.set("V1.0/requirements.md", pk.put_state(text, state))
        with self.assertRaises(pk.KeeperError):
            pk.inventory(self.root)

    def test_cli_record_close_undo_end_to_end(self):
        self.ready()
        body = self.root / "behavior.md"
        body.write_text(sample_body("code-execute", "依据实际样例测试完成本轮记录"), encoding="utf-8")
        def run(*args):
            proc = subprocess.run([sys.executable, "-B", str(SCRIPT), "--project", str(self.root), *args], text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            return json.loads(proc.stdout)
        run("record", "code", "V1.0", "--id", "cli-code", "--body-file", str(body), "--implementation", "app.py", "--implementation", "test_app.py")
        body.write_text(sample_body("test-execute", "实际样例测试完成，证据见结果"), encoding="utf-8")
        run("record", "test", "V1.0", "--id", "cli-test", "--body-file", str(body))
        proposal = self.root / "proposal.json"
        proposal.write_text(json.dumps(self.proposal(), ensure_ascii=False), encoding="utf-8")
        self.assertEqual(run("close", "prepare", "V1.0", "cli-close", "--proposal", str(proposal))["status"], "prepared")
        self.assertEqual(run("close", "apply", "V1.0", "cli-close")["status"], "applied")
        self.assertIn("files", run("close", "status", "V1.0", "cli-close", "--full"))
        self.assertEqual(run("close", "undo", "V1.0", "cli-close", "--reason", "用户重新打开")["status"], "undone")
        self.assertTrue(run("validate", "--version", "V1.0", "--stage", "test")["valid"])
        self.assertIn("cli-code", run("read", "log.md", "--event", "cli-code")["text"])

    def roadmap_proposal(self):
        before = self.get("roadmap.md")
        return {"before_sha256": pk.digest(before), "after": before + "\n- [ ] 用户要求支持离线读取。\n",
                "summary": "记录用户提出的离线读取要求", "sources": {
                    "todo": {"statement": "请把支持离线读取记入 todo", "source": "临时样例用户消息"}}}

    def test_roadmap_new_title_and_legacy_read_without_rewrite(self):
        canonical = self.get("roadmap.md")
        self.assertEqual(tuple(pk.roadmap_parts(canonical)[1]), pk.ROADMAP_SECTIONS)
        legacy = canonical.replace("## todo", "## 短期待办")
        self.set("roadmap.md", legacy)
        result = pk.validate(self.root)
        self.assertTrue(result["valid"])
        self.assertTrue(any("旧标题" in warning for warning in result["warnings"]))
        self.assertEqual(legacy, self.get("roadmap.md"))

    def test_roadmap_missing_source_rejects_without_mutation(self):
        before, log = self.get("roadmap.md"), self.get("log.md")
        proposal = self.roadmap_proposal()
        proposal["sources"] = {}
        with self.assertRaises(pk.KeeperError):
            pk.update_roadmap(self.root, "roadmap-no-source", proposal)
        self.assertEqual(before, self.get("roadmap.md"))
        self.assertEqual(log, self.get("log.md"))

    def test_roadmap_empty_or_malformed_sources_reject(self):
        before = self.get("roadmap.md")
        for sources in ([], {"todo": None}, {"todo": {"statement": " ", "source": "用户"}},
                        {"todo": {"statement": "原话", "source": 3}}, {"其他": {"statement": "原话", "source": "用户"}}):
            with self.subTest(sources=sources):
                proposal = self.roadmap_proposal()
                proposal["sources"] = sources
                with self.assertRaises(pk.KeeperError):
                    pk.update_roadmap(self.root, "malformed", proposal)
                self.assertEqual(before, self.get("roadmap.md"))

    def test_roadmap_source_must_cover_each_changed_module(self):
        proposal = self.roadmap_proposal()
        proposal["after"] = proposal["after"].replace("## 里程碑", "## 里程碑\n\n新增未获来源支持的里程碑。")
        with self.assertRaisesRegex(pk.KeeperError, "里程碑"):
            pk.update_roadmap(self.root, "missing-milestone-source", proposal)
        proposal["sources"]["里程碑"] = {"statement": "请记录这个里程碑", "source": "样例用户消息2"}
        pk.update_roadmap(self.root, "with-both-sources", proposal)
        self.assertEqual(proposal["after"], self.get("roadmap.md"))
        self.assertIn("样例用户消息2", self.get("log.md"))

    def test_roadmap_stale_write_preserves_later_content(self):
        proposal = self.roadmap_proposal()
        changed = self.get("roadmap.md") + "\n用户后续修改。\n"
        self.set("roadmap.md", changed)
        with self.assertRaises(pk.KeeperError):
            pk.update_roadmap(self.root, "stale-roadmap", proposal)
        self.assertEqual(changed, self.get("roadmap.md"))

    def test_roadmap_repeat_preserves_history_and_new_edits(self):
        proposal = self.roadmap_proposal()
        log = self.get("log.md")
        pk.update_roadmap(self.root, "roadmap-once", proposal)
        self.assertTrue(self.get("log.md").startswith(log))
        later = self.get("roadmap.md") + "\n后续工作\n"
        self.set("roadmap.md", later)
        self.assertTrue(pk.update_roadmap(self.root, "roadmap-once", proposal)["replayed"])
        self.assertEqual(later, self.get("roadmap.md"))
        self.assertEqual(len(pk.log_entries(self.get("log.md"))), 1)
        proposal["summary"] = "同 id 不同内容"
        with self.assertRaises(pk.KeeperError):
            pk.update_roadmap(self.root, "roadmap-once", proposal)

    def test_roadmap_log_interruption_retry(self):
        proposal = self.roadmap_proposal()
        with patch.object(pk, "append_log", side_effect=OSError("simulated log interruption")):
            with self.assertRaises(OSError):
                pk.update_roadmap(self.root, "roadmap-resume", proposal)
        self.assertEqual(proposal["after"], self.get("roadmap.md"))
        pk.update_roadmap(self.root, "roadmap-resume", proposal)
        self.assertEqual(len(pk.log_entries(self.get("log.md"))), 1)

    def test_roadmap_prefix_and_structure_cannot_hide_new_plans(self):
        for after in (self.roadmap_proposal()["after"].replace("## 愿景", "新增目标\n\n## 愿景", 1),
                      self.roadmap_proposal()["after"] + "\n## 额外目标\n计划\n"):
            proposal = self.roadmap_proposal()
            proposal["after"] = after
            with self.assertRaises(pk.KeeperError):
                pk.update_roadmap(self.root, "hidden-plans", proposal)

    def test_close_requires_and_persists_roadmap_sources(self):
        self.ready()
        proposal = self.proposal()
        proposal.pop("roadmap_sources")
        with self.assertRaises(pk.KeeperError):
            pk.prepare(self.root, "V1.0", "no-roadmap-source", proposal)
        self.assertFalse(pk.path(self.root, "V1.0/.operations/no-roadmap-source/operation.json").exists())
        proposal = self.proposal()
        pk.prepare(self.root, "V1.0", "with-source", proposal)
        pk.apply_close(self.root, "V1.0", "with-source")
        self.assertEqual(pk.load_operation(self.root, "V1.0", "with-source")["roadmap_sources"], proposal["roadmap_sources"])
        self.assertIn("请将样例任务状态更新为已验证", self.get("log.md"))

    def test_cli_roadmap_update_records_one_event(self):
        proposal = self.roadmap_proposal()
        target = self.root / "roadmap-proposal.json"
        target.write_text(json.dumps(proposal, ensure_ascii=False), encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--project", str(self.root),
                                 "roadmap-update", "--id", "cli-roadmap", "--proposal", str(target)],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(proposal["after"], self.get("roadmap.md"))
        self.assertEqual([meta["action"] for meta, _ in pk.log_entries(self.get("log.md"))], ["roadmap-update"])

    def test_legacy_close_log_replay_preserves_existing_payload(self):
        self.ready()
        pk.prepare(self.root, "V1.0", "legacy-close", self.proposal(changed=False))
        op = pk.load_operation(self.root, "V1.0", "legacy-close")
        op.pop("roadmap_sources")
        op.pop("log_schema")
        pk.save_operation(self.root, op)
        pk.apply_close(self.root, "V1.0", "legacy-close")
        before = self.get("log.md")
        pk.apply_close(self.root, "V1.0", "legacy-close")
        self.assertEqual(before, self.get("log.md"))

    def test_each_action_log_renders_and_validates(self):
        actions = json.loads((SCRIPT.parents[1] / "assets/log-actions.json").read_text())["actions"]
        for number, action in enumerate(actions):
            with self.subTest(action=action):
                data = {title: "- 已核对样例材料。\n- 未知部分：待用户确认。" for title in pk.log_fields(action)}
                body = pk.format_log(action, dict(reversed(list(data.items()))))
                pk.append_log(self.root, "format-" + str(number), action, body, outcome="partial")
                meta, entry = pk.log_entries(self.get("log.md"))[-1]
                self.assertEqual(meta["schema"], 1)
                self.assertIn("执行状态：partial", entry)
                self.assertEqual([h["title"] for h in pk.headings(entry, 3)], list(data))
                self.assertEqual(pk.body_from_log_entry(meta, entry), body)
        self.assertTrue(pk.validate(self.root)["valid"])

    def test_structured_log_rejects_missing_extra_empty_and_injection(self):
        fields = pk.log_fields("project-update")
        valid = {title: "样例实际内容" for title in fields}
        first = next(iter(fields))
        cases = [{key: value for key, value in valid.items() if key != first},
                 dict(valid, 未知字段="不应接受"), dict(valid, **{first: " "}),
                 dict(valid, **{first: []}), dict(valid, **{first: "## 新行为\n绕过章节"})]
        before = self.get("log.md")
        for data in cases:
            with self.subTest(data=data), self.assertRaises(pk.KeeperError):
                pk.format_log("project-update", data)
        self.assertEqual(before, self.get("log.md"))

    def test_new_plaintext_unknown_action_wrong_order_and_status_reject(self):
        valid = sample_body("project-update", "实际内容")
        parts = valid.split("\n\n### ")
        wrong_order = "### " + parts[1] + "\n\n" + parts[0] + "\n\n### " + "\n\n### ".join(parts[2:])
        before = self.get("log.md")
        for action, body, outcome in (("project-update", "没有章节", "completed"),
                                      ("undefined", valid, "completed"),
                                      ("project-update", wrong_order, "completed"),
                                      ("project-update", valid, "passed")):
            with self.subTest(action=action, outcome=outcome), self.assertRaises(pk.KeeperError):
                pk.append_log(self.root, "reject", action, body, outcome=outcome)
        self.assertEqual(before, self.get("log.md"))

    def test_mixed_history_keeps_old_bytes_and_old_retry(self):
        pk.append_log(self.root, "old-log", "project-update", "旧版无章节原文", legacy=True)
        historical = self.get("log.md")
        pk.append_log(self.root, "new-log", "project-update", sample_body("project-update", "新事实"))
        mixed = self.get("log.md")
        self.assertTrue(mixed.startswith(historical))
        self.assertFalse(pk.append_log(self.root, "old-log", "project-update", "旧版无章节原文")["appended"])
        self.assertEqual(mixed, self.get("log.md"))
        self.assertTrue(pk.validate(self.root)["valid"])
        with self.assertRaises(pk.KeeperError):
            pk.append_log(self.root, "another-new", "project-update", "不能借旧行为使用旧格式")

    def test_log_validation_detects_content_header_and_evidence_tampering(self):
        self.ready()
        original = self.get("log.md")
        for changed in (original.replace("样例实现和开发验证完成", "篡改为未执行", 1),
                        original.replace("> 执行状态：completed", "> 执行状态：failed", 1),
                        original.replace("<summary>机器执行依据</summary>", "<summary>假证据</summary>", 1)):
            with self.subTest(changed=changed[:80]):
                self.set("log.md", changed)
                self.assertFalse(pk.validate(self.root)["valid"])
        self.set("log.md", original)
        self.assertTrue(pk.validate(self.root)["valid"])

    def test_malformed_execution_log_does_not_change_completion_state(self):
        self.ready()
        before, log = self.get("V1.0/requirements.md"), self.get("log.md")
        with self.assertRaises(pk.KeeperError):
            pk.record(self.root, "V1.0", "code", "invalid-record", "没提供规定内容", ["app.py"])
        self.assertEqual(before, self.get("V1.0/requirements.md"))
        self.assertEqual(log, self.get("log.md"))
        meta, entry = pk.log_entries(log)[-1]
        self.assertIn("code_id", meta["evidence"])
        self.assertIn("<summary>机器执行依据</summary>", entry)

    def test_partial_close_and_undo_follow_their_log_definitions(self):
        self.ready()
        pk.prepare(self.root, "V1.0", "partial-log", self.proposal())
        self.set("roadmap.md", self.get("roadmap.md") + "\n后续编辑\n")
        self.assertEqual(pk.apply_close(self.root, "V1.0", "partial-log")["status"], "partial")
        meta, entry = pk.log_entries(self.get("log.md"))[-1]
        self.assertEqual((meta["action"], meta["outcome"], meta["parent"]), ("version-close", "partial", "partial-log"))
        pk.validate_log_body(meta["action"], pk.body_from_log_entry(meta, entry))
        pk.undo_close(self.root, "V1.0", "partial-log", "用户要求撤销部分关闭")
        meta, entry = pk.log_entries(self.get("log.md"))[-1]
        self.assertEqual(meta["action"], "undo")
        pk.validate_log_body("undo", pk.body_from_log_entry(meta, entry))
        self.assertIn("后续编辑", self.get("roadmap.md"))

    def test_legacy_execution_log_retry_keeps_original_payload(self):
        self.ready()
        capture = {"id": "legacy-code", "basis": pk.basis(self.root, "V1.0", "code"),
                   "implementation": pk.source_hashes(self.root, ["app.py", "test_app.py"])}
        body = "旧版实现记录"
        details = body + "\n\n- 执行依据：" + pk.encode(capture)
        pk.append_log(self.root, "legacy-code", "code-execute", details, "V1.0", legacy=True)
        historical = self.get("log.md")
        pk.record(self.root, "V1.0", "code", "legacy-code", body, ["app.py", "test_app.py"])
        self.assertEqual(historical, self.get("log.md"))
        self.assertEqual(pk.get_state(self.get("V1.0/requirements.md"))["code"], capture)

    def test_old_undo_pending_log_recovery_keeps_legacy_format(self):
        self.ready()
        pk.prepare(self.root, "V1.0", "legacy-undo", self.proposal(changed=False))
        op = pk.load_operation(self.root, "V1.0", "legacy-undo")
        op.pop("log_schema")
        pk.save_operation(self.root, op)
        pk.apply_close(self.root, "V1.0", "legacy-undo")
        with patch.object(pk, "append_log", side_effect=OSError("old pending log interrupted")):
            with self.assertRaises(OSError):
                pk.undo_close(self.root, "V1.0", "legacy-undo", "用户撤销")
        pk.undo_close(self.root, "V1.0", "legacy-undo", "恢复旧操作日志")
        self.assertNotIn("schema", pk.log_entries(self.get("log.md"))[-1][0])
        self.assertTrue(pk.validate(self.root)["valid"])

    def test_cli_log_schema_readonly_and_structured_write(self):
        before = self.get("log.md")
        def run(*args):
            return subprocess.run([sys.executable, "-B", str(SCRIPT), "--project", str(self.root), *args], capture_output=True, text=True)
        result = run("log-schema", "plan")
        self.assertEqual(result.returncode, 0, result.stderr)
        fields = json.loads(result.stdout)["fields"]
        self.assertEqual(before, self.get("log.md"))
        data = self.root / "plan-log.json"
        data.write_text(json.dumps({title: "真实样例依据，未知项待确认。" for title in fields}, ensure_ascii=False), encoding="utf-8")
        result = run("log", "--id", "json-plan", "--action", "plan", "--data-file", str(data))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(pk.validate(self.root)["valid"])
        failed = run("log", "--id", "two-inputs", "--action", "plan", "--data-file", str(data), "--body-file", str(data))
        self.assertEqual(failed.returncode, 2)

    def test_close_prechecks_log_format_before_any_target_changes(self):
        self.ready()
        proposal = self.proposal()
        proposal["summary"] = "### 插入错误层级\n内容"
        before = {name: self.get(name) for name in pk.PROJECT_DOCS}
        with self.assertRaises(pk.KeeperError):
            pk.prepare(self.root, "V1.0", "bad-log-summary", proposal)
        self.assertFalse(pk.path(self.root, "V1.0/.operations/bad-log-summary/operation.json").exists())
        self.assertEqual(before, {name: self.get(name) for name in pk.PROJECT_DOCS})

    def test_undo_prechecks_log_reason_before_restoring_files(self):
        self.ready()
        self.close()
        before = {name: self.get(name) for name in pk.PROJECT_DOCS}
        with self.assertRaises(pk.KeeperError):
            pk.undo_close(self.root, "V1.0", "close-1", "### 错误层级\n用户撤销")
        self.assertEqual(before, {name: self.get(name) for name in pk.PROJECT_DOCS})
        self.assertEqual(pk.operation_status(self.root, "V1.0", "close-1")["status"], "applied")


if __name__ == "__main__":
    unittest.main(verbosity=2)
