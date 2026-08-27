# Verification: Continuous Vibe Kit feedback

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | AGENTS、operating model 与 Skill 将 M/L Close 的归因检查设为静默；临时项目正常 `doctor` 后未生成反馈目录。 | Pass |
| AC-2 | 实际 draft 的 `report.json` 包含结构化信号、环境、隐私、fingerprint 与证据字段。 | Pass |
| AC-3 | fake `gh` 监控下，draft/list/review/dismiss 均无远端调用；`.vibe/local/.gitignore` 排除 report/state/preview。 | Pass |
| AC-4 | 路径、项目名、邮件、URL、电话会泛化；11 类 synthetic credential 均返回 2，且无新增候选。 | Pass |
| AC-5 | 回归与独立补测覆盖复用、occurrence、dismiss、同级抑制、新证据或提级再浮现及跨项目稳定 fingerprint。 | Pass |
| AC-6 | 独立重算 canonical SHA-256 与 review hash 一致；repo/body 变化会使旧 hash 在调用 `gh` 前失效。 | Pass |
| AC-7 | 缺 repo、缺 `gh`、未认证、缺失或过期 confirm 均不进入 Issue create，退出 2并保留候选。 | Pass |
| AC-8 | fake GitHub 首次只创建一次；重复提交和“远端已创建但本地收到超时”重试均先按 fingerprint 命中原 Issue。 | Pass |
| AC-9 | README、AGENTS、operating model、quality gate、Skill 与 ADR 0003 一致声明 local-first、non-blocking、逐 payload 授权。 | Pass |
| AC-10 | 本仓库生成 `fb-20260827t061236z-07722c1f`，记录历史 release fixture 风险；无目标 repo 时仅本地 review，明确不触网。 | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `python3 -m py_compile bin/vibe tests/test_cli.py` | Pass | CLI 与测试语法有效。 |
| `python3 -m unittest discover -s tests -v` | Pass | 12/12。 |
| `/usr/bin/python3 -m unittest discover -s tests -v` | Pass | Python 3.9 兼容运行，12/12。 |
| Skill quick validation | Pass | `vibe-feedback-flow` metadata 与目录有效。 |
| `./bin/vibe upgrade .` then `doctor .` | Pass | Self-upgrade 到 0.3.0；版本完整，0 warnings。 |

## Manual scenarios

- 无信号的正常业务问题保持静默。
- 高置信框架缺口生成本地候选并完整 review；缺 repo 时不索要提交授权。
- secret 输入在创建状态目录前被拒绝。
- 用户仅授权一个 report/repo/hash 时，其他候选及变化后的 payload 均不能提交。

## Limitations and follow-ups

- 未访问真实 GitHub；远端协议以 fake `gh` 验证。真实权限、限流和搜索一致性需在选定中央仓库后做发布前 smoke test。
- 当前没有中央反馈仓库，恢复动作是：选择 `owner/repository`，修复 `gh auth`，重新 `feedback review --repo ...` 获取精确 hash，再逐条授权提交。
- “无信号静默”依赖 Agent 遵循仓库指令；没有引入确定性 runtime hook，以避免所有任务都被阻塞或自动遥测。
