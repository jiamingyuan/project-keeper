# Action 日志内容与呈现规范

写入任何独立行为日志前读取本文；再用 `log-schema <action>` 只获取当前 Action 的字段及含义。字段的唯一机器定义在 [log-actions.json](../assets/log-actions.json)，不加载所有 Action 的模板。本文定义语义和呈现约定，不改变各 Action 的授权、就绪与验收边界。

## 通用呈现

每条记录保留机器元数据、二级标题、可读状态行及按顺序排列的三级章节。标题仍为 `时间 — Action — project 或 Vx.x`；状态行显示执行状态、行为 id 与 parent。completed 表示该行为执行完成，不能解释成测试全部通过或用户验收。

每章必填非空内容，可用段落、多个 bullet point、表格或四级小节。未知写“待确认”并说明影响，未执行说明原因，无相关事项明确写“无”并有依据。禁止为凑齐字段编造事实。详细命令输出、完整测试结果和源码用位置引用，正文只保留帮助理解行为的事实。

机器执行指纹由脚本保存到元数据和可展开证据块，避免混进自然语言章节。schema=1 的日志按本规范校验；旧日志保持原文，不重排、补填或自动升级。

## 各 Action 的内容

| Action | 必备章节（依次排列） |
| --- | --- |
| project-initiate | 触发与来源；澄清与决定；创建与复用；待确认事项；结果与后续 |
| project-update | 触发与来源；更新内容；未确认事项；影响与同步；结果与后续 |
| version-create | 版本与来源；需求方向与范围；创建或续接；开放问题与规划关联；结果与后续 |
| plan | 规划依据；方案与测试要点；需求回写；就绪与阻塞；产物与后续 |
| code-execute | 执行依据与范围；任务与修改；开发验证；偏差与阻塞；结果与后续 |
| test-execute | 批次与被测实现；方案与覆盖；实际结果；失败与未执行；证据与后续 |
| version-close | 关闭依据；用户验收；交付与遗留；项目同步；恢复入口与结果 |
| undo | 原操作与原因；恢复范围；保留的后续工作；冲突与剩余事项；结果与依据 |
| roadmap-update | 触发与用户来源；规划变化；范围与关联；结果与后续 |
| context-read | 读取目标；来源与当前状态；未决与冲突；接续建议 |
| github-publish（本项目使用的扩展行为） | 用户授权与目标；发布内容；远端结果；未完成项与后续 |
| correction（历史更正） | 原记录与原因；更正内容；影响与后续 |

各章具体含义通过 log-schema 查看。例如 test-execute 的“批次与被测实现”要说明执行者和环境，“实际结果”区分通过、失败和未执行，“证据与后续”引用 test-results；不能用“运行完毕”替代这些内容。partial、blocked 或 failed 仍保留同一组章节，未完成部分如实说明。

## 写入方式

先获取当前行为字段：

```text
--project <root> log-schema project-update
```

用 apply_patch 创建 UTF-8 JSON 数据文件，键为该行为的全部章节名，值为实际 Markdown 内容。脚本按定义顺序渲染，未知键、漏章、空值或非字符串会报错。JSON 不需要包含时间、id 或机器指纹。

```json
{
  "触发与来源": "- 用户提出更新定位，来源：当前对话。",
  "更新内容": "- project-brief.md 的项目定位补充两个核心场景。",
  "未确认事项": "- 实际跨会话效果仍待验证。",
  "影响与同步": "- 同步 architecture 和 index；未新增 roadmap 事项。",
  "结果与后续": "- 文档已更新，后续由用户审阅。"
}
```

```text
--project <root> log --id update-001 --action project-update --data-file <JSON路径>
--project <root> record code V0.2 --id code-001 --data-file <JSON路径> --implementation <实际文件>
```

也支持 `--body-file` 输入已经按同样章节与顺序写好的 Markdown，但不能给新日志提交无章节散文。record 的字段对应 code-execute 或 test-execute。roadmap-update、close apply、undo 由脚本生成相同规范的日志，不重复调用 log。

历史日志、旧操作的续接和旧执行记录的同 id 重试按原格式保留，不为通过新校验重写历史。新增扩展行为需先补充机器定义和内容说明，不能把未知 Action 静默当成通用散文。

## 粒度与结果

每个独立行为一条，子 Action 另记并通过 parent 关联；工具内部步骤不单独记账。关闭产生关联的 project-update 与 version-close；撤销产生 undo，保留原关闭历史。真正的新尝试使用新 id；同一请求重复提交去重，更正另记。

纯展示、解释或明确只读时不因日志要求扩大写入。结构校验只证明章节与格式满足要求，事实、来源真实性和语义完整性仍由 Agent 核对。
