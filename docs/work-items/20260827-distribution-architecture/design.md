# Distribution design

## Decision summary

采用“双层分发、项目固定”的模型：

```text
Canonical source
  ├─ release bundle + checksum ──> project installer ──> repository-pinned Vibe Kit
  ├─ Codex plugin / marketplace ─> discovery + bundled installer ─┘
  └─ agent adapter packages ─────> host-specific files ──────────┘
```

- **项目层是事实来源**：真正影响开发行为的版本、规范、Skills、Agent 配置和安装状态进入业务仓库。
- **渠道层是获取入口**：GitHub Release、Plugin、私有 marketplace 或离线包负责把同一个版本送到项目，不成为项目运行的隐形依赖。
- **适配层是生成结果**：平台特有文件从同一套核心规范生成，不允许长期手工复制和分别演化。

## Layered architecture

### 1. Core specification

保持平台中立，包含：

- `.vibe/core/` 的工作分级、质量门禁、模板和协议版本；
- PM、UX、RD、QA、Investigator 的职责与交接契约；
- work item、decision、verification 等文档结构；
- 安装 ownership、升级冲突和证据契约。

核心不假设宿主一定支持自定义 Agent、并行执行或某种专有命令。角色代表独立判断职责；能力较弱的宿主可顺序执行。

### 2. Agent adapters

每个宿主适配器只负责三件事：

1. 告诉宿主如何发现项目指令；
2. 把通用 workflow 暴露成该宿主可调用的 Skills/commands；
3. 在宿主支持时映射 PM/UX/RD/QA/Investigator 为独立 Agent。

首个适配器是 Codex：`AGENTS.md` managed block、`.agents/skills/`、`.codex/agents/`。后续适配器必须从同一个 release source 生成，并通过一组共同 conformance scenarios；不支持独立 Agent 的平台必须明确标记为 `sequential-review`，不能假装完成独立审查。

### 3. Project installer

`vibe init/adopt/upgrade/doctor` 是跨渠道共享的 materializer：

- 输入是一个已校验、明确版本的 release payload；
- 输出是业务仓库中固定版本的 managed files 与项目自有文件；
- 使用 manifest 记录文件哈希、版本和未来的来源信息；
- 安装和升级先 preflight，再原子写入；冲突不做静默合并；
- 项目自有上下文不被升级覆盖。

未来远程获取应是独立的 fetch/resolution 步骤，完成校验后才调用现有安装器。安装器不应边下载边修改业务仓库。

### 4. Channel packages

| 渠道 | 适用场景 | 包含内容 | 不承担 |
|---|---|---|---|
| GitHub Release | 默认公开分发、CI、跨主机 | 不可变源码/离线 bundle、SHA-256、release notes | 自动修改项目 |
| Git checkout | 贡献开发、提前试用 | 完整源码；必须固定 tag/commit | 稳定版本发现 |
| Codex Plugin | Codex/ChatGPT 中发现和一键进入流程 | 唯一命名的 bootstrap/maintain Skills、与 Plugin 同版本的安装 payload 或固定 release resolver | 项目运行时 Skills；替代项目内版本 |
| Private marketplace | 团队内测和灰度 | 固定 ref 的 Plugin catalog | 公网信任根 |
| Offline bundle | 隔离网络或审计环境 | release payload、摘要、来源元数据 | 查询最新版 |
| Other-agent adapter | 非 Codex 宿主 | 核心 Skills + 宿主薄适配文件 + 兼容声明 | 分叉核心规范 |

## User flows

### Share an existing project

项目作者完成 `adopt` 或 `init` 后提交项目内 managed files、`.vibe/manifest.json`、`.vibe/version` 和项目上下文。协作者在任意主机 clone 项目，运行 `./bin/vibe doctor`，再开启新的 Agent session。协作者不必单独安装全局 Skill 才能遵循项目规则。

### Start a new project on another host

1. 从 GitHub Release、Plugin 或离线介质选择明确版本。
2. 校验摘要和发布来源。
3. 先用技术栈生成器创建应用。
4. 从已校验 payload 运行 `vibe init <project>`。
5. 运行项目内 `./bin/vibe doctor` 并提交安装结果。

### Adopt an in-progress project

1. 固定并校验 release。
2. 执行未来的 `vibe adopt --plan` 查看将创建、管理和保留的路径。
3. 执行 `adopt`；有托管路径碰撞时停止。
4. 运行 onboarding，补充真实项目上下文。
5. 审查 diff、运行 doctor/verify 后提交。

### Use with another coding agent

1. 选择声明兼容当前 core protocol 的适配器。
2. installer 将核心与对应 adapter 写入项目。
3. conformance check 验证入口、Skill 触发、角色降级和验证证据。
4. 项目文档仍是共享事实；切换 Agent 不迁移历史 Prompt。

## Version and compatibility model

后续 release 同时声明四个维度：

- `kit_version`: 用户看到的 Vibe Kit SemVer；
- `manifest_schema`: 安装状态的读写协议；
- `core_protocol`: workflow、角色与证据契约版本；
- `adapter_compatibility`: adapter 版本、支持的 core protocol、宿主最低版本和能力等级。

原则：

