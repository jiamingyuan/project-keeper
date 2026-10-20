# 辅助脚本接口

Python 3.9+，仅标准库。以下命令接在 `python3 <skill>/scripts/project_keeper.py` 后；全局 `--project <项目根目录>` 放在子命令之前。所有输出为 JSON：0 成功，1 校验失败或部分关闭/撤销，2 参数/路径/冲突错误。检查输出，不只看命令启动成功。

不执行应用代码或测试。写命令仅在当前任务允许时调用；只读命令不记日志。运行脚本不必把源码全部加载到模型；需要诊断时才阅读实现。

## 定位、生成与验证

```text
--project <root> context
--project <root> context --version V1.0
--project <root> init --name <用户提供的项目名>
--project <root> version-create V1.0 --name <项目名>
--project <root> scaffold V1.0 spec.md --name <项目名>
--project <root> scaffold V1.0 test-plan.md --name <项目名>
--project <root> scaffold V1.0 test-results.md --name <项目名>
--project <root> sync-index
--project <root> validate --version V1.0 --stage plan
```

未初始化时 context 返回 initialized=false，不创建文件。init 只补缺失文件，复用文件须由 Agent 读取检查；同名目录/符号链接冲突会失败，部分生成可能已存在，不能声称全部完成。init/version-create/scaffold/sync-index 是 Action 的内部步骤，Agent 完成实际内容后统一记录该行为。

validate 的阶段为 requirements、plan、test、close。按阶段要求文件，不要求未来产物提前存在；close 还要求有效 code/test 执行记录，但不代表已获用户确认。章节序列以各模板为单一来源，允许模板模块内增加内容。log 特殊处理为行为流。

config.toml 只预留注释，非注释内容会被告警但不使用。不提供路径配置或全局配置继承。

## 原文导航

```text
--project <root> read architecture.md --section 关键机制与设计取舍
--project <root> read V1.0/requirements.md
--project <root> read log.md --event code-001
```

路径相对 pjkp；section 按标题精确提取至下一同级/上级标题，保留内容，不摘要或静默截断；标题不唯一报错。context 默认只展开项目文档，--version 增加目标版本，--all-versions 才展开全部版本；返回字节数、指纹、标题与行号，不返回全文，不列全部历史日志标题，也不扫描操作快照正文。发现歧义时读取更完整源材料。

## 日志与执行记录

用 apply_patch 创建 UTF-8 正文文件（可在临时目录），不要把复杂正文嵌进 shell 字符串。

```text
--project <root> log --id init-001 --action project-initiate --body-file <正文路径>
--project <root> log --id plan-001 --action plan --version V1.0 --outcome partial --body-file <正文路径>
--project <root> record code V1.0 --id code-001 --body-file <正文路径> --implementation src/app.py --implementation tests/test_app.py
--project <root> record test V1.0 --id test-001 --body-file <正文路径>
```

log/record 可带 --parent <外层行为或操作id>。日志 id 为 ASCII 字母/数字及 `_.:-`，不超过 120 字符；新一次真实行为用新 id，同次写入重试沿用 id 与相同正文，内容不同报错。

record 会记录一条对应 Action 日志，无需额外 log。code 记录 spec、需求和指定实现文件的指纹，并使旧 test 记录失效；test 引用当前 code 批次和当前测试材料。implementation 是相对项目根的实际文件，不能指向 pjkp 内文档。缺少实现依据、过期 code 记录或已关闭版本会拒绝。

原始行为正文也应保留真实命令、结果、来源和未完成项。脚本只能确认文件与依据存在/一致，无法证明调用者确实执行过、覆盖完整，不能把 record 当完成事实的生成器。需求改动引发告警后，先检查影响和补做必要工作，再记录新依据。

requirements 的 `pjkp:state` 注释是脚本执行元数据，不是配置。不要手改它；当前需求正文和版本结果仍可由 Agent 维护，关闭状态由 close 命令维护。

关闭/undo 时才读取 [关闭辅助接口](close-cli.md)，普通项目任务不加载提案和恢复细节。

## 限制与异常恢复

- 写入锁只协调本脚本。异常退出后锁可能残留；先检查锁中 PID/时间和操作记录，确认没有运行进程后由用户或已获授权的 Agent 移除该单一锁文件。不要自动删除不明锁。
- 每份文件采用原子替换及写前指纹检查，但外部编辑器不参与锁协议；不承诺抵抗恶意竞态或完整多人并发事务。
- 进程中断可根据已落盘操作记录续接；不承诺断电后跨文件/目录的全盘事务持久性。
- 没有自动抓取完整代码树或外部环境快照。显式实现文件之外的依赖变化须人工检查，不把哈希未变当成语义保证。
- 代码/测试与验收记录是调用者对真实依据的记载，不具备身份认证。不能生成一条假的“用户已确认”来通过检查。
