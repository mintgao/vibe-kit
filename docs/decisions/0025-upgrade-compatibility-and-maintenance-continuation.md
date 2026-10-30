# 0025: Bounded payload compatibility checks and controlled upgrade maintenance

- Status: Accepted
- Date: 2026-10-29
- Decision owner: `vibe_tech_lead` author
- Work item: `docs/work-items/20261029-v0-13-local-delivery/brief.md`
- Scope: `scope.md` 的 F1–F4；`acceptance-matrix.md` 的 N01–N36
- Source baseline: `e676446c661e717578b4dd114548cdfecb2b2437`
- Target source version: `0.13.0`

## Context and applicable decisions

本文件是历史已接受本地功能决策的公共投影。原Accepted文件摘要为 d4c93358dda898374908f1f1e72bd948159d444b0b74f2b1f56ee10dba3ec22d；其标头还原Proposed后的全文摘要与[历史最终独立审查](../work-items/20261029-v0-13-local-delivery/technical-review.md#final-review)的approved revision一致。该原件与原收据另行保留。本次仅澄清历史状态、去除特定执行宿主的能力断言并解析公共治理引用，不改变F1–F4语义或N01–N36标准。公共投影字节仍须当前独立审查；本checkout尚未导入0.13实现，新候选的readiness、真实激活、QA和发布验收均不由历史Accepted标头证明。历史范围见[scope](../work-items/20261029-v0-13-local-delivery/scope.md)及[brief](../work-items/20261029-v0-13-local-delivery/brief.md)，当前发布gate见[publication brief](../work-items/20261029-v0-13-publication/brief.md)。

本项按 L 执行：新增项目声明与目标身份比较合同，改变跨工作流的升级维护入口，涉及宿主证据权威、版本兼容、恢复和失败一致性。

ADR0017 保留完整默认检查集合、有效顺序、环境限制和独立 QA；ADR0018 保留结构验证、宿主所有的接管与 custody；ADR0019 保留安装适配器与实际运行宿主的区别及能力诚实；ADR0023 保留 `inspect-run` 的历史证据边界与真实入口验证。既有安装事务及源信任边界继续适用。

现有 `print_plan()` 输出安装动作、冲突和保护信息，不是 postimage API。`validate_source_provenance()` 验证渠道字段并计算 payload 摘要，不认证网络来源。现有 feature/debug/implementation 入口要求升级后默认验证通过才能恢复原工作，因此需要明确的维护分支修复首次 QA 前的已知阻塞；不能把尚未执行的 QA 写成 `verification-failed`。

本次不实现 #21/#24/#25/#26/#30，不新增通用重试器、聚合 CLI、候选谱系、宿主认证协议、custody 状态机或公开发布 profile。

## F1: 可复制、可运行的扩展测试模板

在 `.agents/skills/vibe-implementation-flow/references/extension-testing/` 分发 Python 和 Node 两套模板及说明。verification Skill 引用同一份模板，避免第二份运行时副本。

模板必须包含：

1. 完整合法 default receipt、合法依赖排序和合法 partial 对照；partial 可以结构合法，但不能满足完整默认准入。
2. missing/extra 字段、精确整数版本、检查集合/顺序、coverage、flags、provenance、summary 的逐项变异。
3. 删除未配置检查且同步修改 summary 的反例，明确断言集合层拒绝；summary 另设独立反例。
4. 实际默认 loader/dispatcher 的 origin、参数观测；新 helper 直测成功而真实入口仍加载旧 helper，以及参数错误的反例。
5. 输出语义与完整性两条独立测试轴。
6. doctor 输出不存在和已经生成两种生命周期。

模板调用原始准入 validator，不复制一个较宽松 validator 使测试通过。随包演示使用当前生产 `validate_complete_verify_receipt()`；Python 直接通过有界测试适配器调用，Node 经真实 package script 调用同一个生产 validator 的小型 Python 测试桥。Vibe 本身已有 Python 运行时要求，此桥不引入第三方依赖。桥只返回固定字段路径和加载 origin，不修改 receipt，不构成新的公共 CLI API。项目复制后应接入自己的原始 validator，不能保留演示桥并声称验证了另一个生产入口。

Python focused 使用真实 `unittest discover` 的限定文件选择；Node 使用项目实际 package script 的限定参数。默认与 focused 共用 loader，只改变用例选择；保留历史 caller 与断言。Node runtime 或 dispatcher 不可用时记录 Blocked，不能用替身证明 Node 通过。

语义轴每个变体须明确自己的字节/索引前提：

- absent 只在输出未声明或允许缺席时合法；
- 畸形 JSON、Fail、伪 Pass 若被索引，必须在该变体 setup 中建立相应合法字节摘要；
- 冻结源码/input，禁止通过重建源码身份替输出语义测试遮掩变更；
- 合法 byte/hash/index-only consumer 不因输出语义改变准入；
- 故意根据 inert 输出状态作准入的坏 consumer 必须被捕获；
- 读取、解码、计算摘要本身不构成语义违规。

完整性轴单独制造索引不匹配、缺失索引成员、摘要/模式/执行位错误和未声明路径，保留原 guard 拒绝。模板 setup 与真实 dispatcher 是显式执行，不计入 F2/F3/F4 的只读观察区间。

## F2: 独立、可选的 payload 身份预检

新增命令：

```text
<selected-payload>/bin/vibe check-upgrade-compatibility <target>
  [--source-type <existing-source-type>]
  [--source-ref <existing-exact-ref>]
  [--artifact-sha256 <sha256>]
  [--expected-payload-tree-sha256 <sha256>]
  --format json
```

命令使用所选 target payload 的 CLI。无 `--receipt`、输出文件、诊断 hook、脚本执行、网络、apply、恢复、自动适配或最新版本发现功能。

配置固定为项目所有的 `.vibe/upgrade-compatibility.json`。安装和升级不创建或覆盖该文件；不改 `.vibe/project.yaml` 的既有语法。

配置 schema 1：

```json
{
  "schema_version": 1,
  "enabled": true,
  "rules": [
    {
      "id": "payload-admission",
      "owner": "project-maintainer",
      "kind": "payload-tree-allowlist",
      "allowed_payload_tree_sha256": ["<64 lowercase hex characters>"]
    }
  ]
}
```

准确规则：

- 顶层字段恰为 `schema_version`、`enabled`、`rules`。
- `schema_version` 必须为精确整数 `1`；`enabled` 必须为布尔。
- `rules` 最多 32 项；启用时至少一项。
- `id` 为唯一的 1–64 字符 ASCII identifier，允许字母、数字、点、下划线、连字符。
- `owner` 为固定角色枚举：`project-maintainer`、`vibe-tech-lead`、`vibe-rd`。
- 已支持规则字段恰为四项：`id`、`owner`、`kind`、`allowed_payload_tree_sha256`；允许集为 1–32 个唯一小写 SHA-256。
- 未知字段、重复 JSON key、重复 ID、非法类型/摘要、未知 schema 均为配置错误，不宽松忽略。
- 为区分“合法但超出支持范围”，schema 1 另识别 `composite-candidate`、`merged-file`、`command` 三个保留 kind；它们字段恰为 `id`、`owner`、`kind`、`parameters`。`parameters` 是受资源界限约束的 opaque JSON object，始终不执行、不解引用、不回显；结果固定为 `not-evaluated / unsupported-rule-kind`。
- 其他 kind 为未知配置，不能假定兼容。
- 缺文件或合法 `enabled:false` 返回 `not-configured`，不要求新的 source 参数，不读项目 checks/toolchain，不产生后台状态。

启用时要求 exact source ref 及 `--expected-payload-tree-sha256`。后者由宿主从已选择、已认证的 release/Plugin/local-payload 边界取得；比较本次重新计算的实际 payload 摘要。缺失、损坏或不匹配时不能评估规则。

来源处理保留原渠道字段语义与 payload 算法，但新命令使用独立的有界读取路径。不得调用旧 `validate_source_provenance()` 后再检查，因为该函数会先经旧 source 路径和枚举计算摘要。可提取无 I/O 的字段校验函数供新旧路径共享；旧命令保持原行为，新命令仅使用本决策定义的安全枚举和散列。

来源认证是执行所选 CLI **之前**的宿主责任。可信 release、已认证 Plugin artifact 或明确选择并审阅的 local payload，应已有精确版本和预期 payload 摘要；新命令验证本次读到的 payload 是否与该预期一致。命令不能认证自身加载之前的来源，也不能因 `source_type`、版本、同名文件或摘要相等就证明网络来源可信。其结果始终为 `source_authentication: not-attested`。

Plugin 的新预检入口明确绕过现有 `vibe_from_plugin.py`，直接调用先前已认证、已定位的 bundled payload：

```text
python3 -I -S -B <trusted-plugin-root>/payload/bin/vibe \
  check-upgrade-compatibility <target> \
  --source-type plugin-bundled \
  --source-ref 0.13.0 \
  --expected-payload-tree-sha256 <previously-authenticated-digest> \
  --format json
```

`<trusted-plugin-root>` 与预期摘要来自宿主已完成的授权来源选择/认证，不由预检执行全盘搜索、重新下载或运行旧 wrapper 取得。若这些证据不可用，维护 Agent 停在来源缺口，不调用未经认证的 payload。不能为进入“安全预检”先运行旧 wrapper，再把其读取排除在观察区间之外。

现有 Plugin wrapper 继续服务原有 plan/upgrade/doctor 等操作；这些操作与预检分别记录，不宣称旧 wrapper 获得了本预检的安全读取保证。新预检的实际入口测试必须证明 wrapper 没有执行。新预检不在结束时回调 wrapper，也不通过 wrapper 自动进入后续 plan/apply。

对新命令的只读性计量覆盖其整个调用，包括参数处理、项目/源读取、比较和结果输出；已授权的 Python/CLI 代码加载不构成该命令对来源的认证。此前独立来源认证与此后的 plan/apply 属于各自操作，不能合并为“预检零副作用”证据。

维护 Agent 将两份结果并列呈现：

```text
<selected-payload>/bin/vibe plan upgrade <target> ... --format json
<selected-payload>/bin/vibe check-upgrade-compatibility <target> ... --format json
```

原 plan 提供受管变化、保护范围和冲突；新命令只提供声明规则比较。新结果不能覆盖原 plan conflict，不能被 `upgrade` 当作执行许可或可缓存的放行票据。已声明身份不满足时，维护 Agent 保留 A、推进获授权诊断；安全 plan 仍可能为 safe，不伪造安装 conflict。

**独立 dispatcher。** `main()` 在构造通用 parser、设置 `RECEIPT_CONTEXT` 或进入通用异常处理之前，按 argv 首项精确识别 `check-upgrade-compatibility`，交给专用 parser 和专用结果出口。新路径不能调用 `source_root().resolve()`、`Path.resolve()`、旧 `framework_version()`、旧 payload 枚举或通用 `VibeError` 输出分支。source 根从 `__file__` 的词法绝对位置取得，再按下文固定 descriptor；不是先解析 symlink 再检查。

专用 parser 默认 JSON，仅接受 `--format json`；参数错误也输出下文同一闭合对象，不打印 argparse 的原始错误、参数值或动态 usage。`--help` 可以输出固定帮助文本并 exit 0，不读取项目或 source。未知参数、重复单值选项、缺失 target/选项值及非 JSON format 均映射为 `invalid-arguments`。`--receipt` 不被支持。所有新命令的可处理异常，包括 parser、dispatcher 和读取阶段异常，都由专用出口处理；不得补入 `operation`、`error`、`recovery` 等通用字段或输出 traceback。

无配置路径在完成参数语法、项目根和声明观察后即可返回。source 字段的语义校验及 source payload 读取仅在声明合法且 enabled 时进行；缺文件或合法 disabled 不要求来源字段，也不探测源目录。

## F2 result schema and limits

保留通用 result schema 2。新命令的闭合对象为：

```text
{
  schema_version: 2,
  command: "check-upgrade-compatibility",
  status: "checked" | "not-configured" | "invalid" | "blocked" | "error",
  compatibility: {
    schema_version: 1,
    scope: "payload-identity-only",
    authority: "static-comparison",
    source_authentication: "not-attested",
    project_binding: {
      root_identity_sha256: digest | null,
      declaration_state: "absent" | "disabled" | "enabled" | "invalid" | "unavailable",
      declaration_sha256: digest | null
    },
    source: null | {
      type: "local-payload" | "github-release" | "plugin-bundled" | "offline-bundle",
      ref: validated exact ref,
      artifact_sha256: digest | null,
      payload_tree_sha256: digest,
      expected_payload_tree_sha256: digest
    },
    rules: [{
      index: integer,
      id_sha256: digest,
      owner: "project-maintainer" | "vibe-tech-lead" | "vibe-rd",
      kind: "payload-tree-allowlist" | "composite-candidate" | "merged-file" | "command",
      outcome: "satisfied" | "adaptation-required" | "not-evaluated",
      reason_code: "identity-allowed" | "identity-not-allowed" |
                   "unsupported-rule-kind"
    }],
    findings: [{code: fixed enum, path: fixed logical input path}],
    next_action: null | {
      code: "review-upgrade-plan" | "review-maintenance-adaptation" |
            "resolve-compatibility-input",
      owner: "project-maintainer" | "vibe-tech-lead" | "vibe-rd"
    }
  },
  write_state: "none",
  writes_performed: false
}
```

`digest` 恰为 64 个小写十六进制字符。规则结果保持声明顺序，index 为从 0 开始的位置。ID 只输出摘要，owner 只输出固定角色；不回显任意配置文本。`source.ref` 只能在全部来源校验和稳定性检查完成后输出已验证的 exact ref。

### 固定 findings 和 paths

finding code 恰为以下集合，不保留开放扩展项：

```text
invalid-arguments
invalid-declaration
duplicate-rule-id
unsupported-schema
invalid-source-type
invalid-source-ref
invalid-artifact-sha256
invalid-expected-payload-sha256
invalid-source-version
source-version-mismatch
missing-source-evidence
source-digest-mismatch
unsafe-path
input-unavailable
read-permission-denied
resource-limit
input-changed
unsupported-safety-primitive
execution-interrupted
internal-error
```

`path` 表示逻辑输入位置，不是磁盘路径。它只能是：

```text
$
$.arguments
$.arguments.target
$.arguments.source_type
$.arguments.source_ref
$.arguments.artifact_sha256
$.arguments.expected_payload_tree_sha256
$.project.root
$.source.root
$.source.version
$.source.payload
$.declaration
$.declaration.schema_version
$.declaration.enabled
$.declaration.rules
$.declaration.rules[i]
$.declaration.rules[i].id
$.declaration.rules[i].owner
$.declaration.rules[i].kind
$.declaration.rules[i].parameters
$.declaration.rules[i].allowed_payload_tree_sha256
$.declaration.rules[i].allowed_payload_tree_sha256[j]
```

`i`、`j` 只能为规范十进制 0–31，不带前导零。未知字段归到最近的已知父位置，不能把该字段名插入 path。磁盘成员错误归到 `$.source.payload` 或 `$.declaration`，不能回显成员名称。无原始异常、绝对路径、参数值、命令、parameters 内容或 traceback。

一次 fatal failure 只输出第一个确定 finding；不存在部分接受。正常 checked 和 not-configured 的 findings 为空；不支持的保留 kind 由各规则结果表示，不属于 fatal finding。校验顺序固定为：参数语法、安全原语、项目根、声明、来源字段、source 根/版本、payload 枚举与摘要、预期摘要比较、最终绑定复核、规则结果发布。

### 来源字段、结果和退出规则

启用声明时：

- `source_type` 缺省为 `local-payload`，其他输入必须属于四值枚举。
- `source_ref` 必须提供并满足现有 exact-ref 语法；去除首尾空白后验证。不得把任意路径、分支名或自由文本当 ref。
- `github-release` 与 `offline-bundle` 必须提供 artifact SHA-256。
- `local-payload` 与 `plugin-bundled` 的 artifact SHA-256 必须缺省；显式提供视为 `invalid-artifact-sha256`，遵循现有 takeover source rules。此限制仅属于新命令，不回溯改变旧命令的字段处理。
- 预期 payload SHA-256 必须提供。CLI 的两个摘要参数接受 64 位十六进制并规范为小写；声明允许集仍要求输入本身为小写。
- source `.vibe/core/version` 是必须读取的 regular file，最多 64 bytes；严格 UTF-8，trim 后为现有数字三段版本语法。格式错误为 `invalid-source-version`。
- source ref 若携带 SemVer，必须与实际 source version 相同；commit ref 不虚构版本比较。
- 缺失必须提供的来源参数为 `missing-source-evidence`；已提供但语法错误使用对应 `invalid-*`，不能混为未读取或权限失败。

固定映射：

| 条件/finding | status / exit | next_action.code / owner |
|---|---|---|
| 缺声明或合法 disabled | not-configured / 0 | null |
| 全部规则 satisfied | checked / 0 | review-upgrade-plan / project-maintainer |
| 任一 not-evaluated，包括与 adaptation-required 并存 | checked / 2 | resolve-compatibility-input / vibe-tech-lead |
| 无 not-evaluated，但存在 adaptation-required | checked / 2 | review-maintenance-adaptation / vibe-tech-lead |
| invalid-arguments | invalid / 1 | resolve-compatibility-input / project-maintainer |
| invalid-declaration、duplicate-rule-id、unsupported-schema | invalid / 1 | resolve-compatibility-input / project-maintainer |
| invalid-source-type、invalid-source-ref、invalid-artifact-sha256、invalid-expected-payload-sha256 | invalid / 1 | resolve-compatibility-input / project-maintainer |
| invalid-source-version、source-version-mismatch | invalid / 1 | resolve-compatibility-input / project-maintainer |
| missing-source-evidence、source-digest-mismatch | blocked / 2 | resolve-compatibility-input / project-maintainer |
| unsafe-path、input-unavailable、read-permission-denied | blocked / 2 | resolve-compatibility-input / project-maintainer |
| resource-limit、input-changed、unsupported-safety-primitive | blocked / 2 | resolve-compatibility-input / project-maintainer |
| execution-interrupted、internal-error | error / 2 | resolve-compatibility-input / project-maintainer |

固定 path 对应：

- `invalid-arguments` → `$.arguments`；target 词法错误可用 `$.arguments.target`。
- 来源字段错误和缺失 → 对应 `$.arguments.*`。
- source version 格式/与 ref 不符 → `$.source.version`。
- source digest mismatch → `$.source.payload`。
- 声明错误 → 上述已知声明字段，duplicate ID 指向第二次出现的 `.id`。
- 安全、权限、不可用、限额、漂移 → 正在观察的四个固定范围之一：`$.project.root`、`$.source.root`、`$.declaration`、`$.source.payload`；source version 单独读取时可用 `$.source.version`。
- 中断及未分类内部错误 → `$`。

权限错误 `EACCES/EPERM` 只映射 `read-permission-denied`；不改工具、不提权、不 chmod。确定的 symlink、非 regular 候选、非法路径或特殊节点映射 `unsafe-path`。必要输入缺失和其他无法完成的正常 I/O 映射 `input-unavailable`；未满足安全原语要求映射 `unsupported-safety-primitive`。不把未知 OSError 文本泄露给输出。

fatal failure 时 `source=null`、`rules=[]`，即使之前已计算部分摘要或比较结果也不保留，以免把局部结果误用为放行。`not-configured` 同样为 `source=null`、`rules=[]`。只有 checked 可以携带 source 和完整 rules。

`project_binding` 按实际证据保留：

- 项目根未成功固定并复核，或根/祖先绑定漂移：root digest 为 null，声明状态 unavailable、声明 digest 为 null。
- 项目根稳定且声明确证缺席：状态 absent、声明 digest null。
- 声明完整读取并通过前后稳定性及名称绑定复核：保留实际字节摘要，状态为 disabled、enabled 或 invalid；即使后续来源校验失败，也可保留这个已复核的项目输入事实。
- 声明未读完、超限、权限失败或声明本身漂移：状态 unavailable、声明 digest null。
- 成功固定且复核的项目根可以保留 root digest；但不据此宣称来源可信。
- 发布失败结果前若发现已读取输入或名称绑定发生漂移，最终 finding 使用 `input-changed`，清除受影响绑定；不输出旧规则结果。

解析失败发生于文件读取前，binding 为 null/unavailable/null。异常输出不能走通用 envelope builder 的附加字段分支。输出设施本身中断、进程被强杀或 stdout 不可写时，可能没有完整结果；宿主按“结果缺失”处理，不能拼造 error receipt。命令不得为此另写错误文件或打印原异常。

### 有界读取与枚举

固定预算：

| 对象 | 上限 |
|---|---:|
| 声明字节 | 65,536 |
| 声明 JSON 嵌套深度 | 8 |
| source version 字节 | 64 |
| 单 payload 文件字节 | 8,388,608 |
| payload 文件总字节 | 67,108,864 |
| payload 文件数 | 4,096 |
| source 遍历目录数，含遍历起点 | 1,024 |
| 一轮 source 枚举观察的目录项总数，含最终不选入的项 | 16,384 |
| source 内相对深度 | 32 |
| 单路径组件 UTF-8 字节 | 255 |
| 根路径及单相对路径 UTF-8 字节 | 4,096 |
| 一轮枚举累积保存的相对路径 UTF-8 字节 | 4,194,304 |
| 每条 root 祖先链组件数 | 64 |
| 流式读取 buffer | 65,536 bytes |
| 序列化结果 | 32,768 bytes |

这些限制在读取、递归、append、保存路径或排序**之前**检查；不能先 `list(rglob(...))` 或累积全部路径后才判超限。目录项用 descriptor 相对的有界迭代取得，所有已观察项都计数，包括空目录和不匹配的项。只进入 payload allowlist 所需范围，不扫描 `.git`、无关业务树或宿主目录。

最多两轮有界枚举：初次发现和最终成员复核，每轮独立受同样的目录/节点/路径预算限制；不得无限重扫直到稳定。任何一轮超限即 `resource-limit`。成员摘要只需一轮流式读取；最终复核使用记录的文件/目录签名和成员集合，不能通过无界重读规避预算。

allowlist 与 `release_payload_files()` 一致，但实现从安全 descriptor 出发枚举，不调用其旧路径遍历后补检查。必要的显式路径逐组件打开；只在需要匹配目录项的 allowlist 节点枚举。遇到 unsafe link/type 明确阻塞，不能跟随或悄悄剔除后仍宣称与完整 payload 一致。不存在的可选 allowlist 成员遵循原成员选择语义；缺少必须的 version/CLI 输入仍是缺口。

项目根和 source 根必须：

1. 使用词法绝对路径，拒绝 NUL、无效编码及 `..` 组件；不使用 `resolve()`。相对 target 根据当前工作目录形成绝对词法路径；不能信任未经核对的环境 `PWD`。
2. 从固定 `/` descriptor 逐级打开祖先，目录使用 `O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC`；保留用于名称复核的父 descriptor。
3. 每个组件在打开前、打开后核对 `lstat/fstatat(..., follow_symlinks=False)` 与已打开 fd 的 device/inode/type 一致。
4. 观察结束时再次沿固定父 descriptor 核对每个祖先名称及 project/source 根名称仍绑定同一对象；仅对同一 fd 做 `fstat` 不够。任一名称消失、替换或绑定不同均为 `input-changed`。
5. 捕获根本身的 device/inode/type；后续所有读取从固定根 descriptor 派生。不要重新从字符串路径开成员。

declaration、version 和 payload 叶子均使用 `O_RDONLY|O_NONBLOCK|O_NOFOLLOW|O_CLOEXEC`，打开前检查已观察类型，打开后立即 `fstat` 确认 regular file 与名称身份，再读取。`O_NONBLOCK` 防止检查与打开之间变成 FIFO 时挂起；非 regular 一律不读。必要 flag、fd-relative API 或 no-follow 能力缺失时 blocked，不退回普通 open。

读取前、读取后及最终复核比较成员 device/inode/type/mode/size/mtime/ctime；不比较会被自身读取改变的 atime。成员的每级父目录名称也必须仍绑定原对象。遍历过的 source 目录记录成员集合及相应稳定性签名，最终复核成员集合、目录绑定和文件签名，发现新增、删除、替换或变化即 `input-changed`。祖先绑定只比较身份和类型，不因 `/Users` 等祖先的无关 mtime 改动制造漂移。

缺声明的轻量路径也须复核缺席：若 `.vibe` 或声明叶子缺失，保留最近已存在父目录的固定绑定，在返回前确认缺失组件仍不存在。不能第一次 stat 缺失后直接放行而漏掉观察中出现的声明。

严格 JSON 在受字节上限保护的缓冲中解析，拒绝 duplicate keys、非有限数字；解析递归/深度超限映射 `resource-limit`，不得将 Python traceback 暴露出来。结果在内存中完整序列化并检查字节上限后一次输出；超限返回固定、小型 `resource-limit` 结果，而不是截断 JSON。

`root_identity_sha256` 由规范词法路径及固定 root 的 device/inode 作规范 JSON 摘要，不输出路径。它是输入关联标识，不是来源认证。上述检查检测观察窗口内可见的路径/内容漂移，不构成跨命令锁，也不保证抵御同 OS principal 的恶意伪造。每次维护重新读取声明/目标；安装前另核来源、声明及 plan，安装结果实际 source 不同则停止推进。

## F2: 受控维护分支

业务恢复入口仍要求完整接管条件。新增维护分支专用于本次升级的兼容诊断、精确身份认可或必要 API adapter，不能用它继续原业务。

安装前：

- A 未变，允许已授权只读诊断与方案。
- B 只发生身份变化，需要消费合同及区分性 focused 证据，不能凭哈希差推出接口破坏。
- B′ 有真实参数/字段/语义差异，需要反例和最小 adapter。
- 信息不足保持 `not-evaluated/Blocked`。
- 如需先修改项目，由 A 已激活规则下的独立维护工作项经过适用 gate 实施、验收；不得假装 B 已激活。

安装后的共享代码维修要求同时成立：

1. 宿主已按现有合同确认实际 B 激活；结构 valid、doctor healthy 或 Agent 自报不够。
2. 安装状态已确证，active transaction 不存在；不能跨越 recovery/unknown。
3. 原业务暂停，维护范围和所需操作已有授权。
4. 维护工作项完成适用 readiness；本场景的高风险合同改动须独立技术 review。
5. orchestrator 确认 gate，并有一位 RD writer。
6. 改动所有权、精确前态、预期后态、撤销边界可核对。
7. 原 guard、冻结源码/input、历史断言、检查集合、顺序、预算和验收强度不降低。

首次 default QA 前发现已知阻塞，先完成以上维修门槛，不为制造失败先跑完整 QA。实际 QA 失败则保留原 receipt 和失败原因，进入同一维修门槛。onboarding 仅更新事实，不能代替修复授权或 readiness。

精确认可 B 时只加入受审 B；C 仍被拒绝。API adapter 只修改受审拥有范围，不以删除断言、宽泛放行、跳检查或增预算“修复”兼容。

完成维修后重新核对 context 和目标 doctor，由独立 QA 对最终候选执行完整默认验证。只有所有接管条件满足才重新评估原业务。

## Minimal takeover protocol change

保留 takeover schema 2 的字段、九阶段、stage 依赖、custody 和 ready invariants。

新增唯一 reason/action 配对：

```text
reason: maintenance-required
stage: verified
action: review-maintenance-adaptation
```

表示：此前适用阶段已满足，但完整默认验证尚未进行，存在已定位的维护阻塞。`verified` 为 blocked，后续阶段 not-started；不能放入不存在的 verify receipt。诊断、授权和维护工作项证据在宿主维护上下文及项目工作项中引用，不伪装为 `verify-receipt`。

真实默认失败仍使用原 `verification-failed` 等 reason，保留真实 receipt。若更早阶段仍阻塞，接管对象只记录最早阻塞阶段；维护视图可指出其后的缺口，不能制造多个 blocked stage 或越序提升。

Agent-install protocol **4→5**，显式版本化这一新增词汇和维护行为；schema 保持 **4**，既有层级字段没有改变。旧 protocol 4 的宿主不得解释新 reason；它仍可在原语义下处理旧对象，未知合同须失败关闭。新 validator 不把旧目标身份改写成当前目标；历史对象仍依其原安装的认证合同解释。

同步更新：

- 编译 reason/action/stage registry；
- `agent-install.json` registry 镜像及 `cli.check_upgrade_compatibility` 的闭合 schema-1 声明；
- `.vibe/core/protocol.json`；
- `AGENT_INSTALL.md`；
- 相关 Skills、managed AGENTS 和 Plugin maintenance。

新增命令独立版本化，不给旧 verify、plan、doctor、inspect-run envelope 偷加字段。verify/execution/inspection、activation、manifest、transaction schema 保持原值；core protocol 7、Codex adapter 7、Hermes adapter 1 保持，宿主能力声明不提升。

## F3: 固定栏目只读投影

交付 `.vibe/core/upgrade-maintenance.md` 作为受管的统一规范，AGENT_INSTALL 与受影响 Skills/Plugin 指向它。它包含固定栏目、证据选择顺序、完整正负示例和场景 runbook，不增加聚合 CLI 或运行时状态库。

固定栏目为：

| 栏目 | 内容 |
|---|---|
| 目标与安装事实 | A/B、源证据、apply/doctor、事务是否已确证 |
| 阶段 | installed/upgraded、结构验证、activation、adaptation、verification、re-evaluation 各自事实 |
| 证据与缺口 | 引用来源、缺失/过期/冲突及具体绑定问题 |
| Owner | 角色名，不输出私有 task ID |
| 一个下一动作 | 由最早阻塞决定的唯一安全动作 |

宿主优先消费当前任务边界内的原证据；文件 receipt 通过已有规则读取。`validate-takeover` 只提供结构结论；`inspect-run` 只提供历史执行结论；正向 activation 只消费宿主实际认证结论。无认证时不得提升。

投影限制：最多九个阶段，最多两个必要引用/阶段，固定术语和角色，最多 8 KiB。不得复制 takeover JSON、goal、custody、task ID、原始日志/异常或私有绝对路径。必要非秘密工作项引用可公开；原 receipt 继续按既有私有边界保管。超限保留最早阻塞、owner 和下一动作，并注明省略；不截断成“全部通过”。

缺引用、不支持版本、冲突、错目标、旧 task、同名文件或无证明 reload，保持缺口，不自动裁定为新版事实。无真实 activation 时按既有 manual fallback 给“同项目新建任务”一个动作。已激活但缺匹配完整 QA 时显示 verification pending。

## F4: 升级维护的读回与恢复

同一维护指南提供固定操作表：

```text
action / target / authorization scope / operation correlation /
before evidence / expected after evidence / observed evidence /
certainty / actual reason / owner / one next action
```

它是宿主操作证据的受限表达，不是新事务或 exactly-once 协议。operation ID 仅作关联，不能证明执行。

只读观察范围限于安装事务、本次自有 adapter 文件和原 QA run。观察后：

- 创建前失败须有强证据才判 `not-executed`。
- 丢失回执先 `unknown`，不能据连接恢复推断成功或未执行。
- 两文件部分完成须逐项读回；已落地项不重做。
- 补缺项必须仍在原授权 scope 内、确证尚未落地、精确前态相符且无冲突。旧行匹配失败保留其真实原因。
- 前后态均不匹配、跨项目/旧操作身份、无可靠 probe 或观察中断保持 Blocked。
- denied 停止该动作；原授权、重连、换工具不构成重试依据。只有新的相关授权/证据才按实际权限边界重新判断。
- QA 断连读原 run/receipt；原工作负载 spawnCount 保持 1。只读 CLI/probe 启动另计。running 不证明活性，finished 不证明 Pass。
- 成功/失败原 receipt 不重写；没有最终 receipt 不从日志拼造。

`recover-upgrade` 保留现有语义：

- 未 apply：保留 A，不能称回滚成功。
- rolled-back：证明前态恢复后重新 plan。
- recovery-required：依原授权执行一次既有恢复，再判断准确结果。
- unknown-partial/漂移：先检查，禁止自动覆盖。
- active 存在时不 ordinary upgrade、handoff、activate、adapt 或 verify。
- committed：恢复只能完成事务清理；不能降级。
- 无 active：已有命令返回 blocked，不能把它当撤销 API。
- `inspect-upgrade-transaction` 是 action code，不是 CLI。

项目 adapter 撤销仅覆盖已有授权且现态精确匹配的自身改动，不 reset 目录、不覆盖用户变更。B 仍安装而撤销后 guard 只接受 A，状态仍 blocked；重新核对安装与项目准入，不能宣布恢复 A 或 ready。安装事务不覆盖项目任意代码、数据和外部副作用。

## Version, distribution and affected files

当前 source candidate 改为 0.13.0；不写 source checkout 的 `.vibe/manifest.json`、`.vibe/version` 来制造 installed healthy。

最小切面：

| 路径 | 改动 |
|---|---|
| `bin/vibe` | 新只读命令/安全 reader/声明校验；新 reason/action；版本和镜像校验 |
| `agent-install.json`, `AGENT_INSTALL.md`, `.vibe/core/protocol.json` | protocol 5、registry、预检声明、维护分支及证据边界 |
| `.vibe/core/upgrade-maintenance.md` | F2/F3/F4 统一规范、表格、场景 runbook |
| managed `AGENTS.md` | 业务恢复与维护入口的准确区分 |
| feature/debug/implementation Skills | 引用维护分支，不再形成修 QA 前须 QA 成功的循环 |
| onboarding Skill | 明确事实刷新不豁免维修 gate；最终 QA 可复用 |
| verification Skill | QA 所有权、候选绑定、原 run 读回、一次运行双门槛 |
| implementation references | F1 Python/Node 模板 |
| `distribution/plugin-src/vibe-kit/skills/vibe-maintain/SKILL.md` | 0.13 入口、已认证 payload 的预检直达调用、maintenance 路由及同一停止条件；不通过旧 wrapper 执行预检 |
| 当前版本/Plugin metadata/README/CHANGELOG/0.13 本地 release notes | 准确描述未发布 candidate、版本与能力限制 |
| `tests/test_upgrade_compatibility.py`, `tests/test_extension_testing.py`, `tests/test_upgrade_maintenance.py` | 新 focused 场景 |
| 既有 workflow/CLI/host/release tests | 受影响闭合合同与分发回归 |

bootstrap Plugin 不增加任务创建/reload 能力。既有 wrapper 继续负责原有操作的 bundled identity 检查；`check-upgrade-compatibility` 按 F2 指定的已认证 payload 直达入口执行，不经过该 wrapper。Plugin Skill 必须给出这条准确调用路径和来源证据前置；不能让新命令的文档与实际入口分离。

maintenance bridge 保持 schema 2；predecessor protocol 支持集合增为 `[0,1,2,3,4]`，上界移为 `<0.13.0`，目标 Agent-install schema/protocol 为 4/5。同版本 0.13 重复操作使用当前合同路径，不错误套用严格 predecessor 上界。升级源码当前存在的 `version == "0.12.0"` migration 目标判断与官方 v0.5 target registry 一并移到 0.13，重算相关摘要和镜像，不改变官方 predecessor bytes 或放宽资格。

AGENT_INSTALL 现存桥接文字仍写 schema/protocol 3、0.7 范围，应按实际 0.13 机器合同修正，不能继续保留旧 prose。

publication schema 1–7、closeout schema 1–5 的历史 profile 全部冻结；本项不新增 0.13 发布 profile，不运行远端操作。package/validate-release 可作为本地 focused 分发检查，产物保留在 `.vibe/local/v013/`。

## Verification and actual host evidence

独立复审发现的专门 focused 用例：

- Plugin 正常入口实际直达 bundled CLI；把旧 wrapper 设为一旦执行就失败的测试 sentinel，仍可完成预检。分别记录来源认证准备与预检观察，不能靠缩短观察窗口藏起 wrapper 读取。
- 新命令经真实 `main()` 执行；为旧 `source_root`、旧 provenance/payload 枚举、通用错误输出设置禁止调用断言，覆盖成功、无配置、解析失败和读取失败。
- 空目录/不匹配项数量、深度、单路径和累积路径字节越界，在累积/排序前终止；两个枚举阶段分别覆盖。
- symlink/特殊文件/FIFO 及类型切换；用受控故障注入确认非阻塞打开和 fixed finding，不能让测试无限等待。
- project/source 根或祖先目录在观察中被改名并原名替换，即使原 fd 可继续读，也必须检测为 `input-changed`；声明叶子和 payload 父目录替换同样覆盖。
- 缺声明观察中插入文件，不能返回稳定 absent。
- 全部 finding/status/exit/action/owner/path 映射逐表测试；每类 fatal failure 的 `source=null`、`rules=[]`；根/声明绑定保留或清除符合准确证据。
- 错误 argv、source type/ref/version/digest、unknown key、原异常、秘密 canary、私有路径均不泄漏；所有错误只含同一闭合字段集合，没有 `operation/error/recovery`。

上述是本项安全输入和分发合同的必要 focused 验证，不增加源候选完整 default QA 预跑。

所有新临时目录、fixture、cache、bytecode、receipt、日志位于工作项允许的 `.vibe/local/v013/`，按执行 brief 使用进程级环境，不写系统临时目录。

分三层记录：

1. 文档/静态合同：闭合字段、registry、版本镜像和规则引用。
2. 真实 CLI/dispatcher：实际 Python/Node fixture，真实入口、预检、安装、doctor、reader、恢复和故障注入。
3. 真实宿主/Agent：已加载目标规则的任务实际按规则停止、诊断、维修或继续；正向 activation 要求真实绑定证据。

`tests/fake_takeover_host.py` 明确是 `controlled-fixture`，继续用于第 1/2 层，不能满足 N20。

N20 runbook 对 Python 和 Node 各要求：

- fixture 的 canonical root、A/B source identity、完整 apply/doctor 证据；
- 真实 source task 结束位置；
- **在该 fixture 同一 canonical root 启动的真实后继 task**，其创建/项目关联由宿主实际记录；
- 后继独立重算 manifest 与实际 activation set，读取实际受管规则；宿主依既有 manual contract 判断 `manual-task-start`，再调用真实 installed validator；
- 只在宿主边界保存真实 task/receipt/custody，项目记录角色、证据等级、摘要和结果；
- 正向接续与旧任务/错目录/错目标/伪 reload 反例分开。

宿主能力必须针对实际执行环境和冻结目标核实；工具存在、历史可行性说明或共享另一根目录的 collaboration 子 Agent 均不能证明双 fixture 的后继绑定。N20 与 N18 的真实后继部分始终要求上述实际证据；没有可用且已证实的同根真实任务路径时，相应验收保持 Blocked。

先准备并冻结 Python、Node 两个 fixture，再由实际宿主在各自 canonical root 建立并读回真正后继的任务开始/目录绑定，执行上述 N20 runbook。任务创建或能力声明不等于 activation receipt，也不等于 N20 通过。结果不确定先读回；创建或绑定失败时记录确切动作、目标、原因及结果确定性，不合成 receipt，不让旧源任务越过 STOP，也不另扩宿主操控方案。

最终 QA 绑定同一候选的源码/工具/配置、实际 target、QA role、完整 default/all-configured、所有 configured checks、目标 doctor、有效 receipt 和宿主 applicability。候选绑定用现有项目证据和人工记录，不新增 #21 descriptor。一次实际完整运行同时满足维修和接管条件时共引同一 receipt。不同 fixture/candidate 的专项验证不是源候选重复 QA；源码最终完整默认验证由独立 QA 执行一次。变更、失败、无效证据或独立 gate 的重跑必须记录理由。

## Acceptance mapping

| AC | 最低实现与证据 |
|---|---|
| N01 | 两套模板调用生产 validator；完整/排序/partial 对照 |
| N02 | 固定字段层反例；删未配置项并同步 summary 仍命中 checks |
| N03 | 真实 discovery/package dispatcher 的 origin、参数与历史断言 |
| N04 | 同源码/input 的合法 inert 语义变体、好坏 consumer 对照 |
| N05 | 独立完整性变异及原 guard 拒绝 |
| N06 | doctor 输出存在/不存在、focused/default loader 生命周期 |
| N07 | A-only/B 的真实比较；维护视图并列原 plan 变化/保护范围 |
| N08 | B/有限集允许、稳定重复、原 conflict 不消失 |
| N09 | 无配置/disabled/旧 requires 零新增要求与状态 |
| N10 | malformed 与 reserved unsupported 明确分开，无 hook |
| N11 | 声明/source/root 漂移重新诊断；不缓存旧放行 |
| N12 | no-follow/权限/限额/缺输入具体失败且零写 |
| N13 | B 身份差、B′合同差、信息不足三组区分性证据 |
| N14 | 原授权/无授权/材料变化；保留 A 且维护 owner/动作准确 |
| N15 | 首次 QA 前 maintenance-required 与真实失败两入口；缺门槛反例 |
| N16 | 只认可受审 B、C 拒绝、最小 adapter、guard 强度与前后态 |
| N17 | 独立最终 QA+doctor；partial/旧候选/失败不释放业务 |
| N18 | 双 fixture 完整维护链；静态、CLI、真实后继分别记结果 |
| N19 | apply+doctor+valid 仍 activation pending；源任务无适配写 |
| N20 | 双 fixture 同根真后继、实际目标内容与宿主认证来源；历史能力陈述不代替实际激活，缺证据保持 Blocked |
| N21 | 错目标/目录/版本/旧任务/伪 reload 不能提升 |
| N22 | 原 run 历史结论与当前完整 QA applicability 分开 |
| N23 | 缺引用/未知版本/冲突/manual-only/敏感信息投影限制 |
| N24 | 创建前失败、写后丢回执、真实失败、denied 的不同处置 |
| N25 | 两文件逐项读回；仅授权、精确前态的缺项补写 |
| N26 | 同 QA run 回读，原 workload spawnCount=1，失败 bytes 保留 |
| N27 | 旧/跨项目 identity、漂移、无 probe 保持 unknown/Blocked |
| N28 | 既有事务各状态、committed 清理、无 active、非降级 |
| N29 | 精确自身 adapter 撤销；B 仍不准入不能 ready |
| N30 | 真 Python/Node dispatcher、Python 3.9、标准库、无配置 |
| N31 | 旧 envelope/registry/profile 的原版本语义及新 protocol 5 |
| N32 | 三个 reader 区间前后字节/模式快照与副作用计数 |
| N33 | 合成秘密/path/指令/goal canary、限额与固定错误回显 |
| N34 | 三层证据等级；无 live 不声明模型遵循或效率收益 |
| N35 | source/installed/Plugin/Skills/registry 分发一致 |
| N36 | 独立 QA、最终候选、一次默认运行共引及有理由重跑 |

## Alternatives and remaining gate

未采用：

- 在 `plan` 中预测任意合并 postimage：现有 API 无此保证，扩大 #28 范围。
- 执行声明的 diagnostic/compatibility hook：产生新执行与权限边界，超出本轮。
- 新聚合 CLI 或仓库 takeover 文件：重复宿主状态、增加隐私及认证误读。
- 为维修先制造一次失败 QA：浪费且歪曲真实状态。
- 通用恢复引擎或整批重放：不能可靠证明未执行，扩大 #32。
- 合成后继收据满足 live AC：不能证明实际宿主绑定与规则激活。

本地阶段的独立技术复审已批准上述语义，随后决策被接受；历史初轮问题、最终批准版本与标头转换事实见[technical-review.md#final-review](../work-items/20261029-v0-13-local-delivery/technical-review.md#final-review)，历史授权/readiness记录见[brief](../work-items/20261029-v0-13-local-delivery/brief.md)。这纠正了原Accepted标头与尚称Proposed的收尾文字，不把技术批准变成产品QA或真实N20证据。

当前公共投影和后续发布候选仍需不同Tech Lead审查精确字节，并由orchestrator完成适用readiness和实际校验。审查须保留：预检仅身份比较、protocol 5与旧对象解释、无首次QA循环、reader安全/资源边界、维护写入与只读观察分离、真实后继不可伪造、原guard和一次最终QA。新C/H/M的实现、全部36项验收、隐私、实际目标激活与独立QA不能继承历史状态；当前放行只由新的[publication brief](../work-items/20261029-v0-13-publication/brief.md)管理，仍为blocked。
