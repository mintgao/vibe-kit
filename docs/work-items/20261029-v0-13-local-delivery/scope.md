# 0.13 执行范围（历史已认可产品范围的公共投影）

- Projection status: historical accepted local-stage scope; publication-candidate implementation and acceptance remain unverified.
- Original scope SHA-256: 66cd7d10f6592f56026db493a685b8d7fe97827059d2a169712d91fcd43a081c.
- 本公共投影保留原 scope 的全部四模块正文、N01–N36 与十三项后续边界；移除未发货规划原件的路径依赖，原始文件另行保留。
- 正文的“当前”“未来”“待 TL 决策”与 issue 状态描述均属于原本地阶段的规划时点；最终技术语义以已接受的 [ADR0025](../../decisions/0025-upgrade-compatibility-and-maintenance-continuation.md) 为准，不据此宣称公共候选已实现或最新远端状态。
- 历史授权/readiness 见 [brief](brief.md)，历史独立技术批准见 [technical review](technical-review.md#final-review)，完整产品标准见 [acceptance matrix](acceptance-matrix.md)。
- 新公共候选的独立 gate、实际验收与发布授权由 [publication brief](../20261029-v0-13-publication/brief.md) 管理；本历史范围不释放该 gate，也不授予 issue 操作权限。
- 原公开源码基线：e676446c661e717578b4dd114548cdfecb2b2437；本投影不是产品 QA 记录。

## 先看四个交付模块

| 模块 | 用户得到什么 | 合成例子 | 本轮边界 |
|---|---|---|---|
| F1 扩展测试模板（#29） | 写项目准入扩展时，提前发现测试本身误判或漏检 | 收据少了未配置的 lint 条目应在集合层报错；读取 doctor 输出算摘要仍合法 | Python/Node 各一套可复制模板；保持真实入口、旧断言与独立 QA |
| F2 升级前兼容判断与受控适配接续（#28） | 升级前知道哪些已声明规则未满足，并有人把诊断、适配、验收推进下去 | 项目只认可工具身份 A，目标是 B：先保留 A，查清只是绑定过旧还是接口真变了 | 有限 payload 身份比较＋维护工作流；不自动放宽 guard 或执行陌生 hook |
| F3 升级阶段、缺口、owner、下一动作只读视图（#31） | 看清已安装、已激活、已适配、已验证分别到哪一步 | apply/doctor 成功但没有真实激活证据：显示 activation pending，给同项目新任务动作 | 宿主 Agent 按固定栏目组合现有证据；不新造认证协议或聚合 CLI |
| F4 升级维护未知结果观察与安全恢复（#32 部分） | 断连或部分成功后，先确认发生了什么，再安全接续 | 两个维护文件只改了一个：逐项读回，只补确证尚未落地且仍获授权的一项 | 仅升级维护自有改动、原 QA run 与安装事务；不做通用操作重试器 |

四个模块共同交付一个结果：项目扩展能测对，升级兼容问题能在准确的状态和权限边界内推进至验收，遇到阻塞时明确停在哪里、由谁处理、下一步是什么。普通无扩展项目保持轻量。这里的版本是规划目标，不是发布日期或全功能已完成承诺。

## 12 项开放 issue 的统一归属

“完整/部分”指计划覆盖原议题的诉求，均不代表已经实现、通过验收或获得结案授权。

| Issue | 当前证据判定 | 本轮归属与覆盖 | 未纳入部分/后续 |
|---|---|---|---|
| [#20](https://github.com/mintgao/vibe-kit/issues/20) | PR27/0.12 已交付精确 onboarding 类型校验 | 已交付，只保留回归与独立收尾 | 本轮不再次实现，不操作 issue |
| [#21](https://github.com/mintgao/vibe-kit/issues/21) | 普通应用候选谱系/机器 descriptor 仍缺 | 延期；本轮仅引用已有候选与 QA 证据 | 通用身份模型、复制后适用性、自引用边界；非前置 |
| [#22](https://github.com/mintgao/vibe-kit/issues/22) | PR27/0.12 已交付真实入口 focused 指引 | 已交付，F1 复用 | 只收尾，不重复计算交付 |
| [#23](https://github.com/mintgao/vibe-kit/issues/23) | PR27/0.12 已交付 inspect-run | 已交付，F3/F4 复用 | 只收尾，不另造 reader |
| [#24](https://github.com/mintgao/vibe-kit/issues/24) | 项目通用输出声明预检与清理仍缺 | 延期；不把通用输出预检说成只有清理 | 静态 output-policy 与更高风险 owned-temp 清理分开；非前置 |
| [#25](https://github.com/mintgao/vibe-kit/issues/25) | 基础 toolchain/requires 已有，额外 host/能力/预算 profile 未有 | 延期；仅复用现有能力和预算 | host 绑定、目标能力证明、审阅预算；非前置 |
| [#26](https://github.com/mintgao/vibe-kit/issues/26) | Markdown coverage 已有，机器汇总/live 评估未有 | 延期；本轮维护表不包装成通用 rollup | rollup 与 live 行为基准分别评估；非前置 |
| [#28](https://github.com/mintgao/vibe-kit/issues/28) | 安装健康与项目准入分层正确，静态预检及接续有缺口 | F2，部分覆盖：有限身份比较＋诊断/适配/验收接续 | 任意规则声明/能力执行接口、复合候选预测不承诺；不自动关闭 |
| [#29](https://github.com/mintgao/vibe-kit/issues/29) | #22 之外的收据、语义/字节双轴、生命周期模板缺口 | F1，计划完整覆盖原有限诉求 | 以实际验收与另行结案授权为准 |
| [#30](https://github.com/mintgao/vibe-kit/issues/30) | 子生产者阶段/活动协议增量 | 延期；本轮只用现有 run 级观察 | 建议后续优先；不作为 F3/F4 前置 |
| [#31](https://github.com/mintgao/vibe-kit/issues/31) | 现有输出足够，缺最小组合和缺口呈现 | F3，计划完整覆盖原有限诉求，含原 AC1–5 | 原文未要求新 CLI；不能以未做新 CLI 为由虚构缺项；实际 host 验收不足则相应 AC Blocked |
| [#32](https://github.com/mintgao/vibe-kit/issues/32) | 一般宿主操作逐项读回/故障判读有增量 | F4，部分覆盖：仅升级维护操作 | 通用 host reconciliation adapter、任意文件批次/远端副作用恢复不纳入；不自动关闭 |

#20/#22/#23 只保留既有能力回归，不在本轮重复实现或操作 issue；其余九项没有新证据证明是 0.12 必修核心回归。

## F1 — 扩展测试模板

**用户问题。** 准入 helper 的局部测试通过，仍可能漏掉缺项，或把合法完整性读取误当语义依赖；长 QA 才发现会增加返工。

**具体例子。** 合成 Python CLI 和 Node 项目都消费完整默认收据。删除未配置 lint 条目并同步 summary 后，模板必须直接发现 check 集合不全；另一组把 doctor 输出从 Fail 换成伪 Pass，合法 byte/hash/index consumer 的准入结论不变，而故意依赖该语义的坏 consumer 必须被识别。

**最小实现切面（待 TL 决策）。** 扩展现有 affected-entry reference，提供两类可复制 fixture、完整合法 receipt 和逐字段变异。涵盖 schema 精确类型、check 集合、有效依赖排序、default/only、coverage、cli_invoked、summary/provenance 与结果枚举；以原 public validator 校验，不复制宽松解析器。语义探针须能区分带来源的结果依赖与正常 read/decode。缺席/损坏 JSON/Fail/伪 Pass 的语义独立性仅在项目允许且字节/索引/模式前提合法时成立；已索引文件缺失、摘要或模式错误仍拒绝。有限 setup 建立 doctor 已生成和未生成的真实默认 loader 生命周期，两种执行模式记录 origin/参数和状态。

**非目标。** 通用测试框架、强制配置、增加一轮完整 QA 预跑、删旧断言换绿、禁止所有输出读取、替项目实现准入或把测试作者错误归为 Kit bug。

**依赖/规模/风险。** 依赖已交付 #22 和现有收据合同；不依赖其余新模块。M 共享作者契约，中等工作量；若需要改变公共 schema/API，须按 L 重新决策。主要风险是模板过拟合、弱化完整性或看不见坏 consumer。

**验收。** N01–N06，加 N30–N36；两类真实 dispatcher 都要留下可运行证据，直接 helper 绿灯不能替代。

## F2 — 升级前兼容判断与受控适配接续

**用户问题。** “安装能成功”不等于“项目准入接受新工具”。只抛出不兼容提示仍不足以完成维护，Agent 应组织后续诊断、审查、适配和验收。

**具体例子。** 项目只允许 payload A，可信目标是 B。B 不在允许集只证明身份未获认可；B 的 README 变化也可能改变摘要。要区分“只需审阅后重新准入”“实际消费参数/字段/语义改变”“缺证据尚未评估”，不能直接接受 B 或断言 API 损坏。

**最小实现切面（待 TL 决策）。**

1. 可选只读诊断复用 plan/source/provenance/ownership，支持一类封闭规则：项目允许的 Kit payload 内容身份，固定 SHA 或显式有限允许集。rule ID、owner、声明来源和目标身份可定位；准确字段/位置/入口由 TL 定稿。
2. `print_plan` 有来源和条目，不能当完整未来项目镜像 API。目标身份必须独立从可信目标产物获得并绑定项目、声明与计划；目标/声明漂移需重新诊断。复合候选、合并文件、未知规则或能力明确未评估。
3. 分别报告声明是否有效、支持规则比较、未覆盖规则、原安装冲突与保护范围。无配置无额外门槛；原 conflict 不因匹配消失。首片静态调用零项目脚本、hook、下载、完整 QA 或写入；引用 diagnostic entry 不授予执行权。
4. 维护 Agent 对已启用且发现约束未满足/未知的项目，先保留旧版并分类、整理方案；这是维护路由，不新增 CLI 对所有项目的 apply 全局强阻断。已有授权内可信 focused 诊断由 Agent 选择和组织，不能执行包内陌生钩子。
5. 安装前准备最小适配与撤销边界。确需安装前改项目时，按当时已激活旧规则满足该项 readiness/审查/验证并保护旧版可用。安装后仅真实激活的目标任务进入下文受控维修分支。

**受控维修分支是未来必须补齐的合同。** 当前 feature/debug/implementation 对原业务跨升级恢复要求先适配与完整验证；安装合同又有 fix-configured-check。0.12 尚未完整说明二者之间允许的维修入口。未来需一致更新 AGENT_INSTALL 的 Adaptation/Failure、maintenance Plugin、feature/debug/implementation 入口，并对齐 onboarding/verification：目标真实激活、安装状态已确证且无未处理事务、原业务暂停、维护范围明确、已有授权、适用 readiness、独立技术 review、单 RD writer，缺一不得共享编辑。onboarding 只刷新有证据的上下文，不能作修改代码/guard 的豁免。

首次 default 前已知兼容阻塞可在此有界分支解决，不能先跑整套只为伪造 verification-failed；实际 QA 失败则保存真实失败收据与 candidate。TL 必须决定最小协议/词汇影响及镜像；如旧理由不足，明确版本兼容变更，不能套用虚假理由或宣称现有规则已全面支持。该分支不允许恢复原业务开发或放宽 guard。

**非目标。** 任意项目预测、自动改 pin/预算/检查集合、全项目镜像、通用 runner、自动迁移、以 doctor/onboarding complete 替代项目准入和最终 QA。

**依赖/规模/风险。** 复用现有目标身份/plan/安装、readiness 与工作流；F3/F4 支撑接续，F1 提供测试方法但不是项目启用前提。整体 L，工作量中到大：身份来源、维护入口兼容与权责是关键风险。技术事实若不支持最小切面，报告准确阻塞并评审方案，不能静默删掉已认可闭环或降低验收。

**验收。** N07–N18、N28–N36；真实问题分类、门槛反例、最终候选与原业务恢复均需证据。

## F3 — 最小只读升级交接视图

**用户问题。** apply、doctor、validator、最终 run 都有输出，但用户需手工拼接当前阶段与下一步，容易把安装健康误读成就绪。

**具体例子/交付载体。** 由宿主 Agent 根据现有结果在当前任务生成固定栏目视图，初片配维护指南、合成正反例与受控宿主场景；没有已存在的聚合 CLI，也不承诺必须新增 CLI。视图示例：

| 栏目 | 示例值与来源 |
|---|---|
| 已选择目标/安装事实 | A→B；可信 payload 与 apply/doctor 引用；事务已完成 |
| 阶段 | upgraded；结构 valid；activation pending；adaptation/verification 尚未完成 |
| 缺口 | 当前任务没有按既有合同认证的目标激活结论 |
| owner | 后继任务的维护 Agent（角色名；不写私有 task ID） |
| 一个下一动作 | 在同一项目新建任务；按既有 manual fallback 接续 |

**最小实现切面。** 复用既有身份、stage、evidence、next-action 词汇；安装事实从 apply/doctor 取，结构结果从 validate-takeover 取，历史执行从 inspect-run 取；激活结论只由宿主按现有合同核对真实目标内容并提供。先消费宿主内原证据，不要求把 takeover、goal、custody 转存仓库。原始私有收据可按既有规则留在允许位置，公开/项目摘要只引用必要的非 custodial 证据。

离线 CLI 永不认证宿主。`valid` 不等于 activated/ready；inspect-run 不证明当前候选适用性或项目来源。缺引用、版本不兼容、项目/目标/时间不符、证据冲突不能自行补造或裁决提升。无激活仍给现有同项目新任务动作；已激活但缺当前完整 default 显示 verification pending。真正 ready 只能由宿主满足既有全部条件后呈现。

**非目标。** 新 takeover schema、skeleton、host auth 协议、第二套状态机、库内 goal/custody、CLI 生成或认证 receipt。原 #31 本身不要求通用平台；本轮计划覆盖其全部有限诉求，不以没有新 CLI 制造“未覆盖”。

**依赖/规模/风险。** 仅依赖现有安装/validator/reader 和真实宿主激活能力；manual-only 保持原 fallback，不依赖 #21/#26。载体为 M 范围；涉及跨宿主证据权威与阶段提升，整体按 L 审查，中等工作量。宿主能力不足时不得把静态 fixture 当实际激活证据。

**验收与原议题逐项对应。** #31 AC1→N19（Python/Node源任务）、AC2→N19（healthy/valid不提升）、AC3→N20（真实后继及认证来源）、AC4→N21/N22（旧目标/伪reload、缺QA）、AC5→N23（引用/版本/冲突与manual fallback）。N18/N32/N33/N35/N36共同约束接续与隐私。全部执行通过后才有讨论结案的证据，仍需独立授权。

## F4 — 升级维护的未知结果观察与安全恢复

**用户问题。** 无回执不代表没发生；失败、denied、部分完成和 unknown 需要不同接续。错误整批重放会重复写入或重复长 QA。

**具体例子。** 某个已审查的升级维护 adapter 有两处自有文件改动。第一处确已落地，第二处因旧行不匹配失败；读回逐项前/后摘要后，只在第二处仍匹配前态且范围获授权时补缺项。另一个“写后丢回执”只是待注入的合成情况，先 unknown 再观察，不能把旧行失败归因为断连。

**最小实现切面。** 提供维护流程内的操作/目标/原因/结果确定性/证据/owner/下一动作表与受控场景，复用宿主已有操作关联和允许的非秘密前后态证据，不新增通用事务协议。可观察范围仅本次升级安装、自有维护适配文件、原 QA run；不覆盖任意远端请求或普通业务操作。

| 状态/时点 | 安全动作 | 终点边界 |
|---|---|---|
| 明确进程创建前失败 | 强证据判 not-executed；检查原授权与当前前态 | 若继续只可重试该范围内确未执行项；连接显示正常本身不构成证据 |
| 请求后无回执/写状态不明 | unknown；最小只读读回操作身份、目标、前/后态 | 无可靠 probe 保持 Blocked；不推为失败或成功 |
| 部分成功/普通执行失败 | 保留真实原因，逐项读回；已完成不重做 | 仅 scope 获授权、未执行且前态确证、无并发冲突的缺项可补；其余停止 |
| denied | 记录拒绝动作、目标、理由与已完成项，停止该动作 | 重连或此前授权不构成新权限；不改工具/命令绕过，必要时等待明确的新相关授权 |
| QA 观察断开 | inspect-run 回读同 run/私有 receipt，核对 candidate 适用证据 | 原QA工作负载不另启动；允许只读inspect-run/probe进程并单独计数；running不是活性，finished不是Pass；历史失败保留 |
| 尚未 apply | 保留旧安装；有准备改动则按其独立所有权处理 | 未发生升级不能称回滚成功 |
| 活动安装事务 | 先读已产生证据及既有诊断；plan/doctor可能因active状态返回阻塞 | 按既有授权用目标payload recover-upgrade；unknown-partial禁止自动覆盖，未确证前不handoff/activate/adapt/verify |
| committed / 无活动事务 | committed仅完成事务清理；无active的recover-upgrade返回blocked | 不是降级；项目QA失败只证明安装升级但项目未就绪 |
| 项目适配撤销 | 仅已记录自有改动、权限允许且现态精确匹配时撤销；重新验状态 | 不覆盖用户改动，不reset全目录；B仍安装且旧guard只接受A时仍blocked |

`inspect-upgrade-transaction` 是既有 next_action code，不是可运行 CLI。`recover-upgrade` 是可能写入的恢复操作，不是只读 probe；遵循原 recovery-required 一次恢复及后续确切结果，不把通用表改成盲重试循环。安装事务只覆盖受管文件、合并AGENTS、manifest/version及资格限定的onboarding桥接，不覆盖后来业务代码、数据或外部副作用。

**非目标。** 通用 reconciliation adapter、任意批量 patch 事务、自动补偿、远端补发、exactly-once、强杀未知进程、自动降级。feedback unknown 是既有机制的边界参照，不把 feedback 操作纳入本轮。

**依赖/规模/风险。** 现有恢复/inspect-run及宿主允许的可靠只读观察；缺能力如实阻塞，不要求 #30 子阶段事件。L，故障一致性与所有权风险高；指导/场景工作量中，通用执行器明显越界。

**验收。** N24–N29 与 N18/N32–N36。#32 AC1–2在升级维护合成操作范围覆盖，AC3覆盖原QA回读，AC4覆盖本范围身份/漂移/denied；AC5复用现有恢复并有无probe指导。一般宿主能力适配及范围外操作留 L01，故是部分覆盖。

## 一条完整的端到端维护案例

下面同一案例各在合成 Python/Node 项目执行；A/B表示已核验来源的不同payload，不声称0.13实际存在API破坏。原业务目标仅留宿主边界；规划示例不保存真实goal或custody。

1. **选择目标。** 项目当前A已验证，选定可信B、明确项目/版本授权；只读plan给出受管变化、保护范围、冲突和目标身份。冲突先处理，不强行apply。
2. **预检三分支。** A-only规则不接受B。若只身份未认可，核对B消费合同及有界focused证据；若真实参数/字段/语义不兼容，记录可区分的失败并提出最小adapter；若缺证据/权限/环境能力，保持unknown/Blocked。都不能自动加B、放宽guard或把检查未运行写成失败。
3. **保留旧版或受控推进。** 默认先保留A，已授权只读诊断和方案继续；可行且原范围内的方案经相应技术门槛推进，不重复询问已认可范围。材料性产品/风险/成本变化才给用户一个明确选择。确需先改项目则在A已激活规则下独立验收、保护A。
4. **安装与证据读回。** 安全plan及准确授权后apply。断连/部分成功/失败先由F4核对写状态，不整批重放；活动事务先恢复确证，不启动handoff/适配/QA。committed与目标doctor健康仅证明升级完成。
5. **真实激活。** F3显示当前缺口。没有正向宿主证明时源任务停并给唯一同项目新任务动作；真实后继独立核对目标activation set并按既有manual合同激活。合法JSON、同名文件或自称reload均不够。
6. **有界适配。** 已激活任务刷新必要上下文，原业务暂停；按F2拟定受控维修分支，以该项readiness、独立技术review、已有授权、单writer完成精确B绑定或必要adapter及focused负例。未做首次QA时如实标阻塞，不伪造verification-failed。适配失败走F4精确读回/撤销，B仍不兼容则继续blocked。
7. **最终QA。** 绑定最终源码/工具/配置candidate，目标doctor与独立完整default同时满足接管与适配门槛时引用一次真实运行。观察断连读原run，保留旧失败；真正失败或candidate变化才进入有理由的新验证。不能因两种流程名称多跑，也不能用partial、历史QA或onboarding complete顶替。
8. **恢复原业务。** 仅在适配、验证与其余接管条件满足后，由活跃任务按目标规则重新评估并恢复原业务；若新业务readiness仍阻塞，显示该层owner和一个下一动作，不宣布整体ready。

N18要求这条链的可观察输出与各拒绝分支，不只是文字顺序。静态合同fixture与真实宿主场景分开记证据；真实能力不具备则相应验收Blocked。

## 0.13内部交付顺序

以下是研发分批顺序，不替代上面的用户维护流程，也不删减四模块范围。每批以文档审查或focused证据退出，不增加中途完整QA。

| 批次 | 依赖 | 退出条件 |
|---|---|---|
| 共同技术方案与独立批准 | 已认可的四模块范围、N01–N36及现有合同 | 目标绑定、维修入口、视图权威、恢复所有权、QA复用方案明确；适用决策与独立技术review完成，orchestrator确认readiness |
| F1测试模板 | 自身适用readiness、现有#22与收据合同 | 两类真实入口的模板正负例和生命周期focused证据齐备；可独立交付，非其它模块技术前置 |
| F2静态判断与F4读回基础 | 共同方案与相应readiness；现有plan/provenance、inspect-run和恢复合同 | 有限身份比较、unknown/denied/部分结果与事务边界focused证据齐备；不依赖F1完成 |
| F3视图与F2维修接续整合 | F2/F4基础证据、现有宿主激活合同 | 固定栏目、真实激活边界、受控维修入口及分发合同一致；端到端各分支证据可交QA，缺host能力如实阻塞 |
| 同最终candidate独立QA | 四模块整合完成、最终candidate绑定、开发focused及审查证据齐备 | 独立QA完整default一次及适用专项验收；同一收据满足维修/接管全部条件时共同引用，重跑只依既有明确理由 |

## 后续顺序与不构成前置的能力

本轮36项验收与后续13项分别列在 [矩阵](acceptance-matrix.md)，旧44项（原20＋W8＋后续16）逐项映射。后续先考虑#30子阶段活动；#21候选descriptor与#26机器coverage按真实消费者分别推进，live评估另行设计；#24先静态输出策略，自动清理后拆；#25仅在存在host/能力/预算需求时收敛。#32通用操作adapter需真实可观测能力与独立信任设计，不给版本承诺。延期项都不是本轮四模块的前置，不借本轮引入框架。
