<p align="center">
  <img src="docs/assets/vibe-kit-logo.png" width="136" alt="Vibe Kit 薄荷色模块化 M 标志，末端为已验证的勾选节点">
</p>

<h1 align="center">Vibe Kit</h1>

<p align="center">把可信的 Release 链接和开发目标交给 Codex，让项目自己携带工作范式。</p>

<p align="center"><a href="README.md">English</a> · <strong>简体中文</strong></p>

<p align="center">最新已发布 · <a href="https://github.com/mintgao/vibe-kit/releases/tag/v0.7.0"><code>v0.7.0 Pre-release</code></a></p>

## Vibe Kit 是做什么的

Vibe Kit 是一套随项目固定版本的 Agent 开发工作范式。你只需要描述项目和想要的结果。Codex 会负责可信接入、项目理解、工作流选择、技术决策就绪检查、实现和验证。

这套工作方式会跟随项目仓库。协作者换到另一台电脑后，仍能获得同一版本的指令和项目上下文。目前经过验证的 Agent 运行环境是 Codex。其他 coding Agent 需要单独的适配器和一致性证据，才能获得同样的兼容性声明。

## 主要能力

- **安全接入项目。** Codex 会选择可信的固定 Release，在写入前检查影响，保留项目自有文件。遇到路径冲突或不兼容状态时，它会停下来说明具体原因，并给出一个恢复动作。
- **基于证据理解项目。** 第一次开始实质工作时，Codex 会检查仓库，建立或刷新长期有效的产品与技术上下文，随后继续处理原始请求。
- **自动选择工作流。** 功能、设计、实现、排障和验证请求会进入对应流程。你不需要记住命令、Skill 名称或内部角色。
- **按风险调整严谨程度。** 局部且可逆的小改动保持轻量。会长期影响项目或风险较高的选择先通过技术决策就绪门，交付时再说明已经执行的证据、跳过的检查和已知限制。
- **升级后按证据接管。** 一次确认精确版本后可连续完成安全预检与写入；“已升级”“已激活”“已就绪”是三个独立事实，只有新规则、项目上下文和已配置检查都通过后才继续开发。

## 安装和使用

普通用户只会看到三个步骤。

1. 把准确的 Vibe Kit Release 链接和项目目标交给 Codex。
2. Codex 在内部校验来源、检查预期影响、接入 Kit、检查安装健康度，并建立项目上下文。
3. 接下来继续用日常语言描述开发目标。

### 接入已有项目

用 Codex 打开项目，然后发送下面这段请求。

> 请把 https://github.com/mintgao/vibe-kit/releases/tag/v0.7.0 安全接入当前项目。使用这个可信的固定版本，保留现有业务文件和项目文档，完成健康检查和基于仓库证据的项目理解，然后继续处理下面这个目标。[我的开发目标]

### 基于 Vibe Kit 创建新项目

在同一条请求里写清应用、目标目录和期望技术栈。

> 请使用官方框架生成器，在 `./my-app` 创建一个 Next.js 记账应用。随后把 https://github.com/mintgao/vibe-kit/releases/tag/v0.7.0 接入生成的项目，检查安装结果，建立项目上下文，并继续实现第一个可用版本。

这里使用准确的 Release URL，它已经明确选择当前 Pre-release。如果只提供仓库主页链接，而仓库还没有 stable Release，Codex 应当在选择 Pre-release 前询问一次。

接入完成后，开发请求和平常一样。

> 增加邮箱登录，并记录会影响后续实现的重要产品决定。

> 排查首页第一次加载缓慢的原因，确认根因后完成修复。

> 验证当前版本是否适合发布，并列出每条标准对应的证据。

Codex 最终应当说明版本与来源、安装健康度、新规则激活、项目上下文、已配置检查和下一步。0.7.0 契约定义了同任务重载和自动后继任务回执，但当前 Codex/Plugin 没有正向宿主证据，因此仅保证一个兜底动作：在同一项目中新建 Codex 任务。源任务应预填或提供一句可复制的原目标；新任务不需要再确认升级或执行内部命令。

## 专业开发者与维护者附录

