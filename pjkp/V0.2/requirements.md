<!-- pjkp:state {"closed_by": null, "code": {"basis": {"V0.2/requirements.md": "2630aeb332b35233dd066b2ba64aff023a406760b9c577f37183a1768744d389", "V0.2/spec.md": "2c8b3e7d50cdcc91007c28ce64a094a5b87e62550e3dcc664fbf9ac5feee7d65"}, "id": "code-20261020-v02-001", "implementation": {"SKILL.md": "285476eec822abce2b14d6f066679659b4502f17fe93da6910699e6b1c74e06e", "assets/templates/index.md": "d7e4a4914fb3a48b3fceee3008ac3e361cfbdd53221e7a0593bbc312b912e398", "assets/templates/roadmap.md": "fba15df18630e1453fe8e451cd9801226cfadab1e46bde041d53ddd67e556f16", "references/cli.md": "308f6a1fd2ef827b4b3931660ac8e4d4bfd0ea61021a15f710a148fdeaefa657", "references/close-cli.md": "2241d72ae23a08a249ddb517d2fee5811d0e54523ddfdbd526314052380981b3", "references/closing.md": "9a15997f315dfd94ca78a8288411b23dea5348ff5b5405d7c7ee452d38c78c73", "references/project.md": "65c5c544c3b7eb62c7b751c594d45aec2095550407cb88d1b1e1bd779472e22a", "references/roadmap.md": "2d14f537f4dd75befb70848bce4c50c3e4b0512e934b96321f2f5603ca1b8d6a", "references/verification.md": "68cf5f2a1e75e132787cc017673e4186ad819468b5ee5d5650d930f0fc3d409b", "scripts/project_keeper.py": "93a0f331bbb8f31924c082190d9ce1977e7c4231cadd630947606175061b7077", "tests/measure_context.py": "090d65d1fb10b47ac384931c11b424c3d5510fb74c5ba63df89f7338222e323f", "tests/test_project_keeper.py": "ed32453f43ae79ee496c92bd6ec5264e9b0ef3e1bfd67fb66b51e0dee7a1c07f"}}, "phase": "awaiting-acceptance", "test": {"basis": {"V0.2/requirements.md": "2630aeb332b35233dd066b2ba64aff023a406760b9c577f37183a1768744d389", "V0.2/spec.md": "2c8b3e7d50cdcc91007c28ce64a094a5b87e62550e3dcc664fbf9ac5feee7d65", "V0.2/test-plan.md": "f68f600e64a3d84cee19d0bfa08f921c8fe000726df406a9ce20046679310361", "V0.2/test-results.md": "f55f252462e8dce08a3a8def9a390be5a0a2f032ae20e949df76f756122bdbc4"}, "code_id": "code-20261020-v02-001", "id": "test-20261020-v02-001", "implementation": {"SKILL.md": "285476eec822abce2b14d6f066679659b4502f17fe93da6910699e6b1c74e06e", "assets/templates/index.md": "d7e4a4914fb3a48b3fceee3008ac3e361cfbdd53221e7a0593bbc312b912e398", "assets/templates/roadmap.md": "fba15df18630e1453fe8e451cd9801226cfadab1e46bde041d53ddd67e556f16", "references/cli.md": "308f6a1fd2ef827b4b3931660ac8e4d4bfd0ea61021a15f710a148fdeaefa657", "references/close-cli.md": "2241d72ae23a08a249ddb517d2fee5811d0e54523ddfdbd526314052380981b3", "references/closing.md": "9a15997f315dfd94ca78a8288411b23dea5348ff5b5405d7c7ee452d38c78c73", "references/project.md": "65c5c544c3b7eb62c7b751c594d45aec2095550407cb88d1b1e1bd779472e22a", "references/roadmap.md": "2d14f537f4dd75befb70848bce4c50c3e4b0512e934b96321f2f5603ca1b8d6a", "references/verification.md": "68cf5f2a1e75e132787cc017673e4186ad819468b5ee5d5650d930f0fc3d409b", "scripts/project_keeper.py": "93a0f331bbb8f31924c082190d9ce1977e7c4231cadd630947606175061b7077", "tests/measure_context.py": "090d65d1fb10b47ac384931c11b424c3d5510fb74c5ba63df89f7338222e323f", "tests/test_project_keeper.py": "ed32453f43ae79ee496c92bd6ec5264e9b0ef3e1bfd67fb66b51e0dee7a1c07f"}}, "version": "V0.2"} -->
# project-keeper V0.2 需求

## 版本目标

2026-10-20，用户要求将当前实现定义为 V0.1 并呈现在指定 GitHub 仓库，同时启动 V0.2 开发。本版从 V0.1 基线分支，承接用户已在 roadmap 明确提出的两项 todo：统一 todo 命名，以及规划内容必须由用户提出、不能被 Agent 自行补写。

## 范围与预期行为

- 新建 roadmap 和相关导航统一称 todo；已有旧标题可读取，不为升级覆盖已有内容。
- 愿景与长期规划、里程碑和 todo 的新增、删除或实质修改，应逐个受影响模块提供用户原话与来源。来源不足时保留原文，在对话提出建议，不能作为正式规划写入。
- 为独立 roadmap 更新提供受控写入入口，并在版本关闭同步 roadmap 时使用同一来源检查。保留实际修改范围和来源日志，检测过期写入依据。
- 规则覆盖初始化、project-update、规划维护及版本关闭；undo 仅恢复既有内容，不借撤销添加新规划。
- 本版不增加独立草稿区或自动捕获对话，不扩展为 Plugin、后台监听或多人实时协作。

## 验收标准

以下为将用户两项要求转译成的可检查标准，最终版本验收仍由用户决定。

- 新项目使用 todo；本项目原有标题校验不匹配消除，旧项目内容保持可读且不被静默改写。
- 受控更新缺少用户原话或来源、遗漏受影响模块的来源、依据过期或结构错误时拒绝写入。
- 版本关闭不能绕过规划来源检查；未改变的规划不要求补造新来源。
- 合法更新只写入提案内容，记录一条带来源的 roadmap-update 日志，保留历史；重试不会覆盖后续编辑。
- 回归测试和新增约束测试通过，Skill 格式校验通过；明确程序不能认证用户身份或自动判断自然语言忠实度。

## 已确认决定与开放问题

- 用户决定：V0.1、V0.2 编号和 GitHub 仓库来自 2026-10-20 当前对话；两项改进来自用户此前清空 todo 并重新指定内容的消息。
- Agent 实现选择：以受影响模块为单位提供原话和来源，在写入入口与关闭准备阶段检查。这是实现方案，不增写为用户的 roadmap 目标或里程碑。
- 历史 Agent 草案的确认状态不因本版升级而改变，不自动认证旧里程碑；旧文件只读兼容不代表其中内容已获用户确认。
- 开放边界：来源由调用者据真实消息填写，不提供身份认证；有权限直接改文件的人仍可绕过工具，不能宣称完全阻止伪造。

## 版本结果

开发中。最终验收和 version-close 尚未执行，具体进展见 spec 与测试结果。
