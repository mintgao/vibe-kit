# Release-ready Vibe Kit distribution

- ID: `20260827-distribution-delivery`
- Size: `L`
- Status: complete
- Created: 2026-08-27

## Goal

让 Vibe Kit 能从同一份 canonical source 生成可复现、可离线传输、可校验并能被 Codex Plugin 引导安装的 0.3.0 release candidate；新项目和开发到一半的项目都能在写入前看到 plan，并从实际制品完成安装或升级。

## Context

- 分发总架构已经由 `20260827-distribution-architecture` 和 ADR 0002 固定：渠道只负责获取，业务仓库里的固定安装才是运行时事实来源。
- 第 1 项 self-retrospective 指出升级回归不能长期依赖“改版本号模拟旧 release”，本工作项开始建立不可变制品与历史 fixture 合同。
- 当前仓库无 commit、remote、发布身份和有效 `gh` 登录，因此可以完成 release-ready 本地产物与验证，但不能宣称已公开发布。

## Scope

- In: `plan init|adopt|upgrade` 只读预检，展示将创建、更新、保留、冲突的路径。
- In: `package` 从 canonical managed source 构建 deterministic ZIP、SHA-256 和 machine-readable release manifest。
- In: bootstrap-only Codex Plugin，内含同版本离线 payload，只提供安装与维护入口，不复制项目运行时 workflow Skills，不引入 MCP、hooks 或 apps。
- In: `validate-release` 校验摘要、ZIP 安全、版本/协议、Plugin 能力和 payload 同源性。
- In: 从生成的制品验证 init、adopt、upgrade、冲突原子性、doctor、篡改拒绝与重复构建一致性。
- Out: 创建 GitHub repository/tag/release、发布 Marketplace、注册 npm/PyPI/Homebrew 名称、自动联网更新或签名。
- Out: Windows 和非 Codex Agent 的等价能力声明。

## Acceptance criteria

- [x] AC-1: `plan init|adopt|upgrade` 不写目标项目，并准确标出 create/update/preserve/conflict/no-op；真实写入结果与 plan 一致。
- [x] AC-2: `package` 只使用 Python 3.9+ 标准库，连续两次构建的 release ZIP 和 Plugin ZIP SHA-256 完全一致。
- [x] AC-3: release manifest 声明 kit、manifest schema、core protocol、Codex adapter capability、Python/OS 支持、source 状态与每个制品摘要；`SHA256SUMS` 与其一致。
- [x] AC-4: release ZIP 包含运行 `init/adopt/upgrade/doctor/verify/feedback` 所需的完整 canonical payload，解包后无需网络即可工作。
- [x] AC-5: Plugin 使用规范 manifest，只提供唯一命名的 `vibe-bootstrap` 与 `vibe-maintain` Skills，内含相同 release payload，不含运行时同名 Skills、MCP、hooks 或 apps。
- [x] AC-6: `validate-release` 在写项目之前拒绝 checksum 不符、危险 ZIP 路径、版本漂移、Plugin payload 漂移或越权能力。
- [x] AC-7: 从 release ZIP 在干净临时目录完成新项目 init、已有项目 adopt、0.2 fixture 到 0.3 upgrade；冲突时 managed files 与安装 state 不变，仅生成 review candidate，并在各成功场景通过 doctor。
- [x] AC-8: 从 Plugin ZIP 的 bundled payload 完成至少一个离线 init/adopt 演练，结果与 release ZIP 安装的 managed hashes 一致。
- [x] AC-9: README、release notes、ADR 和发布清单准确说明离线/Plugin/GitHub 使用路径、支持矩阵、验证命令、回滚方式与“未公开发布”边界。
- [x] AC-10: 独立 QA 从最终制品而非工作树完成 criterion-to-evidence 验收，所有跳过项与原因被记录。

## Design and technical notes

- 采用 normalized ZIP：文件顺序、时间戳、权限和 JSON 序列化固定；制品名含精确 SemVer。
- release ZIP 是安装 payload；Plugin ZIP 只在它之外增加安装发现层，Plugin 内 payload 必须逐文件同源。
- 构建 manifest 标为 `release-candidate-unpublished`，没有 Git tag/commit 时 source ref 保持 `null`，不能伪造 provenance。
- 兼容基线：macOS/Linux、Python 3.9+；本机只执行 macOS，Linux 记为 CI 待办，不宣称本轮已运行。
- 具体协议见 ADR 0004；Plugin 权限边界见 ADR 0005。

## Risks and open decisions

- 当前没有已发布的 0.2 不可变 artifact；升级场景会先用规范化 fixture 记录这一事实，首个真实历史制品从 0.3.0 开始保留。
- Plugin 的公开命名、作者身份、仓库 URL、许可证和 marketplace 发布需要用户后续选择。
- SHA-256 提供完整性，不提供发布者身份；签名/provenance 是公开稳定发布前的后续门禁。