普通使用到上一节就可以结束。下面补充实现、信任和维护边界。

### 架构与文件归属

Vibe Kit 由一个无第三方依赖的 Python CLI、项目级指令、专门角色、工作流 Skill 和项目自有的 Markdown 上下文组成。Release 压缩包和引导 Plugin 负责获取与接入。真正影响开发行为的内容仍以已经安装的项目仓库为准。

- **框架管理。** `AGENT_INSTALL.md`、`agent-install.json`、`AGENTS.md` 中带标记的 Vibe 区块、`bin/vibe`、`.vibe/core/`、`.codex/agents/vibe-*` 和 `.agents/skills/vibe-*`。
- **工具维护。** `.vibe/manifest.json`、`.vibe/version` 和自动生成的 `.vibe/conflicts/` 候选文件。
- **项目自有。** `.vibe/project.yaml`、`.vibe/project-rules.md`、`.vibe/onboarding.json` 与 `docs/`。升级不会覆盖这些文件。

完整的组件与归属模型见[架构上下文](docs/context/architecture.md)。

### CLI 与健康检查

这些命令供 Agent、维护者和故障排查使用。普通用户的日常流程不依赖它们。

```bash
./bin/vibe doctor .
./bin/vibe verify .
./bin/vibe work-item settings-page --size M --title "Settings Page"
```

`doctor --format json` 会分别报告安装健康度和项目理解是否就绪，并为每条警告/错误给出固定的 readiness 影响。`verify --format json` 会输出 lint、typecheck、test、build 的完整矩阵，区分通过、失败、未配置和跳过。`verify` 只执行 `.vibe/project.yaml` 中明确配置的项目命令。

### 信任、发布与兼容性

默认信任契约只承认 `https://github.com/mintgao/vibe-kit`。准确的 tag 和 Release URL 会选择一个明确的已发布版本，安装前还会校验 Release 元数据和 SHA-256。移动引用 `main`、未经验证的压缩包、静默切换仓库和 `curl | sh` 都会被拒绝。

面向人和机器的规范契约分别是 [AGENT_INSTALL.md](AGENT_INSTALL.md) 与 [agent-install.json](agent-install.json)。0.7.0 Pre-release 使用 core/Codex protocol 5、Agent-install schema/protocol 3、takeover schema 2、maintenance bridge schema 2、CLI result schema 2、release-manifest schema 2、transaction/commit schema 1 和 feedback protocol 2；历史发布保持不变。

0.7.0 会把这两份 Agent-install 契约作为 framework-managed 文件安装到项目中，并纳入 manifest 与激活身份。`bin/vibe validate-takeover --format json` 会先验证已安装契约与编译后 registry，再对 stdin 中的完整封闭 takeover 结构做校验，不持久化或回显输入。`valid` 只代表结构自洽，不代表宿主回执已被认证，也不代表已就绪。

### 升级与冲突

更新已经接入的项目时，需要使用更高版本的可信 checkout、经过验证的 Release payload，或者 Plugin 内置 payload。项目里的旧 CLI 不会联网获取新版本。

```bash
/path/to/newer-vibe-kit/bin/vibe plan upgrade /path/to/my-app
/path/to/newer-vibe-kit/bin/vibe upgrade /path/to/my-app
```

升级会在替换托管文件前比较安装记录、本地内容和新版本内容。如果项目与新版本同时修改了同一个托管文件，Vibe Kit 会在改动托管文件前停止，并把待审核的新版本候选写入 `.vibe/conflicts/<timestamp>/`。

0.7.0 Pre-release 只提供一个精确的兼容例外：对官方、健康的 v0.5.0 source checkout，将原本未记入 manifest 的两份 Agent-install 契约作为一个完整集认证，然后替换并纳入托管。缺失、修改、混合、符号链接、竞态或其他不健康状态仍会冲突；其他未跟踪文件不会因此获得自动接管。

v0.7 只允许经过审计的 v0.2 fixture 与官方 v0.3/v0.4 身份创建 `pending` onboarding；已有合法状态保持字节不变，v0.5/v0.6 缺失状态会在写入前阻断。升级现在是范围明确、可恢复的事务：失败只会报告已回滚、需要执行 `recover-upgrade`，或无法分类且禁止自动覆盖。

