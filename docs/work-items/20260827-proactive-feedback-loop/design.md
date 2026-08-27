# Design: Proactive Vibe Kit feedback loop

## Experience principles

1. **Primary task first.** 反馈只能出现在主任务结论和验证证据之后。
2. **Default visible, not default sent.** `ask` 默认主动展示提交决策，但不默认联网。
3. **One-turn approval.** 用户不需要操作 report ID、repo 或 hash；Agent 内部绑定这些值。
4. **Exact and inspectable.** 用户批准的内容必须完整可访问，不能只给摘要后索取授权。
5. **Silence is a feature.** 无信号、unchanged duplicate 和 dismissed candidate 不制造噪音。
6. **Fail closed, recover locally.** 授权歧义、内容变化、隐私风险或远端不确定都停止外发并保留本地状态。

## End-to-end flow

```text
Main task completes with verification evidence
  ↓
Silent Vibe Kit gap classification
  ├─ no qualifying signal → no UI, no file, no network
  └─ qualifying reusable signal
       ↓
     local draft → sanitize → fingerprint dedupe
       ├─ blocked/security-sensitive → local blocked receipt, no public action
       ├─ unchanged/dismissed duplicate → silent
       └─ new or material resurface
            ↓
          resolve feedback.mode
            ├─ off   → no proactive candidate or prompt
            ├─ local → save locally; optional one-line receipt
            └─ ask   → local exact review → show one decision block
                                             ├─ submit → remote dedupe → existing/create once
                                             ├─ later  → keep review-ready
                                             ├─ modify → regenerate payload/hash → ask again
                                             └─ ignore → dismiss fingerprint
```

## Mode semantics

| Mode | Silent classification | Local candidate | Close behavior | Network |
|---|---|---|---|---|
| `ask` | Yes | Yes | New/material candidate gets one exact review and explicit question | Only after exact approval |
| `local` | Yes | Yes | At most a one-line local receipt; no submission question | Never proactively |
| `off` | No | No proactive candidate | No feedback output | Never proactively |

Rules:

- `ask` is the default for new installs and for projects where mode is absent.
- Existing explicit mode is project-owned and preserved during upgrade.
- Mode controls discovery/presentation, not authorization. `ask` never means consent.
- Manual `feedback draft/review/submit` remains available in all modes; explicit manual submit still requires exact review approval.
- `auto` is a reserved future value, not accepted by the MVP runtime.

## Close decision block

The Agent-facing presentation should be structurally stable:

```text
Vibe Kit feedback READY — local only

发现 1 个可复用的 Vibe Kit 改进点。
Target: mintgao/vibe-kit
Privacy: CLEAN
Dedupe: UNIQUE LOCAL CANDIDATE
Remote access: NOT USED

--- exact GitHub Issue payload ---
Title: [Vibe Kit feedback] <title>

<complete canonical body>
--- end payload ---

建议提交这条反馈。回复“提交”即可。
也可以回复“稍后”“修改”或“忽略”。
```

Presentation rules:

- The primary task result must already say complete before this block begins.
- Target, privacy and network state appear before the payload and action.
- Supporting clients may collapse the payload body, but it must remain directly expandable and hash-bound.
- Plain terminal output prints the complete body before the action line.
- Report ID and review hash remain visible for audit/recovery, but users never need to copy them during the Agent flow.
- “不回复” equals “稍后”; it is never consent or dismissal.

## Actions and authorization

### Submit

A reply is valid only when it is adjacent to the current review and unambiguously requests submission, for example “提交这条反馈”. The Agent then:

1. Recomputes or re-reads the current repo-bound review hash.
2. Stops and re-presents if report, repository, title, body or labels changed.
3. Runs remote fingerprint lookup.
4. Links an existing Issue or creates at most one new Issue.
5. Returns the resulting URL and stores the submission state.

Generic replies such as “好的”“继续”“确认” without a clear feedback reference are not authorization.

### Later

- Keep `review-ready`.
- Do not network, dismiss or schedule a timer.
- Do not ask again for unchanged evidence in the next task.

