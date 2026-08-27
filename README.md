# Vibe Kit

Vibe Kit 是一套可以随项目版本化的 Codex 研发工作流脚手架。它把长期开发约定、PM/UX/RD/QA/Investigator 角色、需求与排查流程、项目上下文和质量检查放进同一个仓库。

当前版本：`0.3.0`。它以 [GitHub Pre-release](https://github.com/mintgao/vibe-kit/releases/tag/v0.3.0) 分发；尚未提升为 stable，也未发布到 Codex Plugin Directory、npm、PyPI 或 Homebrew。

## 它安装什么

```text
AGENTS.md                         Codex 工作入口和任务路由
.codex/agents/vibe-*.toml        PM、UX、RD、QA、Investigator
.agents/skills/vibe-*/SKILL.md   onboarding、feature、design、implementation、verification、debug、feedback
.vibe/core/                      分级、质量门禁和工作项模板
.vibe/project.yaml               当前项目技术栈和可执行命令
.vibe/project-rules.md           当前项目自己的规则
docs/context/                    产品、架构和设计上下文
docs/work-items/                 需求与验证证据
docs/decisions/                  长期架构决策
bin/vibe                         项目内 CLI
```

安装完成后请开启一个新的 Codex 任务，使项目根目录的 `AGENTS.md` 和 repo Skills 从任务开始时加载。

## 场景一：新项目

先用技术栈自己的生成器创建应用，再引入工作流。例如：

```bash
npx create-next-app@latest /path/to/my-app
/path/to/vibe-kit/bin/vibe plan init /path/to/my-app
/path/to/vibe-kit/bin/vibe init /path/to/my-app --name "My App"
```

如果目标目录还不存在，`init` 也会创建目录。它会识别常见的 Node.js、Python、Rust、Go 和 Swift 项目，并将已存在的 lint、typecheck、test、build 命令写入 `.vibe/project.yaml`。

## 场景二：开发到一半的项目

```bash
/path/to/vibe-kit/bin/vibe plan adopt /path/to/existing-app
/path/to/vibe-kit/bin/vibe adopt /path/to/existing-app
```

`adopt` 会：

- 保留业务代码和已有项目文档；
- 如果已有 `AGENTS.md`，只在其中加入带边界标记的 Vibe Kit 区块；
- 识别现有技术栈和项目命令；
- 只创建尚不存在的项目上下文文件；
- 遇到已有的同名托管文件时，在写入前停止。

接入后，在新的 Codex 任务中说“使用 `$vibe-project-onboarding` 梳理这个项目”，让 Agent 根据真实代码补全 `docs/context/`。它不会为了接入工作流而重构已有应用，也不会要求补录全部历史需求。

## 日常命令

以下命令使用已经复制到业务项目里的 CLI：

```bash
./bin/vibe doctor
./bin/vibe work-item settings-page --size M --title "Settings Page"
./bin/vibe verify
./bin/vibe verify --only test
```

- `doctor` 检查 `.vibe/version`、manifest 与 core 的三方版本完整性，以及托管文件哈希、Skill frontmatter 和 Agent 必填字段。版本缺失或不一致时只做诊断，不修改文件，并提示从目标版本的可信 checkout 重新执行 `upgrade`。
- `work-item` 创建需求 brief 和验收证据模板。
- `verify` 按 `.vibe/project.yaml` 依次执行 lint、typecheck、test 和 build；空命令会跳过。

你仍然可以直接用自然语言工作。`AGENTS.md` 会根据任务把新功能、纯设计、已有方案开发、测试或排查路由到相应 Skill。S 级小改动保持轻量；M/L 级任务才会引入工作项和独立角色审查。

## 持续改进 Vibe Kit

M/L 工作结束或 Vibe CLI/流程本身暴露出高置信、可复现的系统性缺口时，Agent 会使用 `vibe-feedback-flow` 做一次轻量判断。没有有效信号时保持安静；有信号时只生成本地去敏候选，不影响主任务结果，也不会自动联网。

```bash
./bin/vibe feedback list
./bin/vibe feedback review <report-id>
./bin/vibe feedback submit <report-id> --confirm <review-hash>
./bin/vibe feedback dismiss <report-id> --reason "not actionable"
```

候选存放在 `.vibe/local/feedback/`，目录自带忽略规则，默认不进入 Git。提交前 `review` 会展示目标仓库和实际发送的完整 title/body，并为它计算 review hash；repo、正文、标题或 labels 改变后旧 hash 立即失效。`submit` 在创建 Issue 前再次按 fingerprint 查重。

Vibe Kit 不采集遥测，不保存原始代码、日志、Prompt、对话或环境变量，也不会自动创建 GitHub Issue。普通 public feedback 检出明显 secret 或安全内容时会被阻止。发行版默认把审核通过的反馈提交到 `mintgao/vibe-kit`；你仍需先完成 `gh` 登录，并对每一条 payload 执行 `review` 后携带当次 hash 明确确认 `submit`。如需提交到自己的 fork 或内部仓库，可在 `review` 和 `submit` 时用 `--repo owner/repository` 覆盖默认值。

## 升级

先获得一个较新的 Vibe Kit checkout，再用新版本的 CLI 更新目标项目：

```bash
/path/to/newer-vibe-kit/bin/vibe plan upgrade /path/to/my-app
/path/to/newer-vibe-kit/bin/vibe upgrade /path/to/my-app
```

不要用业务项目中旧的 `./bin/vibe upgrade` 期待它自动联网获取新版；v0.3 不包含网络更新器。

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

## 分发与跨主机使用

Vibe Kit 采用“渠道获取、项目固定”：离线包/GitHub Release 是跨主机 payload；Codex Plugin 只提供安装与维护入口；真正影响开发行为的 core、运行时 Skills、Agent 适配器和版本状态仍写入业务仓库。

维护者从 canonical working tree 构建本地 release candidate：

```bash
./bin/vibe package
./bin/vibe validate-release dist/vibe-kit-0.3.0
```

维护者从 clean commit 构建 GitHub Pre-release 时使用：

```bash
./bin/vibe package --status prerelease
```

默认生成：

```text
dist/vibe-kit-0.3.0/
  vibe-kit-0.3.0.zip             完整离线安装 payload
  vibe-kit-plugin-0.3.0.zip      bootstrap-only Codex Plugin + 同版本 payload
  vibe-kit-distribution-0.3.0.zip GitHub/跨主机完整传输包
  release-manifest.json          版本、协议、支持矩阵、来源与逐文件摘要
  SHA256SUMS                     传输完整性校验
  marketplace/                   可加入 Codex 的本地 marketplace
```

从 GitHub 下载 `vibe-kit-distribution-0.3.0.zip` 后，先解压完整目录，再用已有可信 Vibe Kit checkout/Plugin 的 CLI 校验，然后解压安装 payload：

```bash
unzip vibe-kit-distribution-0.3.0.zip
/path/to/trusted-vibe-kit/bin/vibe validate-release vibe-kit-0.3.0
unzip vibe-kit-0.3.0/vibe-kit-0.3.0.zip -d /path/to/vibe-kit-payload
python3 /path/to/vibe-kit-payload/vibe-kit-0.3.0/bin/vibe plan adopt /path/to/existing-app
python3 /path/to/vibe-kit-payload/vibe-kit-0.3.0/bin/vibe adopt /path/to/existing-app
```

新项目把 `adopt` 换成 `init`。Plugin 的本地灰度入口为：

```bash
codex plugin marketplace add /absolute/path/to/release-directory/marketplace
codex plugin add vibe-kit@personal
```

安装或升级项目后都运行项目内 `./bin/vibe doctor`，并开启新的 Codex 任务。Plugin 被卸载或换主机不会影响已经提交到项目仓库的 Vibe Kit。

0.3.0 manifest 状态是 `prerelease`，绑定发布 commit 且要求 clean tree。完整发布说明见 [0.3.0 prerelease](docs/releases/0.3.0.md)、[distribution design](docs/work-items/20260827-distribution-architecture/design.md)、[ADR 0004](docs/decisions/0004-reproducible-release-contract.md) 与 [ADR 0005](docs/decisions/0005-bootstrap-plugin-capabilities.md)。

## 当前限制

- GitHub 只发布 Pre-release；没有自动下载更新、签名或独立 provenance 服务。SHA-256 只证明内容与 manifest 一致，发布者身份仍依赖 GitHub 账号、commit 与 tag。
- Codex Plugin 已作为本地 release artifact 构建并验证，但尚未在本机全局安装或提交公共目录；首版 marketplace 名为 `personal`，如目标主机已有同名 marketplace，需要在正式发布身份确定后解决 catalog 命名。
- `adopt` 只做确定性的浅层技术栈识别；深入项目理解由 onboarding Skill 完成。
- `verify` 执行项目在 `.vibe/project.yaml` 中明确配置的 shell 命令，运行前应像审查其他项目脚本一样审查这些命令。
- 当前适配层只验证了 Codex；其他 coding agent 必须通过单独适配器与 conformance evidence 接入，不能只改文件名就宣称兼容。
