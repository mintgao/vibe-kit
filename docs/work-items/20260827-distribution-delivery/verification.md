# Verification: Release-ready Vibe Kit distribution

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | `test_plan_is_read_only_for_init_adopt_upgrade_and_conflict` 与独立制品验收覆盖 safe/blocked plan、目标快照零变化及后续执行集合。 | Pass |
| AC-2 | Python 3.9 独立重建与最终 dist 逐字节等价：release `806c8b...06c31`，Plugin `ab7b9c...c907c`；自动化双构建相同。 | Pass |
| AC-3 | 最终 `validate-release` 核对 kit/schema/core/adapter/runtime/source/artifacts/payload/marketplace；`SHA256SUMS` 精确覆盖所有传输文件。 | Pass |
| AC-4 | 从 release ZIP 离线执行 init/adopt/synthetic upgrade/doctor/verify/feedback，必要 runtime、模板和说明共 29 个 payload 文件。 | Pass |
| AC-5 | 官方 `validate_plugin.py` 与两个 Skill validator 在解包制品上通过；仅有 bootstrap/maintain，无 MCP/hooks/apps，bundled payload 与 release 相同。 | Pass |
| AC-6 | 聚焦回归证明 checksum tamper、unsafe path、Plugin version/payload/channel drift 被拒绝；实现也禁止 symlink/encrypted/oversized entries 和 forbidden capabilities。 | Pass |
| AC-7 | artifact-based init/adopt、0.2 synthetic fixture→0.3、冲突候选与 managed/version/manifest 原子性均通过；成功后 doctor 通过。 | Pass |
| AC-8 | Plugin wrapper 完成离线 plan/init，安装 manifest 的 managed hashes 与 release 安装逐项一致；独立 QA 以最终 Plugin SHA 等价重建复核。 | Pass |
| AC-9 | README、0.3.0 release notes、ADRs 0004/0005 与 manifest 一致声明本地/Plugin/GitHub 路径、支持矩阵、回滚和 unpublished 边界。 | Pass |
| AC-10 | 独立 QA 只使用最终制品或与最终 SHA 等价的临时重建，未编辑仓库、联网或全局安装 Plugin，并最终签署 Pass。 | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `./bin/vibe verify .` | Pass | 15/15 tests。 |
| Python 3.9 full suite | Pass | 15/15 tests。 |
| `./bin/vibe validate-release dist/vibe-kit-0.3.0` | Pass | 0.3.0、29 payload files、no network。 |
| Official Plugin validator | Pass | source 与最终 expanded Plugin 均通过。 |
| Skill quick validators | Pass | source 与最终 bootstrap/maintain 均通过。 |
| Independent focused matrix | Pass | 3/3 release/plan/tamper tests，Python 3.9，最终 ZIP SHA parity。 |

## Manual scenarios

- 新项目：final release `plan init` → `init` → project `doctor`。
- 开发中项目：`plan adopt` → 保留任意业务字节 → `adopt` → `doctor`/onboarding handoff。
- 升级：0.2 synthetic fixture → release `plan upgrade` → `upgrade` → 0.3 `doctor`。
- 冲突：plan blocked 且零写入；真实 upgrade 只产生 incoming review candidates，managed/state 保持旧版本。
- Plugin：bundled wrapper 离线安装；与 release install 的 managed hashes 一致。
- 篡改：checksum、危险路径、版本/Plugin/channel drift 均拒绝。

## Limitations and follow-ups

- 当前是 `release-candidate-unpublished`；没有 Git commit/tag/remote、发布身份、许可证或有效 `gh`，所以没有创建 GitHub Release 或公共 marketplace。
- macOS 和 Python 3.9 已执行；Linux 是公开 stable 前的 CI gate，Windows 未声明支持。
- 0.2 fixture 是合成协议 fixture，不是历史发布 artifact；首个可保留、可比较的真实制品从本次 0.3.0 candidate 开始。
- SHA-256 不证明发布者身份；公开发布前仍需决定签名/provenance。
- 未做全局 Plugin 安装，以免修改用户主机配置；Plugin archive、expanded marketplace、wrapper 和官方 schema 已在隔离环境验证。