### Modify

- Apply only user-requested, sanitized changes.
- Generate a new preview and review hash.
- Invalidate the previous approval and show the complete payload again.

### Ignore

- Dismiss the fingerprint with a sanitized reason.
- Resurface only after new material evidence or severity increase.

## Eligibility and anti-noise

- Visible prompting is limited to M/L Close, explicit user requests, or a direct Vibe CLI/workflow failure.
- Ordinary S work remains silent.
- Each Close shows at most one decision block.
- Multiple symptoms should be generalized to one root-cause candidate when evidence supports it; remaining candidates stay local and may be summarized as a count.
- A candidate prompts only when newly created or materially resurfaced.
- Local duplicates increment occurrence silently.
- A fingerprint already linked to a remote Issue does not prompt another create.
- No “no feedback found” success message is shown.

## State handling

| State | User experience | Allowed next step |
|---|---|---|
| No signal | No output | None |
| `review-ready` in ask | Exact decision block once | submit/later/modify/ignore |
| `review-ready` in local | Optional local receipt | explicit manual review |
| `dismissed` unchanged | Silent | material evidence only |
| Remote duplicate | Link existing Issue; no create | close |
| Submitted | Show Issue URL | close |
| Missing repo | Save locally; no submit prompt/hash | configure target |
| Missing `gh` or auth | No Issue; preserve approved report | explicit login then retry same hash |
| Offline/duplicate-check failed | No create; preserve report | retry later |
| Create outcome uncertain | Warn not to create again; require fingerprint lookup | checked retry only |
| Privacy blocked | No public submit action; no sensitive echo | revise locally/private channel |

## Privacy and security

- Redaction and secret blocking happen before presentation.
- Error output never repeats a matched secret.
- `privacy=blocked` and security-sensitive signals cannot reach public submission.
- `privacy=redacted` remains ask-only; it can never be silently promoted to a future auto mode.
- A configured repository and authenticated GitHub account provide routing and identity, not consent.
- The canonical hash remains the enforcement boundary even when the UI hides operational syntax.

## CLI and Agent responsibility

- **CLI owns:** mode parsing, report state, privacy gates, fingerprinting, canonical payload/hash, remote dedupe, idempotent submission and failure state.
- **Managed Skill owns:** deciding whether evidence qualifies, keeping the main task non-blocking, invoking local draft/review, and routing natural-language actions.
- **Host adapter owns:** rendering the stable decision block as text, expandable content or action controls without changing authorization semantics.

Implementation should expose effective mode and presentation state deterministically from the CLI rather than requiring every Agent to reinterpret project YAML. Structured output can be a later adapter enhancement; the MVP must retain stable plain text.

## Accessibility and terminal behavior

- Status is textual (`READY`, `BLOCKED`, `SUBMITTED`), never color-only.
- Respect non-TTY and `NO_COLOR`; do not require spinners, arrow keys, countdowns or default `Y/n` prompts.
- Use explicit payload boundaries so Issue content cannot be mistaken for Agent instructions.
- Keep target, privacy and network state before the action request.
- stdout carries normal receipts; stderr carries blocked, failed or uncertain remote states.
- Output order stays stable for screen readers and log capture.

## MVP and follow-ups

### v0.4.0 MVP

- Effective `ask/local/off` behavior.
- Default ask presentation after new/material candidate.
- One-reply submit from Agent conversations.
- No-signal silence, anti-repeat, privacy and remote failure states.
- Regression matrix across modes and authorization boundaries.
- Updated README, managed Skill/AGENTS, product context and protocol metadata.

### Later

- True `auto` with a local, non-Git authorization record bound to user/account, host, repo, project scope, allowed kinds, confidence, privacy policy version and expiry.
- Structured `--json` presentation for native host action cards.
- Private security disclosure channel.
- Batch review, cross-project aggregation and operational feedback analytics without adding automatic telemetry.

## Decision requiring approval

The accepted MVP interprets “Issue submission is the default” as **default proactive ask with a one-reply primary action**, not silent auto-submit. ADR 0006 records this durable consent boundary.
