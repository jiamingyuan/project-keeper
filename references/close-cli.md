# 关闭辅助接口

仅 version-close / undo 时读取。先阅读 [通用 CLI](cli.md) 的命令位置、退出码与写入限制。

## 关闭提案与持久恢复

先用 context 获取本次文件指纹，读取相关全文，通过 apply_patch 创建提案 JSON。`updates` 必须且只能包含本版 requirements、project-brief、architecture、roadmap 四个键；无变化也放原文，说明已检查。示例中的尖括号必须换成实际内容：

```json
{
  "acceptance": {"confirmed": true, "statement": "用户对本版的确认原意", "source": "当前对话的用户验收消息及交付对象"},
  "summary": "实际交付、遗留和延期范围；哪些文档有变化/无变化、规划状态与同步依据",
  "updates": {
    "V1.0/requirements.md": {"before_sha256": "<当前哈希>", "after": "<需求全文，只更新版本结果>"},
    "project-brief.md": {"before_sha256": "<当前哈希>", "after": "<目标全文>"},
    "architecture.md": {"before_sha256": "<当前哈希>", "after": "<目标全文>"},
    "roadmap.md": {"before_sha256": "<当前哈希>", "after": "<目标全文>"}
  }
}
```

```text
--project <root> close prepare V1.0 close-001 --proposal <提案路径>
--project <root> close status V1.0 close-001
--project <root> close apply V1.0 close-001
--project <root> close undo V1.0 close-001 --reason <用户要求撤销的原因>
```

操作 id 在项目中唯一，不超过 80 字符，不含冒号。prepare 写入 `V1.0/.operations/close-001/operation.json`，存储前后全文、指纹、用户确认、执行依据、阶段与进度。日志和 config 不属于回滚目标。该记录可能含项目内部知识，与项目其他私有材料同样保管；不要编辑记录内容绕过冲突检查。

若 roadmap 正文变化，提案另加 `roadmap_sources`，按受影响模块提供用户 `statement` 和 `source`，格式同 [规划写入](roadmap.md) 的 sources。未变化不要求新来源；用户验收不能替代每项新增规划的依据。来源会随关闭操作和关联日志保存。

apply 支持同一操作续接，依次更新描述、规划、版本结果和索引；不是跨文件原子事务。全部完成记关联的 project-update 与 version-close 日志；已完成 apply 重试不覆盖后续编辑。

undo 保留原记录、代码和测试。冲突返回 undo-partial；status --full 仅针对该操作展示快照供合并，不自动装载到每轮上下文。合并 JSON：

```json
{
  "project-brief.md": {
    "current_sha256": "<合并依据的当前哈希>",
    "merged": "<撤销目标变更并保留后续编辑后的全文>",
    "reason": "为何该合并仅撤销目标关闭，保留哪些后续成果"
  }
}
```

```text
--project <root> close resolve V1.0 close-001 --resolutions <合并JSON路径>
--project <root> close undo V1.0 close-001 --reason <继续撤销原因>
```

resolve 只记录已检查的合并，随后 undo 应用；内容仍需 Agent/用户语义核对。后续版本依赖共享摘要时会保守报冲突；index 只重算受管理导航块，不整份还原旧索引。
