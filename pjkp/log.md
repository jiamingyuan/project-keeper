# project-keeper 行为日志

每个独立行为一条记录；按时间追加，原记录保留，更正另记。

<!-- pjkp:log {"action": "project-initiate", "id": "project-initiate-20260927-self-001", "outcome": "completed", "parent": null, "sha256": "ec526ebbe909f0d9670bba67aaf2e795644b87167cd2283fbc53db1ba42a5062", "time": "2026-09-26T18:25:16.038494+00:00", "version": null} -->
## 2026-09-26T18:25:16.038494+00:00 — project-initiate — project

- 来源：用户要求将 project-keeper 项目本身纳入管理，并确认实际源目录 `/Users/jiamingyuan/Desktop/workspaces/skill-factory/project-keeper`；采用 project-initiate 流程，不是再次安装 Skill。
- 依据：本轮对话中已确认的定位、文件职责和生命周期边界；现有 SKILL.md、项目操作与 CLI 说明、模板、初版验证记录；早期 `/Users/jiamingyuan/Desktop/workspaces/project-keeper/docs/` 中的项目简介、原则和规划。
- 初始化前检查：context 返回 initialized=false；全局 `/Users/jiamingyuan/.agents/skills/project-keeper` 符号链接已指向当前源目录，无需重新注册。
- 新建并填写：pjkp/index.md、project-brief.md、architecture.md、rules.md、roadmap.md、log.md，以及仅含预留注释的 config.toml。项目简介只保留项目介绍与项目功能，架构说明机制和源码入口，规划区分现有成果与长期方向。
- 状态校正：早期设计中的“尚未实现”仅为历史状态；当前已存在初版指令、模板、辅助脚本及自动化验证。本次不改写旧设计文档，也不追补或伪造历史行为日志。
- 验证：在工作区执行 `python3 -B -m unittest discover -s skill-factory/project-keeper/tests`，42 项测试通过；执行辅助脚本 `--project /Users/jiamingyuan/Desktop/workspaces/skill-factory/project-keeper validate`，结构与链接检查通过，无错误或警告。
- 未完成与边界：真实项目完整 Agent 行为、跨对话效果、复杂协作、其他 Python 版本兼容性及实际 token/耗时收益尚需验证；自动化通过不能代替这些结论，也不能代替用户版本验收。
- 结果：本项目自身上下文已建立。未修改 Skill 实现、旧设计文档、idea-keeper 或注册位置；未创建版本、关闭版本或发布部署。后续由用户审阅资料，在明确版本编号与范围后再开展迭代。

<!-- pjkp:log {"action": "roadmap-update", "id": "roadmap-update-20260927-user-todo-001", "outcome": "completed", "parent": null, "sha256": "5696ce88b51aa44141638ffd85a5e1e2579b3e694ab8f840a4e2f228703bef52", "time": "2026-09-30T13:28:00.599509+00:00", "version": null} -->
## 2026-09-30T13:28:00.599509+00:00 — roadmap-update — project

- 来源：用户要求去掉 todo 中所有旧内容，提出“短期待办改名为 todo”，并要求愿景与长期规划、todo、里程碑的信息由用户提出，不能由 Agent 根据自己的理解随意写入，需要限制机制。
- 变更：清空 roadmap.md 原短期待办正文，将标题改为 todo，保留用户本次提出的两项需求；index.md 导航名称同步。改名项注明本项目标题已修改，通用模板与校验仍待同步；限制机制仍为待定义和实现的需求，不宣称已实现。
- 范围：未改愿景与里程碑正文，未修改 Skill 模板、指令、脚本或注册位置，未创建版本。未新增 Agent 自拟规划。
- 校验：运行辅助脚本 validate，仅报告 roadmap.md 二级标题与旧模板的“短期待办”不匹配，无其他错误或警告。按用户名称保留 todo，模板同步归入用户提出的改名需求，不通过回改标题或扩大实现范围消除告警。
- 删除内容留档（仅为历史，不再作为当前 todo）：
  - 原已完成项：确定多 Action Skill、项目级文件职责、版本命名和用户验收边界。
  - 原已完成项：实现中文指令、按需参考、模板和 Python 辅助脚本。
  - 原已完成项：建立机械约束、关闭恢复及读取量测量的验证材料。
  - 原已完成项：将实际源目录纳入自身上下文管理，保留早期设计资料，不补建版本。
  - 原未完成项：由用户审阅自身项目上下文，收集遗漏、理解偏差与维护成本反馈。
  - 原未完成项：在后续真实任务中检验按需读取、项目同步和跨对话接续；记录问题而不预设收益。
  - 原未完成项：用户给出版本编号和范围后，以本项目完成一次真实迭代，覆盖规划、执行、测试、验收与关闭；按需要验证撤销。
  - 原未完成项：在实际试用中评估复杂项目与多人协作需求，再明确适配方案。
  - 原附注：待办是后续方向，不是自动执行授权。代码运行兼容性、真实 Agent 行为质量与 token/耗时收益尚需验证；字节量对比不等于效率提升证明。

