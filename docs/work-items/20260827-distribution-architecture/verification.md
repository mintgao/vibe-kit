# Verification: Vibe Kit distribution architecture

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | `design.md` 的 Decision summary、Share an existing project 与 ADR 0002 均把 repository-pinned installation 定义为运行时事实来源。 | Pass |
| AC-2 | `design.md` 将 core specification 与 agent adapters 分层，并要求 adapter 从 canonical release source 生成及执行 conformance scenarios。 | Pass |
| AC-3 | Users and scenarios、channel matrix 与 user flows 覆盖分享给别人、换主机、Codex、其他 Agent 和 offline bundle。 | Pass |
| AC-4 | Version and compatibility、Trust、Upgrade、Rollback 定义精确版本、digest、来源、schema/core/adapter 兼容与 Git/状态快照恢复。 | Pass |
| AC-5 | 路线图将 v0.3 release bundle、v0.4 Codex bootstrap、v0.5 multi-agent adapter 和后续公开发布拆成独立门禁。 | Pass |
| AC-6 | ADR 0002 接受 channel-neutral release + project pinning；Rejected alternatives 明确否决 merge 脚手架、global-only、同名 Skills 重复和多份 core。 | Pass |

## Reviews performed

- 独立 PM/架构评审确认：Git release 应是跨主机/跨 Agent payload 来源，项目 vendoring 是运行时真相，Codex Plugin 只做 bootstrap，其他宿主使用薄 adapter。
- 评审意见已落实：v0.4 Plugin 使用唯一命名的 bootstrap/maintain Skills，不重复项目内六个运行时 Skills；MCP 与 hooks 不进入首版 Plugin。
- 对照 OpenAI 官方 Skills、Plugin packaging 与 AGENTS.md discovery 文档检查了 repo scope、可安装渠道和项目指令发现边界。

## Not executed

- 未构建 GitHub Release、checksum、Plugin、marketplace 或非 Codex adapter；它们是 v0.3+ 的实施范围。
- 未验证 Windows 或任何第二 coding agent；v0.3/v0.5 必须先确定支持矩阵和 conformance evidence。
- 未验证公开 Plugin submission；需要发布身份、许可证、支持与安全流程后再开始。

## Residual risks

- Plugin 是否能在所有目标 Codex surface 中安全执行 bundled installer，需要在 v0.4 宿主测试中验证；不支持时必须回退到固定 digest 的 release resolver，而不能改为追踪 `main`。
- 未来 adapter generation、provenance 与 rollback 仍需各自 ADR，当前总架构不能替代具体协议设计。
