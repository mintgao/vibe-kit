# Proactive Vibe Kit feedback loop

- ID: `20260827-proactive-feedback-loop`
- Size: `L`
- Status: complete
- Created: 2026-08-27

## Goal

让高质量的 Vibe Kit 改进候选不再静默滞留在使用者本地：系统在主任务完成后主动展示已经去敏、去重、绑定目标仓库的 exact Issue payload，并把“提交”作为默认主路径，让用户只需一次明确回复即可完成授权和提交，同时保持零未授权外发。

## Problem statement

现有能力已经能生成本地 candidate、计算 fingerprint、阻止明显敏感内容、展示 exact payload、绑定 review hash，并在提交前查重。但默认体验仍然断裂：

- `feedback.mode: ask` 已写入项目配置，却没有形成“主动询问”的可观察行为；
- candidate 默认留在 `.vibe/local/feedback/`，普通使用者不知道也不会主动运行 `list/review/submit`；
- report ID、仓库和 hash 仍暴露为用户需要理解和复制的工程细节；
- 因此安全机制有效，但维护者收不到足够真实反馈，持续改进闭环无法规模化。

需要改变的是反馈的默认决策路径，不是放松外部写入边界。

## Users and jobs

- **Vibe Kit 使用者：** 主任务完成后，希望系统主动说明发现了什么、会向哪里发送、会发送哪些内容，并让我用一次选择提交、稍后或忽略。
- **Vibe Kit 维护者：** 希望收到结构化、去敏、去重、带环境和影响证据的真实 Issue，而不是依赖使用者记住额外命令。
- **隐私敏感或离线使用者：** 希望不授权、稍后处理、认证失败或离线时都保持本地，不影响主任务结果。

## Evidence

- Vibe Kit 首次公开发布产生了真实本地 candidate；只有 Agent 在 Close 中主动展示完整 review 并询问后，用户才批准并提交为 `mintgao/vibe-kit#1`。
- 用户明确指出：其他使用者不会特意执行 Issue 提交流程，因此提交必须成为默认被看见的主路径。
- 当前 `.vibe/project.yaml` 默认已有 `feedback.mode: ask`，但 CLI 和 managed workflow 尚未执行这一模式语义。

## Product decision

### MVP default: `ask`

`ask` 的正式含义是：

1. M/L Close 静默判断是否存在合格的 Vibe Kit 信号；无信号时完全安静。
2. 对新建或有实质变化的 candidate 自动完成本地 draft、去敏、去重和 review。
3. 先明确主任务已经完成，再展示 target、privacy、network state、dedupe state、完整 title/body/labels 和 review hash。
4. 主操作是“提交”；用户只需明确回复一次，不需要复制 report ID、repo、命令或 hash。
5. 只有这次回复明确指向刚展示的 report/repository/hash，才允许联网查重和最多一次 Issue create。

这使提交成为默认主路径，但不是静默自动外发。

### Supported modes in MVP

- `ask`：主动判断、生成、展示并询问一次；发行默认值。
- `local`：主动判断并保留本地 candidate，不主动询问提交。
- `off`：关闭 Close 阶段的主动判断和生成；显式 feedback 命令仍可使用。

`auto-submit` 不进入 MVP。它会改变逐 payload 授权这一信任边界，需要独立的 L 级授权设计和 ADR。

## Scope

### In

- 让 `feedback.mode` 成为真实、可验证的行为配置，缺失时安全默认 `ask`，保留项目显式选择。
- 更新 managed AGENTS/Skill，使合格 candidate 在主任务结果之后自动进入 mode-aware Close 体验。
- `ask` 自动展示 repo-bound exact review，并接受“提交 / 稍后 / 修改 / 忽略”四种自然语言结果。
- 用户授权绑定 report ID、repository 和当前 review hash；payload 或目标变化后旧授权失效。
- 保留本地/远端去重、dismiss suppression、material resurface、隐私阻断和不确定结果恢复。
- 每次 Close 最多展示一个反馈决策块；多个 candidate 聚合为一个主候选和待处理数量。
- 为纯终端和 Agent 宿主定义稳定、无颜色依赖的输出契约。
- 为 `ask/local/off`、授权、无信号、重复、隐私、离线、认证和不确定提交建立场景测试。