<!-- pjkp:log {"action": "project-update", "id": "project-update-20261019-context-001", "outcome": "completed", "parent": null, "sha256": "1274c35bcdeef4049bddc3c30d41de086f329ff50754d18d6856c003243c6694", "time": "2026-10-19T12:10:04.793745+00:00", "version": null} -->
## 2026-10-19T12:10:04.793745+00:00 — project-update — project

- 来源：用户提出两个核心问题：同一 Agent 会话内通过项目文件保存较早的上下文，补充当前窗口并辅助工作；跨会话通过文档快速理解项目全貌。用户在讨论后要求“根据你的理解，更新一下 project-keeper 的 pjkp”。
- 理解依据：将前述“远端 context”按较早、可能被压缩或移出当前窗口的信息理解；“打草稿”表达保存阶段性工作状态的用途。Agent 在讨论中补充工作记录与已确认项目认识的区别，以及来源、确认状态和适用范围的重要性；本轮据该讨论更新文档。
- project-brief.md：定位改为 Agent coding 中的外部上下文管理；概要解释会话内使用和跨会话交接；价值与功能按两个场景展开，保留原有 Action 及生命周期能力。同步使用 todo 名称及用户此前明确的规划来源约束。
- architecture.md：增加两种场景共用项目文件的记录和恢复机制，说明项目文档、版本材料与 log 的职责，以及假设不会因落盘或回读而变成确认结论。注明现有能力依赖 Agent 主动记录和读取，未实现自动对话捕获、窗口溢出判断或独立草稿区，不把新定位描述为新功能交付。
- rules.md：同步两个核心场景和工作记录的来源、确认状态、适用范围要求；收录用户此前明确的规划内容来源约束，注明通用限制机制仍待实现。
- index.md：同步当前认识、项目简介导航及已知待同步事项。roadmap 的愿景、里程碑和 todo 本轮均未修改，未新增 Agent 自拟规划。
- 影响与范围：仅修改 pjkp 项目文档并追加本行为日志，无现存版本材料需要重审；未修改 Skill 指令、模板、脚本或安装注册，未执行代码开发、创建版本或替用户验收。两个场景的真实使用效果仍待验证。
- 检查：运行辅助脚本 validate，仍只有已知的 roadmap 二级标题错误：本项目按用户要求为 todo，旧模板为短期待办；无其他结构、链接错误或警告。本轮未通过修改通用模板或回改用户命名消除此历史问题。

<!-- pjkp:log {"action": "version-create", "id": "version-create-20261020-baseline-v01", "outcome": "completed", "parent": null, "sha256": "f8e04d30a1dd41a2e63823cacdc3ad26ba6b29ff3ca3c6649351a3c1ec1e7e52", "time": "2026-10-20T11:15:07.739896+00:00", "version": "V0.1"} -->
## 2026-10-20T11:15:07.739896+00:00 — version-create — V0.1

- 来源：用户明确要求当前定义为 V0.1、在 GitHub 呈现并启动 V0.2，随后指定 https://github.com/jiamingyuan/project-keeper 。
- 版本：V0.1 是对现有实现建立发布基线，非重新执行或追造早期迭代。登记版本需求、当前验证结果、README、VERSION 与 Git 忽略规则，保留原有运行代码。
- 验证：42 项现有测试通过；已知 roadmap 标题与旧模板不匹配保留。系统 Python 缺少 PyYAML，Skill 格式验证需使用可用验证环境重试。
- 状态：本次 GitHub 发布授权不被伪造为历史 version-close，未生成虚构代码执行或验收记录。下一步在独立开发分支以用户已有两项 todo 启动 V0.2。
