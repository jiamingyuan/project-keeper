<!-- pjkp:state {"closed_by": null, "code": {"basis": {"V0.2/requirements.md": "a9c1aac2b974f3bbe2930dc8a4fe4923151aa029a269bc6bea36ff9b3e8388bf", "V0.2/spec.md": "1b0c4b8c451776e4ae82e4e23b22361377025bc5700fc7f353c58b9b2467d6a1"}, "id": "code-20261020-v02-002", "implementation": {"SKILL.md": "283392b661dc2c3c1f533fb9dec32425304e4e50dd47b71eace86da615122dde", "assets/log-actions.json": "b583cd28fd68804c46b4662b6dce4e838cafd824fab5228f98e2d065792973b4", "assets/templates/index.md": "d7e4a4914fb3a48b3fceee3008ac3e361cfbdd53221e7a0593bbc312b912e398", "assets/templates/log.md": "350b84d7b7680b745f168e9949c8717fc24f573af8e62876100dc003427c6fbc", "assets/templates/roadmap.md": "fba15df18630e1453fe8e451cd9801226cfadab1e46bde041d53ddd67e556f16", "references/cli.md": "b978cb8444280bf374fba84f9a297e4ec180299eb9bf45acb1ee5ff5e3d0f995", "references/close-cli.md": "b6bb23c07b212064504d8f5918bc0963049a2393f298fc99a68a74515730e0c7", "references/closing.md": "0c93808b84636103d815491fdac33500537b42d9c4b2ebca82f43bc80c721e59", "references/execution.md": "aabd95f5454f8d4bfdcfe1583ea0c0a882b905b71a7ffd91b2267b2eec299a56", "references/logging.md": "c249874ce13b7a3beb45563ad2cfc174e21599eb25fa9183b5f523ffea2d9db1", "references/planning.md": "ac3deb1c855b8dc042f7e0c755a94c4d872f03947b749c41b3fad222a5144fb5", "references/project.md": "1995848c34ceba08b022118db43628c7bae3703e6fa62ce85d027d0b89da907d", "references/roadmap.md": "bcb37361e1ae6347ce6928ca90bf20bd2f02be8f7109a9db916152b750cb9ebd", "references/verification.md": "6fcb58b5395c82b6f14a74da8af8420132255e1e6fe96280f26a63c45e0f5c06", "scripts/project_keeper.py": "62d7043b6e61322d6858baf9062939d756748460359c6a0e7602136a7defefaa", "tests/measure_context.py": "51f9275a7dd320eccc31c9d3b6510124de75b332166beca9147ceb4c9802f255", "tests/test_project_keeper.py": "e592fa6716ff4e219f083751512ed8418ff8446a756107c148435c673ff6e328"}}, "phase": "awaiting-acceptance", "test": {"basis": {"V0.2/requirements.md": "a9c1aac2b974f3bbe2930dc8a4fe4923151aa029a269bc6bea36ff9b3e8388bf", "V0.2/spec.md": "1b0c4b8c451776e4ae82e4e23b22361377025bc5700fc7f353c58b9b2467d6a1", "V0.2/test-plan.md": "a5675b9e1f4e60c9db52d2139ab6411e08b80b0fcefce6edbd1181ca371f4eb9", "V0.2/test-results.md": "efebb23188d5163e3470bfc61195cb27e3c6295771970d611019a09149e9eec4"}, "code_id": "code-20261020-v02-002", "id": "test-20261020-v02-002", "implementation": {"SKILL.md": "283392b661dc2c3c1f533fb9dec32425304e4e50dd47b71eace86da615122dde", "assets/log-actions.json": "b583cd28fd68804c46b4662b6dce4e838cafd824fab5228f98e2d065792973b4", "assets/templates/index.md": "d7e4a4914fb3a48b3fceee3008ac3e361cfbdd53221e7a0593bbc312b912e398", "assets/templates/log.md": "350b84d7b7680b745f168e9949c8717fc24f573af8e62876100dc003427c6fbc", "assets/templates/roadmap.md": "fba15df18630e1453fe8e451cd9801226cfadab1e46bde041d53ddd67e556f16", "references/cli.md": "b978cb8444280bf374fba84f9a297e4ec180299eb9bf45acb1ee5ff5e3d0f995", "references/close-cli.md": "b6bb23c07b212064504d8f5918bc0963049a2393f298fc99a68a74515730e0c7", "references/closing.md": "0c93808b84636103d815491fdac33500537b42d9c4b2ebca82f43bc80c721e59", "references/execution.md": "aabd95f5454f8d4bfdcfe1583ea0c0a882b905b71a7ffd91b2267b2eec299a56", "references/logging.md": "c249874ce13b7a3beb45563ad2cfc174e21599eb25fa9183b5f523ffea2d9db1", "references/planning.md": "ac3deb1c855b8dc042f7e0c755a94c4d872f03947b749c41b3fad222a5144fb5", "references/project.md": "1995848c34ceba08b022118db43628c7bae3703e6fa62ce85d027d0b89da907d", "references/roadmap.md": "bcb37361e1ae6347ce6928ca90bf20bd2f02be8f7109a9db916152b750cb9ebd", "references/verification.md": "6fcb58b5395c82b6f14a74da8af8420132255e1e6fe96280f26a63c45e0f5c06", "scripts/project_keeper.py": "62d7043b6e61322d6858baf9062939d756748460359c6a0e7602136a7defefaa", "tests/measure_context.py": "51f9275a7dd320eccc31c9d3b6510124de75b332166beca9147ceb4c9802f255", "tests/test_project_keeper.py": "e592fa6716ff4e219f083751512ed8418ff8446a756107c148435c673ff6e328"}}, "version": "V0.2"} -->
# project-keeper V0.2 需求

