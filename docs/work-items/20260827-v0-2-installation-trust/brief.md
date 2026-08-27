# Vibe Kit v0.2 — Installation state trust

- ID: `20260827-v0-2-installation-trust`
- Size: `M`
- Status: complete
- Created: 2026-08-27

## Goal

将 v0.2 严格收敛为“安装状态可信度加固”：让维护者能够可靠判断当前 Vibe Kit 安装是否完整、一致、可继续使用或升级，并用自动化证据证明 `adopt` 不会覆盖已有项目自己的配置与上下文。

## Context

- Self-hosting pilot 已通过，但在 `docs/work-items/20260827-self-hosting-pilot/verification.md` 中确认了两个可信度缺口。
- `doctor` 当前不会检查 `.vibe/version` 缺失或与 manifest/core 版本不一致，可能错误报告健康。
- 现有 adoption 自动化测试验证了业务文件和 AGENTS 自定义内容，但没有固定断言关键项目自有配置与上下文逐字节保持不变。

## Scope

- In（P0）: 为 `doctor` 增加 `.vibe/version`、manifest `framework_version`、`.vibe/core/version` 三方完整性与一致性诊断；增加项目自有配置和上下文的 adoption 不覆盖回归测试。
- In（发布必需）: 将框架版本统一提升为 `0.2.0`；更新 README、长期上下文和验收证据；从 v0.1 状态完成一次 v0.2 self-upgrade 与独立 QA。
- Out: 联网更新、自动下载、PyPI/npm/Homebrew 发布、全局安装、自动修复版本、交互式向导、新角色、新 Skill、新工作流、任意 YAML 解析、自动删除过期托管文件或 CLI 全面重构。

## Acceptance criteria

- [x] AC-1: `.vibe/version`、manifest 版本和 core 版本均存在、非空且精确一致时，`doctor` 返回 0；stdout 显示版本完整性通过，stderr 为空。
- [x] AC-2: `.vibe/version` 缺失或为空时，`doctor` 返回 1，stderr 列出缺失路径、另外两处实际值、可信 checkout 的 upgrade 指引和复查命令。
- [x] AC-3: installed/manifest/core 任一版本缺失、为空或与另外两处不一致时，`doctor` 返回 1 并聚合显示三处状态；不得抛出未处理异常或返回表示用法错误的 2。
- [x] AC-4: 对预置 `.vibe/project.yaml`、`.vibe/project-rules.md`、`docs/context/` 关键文档及其他项目文件的已有项目执行 `adopt` 后，这些内容逐字节不变，同时托管资产安装成功。
- [x] AC-5: 从 v0.1 安装状态使用 v0.2 checkout 无冲突升级后，托管资产更新、项目自有文件不变，三处版本统一为 `0.2.0`，随后 `doctor` 通过。
- [x] AC-6: 既有冲突升级原子性、非版本 warning 和退出码语义不回退；失败的 `doctor` 全程只读，不修改文件。
- [x] AC-7: 完整场景测试和语法检查在 Python 3.9+ 通过，本仓库的 `vibe doctor .` 与 `vibe verify .` 通过；跳过的检查必须记录原因。
- [x] AC-8: README、项目上下文与 verification 对 v0.2 能力、限制和证据表述一致，不宣称联网更新、自动修复或其他未交付能力。

## Design and technical notes

- CLI 版本完整性只比较去除首尾空白后的精确值，不判断 SemVer 大小，也不声称是否为最新版。
- 成功信息写 stdout，退出码 0；缺失或不一致写 stderr，退出码 1。
- 错误应作为一个聚合诊断列出 installed、manifest、core 三处实际状态，避免同一问题重复轰炸用户。
- 修复指引要求从“用户希望安装的版本对应的可信 Vibe Kit checkout”运行 `upgrade`，不得建议直接编辑 manifest 或 `.vibe/version`。
- `doctor` 只诊断不修复、不写文件；其他现有 warning 行为保持不变。
- 这是 CLI 交互的轻量 UX 契约，不需要页面、视觉稿或完整设计文档。

## Risks and open decisions

- 修改版本诊断时不能破坏 v0.1 → v0.2 的正常升级路径；升级前的旧状态可能正是 v0.2 需要修复的状态。
- 若实现要求改变 ownership 模型、manifest 兼容协议或引入迁移，应停止并重新评估为独立 M/L 工作项，而不是夹带进入 v0.2。
- 实现保持 manifest schema 与 ownership 不变：新增只读版本状态解析和聚合诊断；场景矩阵覆盖正常、缺失、空值、不一致、warning、adopt 保留、无冲突升级和冲突原子性。
