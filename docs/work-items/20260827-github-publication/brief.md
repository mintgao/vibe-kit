# Publish Vibe Kit v0.3.0 GitHub prerelease

- ID: `20260827-github-publication`
- Size: `L`
- Status: implementing
- Created: 2026-08-27

## Goal

将已经通过本地制品验收的 Vibe Kit 0.3.0 以可验证的 GitHub Public Pre-release 形式发布，让其他人或主机可以从 `mintgao/vibe-kit` 下载完整附件、恢复 marketplace、验证摘要并安装，而不会把尚未完成的 Linux CI、签名或公共 Plugin Directory 审核误称为 stable。

## Context

- `20260827-distribution-delivery` 已独立验收 deterministic release、Plugin 与离线安装；当前 dist 仍标记 unpublished，source ref 为空。
- 用户确认发布参数：`mintgao/vibe-kit`、Public、MIT、Git author `mintgao <154321591+mintgao@users.noreply.github.com>`、tag `v0.3.0`、GitHub Pre-release。
- GitHub CLI 已重新认证为 `mintgao`，目标仓库名当前未占用。

## Scope

- In: 补齐 MIT LICENSE、GitHub/作者元数据、中央 feedback repository 和 prerelease 状态。
- In: 生成适合 GitHub Release 单独下载的完整 distribution bundle，保留内部 manifest/SHA 校验。
- In: 首个 commit、annotated tag、Public GitHub repository、Pre-release 和附件上传。
- In: 从 GitHub 重新下载附件，在隔离目录执行 checksum、release validation 和 smoke install。
- Out: stable promotion、Linux CI、签名/provenance、Plugin Directory 发布、自动更新或包管理器发布。

## Acceptance criteria

- [ ] AC-1: 仓库包含用户确认的 MIT LICENSE，Git/Plugin/README/release metadata 使用 `mintgao` 与 `https://github.com/mintgao/vibe-kit`，不保留占位发布身份。
- [ ] AC-2: prerelease package 记录非空 commit source ref、clean tree 和 `prerelease` 状态；validator 接受已知状态并拒绝未知状态。
- [ ] AC-3: GitHub 附件包含 deterministic distribution bundle；解压后具备 release ZIP、Plugin ZIP、expanded marketplace、manifest 与 SHA256SUMS，可独立完成 `validate-release`。
- [ ] AC-4: 全量测试、Python 3.9、官方 Plugin/Skill validator、bundle rebuild parity 与独立 QA 全部通过。
- [ ] AC-5: 初始 commit 不包含 `.vibe/local/feedback`、dist、secret、缓存或本机凭据；commit author 与用户确认一致。
- [ ] AC-6: `mintgao/vibe-kit` 被创建为 Public，`main` 推送成功，annotated `v0.3.0` tag 指向验收 commit。
- [ ] AC-7: GitHub `v0.3.0` Release 标记 Pre-release，标题、notes 与所有附件完整且远端摘要/大小可核对。
- [ ] AC-8: 从 GitHub 下载完整 bundle 后在隔离目录完成解包、`validate-release`、`plan init`、`init` 和项目内 `doctor`。
- [ ] AC-9: `.vibe/core/feedback.json` 指向 `mintgao/vibe-kit`，但仍保持逐 payload 授权、无自动 Issue/遥测。
- [ ] AC-10: 发布证据记录真实 URL、commit/tag、附件摘要、跳过项和 rollback；发布后的 Vibe Kit gap 复盘按 feedback flow 执行。

## Design and technical notes

- 发布为 GitHub Pre-release，不修改公共 stable 语义。
- distribution bundle 是外层传输包装，不进入内部 manifest 自引用；解压后由内部 `SHA256SUMS` 和 `validate-release` 建立内容完整性。
- 远端创建与上传使用 `gh`；任何返回不确定时先读取远端状态再重试，避免重复仓库、tag 或 Release。
- rollback：删除或将 GitHub Release 标记 draft、删除远端 tag；Public 仓库与首个 commit 不在不确定状态下自动删除。

## Risks and open decisions

- GitHub Release 无法替代发布者签名；本次使用认证账号、Git commit/tag 和摘要作为 prerelease 信号。
- 首次 release 在 Linux 未执行，因此必须保留 Pre-release 标记。