最终安装条目只使用经过能力探测的 fd-relative 无损发布协议：缺失叶使用硬链接 no-clobber，既有叶使用原子 exchange，首次缺失的托管父目录则作为相邻预备目录单元以 no-replace 发布。所需原语不受支持时会阻断；普通 rename/replace 不会作为最终安装条目的兜底。

写入成功后，CLI 仍然不会声称当前 Agent 已加载新规则。宿主若提供符合契约的重载/后继回执可自动继续；否则当前仓库和 Plugin 如实停在“手动新建任务”兜底。只有已激活任务可刷新 onboarding、执行最终默认验证、按新规则重新评估原目标、恢复共享代码编辑或宣告可以继续开发。

### 验证与发布工程

项目验证不依赖第三方包，并以场景测试为主。

```bash
python3 -m unittest discover -s tests -v
./bin/vibe package --status prerelease
./bin/vibe validate-release dist/vibe-kit-0.7.0
```

维护者通过仓库内 `vibe-release` Skill 和离线的 `publication-plan`、`validate-publication` 管理精确五资产 Pre-release。GitHub 凭据与远端写入仍归 Agent/宿主所有；精确选择和 SHA-256 校验不等于平台强制不可变。

发布校验会检查压缩包路径安全、摘要、版本、Agent 契约与编译后 registry 一致性、激活 v2 独立重算、有界生产 validator 用例，以及直接 Release、Plugin payload 和展开后的 marketplace 之间是否漂移。详细信息见 [0.7.0 发布说明](docs/releases/0.7.0.md)、[升级后接管决策](docs/decisions/0009-post-upgrade-takeover.md)与[可复现发布决策](docs/decisions/0004-reproducible-release-contract.md)。

静态契约测试能够确认分发指令包含必要边界。真实 Agent 是否正确执行这套流程，仍需受控场景和独立 QA。文档字符串测试不能替代这类行为证据。

### 反馈与隐私

Vibe Kit 不采集遥测，也不会静默提交反馈。可复现的 Kit 缺口可以保存在本地并自动去重。`ask` 模式会展示一次经过清理的 GitHub Issue 完整内容，提交仍然需要紧邻这份内容的明确授权，并与当次报告、目标仓库和当前 review hash 绑定。`local` 会把候选留在本地且不询问，`off` 会关闭主动判断。

```bash
./bin/vibe feedback mode
./bin/vibe feedback list
./bin/vibe feedback review <report-id>
```

涉及安全敏感信息的候选可以留在本地，但不能生成公开 review hash，也不能进入远端提交。完整边界见[反馈流程设计](docs/work-items/20260827-proactive-feedback-loop/design.md)。

### 当前限制

- `v0.7.0` 是最新 GitHub Pre-release。目前没有 stable Release、公共 Plugin Directory 条目、自动联网更新器，也没有发布者签名和外部 provenance 证明。
- SHA-256 元数据能验证附件和 manifest 是否一致。发布者身份仍然依赖 GitHub 账号、commit 和 tag。
- Codex 是目前唯一经过验证的 Agent 适配。当前仓库与 Plugin 对升级激活仅声称手动兜底；同任务重载、自动后继任务、真实 Linux 和真实 Plugin host 仍缺少正向证据。
- 安装不是整个目录级事务。升级只对托管/工具维护状态及狭窄的 onboarding 兼容桥提供可恢复事务，不覆盖业务文件或整个 Git 工作区。
- 技术决策就绪依靠 prompt、角色分离和 Markdown 证据组成一套遇到缺口就停止的仓库工作流契约。CLI 会分发并校验这些文件的摘要，当前不会解析 work-item 状态或机械阻止文件写入。
- 接入阶段只做浅层技术栈识别。安装后的项目理解流程会根据仓库证据建立更深入的上下文。

更多实现细节见 [Agent-first 接入决策](docs/decisions/0007-agent-first-adoption-contract.md)、[技术决策就绪契约](.vibe/core/technical-decision-readiness.md)和[分发设计](docs/work-items/20260827-distribution-architecture/design.md)。
