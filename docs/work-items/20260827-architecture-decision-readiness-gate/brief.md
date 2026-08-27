# Architecture decision readiness gate

- ID: `20260827-architecture-decision-readiness-gate`
- Size: `L`
- Status: complete
- Created: 2026-08-27

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: L workflow change spanning role authority, lifecycle, host adapters, and protocol compatibility.
- Decision owner: Tech Lead perspective
- Governing decision: [ADR 0008 — Accepted](../../decisions/0008-technical-decision-readiness-gate.md)
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: Independent Tech Lead re-review on 2026-08-27 approved the exact persisted ADR 0008. The readiness state and fail-closed transition contract, native and sequential author-review separation, exact-versus-semantic rollback boundary, protocol/release alignment, and unique ADR numbering are resolved. Accepted ADR 0007 and work item `20260827-agent-first-adoption` already establish the repository's unpublished `0.5.0` / core protocol 3 development target; ADR 0008 introduces no publication action. No technical blocker remains.
- Material product decisions: none
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator
- Confirmed at: `2026-08-27T14:56:41Z`
- Confirmation basis: Accepted PM brief, Accepted ADR 0008, approved independent-agent review, and the existing unpublished 0.5.0/protocol 3 development decision in Accepted ADR 0007.
- Readiness history: `2026-08-27 — not-assessed → decision-required/blocked; ADR 0008 proposed; independent review requested changes; state, review, rollback, protocol/release, and numbering blockers resolved; ADR 0008 accepted; gate confirmed implementation-ready.`

## Goal

让高风险或包含持久技术取舍的工作在进入代码实现前，自动完成一次与 size 和风险相称的技术决策就绪检查：需要新决策时先形成并评审决策记录；既有决策已覆盖或无需新增持久决策时留下可审查的依据。用户不再需要自己意识到“这里应该先做 ADR”，实现 writer 也不会在关键架构、恢复或兼容性边界仍未决定时开始修改代码。

## Problem and evidence

Vibe Kit 已经定义了部分正确原则，但没有把它们连接成完整的 pre-implementation handoff：