## 版本目标

2026-10-20，用户要求将当前实现定义为 V0.1 并呈现在指定 GitHub 仓库，同时启动 V0.2 开发。本版从 V0.1 基线分支，承接用户已在 roadmap 明确提出的两项 todo：统一 todo 命名，以及规划内容必须由用户提出、不能被 Agent 自行补写。

## 范围与预期行为

- 新建 roadmap 和相关导航统一称 todo；已有旧标题可读取，不为升级覆盖已有内容。
- 愿景与长期规划、里程碑和 todo 的新增、删除或实质修改，应逐个受影响模块提供用户原话与来源。来源不足时保留原文，在对话提出建议，不能作为正式规划写入。
- 为独立 roadmap 更新提供受控写入入口，并在版本关闭同步 roadmap 时使用同一来源检查。保留实际修改范围和来源日志，检测过期写入依据。
- 规则覆盖初始化、project-update、规划维护及版本关闭；undo 仅恢复既有内容，不借撤销添加新规划。
- 2026-10-20 用户追加要求：规范化 log 的内容呈现，对每个 Action 定义日志内容。覆盖七个主要 Action、undo 和现有辅助/扩展行为，明确必备内容、顺序、格式、状态与证据位置。
- 新写入采用可检查的规范结构；旧日志及已有恢复操作保持原格式，不补造历史字段。
- 本版不增加独立草稿区或自动捕获对话，不扩展为 Plugin、后台监听或多人实时协作。

## 验收标准

以下为将用户两项要求转译成的可检查标准，最终版本验收仍由用户决定。

- 新项目使用 todo；本项目原有标题校验不匹配消除，旧项目内容保持可读且不被静默改写。
- 受控更新缺少用户原话或来源、遗漏受影响模块的来源、依据过期或结构错误时拒绝写入。
- 版本关闭不能绕过规划来源检查；未改变的规划不要求补造新来源。
- 合法更新只写入提案内容，记录一条带来源的 roadmap-update 日志，保留历史；重试不会覆盖后续编辑。
- 回归测试和新增约束测试通过，Skill 格式校验通过；明确程序不能认证用户身份或自动判断自然语言忠实度。
- 每个已定义 Action 都能查询其日志字段并按统一形式写入；缺章、空内容、错序和未知 Action 不能以新格式成功落盘。
- 自动生成的规划、关闭、撤销和执行记录遵循同一规范，保留失败、部分完成与父子关联；旧历史和重试兼容。

## 已确认决定与开放问题

- 用户决定：V0.1、V0.2 编号和 GitHub 仓库来自 2026-10-20 当前对话；两项改进来自用户此前清空 todo 并重新指定内容的消息。
- 追加来源：用户原话“V0.2 中，我要求规范化 log 中的内容呈现，这需要 pjkp 对每个 action 都进行一下 log 内容的定义”。
- Agent 实现选择：以受影响模块为单位提供原话和来源，在写入入口与关闭准备阶段检查。这是实现方案，不增写为用户的 roadmap 目标或里程碑。
- 历史 Agent 草案的确认状态不因本版升级而改变，不自动认证旧里程碑；旧文件只读兼容不代表其中内容已获用户确认。
- 开放边界：来源由调用者据真实消息填写，不提供身份认证；有权限直接改文件的人仍可绕过工具，不能宣称完全阻止伪造。

## 版本结果

开发中。最终验收和 version-close 尚未执行，具体进展见 spec 与测试结果。
