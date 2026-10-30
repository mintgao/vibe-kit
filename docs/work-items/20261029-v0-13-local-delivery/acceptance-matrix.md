# 0.13 执行验收矩阵（R2 产品标准副本，未执行）

本轮 **36项：N01–N36**；后续 **13项：L01–L13**，不混算。旧A01–13/X01–07共20项、W01–08共8项、旧后续B/C/D/E共16项，合计44项在末表逐项映射。旧ID只作溯源，不是另一套当前验收，也不把设计计为Pass。

通用fixture为隔离合成Python unittest与Node package-script项目。标“双方”的项目都必须实际执行；不访问真实业务项目或远端服务作故障靶。每项未来记录输入/候选身份、操作、观察、证据引用和QA四态Pass/Fail/Blocked/Not applicable。宿主场景不能用静态字符串测试替代；能力不足须Blocked。

## 本轮：F1 扩展作者模板（6项）

| ID | 可执行输入/操作 | 可观察预期与证据 |
|---|---|---|
| N01 | 双方合法完整default receipt、有效依赖排序与only partial对照 | 原validator确认完整shape、四check集合、coverage/cli_invoked/provenance/summary；有效排序接受，partial不闭合default；记录fixture身份 |
| N02 | 逐次变异missing/extra、bool/float version、check集合/排序、coverage/flags/summary | 命中相应契约层。删除未配置项且同步summary使局部自洽，仍在集合/shape层拒绝；仅summary报错不够。summary独立反例；不改输入、不用较松helper |
| N03 | helper直测Pass，默认discovery或package dispatcher仍加载旧helper/错参数 | 双方真实入口focused观察origin/参数发现问题；只修受审入口后通过，历史调用与断言保留 |
| N04 | 同一候选在允许的字节/索引/模式前提下变换输出缺席/畸形JSON/Fail/伪Pass | 合法byte/hash/index-only consumer保持准入；故意以inert语义左右准入的坏consumer被捕获；正常read/decode不自动违规。逐变体记录完整性前提 |
| N05 | 独立改变索引、删被索引输出、改摘要/执行位/模式、加入未声明路径 | 原完整性guard拒绝，与N04分轴记录；不以语义无关豁免字节/所有权约束 |
| N06 | doctor输出已生成与未生成；同有限用例经focused和真实默认loader生命周期 | 双方记录输出状态、loader、origin/参数及断言；有限setup不新增完整QA预跑，不只测空目录 |

## 本轮：F2 静态预检与维护接续（12项）

| ID | 可执行输入/操作 | 可观察预期与证据 |
|---|---|---|
| N07 | 双方A-only声明选择可信payload B，在apply前调用只读预检 | 真正报告已声明身份约束未满足/需适配；语法有效不足以通过。列rule/owner/来源/目标证据、受管变化与保护范围；项目零写入 |
| N08 | B被允许或有限集含B；重复同目标诊断；原plan含conflict | 仅该规则满足、结果稳定；原conflict保留，不报全面兼容/ready；字节与模式不变 |
| N09 | 无声明/未启用，以及仅旧toolchain/checks.requires | 双方旧行为/配置/receipt保持，无新强制字段、后台记录、诊断脚本或依赖；不要求后续功能 |
| N10 | 畸形声明、重复ID、未知必需字段；合法但非支持复合候选/合并文件/命令规则 | 前者报配置问题；后者报未评估、具体原因与支持边界；不默认兼容或执行引用入口 |
| N11 | 目标/声明漂移、身份来源缺失/损坏、跨项目复制报告 | 不复用旧比较；要求重新绑定/诊断，未掌握postimage不猜；保留原安装冲突 |
| N12 | 拒绝读取、输入不可用、unsafe link/path、超限输入/权限拒绝 | 有界具体诊断；区分未执行/未知/denied；零提权、外写、联网、换工具重试；无授权不执行项目diagnostic |
| N13 | 合成B仅身份变、B′消费合同确变、第三例信息不足 | 哈希差仅判身份未认可；有区分性focused证据才判参数/字段/语义不兼容；信息不足未评估。旧版可用性与下一owner明确 |
| N14 | A-only遇B后进入维护Agent；分别有原适配授权、无授权、材料性范围变化 | 先保留A并继续已授权只读诊断/方案；精确下一动作与owner；未授权apply/适配=0，不伪造安装冲突或QA失败；只有材料选择/真实权限才请求决定 |
| N15 | 已激活且无未处理事务；首次default前已知阻塞与真实default失败各一例；另缺激活/readiness/review/授权、denied反例 | 两个真实维修入口均能路由；原业务执行=0，满足门槛才单writer。已知阻塞不先跑QA制造verification-failed；真实失败收据保留。onboarding不豁免代码修复门槛 |
| N16 | 审查后精确B重新准入、最小API adapter、未知C负例 | 仅认可受审B、C仍拒绝；仅改拥有范围，源码/input冻结、旧断言、check集合、预算不弱化；记录现态与可撤销改动 |
| N17 | 修复最终candidate，完整默认QA/partial/旧候选/失败变体 | RD focused；目标doctor与独立完整default及其他接管条件满足才重新评估/恢复原业务。一次真实run满足两门槛可共同引用；失败/变化不套旧QA |
| N18 | 双方按主计划端到端案例，从可信目标经三类兼容判断，选择保留A或受控升级至真实激活/适配/QA/恢复；各阶段加入受控断连/部分/失败分支 | 安全终点/每阶段事实、缺口、owner、一个下一动作正确；中断先读回，未激活不维修，未验收不恢复业务。静态合同与真实host执行证据分列，真实后继缺能力则Blocked |

