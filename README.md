# Project Keeper

软件项目的轻量项目记忆：让 Agent 找回同会话中较早的决定，并在新会话中接续。它记录源码之外的方向、约束和真实进展，不接管开发流程。

当前版本：[V0.3](https://github.com/jiamingyuan/project-keeper/releases/tag/V0.3)。按用户要求将当前状态归档发布；发布不代表已完成独立模型行为验证、真实项目收益对照或用户验收。历史发布基线 [V0.1](https://github.com/jiamingyuan/project-keeper/releases/tag/V0.1) 保留。

## 使用

将本目录作为 `project-keeper` Skill 安装或链接到宿主支持的 Skill 目录。按 [SKILL.md](SKILL.md) 直接读写项目 Markdown，不需要 Python、辅助 CLI 或固定 Action 命令。

已明确采用 `pjkp/` 的项目可在普通开发任务中使用。新项目由用户明确选择后初始化；经同意在项目入口追加指针，是否自动加载仍取决于宿主。

每个项目独立保存：

```text
pjkp/
  index.md
  rules.md
  project-brief.md
  architecture.md       # 必要时创建
  Vx.x/iteration.md     # 用户指定版本后创建
```

[模板](assets/templates) 只是内容示例，不是固定格式。当前部分优先，候选与被取代的决定不能冒充现行结论；只要求记录不等于授权开发。旧项目可直接读取，不会自动迁移。

## 本项目

- [当前入口](pjkp/index.md)
- [V0.3 变化与验证边界](pjkp/V0.3/iteration.md)
- [V0.2 开发历史](pjkp/V0.2/iteration.md)（未单独打发布标签）
- [V0.1 基线](pjkp/V0.1/requirements.md)与[当时的验证](pjkp/V0.1/test-results.md)

本版移除了阶段链、独立执行记录、关闭/undo 事务、逐 Action 日志和运行时脚本。旧历史仍可追溯；实际接续效果与维护成本需要真实项目对照验证，不能由结构检查推出。