- operating model 区分 PM 的 problem framing / acceptance 与 RD 的 technical decisions / implementation，并要求 L 级记录重要架构决策。
- lifecycle 从 Shape 进入 Plan 和 Implement，但没有技术决策 readiness 阶段、进入条件或阻断状态。
- quality gates 只要求 durable choice 最终存在 decision record，没有明确要求它在代码编辑前已被接受。
- feature flow 在 PM/UX shaping 后可以直接交给 implementation writer；debug flow 在根因确认后也可直接交 writer；implementation flow 不要求先扫描未决的 durable/high-risk technical decisions。
- work-item 模板只能表达 generic technical notes 和 ADR link，不能稳定表达“需要决策、正在决策、已满足 gate、无需新增决策及其理由”。
- [GitHub #3](https://github.com/mintgao/vibe-kit/issues/3) 已记录此 gap：高风险工作可能在没有 mandatory technical-decision scan、accepted decision evidence 或明确 gate owner 的情况下进入实现。

实际 dogfood 是 `20260827-permission-safe-atomic-upgrade`：它是 L 级，涉及 permissions、跨文件一致性、rollback/recovery、恢复再次失败、crash boundary、ownership 与 compatibility。当前 brief 后来加入了案例专属的“实现前必须 ADR”和 `Decide → Implement`，但通用流程并不能保证 Agent 在这些提示不存在时仍会识别并阻断实现。这说明个别 Agent 可以补救，Vibe Kit 机制本身尚不能稳定保证交接。

## Users and jobs

- **项目维护者 / product owner：** 希望定义清楚产品结果和验收后，把内部技术取舍交给合适的技术决策职责；只有当选择会改变 scope、用户可观察行为、风险、成本或不可逆外部边界时才需要本人决策。
- **Product shaping owner：** 需要明确 what、why、users、scope、non-goals、observable behavior 和 acceptance，并能把未决技术问题交出，而不是被迫替技术角色选择方案。
- **Technical decision owner：** 需要在实现前收到明确问题、约束和 AC，识别 durable trade-offs，形成或引用决策记录，并说明决策如何覆盖风险、恢复、迁移和兼容性。
- **Independent technical reviewer：** 需要在高风险工作中独立检查方案、替代方案、失败边界和后续影响，而不是由 implementation writer 自行认证。
- **Workflow orchestrator / Coding Agent：** 需要从 size、风险和需求特征自动判断 gate 是否适用，路由所需角色，核对证据，并在 gate 未满足时停止实现。
- **Implementation writer：** 需要拿到已经就绪的技术决策边界；若实现中发现新的 durable decision，能够停止并重新打开 gate，而不是做静默架构选择。
- **QA：** 需要根据产品 AC 和已接受的技术边界独立验证最终行为，但不代替实现前的技术决策评审。

## Scope

### In

- 在所有会进入代码实现的 Vibe Kit 路径中建立统一的 technical-decision readiness contract，至少覆盖 feature、debug-to-fix 和直接 implementation handoff。
- 明确 Shape complete 只表示产品需求就绪，不自动等于 Implementation ready。
- 定义 S/M/L 下检查深度、触发条件、允许的 readiness 结果和阻断行为。
- 定义何时必须新建或更新 ADR，何时可以引用既有 accepted ADR，何时可以记录 no-new-decision rationale。
- 明确 product shaping、technical decision、independent review、gate transition、implementation 和 QA 的职责边界与交接证据。
- 让 Coding Agent 根据 work size、风险、scope、AC、open decisions 和既有 architecture 自动识别 gate；不得依赖用户或 brief 明说“需要 ADR”。
- 在 work item 中以可审查方式表达 open technical decisions、governing decision evidence、review 结果和 implementation readiness。
- 支持有独立 Agent 的宿主和只能顺序执行不同 perspective 的宿主；两者必须保持同一阻断语义和证据契约。
- 使用 `permission-safe-atomic-upgrade` 的无显式 ADR 提示版本作为必须命中 gate 的 dogfood/conformance case。
- 保持既有轻量任务的低流程成本，并为已开始或已有 work item 的任务定义非破坏性采用方式。

### Out

- 决定新增 `vibe_tech_lead` 角色，还是由现有 `vibe_rd` 的 architecture perspective 承担；这是后续技术/adapter 决策。
- 规定 ADR 文件格式、状态存储、CLI schema、Agent 配置或具体自动化实现方式。
- 为每个 L 工作项强制新建 ADR；L 必须有显式 readiness 结果，但既有 accepted decision 或可信 no-new-decision rationale 可以满足 gate。
- 为局部、可逆、无共享契约影响的实现选择创建 ceremonial ADR。
- 让 PM 决定 architecture / trade-off / technical approach，或让用户审批每一个内部技术选择。
- 用 implementation writer 的自我说明替代高风险工作所需的独立技术评审。
- 改变 QA 对产品验收的独立责任，或把 ADR review 当成实现后的 QA。
- 在本工作项中决定 `permission-safe-atomic-upgrade` 的事务、日志、备份、恢复或 crash-recovery 方案。
- 引入组织级审批系统、远端签字服务、复杂 workflow engine 或遥测。
- 为已经 complete 的历史工作补造 ADR 或 readiness 记录。

## Assumptions

- 角色是独立判断职责；宿主是否用独立 Agent、同一角色的不同实例或顺序 perspective 承担，由技术设计决定。
- “Accepted decision”表示 required author/review evidence 已齐备且没有阻断 implementation 的开放问题；具体状态载体由后续技术设计决定。
- Product owner 只处理会实质改变产品 contract、风险、成本或不可逆边界的选择；其余技术取舍由技术决策职责完成。
- 对尚未进入实现的 active M/L 工作采用新 gate；已完成工作不追溯。实现中的工作若发现尚未决定的 durable/high-risk boundary，应停止并补做 gate。
- 本工作项改善开发机制，不承诺通过遥测统计真实组织行为；验收以受控场景、artifact evidence 和独立 verification 为主。

## Observable behavior contract

### After Shape

- Agent 明确区分 `product-shaped` 与 `implementation-ready`；完成目标、范围和 AC 不再自动触发 writer。
- 对适用的 M/L 工作，Agent 检查 size、风险、跨系统边界、失败/恢复语义、迁移与兼容性、权限/安全/隐私、不可逆状态、open decisions 和 governing ADR。
- 检查结果必须能被用户和后续角色看懂，并表达为以下语义之一：
  1. **Decision required:** 存在未决 durable/high-risk technical choice；实现被阻断，并说明需要决定什么、为什么影响实现、下一责任 perspective 是谁。
  2. **Covered by accepted decision:** 既有 accepted decision 完整覆盖本工作；记录关联和适用理由后可进入实现。
  3. **No new durable decision:** 检查已完成，剩余选择局部、可逆且不改变共享契约；按 size policy 记录必要理由后可进入实现。
  4. **Decision accepted:** 新建或更新的 required decision 已完成独立评审、产品层开放问题已解决，可由 gate owner 确认进入实现。

### When blocked

- Agent 不开始代码编辑、不把某个技术方案伪装成“合理默认”，也不把开放 trade-off 留给 writer 静默处理。
- Agent 给出单一、明确的下一交接：technical decision owner 需要产出的决策范围；只有存在 material product choice 时才请求用户。
- 缺少角色映射或宿主不能并行时，流程可以顺序完成不同 perspective，但不能跳过 decision/review evidence 或宣称 gate 已通过。

### When ready

- Implementation writer 能看到 accepted decision、governing ADR 或 no-new-decision rationale，以及与 scope/AC、风险、migration/recovery/compatibility 的相关边界。
- Gate owner 只在 required evidence 完整、required review 完成、无阻断 open decision 时确认 implementation-ready。
- 实现中若发现 schema、protocol、ownership、compatibility、recovery、security 等新的 durable choice，readiness 被重新打开，writer 停止相关实现并交回决策阶段。
- 用户无需批准不改变产品 contract 的内部技术细节；如决策会改变 scope、observable behavior、risk/cost 或 irreversible/external boundary，Agent 在进入实现前请求用户确认该产品选择。

## Size and trigger policy

### S — lightweight by default

- 清晰、局部、低风险、可逆且不改变共享契约的 S 工作不要求独立 readiness artifact 或 ADR，可直接实现并做 focused verification。
- 若扫描需求特征后发现 permissions/security、migration、recovery、irreversible state、跨系统 contract 或 durable architecture change，则说明原 size 不再可信；在实现前重新分级并按 M/L gate 处理。

### M — conditional gate

- M 工作在 planning/handoff 时必须检查 technical-decision triggers，但未命中时无需制造独立 ADR 或冗长 artifact。
- 命中任一 trigger 时，进入 decision-required 状态；存在新的或变更的 durable choice 时必须有 accepted decision record，既有 decision 完整覆盖时可以引用后放行。
- 典型 trigger 包括：公共或共享 contract、跨组件/子系统边界、schema/protocol/version compatibility、migration、auth/permissions/security/privacy/trust boundary、rollback/recovery/crash/failure consistency、不可逆状态，以及多个方案在风险、成本或长期约束上存在重大差异。

### L — explicit readiness outcome required

- 每个 L 工作在 implementation 前必须有显式、可审查的 readiness outcome；仅有 shaped brief、technical notes 或 implementation plan 不足以放行。
- 新建或改变 durable architecture / contract / recovery / migration / security decision 时，必须先有 accepted decision record 和独立 technical review。
- 若 accepted ADR 已完整覆盖，记录关联和适用性；若没有新 durable decision，记录 no-new-decision rationale。两者均不得用来掩盖仍未解决的高风险 trade-off。
- L 的 implementation writer 不得同时成为 required decision 的唯一 author、唯一 reviewer 和 gate approver。

## Role boundary and handoff contract

- **Product shaping owner:** owns `what / why / users / scope / non-goals / observable behavior / acceptance / product-level assumptions`; 标出技术问题和需要用户决定的产品取舍，但不规定 architecture 或 implementation approach。
- **Technical decision owner:** owns `architecture / alternatives / trade-offs / technical approach boundaries / migration / recovery / compatibility / technical risks`; 形成或更新 decision evidence，并映射到产品 AC，但不扩大产品 scope。
- **Independent technical reviewer:** 检查 decision 是否覆盖关键替代方案、failure modes、rollback/recovery、安全与兼容性；不得以 implementation writer 的自我认证替代 L/高风险 M 的 required review。
- **Workflow orchestrator / gate owner:** 负责识别 trigger、路由 perspective、核对 evidence 和 open decisions，并声明是否 implementation-ready；不得替 technical decision owner 暗定方案，也不得替用户回答 material product choice。
- **Implementation writer:** 只在 gate 通过后实现 accepted boundary；发现新 durable/high-risk decision 时停止并重新交接；不得自行 waive gate。
- **QA:** 在实现后独立把产品 AC 映射到证据，同时验证实现没有越出 accepted decision boundary；QA 不能补做或替代 pre-implementation gate。
- **User / product owner:** 只对改变 scope、用户可观察行为、风险/成本承诺、不可逆状态或外部兼容性的选择作最终产品决策；普通内部技术方案不需要用户逐项审批。

本 work item 只定义上述职责与权限，不决定这些职责映射到新的 `vibe_tech_lead`、现有 `vibe_rd`、同一角色的独立实例或其他 adapter 结构。

## Acceptance criteria

- [x] **AC-1 — Product/technical boundary:** operating model、相关 flow、角色说明和 work-item guidance 一致区分 product shaping owner 的 `what/why/scope/observable behavior/acceptance` 与 technical decision owner 的 `architecture/trade-off/technical approach/migration/recovery/compatibility`；不存在要求 PM 选择实现方案的冲突表述。
- [x] **AC-2 — Lifecycle gate:** 任一适用 flow 从 Shape/Investigation 进入 Implement 前都有明确 technical-decision readiness check；`product-shaped` 不被视为 `implementation-ready`，required evidence 缺失时流程明确停止代码编辑。
- [x] **AC-3 — Size policy:** S/M/L policy 可按上述规则判定：普通 S 保持轻量；M 命中 trigger 才进入显式 gate；每个 L 都有显式 readiness outcome，但不要求每个 L 新建 ADR。
- [x] **AC-4 — ADR trigger:** guidance 明确列出 durable/shared contract、cross-system boundary、schema/protocol/compatibility、migration、permissions/security/privacy/trust、rollback/recovery/crash consistency、irreversible state 和 material trade-off 等 trigger；局部可逆实现选择明确不需要 ADR。
- [x] **AC-5 — Readiness outcomes:** work item 或等价 durable artifact 能无歧义表达 `decision required`、`covered by accepted decision`、`no new durable decision`、`decision accepted / implementation ready`，并包含 governing decision、review evidence、open blockers 和 gate confirmation 所需信息。
- [x] **AC-6 — Ownership and authority:** guidance 明确谁负责 product contract、谁负责提出 technical decision、谁独立 review、谁核对 gate 并确认进入 implementation、writer 在何时必须停止，以及何种 product choice 必须交给用户；不要求在本 AC 中决定具体 Agent 名称。
- [x] **AC-7 — Independent review:** L 和命中高风险 trigger 的 M 不能由 implementation writer 作为 required decision 的唯一 author、唯一 reviewer 和 gate approver；不支持独立 Agent 的宿主必须保留顺序 perspective、明确 review evidence 和相同阻断语义。
- [x] **AC-8 — Direct implementation preflight:** 即使用户直接请求 implementation，Agent 也会先读取 size、risks/open decisions、相关 architecture 和 decision status；required gate 未满足时返回阻断原因与下一交接，不修改 application/shared code。
- [x] **AC-9 — Debug-to-fix coverage:** M/L bug 或 incident 在 investigator 确认根因后，如修复引入或改变 durable/high-risk technical boundary，不能从 root cause 直接跳到 writer，必须先满足同一 readiness gate。
- [x] **AC-10 — Dogfood without hint:** 给 Agent 一个不包含 `ADR`、`architecture decision`、`先做技术方案` 等显式提示的 `permission-safe-atomic-upgrade` 场景，仅保留 L size、permissions、跨文件原子性、rollback/recovery、恢复失败、crash boundary、ownership/compatibility 等需求特征；Agent 必须识别至少事务/恢复/crash boundary 为 implementation-blocking technical decisions，停止代码编辑并路由 decision stage。
- [x] **AC-11 — Gate release:** 在同一 dogfood 场景补充 accepted decision 与 required review evidence、解决 material product open decisions 后，Agent 能确认 implementation-ready 并把 accepted boundary 交给一个 writer；不得重复要求 PM 决定内部实现细节。
- [x] **AC-12 — Negative/false-positive coverage:** 代表性的 copy-only S、局部可逆 bug fix 和不改变共享 contract 的普通 M 不会被要求创建 ADR；若 S 实际命中高风险 trigger，则先重新分级而不是静默绕过 gate。
- [x] **AC-13 — Reopen behavior:** writer 在实现中发现新的 schema、compatibility、ownership、recovery 或 security decision 时，相关实现停止，work item 回到 decision-required；更新/新 decision accepted 后才重新放行。
- [x] **AC-14 — Existing work adoption:** 尚未进入实现的 active M/L work item 使用新 gate；complete 历史 work item 不追溯补造；正在实现的工作只在发现未决 durable/high-risk boundary 时暂停并补做 gate。
- [x] **AC-15 — Verification evidence:** 独立 QA/verification 将 AC-2 至 AC-14 映射到至少 dogfood positive case、accepted-decision release case、direct implementation case、debug-to-fix case、S/M negative cases和 sequential-host case，并记录任何未验证的宿主能力限制。

## Success measures

- 所有受控 L dogfood 场景在 required decision evidence 缺失时，进入代码实现或产生代码写入的次数为 0。
- `permission-safe-atomic-upgrade` 无显式 ADR 提示场景的 trigger 识别率为 100%，accepted decision 后放行率为 100%。
- 代表性普通 S 与非 trigger M 场景被错误要求创建 ADR 的次数为 0。
- 验收样本中的每个 L work item 在实现前都能找到唯一、明确的 readiness outcome、governing decision evidence 和 gate owner 结论。
- 需要用户回答的问题全部可追溯到 scope、observable behavior、risk/cost、irreversibility 或 external compatibility；内部技术细节的无必要用户审批次数为 0。
- feature、debug-to-fix 和 direct implementation 三条入口在相同输入下产生一致的 gate/block behavior。

## Risks and open decisions

### Risks

- **过度流程化：** 如果把 L readiness review 等同于“每次新建 ADR”，会制造 ceremonial artifact 并拖慢工作；size policy 和 no-new-decision rationale 必须保留轻重比例。
- **触发器解释漂移：** 不同 Agent 可能对 durable、high-risk 或 material trade-off 理解不一；需要 positive/negative conformance cases，而不能只依赖抽象文字。
- **伪独立评审：** 不支持 subagent 的宿主可能把顺序自检误称为独立评审；必须明确 capability limitation 和 review evidence，不能假装并行能力。
- **状态语义分叉：** operating model、work-item template、flow Skills、Agent prompts 与 adapter 若分别定义 readiness，可能再次产生规则不一致。
- **Gate owner 变成隐形架构师：** orchestrator 若在核对证据时顺手替 technical owner 做方案，会破坏职责边界。
- **用户审批泛化：** 若任何 ADR 都要求用户确认，会把内部技术决策重新推回用户；用户 gate 必须限于 material product choices。
- **既有工作兼容：** 对 active work 全量追溯可能制造噪声；采用范围需遵守本 brief 的非追溯规则。

### Open product decisions

- 当前没有阻断 Shape 的产品决策。默认产品契约已固定为：L 必须显式 readiness outcome、M 按 trigger、S 默认轻量；gate 覆盖所有进入实现的 flow；用户只决定 material product choices。

### Technical decisions deferred to the next phase

- 新增 `vibe_tech_lead`，还是复用/细分现有 `vibe_rd` perspective。
- readiness state、review evidence 和 gate confirmation 的权威存储位置及状态模型。
- 如何在 managed Skills、Agent prompts、work-item template、quality gates 与 host adapters 之间保持单一事实来源。
- native-subagent 与 sequential-review 宿主如何实现独立性和 conformance evidence。
- 是否需要 CLI validation，还是先以 workflow contract 和 scenario verification 交付最小版本。

## References

- [GitHub #3: Add an architecture-decision readiness gate before implementation](https://github.com/mintgao/vibe-kit/issues/3)
- `.vibe/core/operating-model.md`
- `.vibe/core/quality-gates.md`
- `.vibe/core/templates/work-item-brief.md`
- `.agents/skills/vibe-feature-flow/SKILL.md`
- `.agents/skills/vibe-debug-flow/SKILL.md`
- `.agents/skills/vibe-implementation-flow/SKILL.md`
- `docs/work-items/20260827-permission-safe-atomic-upgrade/brief.md`
- `docs/work-items/20260827-distribution-architecture/design.md`
