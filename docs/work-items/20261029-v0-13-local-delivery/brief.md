# Vibe Kit 0.13 本地执行交付：历史治理公共投影

- ID: 20261029-v0-13-local-delivery
- Size: L
- Status: historical accepted local-stage governance; no current publication-candidate release
- Created: 2026-10-29
- Source baseline: e676446c661e717578b4dd114548cdfecb2b2437 / source version 0.12.0
- Original brief SHA-256: ddcdf087c7d561f19ee66a0b71b72a22ec03058b8c1af92975fd817e72f60d69

## Projection and authority

本文件是原本地阶段 brief 的忠实、精简公共投影。保留已认可范围、原授权边界、历史 readiness 记录及技术审查关系；不导入私有准备/环境记录、执行报告、QA 原始输出或未发货规划材料。原文件与原收据保留原身份。省略的执行事实不被改写为公共证据或产品 Pass。

本公共 checkout 在本次投影时仍是 0.12 公共源码基线，尚未导入 0.13 实施代码。本文件中的历史批准不释放新候选的实施、验收或发布；当前授权和 blocked gate 见 [publication brief](../20261029-v0-13-publication/brief.md)。

## Accepted scope and criteria

[scope.md](scope.md) 保留 F1–F4、完整端到端维护链、非目标与分批退出条件。[acceptance-matrix.md](acceptance-matrix.md) 保持原字节，含 N01–N36 共36项本轮标准、L01–L13 共13项后续边界及旧44项映射；本投影不减少或重新解释标准。

- F1 / #29：Python 与 Node 各一套可运行模板；真实入口、严格原 validator、语义/完整性双轴和 doctor 生命周期。
- F2 / #28（部分覆盖）：有限 payload 身份规则的可选只读预检；真实激活、授权、readiness、独立审查和单 writer 下的受控诊断/适配/验收；不放宽 guard。
- F3 / #31：复用 apply/doctor/validate-takeover/inspect-run 及宿主已认证事实，呈现阶段、缺口、owner、一个下一动作；不新增聚合 CLI 或宿主认证协议。
- F4 / #32（部分覆盖）：仅升级维护自有改动、原 QA run、既有安装事务的只读核对与有界恢复；不做通用重试器。
- #21/#24/#25/#26/#30 延期且非前置；#20/#22/#23 不重复研发，不自动评论或关闭 issue。

技术语义由 [ADR0025](../../decisions/0025-upgrade-compatibility-and-maintenance-continuation.md) 管理；历史技术 review 的初轮问题与最终批准见 [technical-review.md](technical-review.md#final-review)。规划批准和技术批准均不是产品 QA。

## Historical execution authorization and boundaries

原阶段仅获准本地实现、必要验证、独立验收与可审阅交付；须先满足 Accepted 决策、独立技术批准、orchestrator gate 与实际 readiness 校验。其当时的公开 push/PR/merge/release 和 issue 写入尚未获授权。原阶段禁止 commit、push、PR、merge、release、issue 写入及其他项目/服务访问；此处作为历史范围保留，不倒改成后来授权。

原阶段只在隔离源码 checkout 工作，保护原目录及既有本地改动，不切原分支，不改原安装状态，不复制私有历史或宿主 goal/transfer/custody。运行输出、cache 与 bytecode 使用指定项目内路径和进程级环境；不写系统临时目录，不改系统环境或凭据，不安装依赖。源码 checkout 不因版本文件或 manifest 被手改而取得 installed healthy 或 activation 结论。

后来新增的发布授权另由新 publication brief 明确；它不改变原记录的时间与范围，也不授予 issue 操作或绕过保护的权限。

## Historical technical decision readiness

以下为历史原 brief 中记录的已接受决策与 gate 信息，按原字段保留。它只解释本地阶段的治理，不是本公共候选的当前 readiness，也不把历史执行或宿主证据移植到新目标：

> - Outcome: `decision-accepted`
> - Trigger evidence: F2 payload身份/项目声明兼容合同与跨工作流维护入口；F3宿主证据权威与阶段提升；F4恢复、失败一致性与所有权；N07–N29及N31/N35/N36
> - Decision owner: vibe_tech_lead author / Astra xhigh
> - Governing decision: `docs/decisions/0025-upgrade-compatibility-and-maintenance-continuation.md`
> - No-new-decision rationale: none
> - Review mode: `independent-agent`
> - Review result: `approved`
> - Review evidence: `docs/work-items/20261029-v0-13-local-delivery/technical-review.md#final-review`
> - Material product decisions: R2四模块范围已认可；#29/#31覆盖原有限诉求、#28/#32部分覆盖；原业务暂停、guard不放宽、延期项非前置；见scope.md与acceptance-matrix.md
> - Open blockers: none
> - Gate: `implementation-ready`
> - Gate owner: Workflow orchestrator
> - Confirmed at: 2026-10-29T07:29:30.929626+00:00
> - Confirmation basis: Accepted ADR0025正文、不同Astra xhigh实例独立approved复审、已认可R2四模块/N01–N36、仅本地执行授权；实际validate-readiness结果随放行包记录
> - Readiness history: 2026-10-29初始decision-required/blocked；第一轮review changes-required的四项均保留且已修订；独立复审approved后接受ADR0025并确认implementation-ready，实际validator通过前不开始实现

历史原件所载 Final review 批准版本为 93ea22d082e0422406ad6c474bcff18483c910b5127d2d0dcb823088c78a4fdd。仅将其 Status 从 Proposed 改为 Accepted 后，原 ADR0025 的身份为 d4c93358dda898374908f1f1e72bd948159d444b0b74f2b1f56ee10dba3ec22d。本次公共投影的新增说明/宿主表述修订必须由当前独立 reviewer 检查，不能借历史批准推定新字节已批准。

## Evidence and verification boundary

本投影不提供旧阶段完整 default、产品验收或真实宿主 receipt。原环境准备的局部事实不等于 N30 整项 Pass；源候选测试不等于 N18/N20 的真正同根后继与目标内容激活。新 C/H/M 必须分别完成其实际 readiness、全部36项验收、隐私检查及适用独立 QA。

RD 只运行 focused 开发检查；独立 QA 拥有每个适用不变最终候选的一次完整 default。同一真实最终 fixture run 可以在满足全部条件时同时用于维修和接管；候选变化、失败/无效证据或独立 gate 的新运行须明确理由，不能因流程名称重复运行。原 receipt 保留原身份，不重写失败，不用结构 valid、doctor healthy、onboarding complete 或工具存在替代宿主激活。

## Relationship to publication

本地阶段不定义 0.13 publication profile。新发布工作的精确 profile、公共源投影、H/M/E、实际远端核验与无 issue 操作范围由 [ADR0026](../../decisions/0026-v0-13-publication.md) 和 [publication brief](../20261029-v0-13-publication/brief.md) 单独管理。它们仍需当前独立审查与 orchestrator 放行；本文件不自批、不宣布新候选 ready。
