# Vibe Kit distribution architecture

- ID: `20260827-distribution-architecture`
- Size: `L`
- Status: designed
- Created: 2026-08-27

## Goal

让个人、团队、不同主机和不同 coding agent 都能以可验证、可固定版本、可升级和可回滚的方式采用 Vibe Kit，同时保证项目里的执行规则不依赖某个用户的本机配置。

## Users and scenarios

1. 项目作者把 Vibe Kit 分享给协作者；协作者 clone 项目后直接获得同一套项目规则。
2. 同一个人在新主机上继续项目；除 Python 3.9+ 和项目仓库外，不依赖旧主机的个人目录。
3. 用户在新的项目中从可信版本初始化，或在开发到一半的项目中保守接入。
4. Codex 用户通过可安装入口发现和使用工作流，不需要先理解仓库内部结构。
5. 其他 coding agent 在能力不同的情况下复用同一套核心规范；不支持并行子 Agent 时可以退化为顺序角色审查。

## Scope

- In: 定义规范内核、Agent 适配器、项目安装器和渠道包装的边界。
- In: 定义 GitHub Release、Codex Plugin、离线包和其他 Agent 适配器的职责。
- In: 定义版本固定、来源记录、完整性校验、兼容性、升级、回滚和发布门禁。
- In: 给出分阶段落地路线图和首个可交付里程碑。
- Out: 在 v0.2 中实现远程下载、公开发布、包管理器安装或其他 Agent 适配器。
- Out: 让个人级或主机级安装覆盖项目中固定的规则。
- Out: 为了跨平台而把所有平台差异塞进一份通用 Prompt。

## Acceptance criteria

- [x] AC-1: 明确项目内固定安装是运行时事实来源，个人/主机安装只是获取入口。
- [x] AC-2: 明确一个规范内核、多个生成式适配器，避免手工维护多份规则。
- [x] AC-3: 覆盖给别人、换主机、Codex、其他 Agent 和离线环境五类分发场景。
- [x] AC-4: 定义不可变版本、摘要校验、来源记录、兼容矩阵和回滚原则。
- [x] AC-5: 给出从 v0.2 到公开分发的分阶段路线图，且每阶段可以独立验收。
- [x] AC-6: 形成 ADR，记录为什么不采用“直接 merge 脚手架仓库”或“只装全局 Plugin”。

## Deliverables

- `design.md`: 分发架构、用户流程、制品模型和路线图。
- `docs/decisions/0002-project-pinned-distribution.md`: 长期架构决策。

## External constraints reviewed

- OpenAI 将 repo-scoped Skills 定位为本地/项目内工作流，将 Plugins 定位为超出单仓库的可安装分发方式：[Build skills](https://learn.chatgpt.com/docs/build-skills)。
- Plugin 可以打包一个或多个 Skills，并以 `.codex-plugin/plugin.json` 作为入口；本地 marketplace 可以来自 Git 仓库并固定 ref：[Package your plugin](https://developers.openai.com/plugins/build/plugins)。
- Codex 会在项目根目录到当前目录的路径上加载 `AGENTS.md`，所以项目内适配器可以随仓库传给协作者：[Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。

## Open decisions for implementation

- 首个公开仓库、发布身份、许可证和签名方式。
- v0.3 是否只提供压缩包与校验和，还是同时提供 `vibe package` 构建命令。
- 第一个非 Codex 适配器的目标宿主及其最低版本。
- Plugin 是仅提供工作流入口，还是内含同版本离线安装 payload；设计建议后者，但需先做宿主权限验证。