- 默认安装必须固定 tag、commit 或精确 release version，不能隐式跟随 `main`。
- Plugin、离线 bundle 和 GitHub Release 使用同一个 `kit_version`，由发布流水线生成，禁止手工同步。
- adapter 可以独立修复，但必须声明可接受的 core protocol 范围。
- schema migration 必须向前检查；不理解的新 schema 停止写入，不猜测兼容。

## Trust, upgrade, and rollback

### Trust

- Release 制品不可变，至少发布 SHA-256；成熟阶段增加签名和构建 provenance。
- manifest 后续记录 `source_type`、`source_ref`、`artifact_digest` 和 `installed_at`。
- 执行前先校验制品；默认文档不推荐未固定版本的 `curl | sh`。
- Plugin 目录审核是渠道信号，不替代项目内 hash 和版本检查。

### Upgrade

- resolver 只负责选择和下载；installer 只接收本地可信 payload。
- 默认先展示 plan：当前版本、目标版本、managed changes、local conflicts 和 schema migration。
- 保持现有三方 hash 冲突判断；冲突时不改变 managed files。
- 升级完成后必须运行新版本项目内 CLI 的 `doctor`，再运行项目配置的 `verify`。

### Rollback

- 最可靠的项目回滚是 Git revert，因此 managed files 和安装状态必须提交到版本控制。
- installer 在未来涉及 schema migration 时，写入 `.vibe/backups/<operation-id>/` 的安装状态快照；只备份 Vibe Kit 管理或维护的状态，不复制整个业务仓库。
- 回滚使用明确的旧 release payload 再执行受控 upgrade/downgrade；不通过直接编辑版本文件伪造状态。

## Release pipeline and gates

发布流水线应从一个 tag 生成所有制品：

1. 校验 managed source、Skill metadata、adapter 清单和版本一致性。
2. 构建 core bundle、Codex project adapter、Codex Plugin 和离线包。
3. 在干净临时目录运行 new project、adopt、upgrade、conflict、doctor、verify 场景。
4. 解包每个渠道制品，验证生成内容 hash 与 canonical source 一致。
5. 在支持的 OS/Python/宿主版本上运行兼容矩阵。
6. 生成 checksum、provenance 和 release notes；先发布候选版，验证后再提升 stable 指针。

任何渠道构建失败都不能单独发布同一版本，避免“GitHub 是 0.4，Plugin 实际还是 0.3”的漂移。

## Rollout roadmap

### v0.2 — installation trust

只完成三方版本完整性、adopt 保留证据和 0.1→0.2 升级验证。分发架构在此版本只形成设计，不实现联网行为。

### v0.3 — reproducible release bundle

- 由 canonical source 生成离线 bundle 与 SHA-256；
- release manifest、`vibe package`、`validate-release` 与 read-only plan；
- bootstrap-only Codex Plugin 与同版本 bundled payload；
- 本地 marketplace、artifact-based init/adopt/upgrade/conflict/tamper 验证；
- macOS 本地证据与 Linux/Python 3.9+ 的发布矩阵声明。

本地 release candidate 已实现；在 GitHub 身份、许可证、tag 和 Linux CI 完成前仍是 unpublished，不称为公开稳定版。

### v0.4 — Codex install experience

- 选择正式 marketplace 名称、发布者身份、许可证、支持与隐私页面；
- 以固定 tag/ref 发布 GitHub Release 和 Plugin marketplace；
- 验证 ChatGPT desktop、Codex CLI、Linux CI 和 repo-scoped install 的一致性；
- 下载已发布制品重跑 checksum、Plugin install 和项目 smoke test。

### v0.5 — multi-agent adapters

- 发布 adapter contract 和 conformance suite；
- 选择一个非 Codex 宿主做完整 pilot；
- 加入 capability level 与降级行为；
- 根据 pilot 决定第二个 adapter，而不是一次支持所有平台。

### Later — public directory and package managers

- 完成发布者身份、许可证、隐私/支持页面和公开 Plugin 审核；
- 根据真实使用量决定 PyPI、Homebrew、npm 等便捷入口；
- 包管理器只做获取，不改变项目固定与可信 payload 的架构。

## Rejected alternatives

- **把脚手架仓库 merge 进业务仓库**：Git 历史和业务变更耦合，升级冲突难以解释，也无法清晰区分 ownership。
- **只安装全局 Plugin/Skill**：换主机或换协作者后行为漂移，项目无法证明当时使用的规范版本。
- **Plugin 与项目同时暴露同名运行时 Skills**：安装后形成重复入口和选择歧义；Plugin 应负责 bootstrap/maintain，项目负责日常 workflow。
- **每个平台维护一份完整规则**：短期简单，长期一定发生语义漂移；应生成薄 adapter。
- **默认追踪 `main` 或自动升级**：不可复现，且上游变化可在无审查时改变项目开发行为。
- **一个版本同时支持所有 Agent**：缺少能力模型和真实兼容证据，容易把“文件可读”误称为“流程等价”。

## Follow-up ADRs before implementation

本 ADR 只固定总架构。进入对应里程碑前，还应分别决策：release identity/provenance、adapter contract、升级事务与回滚边界、Codex Plugin capability policy、支持矩阵与 conformance evidence。
