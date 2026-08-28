# Design: Post-upgrade automatic takeover

## Experience principle

The human confirms one exact project/version upgrade. Vibe Kit owns the remaining
healthy path: plan, apply, installed health, activation, evidence-backed project
adaptation, target-version re-evaluation, verification and original-goal resumption.
Progress may be visible but requires no response.

Additional input is allowed only for a newly discovered material product choice,
expanded source or permission scope, irreversible action, external compatibility
commitment or recovery decision. Host-controlled permission prompts remain valid.

## State model

| State | Evidence | Permitted user claim |
|---|---|---|
| Upgraded | Exact target files/state applied consistently; target doctor not broken | “Vibe Kit 已升级到 …” |
| Activated | Positive host evidence that current or successor task loaded target rules/Skills | “新版规则已生效” |
| Adapted | Onboarding complete and consistent with repository evidence | “项目上下文已完成检查” |
| Verified | Required installed/project checks passed; skipped states explicit | “安装检查和项目验证已通过” |
| Ready | Upgraded + activated + adapted + verified; no blocker | “可以继续开发” |

Unknown activation, onboarding, warning, verification or protocol states fail
closed. `doctor=broken` is never complete. A known non-blocking warning may produce
qualified ready language only when its classification is versioned and stable.

## Healthy flow

```text
confirmed exact upgrade
  -> trusted source and target resolution
  -> read-only plan
  -> safe apply without redundant confirmation
  -> installed target-version doctor
  -> activate target rules
       -> same-task verified reload, or
       -> automatic successor-task handoff, or
       -> unsupported-host degraded fallback
  -> check onboarding and durable context
       -> unchanged complete evidence, or
       -> automatic evidence-backed refresh, or
       -> invalid/contradicted blocked state
  -> run required verification
  -> re-evaluate unfinished original goal under target rules
  -> resume original goal or report maintenance-only readiness
```

If the request is maintenance-only, the flow must not invent application work. If
upgrade is a prerequisite to an existing goal, that exact goal resumes without the
user repeating it.

## Progress hierarchy

Healthy progress uses goal language and hides commands, JSON, archives and
per-file copying:

1. “正在检查从 0.4.0 到 0.5.0 的升级影响。”
2. “安全预检已通过，正在升级。”
3. “新版文件已通过安装检查，正在加载新版规则。”
4. “新版规则已生效，正在检查项目上下文与验证结果。”

For automatic handoff, the source task reports only that a successor is loading
the new rules. The successor owns the final success message so completion is not
announced twice.

## Success response

Report in this order:

1. previous and target versions plus trusted source;
2. activation path and evidence;
3. onboarding/adaptation outcome;
4. checks executed, unconfigured or skipped and their results;
5. resumed original-goal status, or maintenance-only readiness.

Recommended maintenance-only copy:

> Vibe Kit 已从 0.4.0 升级到 0.5.0。新版规则已生效，项目上下文已完成检查；安装检查和项目验证均通过。可以继续开发。

Recommended resumed-goal copy:

> Vibe Kit 已从 0.4.0 升级到 0.5.0，新版规则和项目上下文均已就绪。我将继续处理原目标：“……”。

An apply receipt alone can never generate either message.

## Incomplete states

Every blocked or degraded response contains exactly:

1. the incomplete layer;
2. whether writes occurred and the last proven stage;
3. one concrete reason;
4. one safe next action or material decision.

### Conflict

State that upgrade did not complete, managed files were not replaced, incoming
review candidates were written, list only conflicting relative paths, and recommend
one action: review and resolve those candidates before upgrading again.

### Permission or partial mutation

If no write or rollback is proven, report the old version as intact. For
`unknown-partial`, automatically inspect the target and run the installed doctor
when possible; if consistency cannot be proven, pause and recommend scoped Git or
trusted-payload recovery. Never retry blindly.

### Activation unavailable

> Vibe Kit 文件已升级到 0.5.0，安装检查通过；当前宿主无法在本任务加载新版规则，因此尚未激活，不能宣告项目已就绪。下一步：在此项目中新建一个 Codex 任务。

If the host can carry the original goal, prefill it. Otherwise provide one
copyable original-goal sentence while still requiring only the single task action.

### Invalid or contradicted onboarding

State that upgrade and activation succeeded but adaptation did not. Do not replace
invalid project-owned state. Ask only for the one fact or permission that changes
the outcome; never expose an internal Skill name.

### Verification failed

State that upgrade and activation succeeded but readiness did not; name the failed
configured check, stop resumed implementation, and give one action to address it.
No configured command is “unconfigured, non-blocking”; a permission-denied or
side-effect-uncertain required check is skipped and blocking.

### Original goal blocked by new rules

Separate framework readiness from application-task readiness:

> Vibe Kit 已升级、激活并完成项目适配；原开发任务因新版技术决策门禁暂停，需要确认：“……”。

This is not an upgrade failure, but implementation must not resume until the
target-version blocker is resolved.

## Accessibility and consistency

- Do not rely on color, icons, animation or table alignment to convey state.
- Emit one fact per line and allow narrow-terminal wrapping.
- Use relative scoped paths; avoid raw exceptions and unrelated project content.
- Follow the user language; keep closed internal enums out of healthy prose.
- Across channels, reserve “已升级 / 已激活 / 已就绪” for their exact meanings.
- Give one recovery action, not parallel CLI/Git/permission/manual-edit menus.