## 本轮：F3 只读交接视图（5项）

| ID | 可执行输入/操作 | 可观察预期与证据 |
|---|---|---|
| N19 | 双方源任务仅apply+doctor，再输入结构valid结果；无host激活结论 | 固定栏目列目标、各阶段、证据、缺口、owner与一个下一动作；只能upgraded/activation pending，按既有manual fallback新建同项目任务；无适配写入。对应#31 AC1–2 |
| N20 | 双方真实后继任务核对实际activation set，宿主按现有合同认证manual或实际具备的正向激活路径 | 视图仅消费宿主提供的已认证结论及来源；离线CLI始终不认证host；不得用Agent自报/工具存在/合成receipt代替。对应#31 AC3 |
| N21 | 目标/目录/版本改变、旧任务证据、声称reload无证明、同名文件 | 拒绝提升activated/ready，指出具体绑定缺口；不凭一致hash认证来源。对应#31 AC4的一部分 |
| N22 | 真激活后无当前完整QA、only/旧候选Pass/缺终态，与真实匹配完整default对照 | verification pending或准确阻塞；inspect-run仅历史事实，另验candidate适用性；全部接管门槛才可呈现ready。对应#31 AC4其余部分 |
| N23 | 缺引用、不支持版本、证据冲突、manual-only、合成敏感goal/custody混入 | 保留缺口，不能补造记录/自裁冲突；宿主内证据优先，只投影必要非custodial事实；项目/公开输出不含真实goal/custody/私有task ID。对应#31 AC5 |

## 本轮：F4 升级维护安全读回（6项）

| ID | 可执行输入/操作 | 可观察预期与证据 |
|---|---|---|
| N24 | 双方维护fixture模拟创建进程前明确失败、写后回执丢失、执行失败、独立denied | 强证据才not-executed；丢回执先unknown再观察前后态；已执行不重复，失败保存实际原因；denied不因重连/原授权重试。记录动作/目标/理由/确定性/owner |
| N25 | 双方已授权维护两文件批次首项已写；第二项未写；另旧行匹配失败、冲突/并发改动变体 | 逐项读回；已完成计数不增加；仅授权scope内、确知未落地且前态精确匹配无冲突的缺项可补；否则Blocked，不整批重放，不把old-line failure归因断连 |
| N26 | 双方升级维护QA观察断开，回读原run/receipt；已Pass与真实Fail对照 | 原QA工作负载spawnCount仍1；inspect-run等只读CLI/probe进程启动单独计数，不算重复QA；不更改预算/顺序/断言；完整当前绑定证据才可引用；失败原字节保留；running/日志/connected不证明活性或完成 |
| N27 | stale/跨项目操作身份、摘要漂移、前后态均不符、无可靠probe/观察中断 | 先只读最小核对；不能判完成或未执行，显示unknown/Blocked、确切能力缺口及一个安全下一动作；不扩大观察/写入范围 |
| N28 | 安装前、rolled-back、recovery-required、unknown-partial、committed待清理、无active、漂移各例 | 区分保留A/既有恢复/停止；有active时不ordinary upgrade/handoff/activate/adapt/verify。recover-upgrade依原授权/合同；committed仅清理，无active返回blocked，均不当降级；action code不伪装CLI |
| N29 | 自有项目适配撤销：现态精确匹配/并发变化/用户既有改动；B仍安装而旧guard只接受A | 仅授权且精确匹配的自身改动可撤销，不reset目录、不动用户改动；重新验状态，B不被接受仍blocked；安装事务不覆盖任意项目数据/外部副作用 |