### Out

- 静默自动提交、后台上传、自动遥测或 blanket consent。
- 由仓库配置、已安装 Plugin、`gh` 登录或过去授权推导本条提交许可。
- 自动公开 security-sensitive 内容或建立私密安全披露渠道。
- 跨项目后台聚合、定时提醒、批量提交、GitHub 之外的新渠道。
- 自动修复 Vibe Kit，或自动评论、关闭 GitHub Issue。

## Acceptance criteria

- [x] AC-1: `ask` 下无合格信号时不创建 candidate、不显示反馈提示、不访问网络，主任务结果保持不变。
- [x] AC-2: `ask` 下新建或 material-resurfaced candidate 后，系统先完成主任务，再自动展示一次本地 exact review；用户不需要主动调用 feedback CLI。
- [x] AC-3: review 完整显示 report ID、target、privacy、dedupe、network state、exact title/body/labels 和 review hash；展示过程不联网。
- [x] AC-4: 用户只需回复“提交”即可授权刚展示的 report/repository/hash；普通“好”“继续”、无响应、转向新任务和“稍后”都不构成授权。
- [x] AC-5: repository、title、body、labels 或 candidate 改变时旧 hash 和旧授权失效；必须重新展示并取得新授权。
- [x] AC-6: “稍后”保持 `review-ready` 且 unchanged 时不再次打扰；“忽略”进入 dismissed，只有新增实质证据或 severity 提升才 resurfaced。
- [x] AC-7: unchanged local duplicate 静默累计；远端 duplicate 链接已有 Issue，不创建第二条。
- [x] AC-8: secret 在落盘前阻断，常见 PII 在 review 前去敏，security-sensitive candidate 不提供 public submit；错误信息不回显敏感原文。
- [x] AC-9: 缺 `gh`、未认证、离线、权限不足或远端结果不确定时不丢失 candidate、不盲目重试、不阻塞主任务，并提供单一恢复动作。
- [x] AC-10: `local` 只生成本地 candidate、不主动询问；`off` 不做主动生成或询问，但不删除已有状态，显式 feedback 命令仍可工作。
- [x] AC-11: 每个 Close 最多一个反馈决策块；S 级普通任务、无信号和 unchanged candidate 都不产生可见噪音。
- [x] AC-12: tracked config、Plugin 安装、canonical repo、`gh auth` 和历史授权均不能单独触发外部写入；未授权外部写入率为 0。

## Success measures

- `ask` 下合格的新建/material-resurfaced candidate 可见率为 100%。
- 从 review 到批准只需要一次自然语言回复，不要求用户输入 CLI 命令或复制 hash。
- 无信号提示率、未授权写入率、重复 Issue 率均为 0。
- unchanged/dismissed candidate 重复提示率为 0。
- 反馈失败不改变主任务 completion、verification 或 exit status。
- 不新增遥测；使用场景测试、dogfood 和中央仓库 Issue 质量评估闭环效果。

## Risks

- 阈值过低会造成提示疲劳和中央仓库噪音。
- exact payload 过长可能淹没任务完成摘要；必须允许折叠但保持完整可访问。
- 自然语言同意存在歧义；只有紧邻当前 review、明确指向提交的回复才有效。
- 并发更新可能让批准过期；hash 变化必须 fail closed。
- 升级后一次性展示历史 backlog 会造成洪泛；MVP 只提示本次新建或 material resurface。
- `privacy=clean` 不是绝对安全证明，用户仍需能检查完整 payload。

## Confirmed decisions

1. 所有新安装和缺失配置的历史项目默认 `ask`；显式已有 mode 在升级时保留。
2. “稍后”不做基于时间的自动提醒，只有 material change 或用户主动查看时再出现。
3. MVP 不提供 `auto-submit`；未来需要时另做本机用户、GitHub account、repo、project、policy version 和 expiry 绑定的长期授权设计。
4. Issue 保持 candidate 原语言和空 labels；运营分类不阻塞 MVP。

## Role review

- PM：推荐 `ask` 默认主动展示并询问，不把 silent auto-submit 纳入本工作项。
- UX：推荐 Agent 自动完成发现、去敏、去重和 review，用户只需回复“提交”；纯 CLI 仍完整输出 exact payload。
