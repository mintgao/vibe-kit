# 0004: Build deterministic local release candidates before channel publication

- Status: Accepted
- Date: 2026-08-27

## Decision

Vibe Kit 从 canonical working tree 生成两个 normalized ZIP：项目安装 payload 与 bootstrap-only Codex Plugin。ZIP 的路径顺序、时间戳、权限和压缩参数固定；同一输入必须产生相同 SHA-256。一个 machine-readable release manifest 声明版本、协议、支持矩阵、source 状态、payload 文件摘要和最终 artifact 摘要，`SHA256SUMS` 是面向常用工具的等价视图。

构建与校验分离。`vibe package` 只构建本地 release candidate；`vibe validate-release` 先验证外层摘要、ZIP 路径安全、版本/协议、Plugin 权限边界和 bundled payload 同源性，才允许把制品交给安装演练。没有 Git commit/tag 时 source ref 必须为空，状态必须是 `release-candidate-unpublished`。

## Rationale

- 跨主机传输需要一个不依赖原始 checkout 的完整离线输入。
- 可复现构建能识别渠道内容漂移，并让 Plugin 与 release ZIP 共享同一信任根。
- 显式记录未知 provenance 比从工作树状态伪造 release 身份更安全。
- 把远端发布留在构建之后，可在没有 GitHub 身份或网络时完成绝大多数质量验证。

## Consequences

- 发布物只包含 allowlist 中的 managed runtime 与必要说明，不包含本地反馈、业务 work item、Git 历史或缓存。
- SHA-256 只证明内容与清单一致；公开发布前仍需选择发布身份、许可证、仓库、tag 和后续签名策略。
- 任何 archive、manifest、checksum 或 Plugin payload 漂移都使整个 release candidate 失败，不能只发布其中一个渠道。

## Recovery

删除失败的候选输出并从同一 canonical source 重建。项目级恢复继续使用 Git revert 或受控地从旧版可信 payload 执行 upgrade；禁止手改版本或摘要。