## 本轮：共同交付门槛（7项）

| ID | 检查/操作 | 必须留下的证据与边界 |
|---|---|---|
| N30 | 无配置Python/Node路径、Python最低3.9、标准库依赖 | 沿真实命令工作；环境/dispatcher不可用记Blocked，不以stub冒充；轻量路径保留 |
| N31 | 0.12旧receipt/progress/takeover及历史publication profile | 原对象依原合同解释；新字段/词汇若必需由TL明确版本兼容，不暗改closed字段或历史profile |
| N32 | 只读性/输入所有权，对F2预检、F3投影、F4观察区间分别计量 | 相应读调用零新增项目/receipt文件、零状态写入，零项目check/hook/维修/恢复/原操作重放；允许调用已有只读CLI/probe进程并单独计数。F1 setup、真实dispatcher、获授权维修/恢复另计，不能借此放宽reader |
| N33 | 合成秘密/私有路径/指令/goal与超限异常 | 公共摘要不泄漏，限制大小/字段/回显，无自动上传；既有允许的私有工件保持私有；真实takeover/custody留宿主 |
| N34 | 每个正负场景的适用层与证据复核 | 区分文档/静态协议、真实CLI、真实host/Agent观察；无live证据不声称行为遵循、隔离或效率收益；规划不是实测 |
| N35 | 受影响bin/managed指南/Agent合同/Plugin镜像/安装后的入口 | 维修分支与停止条件一致，source/installed行为对齐；只改实际受影响面并保留历史兼容；不能只改F2页面声称闭环 |
| N36 | QA所有权、最终candidate和receipt复核 | 独立QA拥有未变化最终candidate一次完整default；能同时满足维修与接管条件引用同收据，不因流程名重复。缺失/失败/Blocked/畸形/partial/过期/失效、candidate改变或独立gate才重跑并记理由；旧195项不代新candidate |

## 后续：13项独立进入条件，不是本轮前置

| ID | 后续能力/可执行场景 | 预期与边界 |
|---|---|---|
| L01 | #32一般宿主操作adapter：范围外批次、ACK/目标不符、无可靠probe | 有明确操作身份/目标authority/授权与前后态才判断；无证据Blocked；不补发未授权外部请求。升级维护子集已在N24–N29，通用引擎不在本轮 |
| L02 | #30 Python/Node producer阶段事件、buffered/静默/无producer | 明确来源能力，缺事件未知；mtime/日志前缀不是当前子项或活性 |
| L03 | #30跨run/重复/逆序/过期/损坏/冲突terminal | 不覆盖可信终态、不提升为Pass或活着；有界处理 |
| L04 | #30观察断开回读原run及可选阶段事件 | 保持run身份/单次spawn，不推断未知后代已停；新增阶段reader部分待做，既有run回读已N26 |
| L05 | #30阶段完成但receipt缺失/失败/only/中断残留running | 活动与验收分列，不Pass；保留旧日志/收据/版本兼容 |
| L06 | #21 A通过、B未验证、C继承；源码/工具/input/未知路径变化 | 仅绑定范围内引用A；C不继承未经证明的Pass；descriptor与新clone关系可恢复 |
| L07 | #21已声明metadata-only变化对照完整性/模式错 | 不自引用hash循环，不任意排除变化；例外需项目显式定义与验证 |
| L08 | #26机器rollup：源码Pass/API Blocked/导出Unverified/Pending占位 | 仅源码阶段完成、保留owner/下一动作/真实等待条件；QA四态不扩；本轮人工维护表不冒充机器汇总 |
| L09 | #26目标资产与ACK/UI不一致；另行live评估 | 项目定义authority/变换/时效，未授权不探测；静态fixture与live指标分列，未测不报收益 |
| L10 | #24静态输出策略：声明路径、固定外写、例外、unknown工具 | 仅证明声明覆盖，不证明OS confinement，不改HOME/凭据/安全设置 |
| L11 | #24清理：仍running/unknown、symlink、owner/mode错、逃逸 | 默认保留；已知终态/身份/所有权完整且授权才可精确清理 |
| L12 | #25可移植版本、host绑定、过期能力证明、预算不足 | 明确缺口；不自动安装/扩预算/跳QA/改顺序 |
| L13 | #24/#25无配置/旧toolchain、跨平台缺安全primitive | 默认轻量；不支持明确降级/Blocked，无宽松回落 |

