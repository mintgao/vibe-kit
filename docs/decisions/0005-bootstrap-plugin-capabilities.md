# 0005: Keep the first Codex Plugin bootstrap-only

- Status: Accepted
- Date: 2026-08-27

## Decision

首个 Vibe Kit Codex Plugin 只包含两个唯一命名的入口：`vibe-bootstrap` 用于 plan/init/adopt，`vibe-maintain` 用于 plan/upgrade/doctor/验证制品。Plugin 内嵌与 release ZIP 同版本、逐文件同源的离线 payload。

Plugin 不复制项目内 `vibe-feature-flow` 等运行时 Skills，不提供 MCP server、hooks、apps 或后台网络能力。安装完成后，项目根目录的 `AGENTS.md`、repo Skills、custom agents 与 pinned manifest 成为唯一运行时事实来源；用户开启新的 Agent 任务后才依赖它们。

## Rationale

- 避免全局 Plugin 与项目内同名 Skills 同时出现而产生路由歧义。
- 离线 payload 让新主机和受限网络环境不依赖 `main`、临时 URL 或隐式更新。
- 极小能力面使公开发布前的权限审核和制品同源校验可理解、可测试。

## Consequences

- Plugin 负责发现、安装与维护体验，不替代项目内流程。
- Plugin 版本必须与 bundled kit version 完全一致。
- 真实 marketplace 发布、作者身份、仓库 URL 和许可证在用户选择后补入，不能由本地构建猜测。

## Recovery

卸载 Plugin 不影响已经固定到业务仓库的 Vibe Kit。若 bundled payload 校验失败，停止安装并从已验证的 release ZIP 恢复，不回退到联网获取未固定内容。
