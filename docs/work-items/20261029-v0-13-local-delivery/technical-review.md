# ADR0025 historical independent technical review: public projection

- Projection: faithful historical review summary; not approval of revised public bytes or the current publication candidate.
- Original review SHA-256: 76d25265681cc11cb17dd32473309734ab60dd5110cc658958be105b3dbcbfc9.
- 原文保留初轮 changes-required 与最终 approved 的先后事实、四项问题及解决依据；移除私有 reviewer 实例标识，并将历史宿主可行性陈述限定为当时的计划背景。原件另行保留。
- 公开依赖：[scope](scope.md)、[historical brief](brief.md)、[unchanged acceptance matrix](acceptance-matrix.md)、[ADR0025](../../decisions/0025-upgrade-compatibility-and-maintenance-continuation.md)。

- Reviewer role: vibe_tech_lead / reviewer
- Requested model/effort: gpt-6-astra / xhigh
- Historical initial decision: changes-required
- Reviewed artifact: `docs/decisions/0025-upgrade-compatibility-and-maintenance-continuation.md`
- Reviewed SHA-256: `89aea072e59f8041353c7b3c891b2038a7d32c2bf7b7d42cf0ccb998e3909b37`
- Historical initial implementation gate: blocked; current publication gate remains separate and blocked

## Findings

1. P2: 支持规则字段计数“五项”与四字段示例矛盾。明确列出id、owner、kind、allowed_payload_tree_sha256四项，不新增第五字段。
2. P1: Plugin实际wrapper在进入CLI前resolve/rglob/is_file/read_bytes且可回显异常；不能只保护新CLI reader就宣称实际Plugin入口安全。作者需明确预检入口、来源认证与观察区间；经过wrapper则前置读取纳入约束，独立入口则明确不经过不安全前置路径。新命令dispatcher至失败输出不得调用旧source_root/枚举/原异常回显分支。
3. P1: 源枚举仅限制payload文件数量/字节，不限制空目录、目录项、深度、路径累积；FIFO打开后才验类型可能阻塞。补全遍历预算，在累积/排序前限制，non-blocking no-follow打开与类型复核；漂移复核覆盖project/source根及祖先名称到固定descriptor的绑定，不能只fstat同一fd。无需跨命令锁。
4. P2: findings“闭合且至少包括”未冻结；path语法、source type/ref/version错误、status/exit/next_action/owner映射及失败source/rules保留规则未确定。通用dispatcher会加operation/error/recovery并回显异常。需冻结全部词汇、路径和映射，新命令全部错误用同一闭合合同。

## Supported boundaries

预检仅身份比较，不认证网络；plan冲突保留。maintenance-required在verified阶段表达真实未运行QA的已知阻塞，真实失败保留原receipt。Agent-install protocol4→5足以版本化新增词汇，takeover schema2、Agent-install schema4、core/Codex7可保留；镜像/摘要同步，历史profile冻结。

F1真实入口/生产validator/双轴；F3/F4受管指南、证据权威、deny/unknown/partial/恢复/一次QA边界可行。source安装state不重写。产品N01–N36足够；无待用户材料选择。历史材料曾把宿主接续可行性作为待实测前提；该陈述不证明当前宿主能力、实际后继创建或目标激活。N20/N18始终须按矩阵取得真实同根后继及宿主认证证据，缺证据则Blocked。

## Next action

只读作者修订以上四项；root持久化后由同一独立reviewer复审。期间不改实现，不释放gate。本次只读，无产品QA/完整verify/readiness放行、无拒绝或不确定动作。

## Final review

- Result: approved
- Reviewer: a distinct vibe_tech_lead independent reviewer
- Requested model/effort: gpt-6-astra / xhigh
- Reviewed revision SHA-256: `93ea22d082e0422406ad6c474bcff18483c910b5127d2d0dcb823088c78a4fdd`
- Four prior findings: resolved; no new blocking technical issue

四字段集合一致；Plugin直达已认证payload且不先走旧wrapper；专用dispatcher/parser/error避开旧读取/异常回显；遍历和读取预算、nonblocking/no-follow、根/祖先名称绑定、缺席复核明确；全部finding/path/status/exit/action/owner及fatal清空/binding规则已冻结，focused场景覆盖。

历史最终审查认定N01–N36有可实施技术边界，无待用户材料选择。真正后继仍须针对冻结的双fixture分别在同一canonical root建立并取得宿主认证；历史能力说明不等于激活或验收通过。

此为历史独立技术批准，不是产品QA。原ADR随后仅将Status由Proposed变Accepted；还原标头后可复算出上述approved revision摘要，Accepted原件摘要为d4c93358dda898374908f1f1e72bd948159d444b0b74f2b1f56ee10dba3ec22d。历史规则仍要求实际readiness通过后才交单RD实施。历史review本身只读，未运行产品QA或放行gate；无拒绝或不确定动作。

本公共投影不是原receipt，也不把该历史批准绑定到新修订的ADR0025、ADR0026或C/H/M。当前独立reviewer需审查精确公共投影字节；当前publication brief保持review pending与Gate blocked。