## 旧20项＋W8：逐项映射到本轮

| 旧ID | 当前ID | 保留/去重说明 |
|---|---|---|
| A-01 | N01 | 完整收据与partial |
| A-02 | N02 | 集合层反例保留 |
| A-03 | N03 | 真实接线 |
| A-04 | N04 | 好/坏consumer双轴 |
| A-05 | N05 | 完整性负例 |
| A-06 | N07 | 真正身份比较 |
| A-07 | N08 | 匹配不覆盖冲突 |
| A-08 | N09 | 无配置 |
| A-09 | N10 | 畸形与不支持分开 |
| A-10 | N11 | 来源/漂移 |
| A-11 | N12 | 输入和权限 |
| A-12 | N18 | 扩成完整E2E；N19–N23具体约束阶段 |
| A-13 | N06 | doctor生命周期 |
| X-01 | N30 | 实际运行环境 |
| X-02 | N31 | 旧合同 |
| X-03 | N32 | 准确观测区间扩至只读view/读回 |
| X-04 | N33 | 隐私有界 |
| X-05 | N34 | 静态/live边界 |
| X-06 | N35 | 分发一致性 |
| X-07 | N36 | QA所有权 |
| W-01 | N13 | 身份/语义/unknown分类 |
| W-02 | N14 | 安装前接续 |
| W-03 | N19, N28 | 激活缺口及活动事务禁区 |
| W-04 | N15 | 首次QA前与真失败维修入口 |
| W-05 | N16 | guard强度 |
| W-06 | N17, N36 | 最终候选/QA/恢复 |
| W-07 | N28, N29 | 安装恢复与项目撤销分开 |
| W-08 | N12, N23–N27, N33 | 缺证据/权限/读回/隐私分到对应责任层 |

## 旧后续16项：逐条说明吸收与保留边界

| 旧ID | 本轮吸收 | 后续保留 | 判定与理由 |
|---|---|---|---|
| B-01 | N19 | 无 | 完整吸收，最小只读view本轮 |
| B-02 | N20–N23 | 无 | 完整吸收，真实host/缺QA/冲突本轮 |
| B-03 | N24, N25, N27 | L01 | 部分：仅升级维护；一般宿主批次仍后续 |
| B-04 | N24, N26, N27 | L01 | 部分：本地维护写后丢回执/观察中断；任意外部ACK/目标authority后续 |
| C-01 | 无 | L02 | producer事件非本轮 |
| C-02 | 无 | L03 | 子阶段协议负例非本轮 |
| C-03 | N26 | L04 | 部分：复用已有run读回；新增阶段reader仍后续 |
| C-04 | N22仅复用已有验收边界 | L05 | 子阶段完成与receipt关系仍后续；不以常识约束宣称交付#30 |
| D-01 | N11/N17仅本轮已有candidate绑定 | L06 | 通用谱系完整保留后续；不新增descriptor |
| D-02 | 无 | L07 | metadata规则非本轮 |
| D-03 | N18/N23仅复用人工阶段/owner表达 | L08 | 机器rollup仍后续，已有#18不再计算研发 |
| D-04 | N27仅本地维护证据优先原则 | L09 | 通用目标authority/外部结果/live评估仍后续 |
| E-01 | N32/N33仅本模块输入/隐私保护 | L10 | 通用静态output-policy仍后续，不误称只有清理 |
| E-02 | 无 | L11 | 通用owned-temp清理未纳入；安装事务自身清理依原合同 |
| E-03 | 无 | L12 | host/预算profile非前置 |
| E-04 | N09/N30仅现有无配置路径回归 | L13 | 新profile跨平台退化仍后续 |

原B后续中的狭窄交接需求被吸收，其余多数只复用既有证据原则。上述映射不能把后续特性说成“顺便已实现”。本轮产品验收0项已执行；R2 规划审查仅确立产品范围，执行门槛见[brief](brief.md)。
