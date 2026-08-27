# Continuous Vibe Kit feedback

- ID: `20260827-continuous-kit-feedback`
- Size: `L`
- Status: complete
- Created: 2026-08-27

## Goal

让任何采用 Vibe Kit 的项目都能在真实开发中识别脚手架自身的系统性改进点，形成去敏、去重、可追踪的本地候选，并在用户审阅精确 payload 后可控地提交到指定 GitHub 仓库。

## Context

- 当前 workflow 会沉淀业务 work item 和验证证据，但没有把跨项目出现的 Vibe Kit 摩擦转化为维护者可感知的改进输入。
- 反馈可能包含私有项目信息；安装 Plugin、存在 GitHub token 或过去曾授权，都不能视为本条报告的外发许可。
- 当前仓库没有 Git remote，`gh` 登录状态失效，因此本工作项只能实现通用 GitHub 提交能力并用隔离 fixture 验证，不能替用户选择或实际创建中央仓库。

## Scope

- In: 新增 `vibe-feedback-flow` Skill，并在 M/L Close、Vibe 命令/流程异常和用户明确要求时做轻量归因检查。
- In: 新增 `vibe feedback draft/list/review/check/submit/dismiss` 命令；本地草稿、去敏、fingerprint 去重和 dismiss 全部离线可用。
- In: 本地状态默认写入 `.vibe/local/feedback/`，由嵌套 `.gitignore` 排除，不采集原始日志、代码、对话或环境变量。
- In: GitHub 查重和提交使用显式 `--repo` 或 managed 配置；提交必须携带当前 payload 的 review hash，并在创建前再次查重。
- Out: 自动遥测、后台上传、自动提交、跨项目全局聚合、自动修复 Vibe Kit、自动处理安全漏洞、替用户创建 GitHub 仓库或身份。

## Acceptance criteria

- [x] AC-1: M/L Close 或高置信 Vibe Kit 异常会触发轻量复盘；无有效信号时不创建草稿、不打扰用户、不改变主任务结果。
- [x] AC-2: 有证据的问题生成包含 kind/component/title/summary/expected/observed/impact/reproduction/evidence、Vibe 版本、workflow/role、confidence/severity、privacy、fingerprint 的本地候选。
- [x] AC-3: `draft/list/review/dismiss` 在默认和离线环境中不发起网络请求；状态位于默认不进 Git 的 `.vibe/local/feedback/`。
- [x] AC-4: 常见路径、邮件、URL 和项目标识被泛化；token、Authorization、私钥或疑似 raw secret 会阻止落盘和外发。
- [x] AC-5: 同 fingerprint 只保留一条候选并累计 occurrence/last_seen/新证据；dismiss 后同级无新证据的候选保持抑制，严重度提升时重新浮现。
- [x] AC-6: `review` 展示目标 repo、完整 title/body、privacy、dedupe marker 和由 canonical payload 计算的 review hash；payload 任一字段变化都会使旧 hash 失效。
- [x] AC-7: 未配置 repo、无 `gh`、未认证、未提供/提供过期 confirm hash 时不创建 Issue，候选保持可恢复。
- [x] AC-8: 隔离 GitHub fixture 中，提交前再次查重；首次成功只创建一个 Issue并记录 URL，重复提交或超时后重试不会创建第二个。
- [x] AC-9: README、operating model 和 Skill 明确 local-first、non-blocking、consent-based，不宣称自动遥测、自动提交或自动修复。
- [x] AC-10: 本仓库实际完成一次 self-retrospective；若不能提交到真实 GitHub，记录准确阻塞原因和恢复动作。

## User flow

```text
Agent observes a reusable Vibe Kit gap
  ├─ insufficient evidence / business issue → stay silent
  └─ high-confidence framework signal
       → local draft + sanitize + local dedupe
       → user-visible exact review + review hash
       → optional remote duplicate check (explicit)
       → per-report confirmation
       → submit once or link existing issue
```

## Exit-code contract

- `0`: safe intended outcome, including local draft, review, dismissal, successful submit, or detected remote duplicate without a new Issue.
- `1`: remote operation failed or outcome is uncertain; no second create is attempted and the local record remains recoverable.
- `2`: usage or local precondition failure, including unsafe content, missing repo/gh/auth, invalid report, or stale confirmation hash.

## Risks and decisions

- Feedback is self-evaluation; hypotheses must retain confidence and may be dismissed by the user.
- Simple redaction is not proof of privacy. The system minimizes stored fields, blocks obvious secrets, shows exact payload, and requires per-payload confirmation.
- Security-sensitive findings must not use ordinary public GitHub Issue flow.
- Ownership, state path, consent and idempotency are fixed by ADR 0003.
