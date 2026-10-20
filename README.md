# Project Keeper

当前发布基线：[V0.1](https://github.com/jiamingyuan/project-keeper/releases/tag/V0.1)；本分支为 **V0.2 开发中**，尚未用户验收。这是在 Agent coding 中维护项目外部上下文的多 Action Skill。

- 会话内：将需要持续使用的信息、决定、进展与未决问题保存到项目文件，按需找回。
- 跨会话：让新会话通过文档理解项目全貌、约束和当前状态，接续开发。

## 使用

将本仓库作为 `project-keeper` Skill 安装到你的 Agent 所支持的 Skill 目录，然后按 [SKILL.md](SKILL.md) 使用。运行辅助脚本需要 Python 3.9+，仅依赖标准库。

每个受管理项目使用自身根目录下的 `pjkp/`，不会把不同项目的数据集中到 Skill 目录。本仓库的 `pjkp/` 是 Project Keeper 自身的项目记录，不是新项目的模板；新项目由 `assets/templates/` 生成。

```sh
python3 scripts/project_keeper.py --project /path/to/project context
```

支持 `project-initiate`、`project-update`、`version-create`、`plan`、`code-execute`、`test-execute`、`version-close`，以及关闭操作的 `undo`。自然语言判断、代码修改及真实测试由 Agent 执行；辅助脚本负责确定性维护。

## 项目资料与验证

- [自身项目入口](pjkp/index.md)
- [V0.1 基线范围](pjkp/V0.1/requirements.md)
- [本轮基线验证](pjkp/V0.1/test-results.md)
- [V0.2 需求](pjkp/V0.2/requirements.md)、[执行方案](pjkp/V0.2/spec.md)、[测试方案](pjkp/V0.2/test-plan.md)
- [V0.2 开发草稿 PR #1](https://github.com/jiamingyuan/project-keeper/pull/1)
- [早期验证及已知限制](tests/verification-report.md)

```sh
python3 -B -m unittest discover -s tests -v
```

V0.1 保留现有实现和已知问题：本项目 roadmap 的 `todo` 标题与通用模板旧标题尚未同步；规划来源的通用写入限制尚待落实。实际 Agent 使用效果、跨会话恢复质量及复杂协作仍需真实项目验证。

V0.2 开发分支已统一新模板的 todo 名称并兼容旧标题，增加规划写入和关闭同步的逐模块用户来源检查。首批 53 项自动化测试通过，等待用户审阅；两项用户 todo 尚未自动勾选，尚未执行 version-close。

本轮追加 [逐 Action 日志规范](references/logging.md)：统一标题、状态与专属必备章节，提供按 Action 查询和 JSON 渲染，自动生成路径也遵守相同定义。当前 65 项测试通过；历史日志不重写，执行完成仍不代表用户验收。

本次按用户要求为已有实现建立发布基线，没有追造历史开发过程或执行 `version-close`。发布标签与项目生命周期的关闭记录分别维护。
