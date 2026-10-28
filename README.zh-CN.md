<p align="center">
  <img src="docs/assets/vibe-kit-logo.png" width="136" alt="Vibe Kit 薄荷色模块化 M 标志，末端为已验证的勾选节点">
</p>

<h1 align="center">Vibe Kit</h1>

<p align="center">让 AI 编程有一套随项目保存的工作方式。</p>

<p align="center"><a href="README.md">English</a> · <strong>简体中文</strong></p>

<p align="center">最新已发布 · <a href="https://github.com/mintgao/vibe-kit/releases/tag/v0.11.0"><code>v0.11.0 Pre-release</code></a></p>

本 checkout 另含 **未发布的 0.12.0 源码候选**，增加精确的 onboarding 版本校验、有界只读 `inspect-run` 与真实入口聚焦证据指引。见[本地候选说明](docs/releases/0.12.0.md)；下方公开安装链接仍指向 v0.11.0。

## 把开发目标变成有依据、可跟进的工作

告诉 Agent 你想做什么、哪里出了问题。Vibe Kit 提供项目指令、可复用的工作流和本地验证工具，让工作有起点、检查有依据、没完成的步骤有记录。

规范和项目上下文保存在仓库里。换一个任务或协作者，也能读取同一固定版本，不必只依赖上一段对话。

## 你可以用它做什么？

下面是使用示例，以及 Kit 为这些任务提供的流程或工具支持。

| 你想做什么 | 可以这样提需求 | Kit 提供什么 |
|---|---|---|
| 接手已有项目 | “先了解这个项目，再增加邮箱登录。” | 基于仓库证据建立上下文，明确改动范围，重要技术选择先评审。 |
| 修复问题 | “排查首页首次加载慢的原因，确认后修复。” | 把排查、修复依据和验证连起来的工作流。 |
| 看懂长时间检查 | “现在跑到哪一项了，什么时候开始的？” | 可用的本地进度元数据，也覆盖静默检查；需要时可保留完整日志供事后查看。 |
| 更新开发规范 | “升级这个项目的 Vibe Kit，保留我的项目文件。” | 写入前先看计划，保留冲突保护与恢复路径，单独核实安装健康度。 |

交付指引要求 Agent 说明做完了什么、检查过什么、还缺什么动作或权限。未完成的步骤应继续保留，不能算成整个目标已完成。

## 快速开始

当前版本为 **[v0.11.0 Pre-release](https://github.com/mintgao/vibe-kit/releases/tag/v0.11.0)**。用 Codex 打开项目，发送下面这段话，替换最后的目标：

> 请把 https://github.com/mintgao/vibe-kit/releases/tag/v0.11.0 接入当前项目。保留已有文件和项目文档，验证安装并建立项目上下文，然后继续处理这个目标：[我想做的功能或要修复的问题]。

**从零新建应用**时，把应用想法、技术栈偏好和目标目录一起写进去。例如：“在 `./my-app` 新建一个记账应用，然后接入上面这个固定版本的 Vibe Kit。”

**已经接入的项目**可以这样说：“请升级到上面的准确 Release，先说明计划，保留项目自有文件，并检查升级结果。”升级使用目标版本的可信 payload，旧 CLI 不会自行联网获取新版本。

激活流程提示时，**在同一项目新建一个任务**。安装健康和新规则已生效是两个事实；自动重载或接续仍须有宿主证据。

如需手动获取：[直接 Kit ZIP](https://github.com/mintgao/vibe-kit/releases/download/v0.11.0/vibe-kit-0.11.0.zip) · [Codex 引导 Plugin ZIP](https://github.com/mintgao/vibe-kit/releases/download/v0.11.0/vibe-kit-plugin-0.11.0.zip)。Agent 使用下载内容前会核对发布摘要。所有资产与技术步骤见[安装和维护指南](docs/maintainers-guide.zh-CN.md)。

## 0.11.0 最近更新

- **检查过程更容易查阅。** 可按需开启完整脱敏成功日志（`all-configured`）；可用的持久进度能定位当前检查，即使它长时间没有输出。
- **可以再次执行同版本升级。** 再次运行升级时，继续保留原有的冲突保护与恢复路径。
- **多阶段任务保留未完成项。** 适用的工作指引可记录阶段覆盖、下一步、负责人和等待条件；标为未验证（Unverified）的阶段仍未完成。

进度属于诊断信息，可能过期或不可用。完整成功日志需主动开启，并须保持私有。多阶段结果指引的证据限于静态契约和场景检查，不代表已测得实际模型遵循或效率提升。

[完整更新说明](docs/releases/0.11.0.md) · [实际发布验收记录](docs/work-items/20261010-feedback-closure/postpublication.md)

## 适合哪些项目？

- **以仓库为中心的开发。** 可接入已有项目，也可在生成新应用后接入。CLI 需要 Python 3.9+，仅使用标准库；本地写入和维护可离线完成。
- **有支持的 Agent 宿主。** Codex 和 Hermes 都有已验证的适配器一致性记录。工具、权限和激活仍取决于宿主；其他宿主需要自己的适配器与证据。
- **愿意配置项目检查。** Kit 报告观察到的结果，以及缺失或阻塞的步骤；它不会替每个项目提供测试，也不能保证 Agent 每次都严格遵循指令。
- **希望明确控制分享。** 不采集遥测，也不会静默公开提交反馈。日志须保持私有；按已知模式脱敏不能识别所有秘密。

当前是 Pre-release，没有 stable Release 或发布者签名。进一步了解[能力与限制](docs/maintainers-guide.zh-CN.md)、[验证和日志设置](docs/verification-observability.md)、[Agent 安装契约](AGENT_INSTALL.md)。历史版本：[v0.10.1](https://github.com/mintgao/vibe-kit/releases/tag/v0.10.1)。

## 维护检查

CLI `validate-readiness` 只读验证有限格式的 work-item 就绪证据。`inspect-managed-agents` 可使用 `unicode-whitespace-v1` 计数策略；2858 词的文件不能通过 2800 词上限，检查不会降低项目标准。文档字符串测试不能替代这类行为证据，真实 Agent 场景仍需单独验证。命令与先前 v0.10.1 契约历史见[维护指南](https://github.com/mintgao/vibe-kit/blob/v0.12.0/docs/maintainers-guide.md)。
