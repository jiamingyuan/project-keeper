"""Reproducible UTF-8 reading-volume estimate, not token/latency/quality proof.

Isolated fixture: three versions and 60 historical behavior records. Routes read
full required instruction groups and whole selected project docs, not summaries.
Snapshot content is counted only for undo. Navigation output is counted as cost.
"""
import json
from pathlib import Path
from test_project_keeper import KeeperTests, SCRIPT, pk


def measure():
    skill = SCRIPT.parents[1]
    runtime = [skill / "SKILL.md"] + [skill / "references" / (name + ".md") for name in ("project", "planning", "execution", "closing", "cli", "close-cli")]
    templates = list((skill / "assets/templates").iterdir())
    def size(files):
        return sum(len(p.read_bytes()) for p in set(files))
    entry_cli = [skill / "SKILL.md", skill / "references/cli.md"]
    initial_route = entry_cli + [skill / "references/project.md"] + [skill / "assets/templates" / name for name in (*pk.PROJECT_DOCS, "config.toml")]
    report = {"method": "UTF-8 bytes; complete selected files + JSON navigation; estimates, not tokenizer counts or performance measurements", "cases": []}
    report["cases"].append({"task": "project-initiate (fresh project)", "all_bytes": size(runtime + templates), "routed_bytes": size(initial_route), "loaded": [str(p.relative_to(skill)) for p in initial_route]})
    case = KeeperTests()
    case.setUp()
    try:
        for n, version in enumerate(("V0.1", "V0.2", "V1.0"), 1):
            case.ready(version)
            if version != "V1.0":
                case.close(version, "measure-close-" + str(n))
        for n in range(60):
            pk.append_log(case.root, "history-" + str(n), "project-update", f"历史决定 {n}：保留原始背景与约束。\n- 依据：关联既有实现，不作为当前决策的唯一依据。\n- 原因：本条为独立已发生行为，不能用摘要替换原文。", "V0.1")
        pjkp = case.root / "pjkp"
        project_all = [p for p in pjkp.rglob("*") if p.is_file()]
        code = [case.root / "app.py", case.root / "test_app.py"]
        nav_bytes = len(json.dumps(pk.inventory(case.root, "V1.0"), ensure_ascii=False, indent=2).encode("utf-8"))
        base = [pjkp / name for name in ("index.md", "rules.md", "project-brief.md")]
        executing = base + [pjkp / "architecture.md"] + [pjkp / "V1.0" / name for name in pk.VERSION_DOCS] + code
        undoing = base + [pjkp / "architecture.md", pjkp / "roadmap.md", pjkp / "V1.0/requirements.md", pjkp / "V1.0/.operations/measure-close-3/operation.json"] + code
        for task, group, files in (("code-execute", "execution", executing), ("test-execute", "execution", executing), ("undo", "closing", undoing)):
            if task == "undo":
                case.close("V1.0", "measure-close-3")
            project_all = [p for p in pjkp.rglob("*") if p.is_file()]
            nav_bytes = len(json.dumps(pk.inventory(case.root, "V1.0"), ensure_ascii=False, indent=2).encode("utf-8"))
            instructions = entry_cli + [skill / "references" / (group + ".md")]
            # Undo may need project-update semantics when resolving a conflict.
            if task == "undo":
                instructions.append(skill / "references/project.md")
                instructions.append(skill / "references/close-cli.md")
            report["cases"].append({"task": task, "all_bytes": size(runtime + templates + project_all + code), "routed_bytes": size(instructions + files) + nav_bytes,
                                    "navigation_bytes": nav_bytes, "loaded_instructions": [str(p.relative_to(skill)) for p in instructions], "loaded_project": [str(p.relative_to(case.root)) for p in files]})
        for row in report["cases"]:
            row["reduction_percent"] = round(100 * (1 - row["routed_bytes"] / row["all_bytes"]), 1)
        return report
    finally:
        case.doCleanups()


if __name__ == "__main__":
    print(json.dumps(measure(), ensure_ascii=False, indent=2))
