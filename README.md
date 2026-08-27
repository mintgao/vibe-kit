# Vibe Kit

Vibe Kit 是一套随项目版本化的 Codex 工作范式。人负责表达项目意图和开发目标；Codex 负责可信版本选择、安全接入、项目理解、工作流路由和验证。

当前公开版本：[`0.5.0` GitHub Pre-release](https://github.com/mintgao/vibe-kit/releases/tag/v0.5.0)。不要让 Agent 跟随 `main`。

## 把它接入已有项目

把下面这句话交给当前项目里的 Codex：

> 请把 https://github.com/mintgao/vibe-kit 安全接入当前项目。选择可信的固定版本，保留现有业务文件和项目文档，完成检查后告诉我是否可以继续开发。

## 用它创建新项目

直接描述应用、目标目录和期望技术栈，例如：

> 请基于 https://github.com/mintgao/vibe-kit，在 `./my-app` 创建一个 Next.js 记账应用。先用框架生成器创建项目，再接入 Kit 并完成检查。

接入后，继续像平常一样描述开发目标即可：

> 增加用户登录功能。

> 排查首页首次加载慢的问题。

> 验证当前版本是否适合发布。

用户不需要选择 `init`/`adopt`、执行安装命令或点名内部 Skill。Codex 从根目录的 [Agent installation contract](AGENT_INSTALL.md) 发现版本化协议，在内部完成来源校验、只读 plan、安装、doctor、新任务交接和首次 onboarding；之后由项目 `AGENTS.md` 自动路由普通开发语言。

只有来源不是 canonical 仓库、裸仓库没有 stable Release、已有安装版本不同、托管文件冲突或需要扩大权限时，Agent 才应请求一次会改变结果的决定。

## Agent 与维护者参考

下面的命令是 Agent、维护者和故障排查接口，不是日常用户流程。默认文本输出保持向后兼容；安装关键命令也支持 `--format json` 的版本化机器结果。

Vibe Kit 会把 managed core、Codex agents、workflow Skills 和 `bin/vibe` 固定进项目；`.vibe/project.yaml`、`.vibe/project-rules.md`、`.vibe/onboarding.json` 与 `docs/` 保持项目自有。新接入的 readiness 是 `pending`，Codex 首次实质工作时自动基于仓库证据完成 onboarding，然后继续原始请求。

进入实现前，Agent 还会自动应用技术决策就绪门禁。普通、局部且可逆的 S 工作保持轻量；M 工作扫描 durable/high-risk trigger；每个 L 工作留下明确 readiness outcome。涉及共享契约、迁移、权限/安全、rollback/recovery、crash consistency、兼容性或不可逆状态时，Agent 会先交给只读 Tech Lead 形成或评审决策证据，等 workflow orchestrator 确认 `implementation-ready` 后再交给一个 RD writer。用户不需要主动说“先做 ADR”，也只会在技术选择改变产品 scope、可观察行为、风险/成本、不可逆状态或外部兼容性时被询问。

常用维护检查：

```bash
./bin/vibe doctor
./bin/vibe verify
./bin/vibe work-item settings-page --size M --title "Settings Page"
```

`doctor` 将安装健康度与 onboarding readiness 分开报告。`verify` 运行 `.vibe/project.yaml` 中明确配置的项目命令。

## 持续改进 Vibe Kit

M/L 工作结束或 Vibe CLI/流程本身暴露出高置信、可复现的系统性缺口时，Agent 会使用 `vibe-feedback-flow` 做一次轻量判断。没有有效信号时保持安静；有信号时按项目的 `feedback.mode` 收口，并且始终先完成主任务。

- `ask`（新项目和缺失配置的默认值）：新建或有实质变化的候选会主动展示一次完整 Issue payload，用户回复“提交这条反馈”即可授权当次 payload。
- `local`：生成本地候选，不询问提交。
- `off`：关闭主动判断和生成；手工反馈命令仍可使用。

任何模式都不会静默联网或自动提交。普通“好”“确认”“继续”、无响应、历史授权、已配置仓库或 `gh` 登录都不构成本条 Issue 的授权。

```bash
./bin/vibe feedback mode
./bin/vibe feedback list
./bin/vibe feedback review <report-id>
./bin/vibe feedback revise <report-id> --input revision.json
./bin/vibe feedback submit <report-id> --confirm <review-hash>
./bin/vibe feedback dismiss <report-id> --reason "not actionable"
```

候选存放在 `.vibe/local/feedback/`，目录自带忽略规则，默认不进入 Git。Agent 的主动入口是 `feedback close`；它会根据 mode、fingerprint 和 attention revision 决定是否展示，unchanged duplicate、dismissed candidate 和升级前的 legacy backlog 都不会重复打扰。`review`/`revise` 支持手工恢复。repo、正文、标题或 labels 改变后旧 hash 立即失效；`submit` 在创建 Issue 前再次按 fingerprint 查重。

Vibe Kit 不采集遥测，不保存原始代码、日志、Prompt、对话或环境变量。检出明显 secret 会在落盘前阻止；标记为 security-sensitive 的候选可以本地保留，但不会生成公开 review hash，也不能执行远端 check/submit。发行版默认把审核通过的普通反馈提交到 `mintgao/vibe-kit`；每一条仍需绑定当次 report、repo 和 hash 的明确授权。如需提交到自己的 fork 或内部仓库，可在 `review`、`revise` 和 `submit` 时用 `--repo owner/repository` 覆盖默认值。

## 升级

先获得一个较新的 Vibe Kit checkout，再用新版本的 CLI 更新目标项目：

```bash
/path/to/newer-vibe-kit/bin/vibe plan upgrade /path/to/my-app
/path/to/newer-vibe-kit/bin/vibe upgrade /path/to/my-app
```

不要用业务项目中旧的 `./bin/vibe upgrade` 期待它自动联网获取新版；Vibe Kit 不包含网络更新器。

升级只管理：

- `AGENTS.md` 中两个 Vibe Kit 标记之间的区块；
- `bin/vibe`；
- `.vibe/core/`；
- `.codex/agents/vibe-*`；
- `.agents/skills/vibe-*`。

升级不会覆盖 `.vibe/project.yaml`、`.vibe/project-rules.md` 或 `docs/`。安装时的托管文件哈希记录在 `.vibe/manifest.json`，版本记录在 `.vibe/version`。

如果某个托管文件在项目本地和新版本中都发生了变化，升级会在修改任何托管文件前终止，并把新版本候选文件写到 `.vibe/conflicts/<timestamp>/`，供人工比较。

## 开发与验证 Vibe Kit

Vibe Kit CLI 只依赖 Python 标准库，支持 Python 3.9 及以上版本。

```bash
python3 bin/vibe doctor .
python3 -m unittest discover -s tests -v
```

自动化测试覆盖：新项目初始化、已有项目接入及项目自有文件逐字节保留、init/adopt/upgrade plan 只读性、托管路径冲突、历史 fixture 升级、冲突升级原子性、三方版本诊断、反馈隐私与 GitHub 幂等、制品可复现性、离线/Plugin 安装、危险 ZIP、渠道漂移和篡改拒绝。

技术决策就绪的自动化覆盖验证 managed core、Tech Lead role、work-item readiness block 和三条 workflow 入口的静态/分发契约。真实 Agent 是否识别 trigger、停止写入并正确 handoff，必须由独立 QA 运行受控 Agent 场景；文档字符串测试不能替代这类行为证据。

## 分发与跨主机使用

Vibe Kit 采用“渠道获取、项目固定”：离线包/GitHub Release 是跨主机 payload；Codex Plugin 只提供安装与维护入口；真正影响开发行为的 core、运行时 Skills、Agent 适配器和版本状态仍写入业务仓库。

维护者从 canonical working tree 构建本地 release candidate：

```bash
./bin/vibe package
./bin/vibe validate-release dist/vibe-kit-0.5.0
```

维护者从 clean commit 构建 GitHub Pre-release 时使用：

```bash
./bin/vibe package --status prerelease
```

默认生成：

```text
dist/vibe-kit-0.5.0/
  vibe-kit-0.5.0.zip             完整离线安装 payload
  vibe-kit-plugin-0.5.0.zip      bootstrap-only Codex Plugin + 同版本 payload
  vibe-kit-distribution-0.5.0.zip GitHub/跨主机完整传输包
  release-manifest.json          版本、协议、支持矩阵、来源与逐文件摘要
  SHA256SUMS                     传输完整性校验
  marketplace/                   可加入 Codex 的本地 marketplace
```

排查或离线验证 `vibe-kit-distribution-0.5.0.zip` 时，先解压完整目录，再用已有可信 Vibe Kit checkout/Plugin 的 CLI 校验，然后解压安装 payload：

```bash
unzip vibe-kit-distribution-0.5.0.zip
/path/to/trusted-vibe-kit/bin/vibe validate-release vibe-kit-0.5.0
unzip vibe-kit-0.5.0/vibe-kit-0.5.0.zip -d /path/to/vibe-kit-payload
python3 /path/to/vibe-kit-payload/vibe-kit-0.5.0/bin/vibe plan adopt /path/to/existing-app
python3 /path/to/vibe-kit-payload/vibe-kit-0.5.0/bin/vibe adopt /path/to/existing-app
```

新项目把 `adopt` 换成 `init`。Plugin 的本地灰度入口为：

```bash
codex plugin marketplace add /absolute/path/to/release-directory/marketplace
codex plugin add vibe-kit@personal
```

安装或升级项目后都运行项目内 `./bin/vibe doctor`，并开启新的 Codex 任务。Plugin 被卸载或换主机不会影响已经提交到项目仓库的 Vibe Kit。

0.5.0 已作为 GitHub Pre-release 发布。完整说明见 [0.5.0 release](docs/releases/0.5.0.md)、[Agent contract](AGENT_INSTALL.md)、[distribution design](docs/work-items/20260827-distribution-architecture/design.md) 与 [ADR 0007](docs/decisions/0007-agent-first-adoption-contract.md)。

## 当前限制

- GitHub 只发布 Pre-release；没有自动下载更新、签名或独立 provenance 服务。SHA-256 只证明内容与 manifest 一致，发布者身份仍依赖 GitHub 账号、commit 与 tag。
- Codex Plugin 已作为本地 release artifact 构建并验证，但尚未在本机全局安装或提交公共目录；首版 marketplace 名为 `personal`，如目标主机已有同名 marketplace，需要在正式发布身份确定后解决 catalog 命名。
- `adopt` 只做确定性的浅层技术栈识别；深入项目理解由 onboarding Skill 完成。
- `verify` 执行项目在 `.vibe/project.yaml` 中明确配置的 shell 命令，运行前应像审查其他项目脚本一样审查这些命令。
- 当前适配层只验证了 Codex；其他 coding agent 必须通过单独适配器与 conformance evidence 接入，不能只改文件名就宣称兼容。
- 技术决策就绪是 prompt、角色分离和项目自有 Markdown evidence 共同执行的 fail-closed workflow contract；CLI 会分发这些文件，但当前不会解析 work-item 状态或机械阻止文件写入。
