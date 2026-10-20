# project-keeper 项目入口

## 项目入口

- 项目：project-keeper
- 根目录：`/Users/jiamingyuan/Desktop/workspaces/skill-factory/project-keeper`
- 形态：单个多 Action Skill；本目录的 `pjkp/` 是项目自身上下文，不是其他项目的数据集中存储。
- 当前状态：V0.1 已发布，V0.2 在 develop/V0.2 分支完成首批实现与 53 项自动化验证，等待用户审阅；本轮没有补造历史 version-close。
- GitHub：https://github.com/jiamingyuan/project-keeper ，发布版本以 V0.1 标签与 Release 为准。
- 配置：[config.toml](config.toml)（仅预留，不参与运行）

## 文件导航

- [项目简介](project-brief.md)：定位、会话内管理与跨会话恢复的核心场景及功能。
- [架构](architecture.md)：框架、机制与源码入口。
- [规则](rules.md)：原则和边界。
- [规划](roadmap.md)：愿景、里程碑、todo。
- [日志](log.md)：行为历史。
- [Skill 入口](../SKILL.md)：复用能力及 Action 路由。
- [验证记录](../tests/verification-report.md)：初版测试、读取量测量与已知限制；其中安装状态是验证当时的历史状态。
- [需求追踪](../references/verification.md)：设计要求与实现、测试的映射。

## 版本状态

<!-- pjkp:versions:start -->
最近完成版本：暂无

| 版本 | 状态 | 来源 |
| --- | --- | --- |
| V0.1 | requirements | [需求](V0.1/requirements.md) |
| V0.2 | awaiting-acceptance | [需求](V0.2/requirements.md) |
<!-- pjkp:versions:end -->

## 当前阻塞与待同步事项

V0.1 为已有实现的发布基线，需求文件中的机械阶段不等于基线发布状态；详见 [V0.1 记录](V0.1/requirements.md)。V0.2 启动范围承接用户已提出的两项 [todo](roadmap.md#todo)，不新增里程碑。

V0.2 已消除 todo 标题不匹配，新增规划写入来源检查，详见 [需求](V0.2/requirements.md)、[spec](V0.2/spec.md)、[测试方案](V0.2/test-plan.md)。开发分支未验收或关闭；规划中的两项 todo 未自动勾选。

历史 M1–M4 为早期 Agent 建议，尚无用户逐条确认的依据；本轮未改写其正文或把它们升级为正式承诺。

早期设计资料保留在 `/Users/jiamingyuan/Desktop/workspaces/project-keeper/docs/`，未迁移或修改。当前上下文以本目录文件为入口；若历史设计、当前指令与源码冲突，应核对依据并显式澄清，不能静默覆盖。
