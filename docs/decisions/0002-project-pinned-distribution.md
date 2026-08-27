# 0002: Use channel-neutral releases with project-pinned installations

- Status: Accepted
- Date: 2026-08-27

## Decision

Vibe Kit 的 canonical source 生成不可变 release payload，再通过 GitHub Release、Codex Plugin、私有 marketplace、离线包或其他 Agent adapter 分发。所有渠道最终调用同一项目安装器，把明确版本的 core 与宿主 adapter 写入业务仓库。

业务仓库中的 managed files、manifest 和 installed version 是执行时事实来源。个人、主机或 Plugin 级安装只负责发现、获取和 materialize，不覆盖项目固定版本。

平台中立 core 只维护一份。Codex 和其他宿主的入口文件、Skills 布局与自定义 Agent 配置是由 release pipeline 生成并单独验证的 adapter。宿主缺少某项能力时，adapter 必须声明降级，而不是改变核心质量契约。

## Rationale

- 项目固定使协作者、CI 和新主机能够复现同一套开发行为。
- 渠道中立让用户可以从 Plugin 获得便捷体验，也可以在离线或受控环境使用 release bundle。
- 生成式 adapter 降低跨 Agent 复制规则产生语义漂移的风险。
- resolver 与 installer 分离后，网络、身份和 registry 变化不会进入业务仓库写入事务。

## Consequences

- 发布系统必须从一个 tag 构建并交叉校验所有渠道制品。
- manifest 未来需要记录来源和 artifact digest，并为 schema/core/adapter 分别建模兼容性。
- Plugin 是推荐的 Codex 分发入口，但不能成为项目唯一依赖。
- Plugin 首版只提供唯一命名的 bootstrap/maintain Skills，不复制项目内同名运行时 Skills，也不引入 MCP 或 hooks。
- 新增一个 Agent adapter 需要 conformance evidence，不只是复制 Markdown 文件。
- v0.2 不实现该分发系统；v0.3 从可复现 release bundle 开始落地。

## Recovery

- 项目级 managed changes 通过 Git revert 恢复。
- schema migration 前保存 Vibe Kit 安装状态快照。
- 使用旧版本的可信 payload 进行受控回退；禁止直接修改版本字段绕过诊断。
