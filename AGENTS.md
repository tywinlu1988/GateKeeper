# AGENTS.md — Gatekeeper 跨 CLI 通用入口

**项目**：Gatekeeper（科创板 Pre-IPO 外部视角推演引擎）
**版本**：v0.4.0
**一句话**：为科创板 IPO 保荐承销机构提供 Pre-IPO 投资人、上市后买方、舆论三个外部视角的结构化风险推演。

> 任何 agent CLI 都从这里开始：先读你的 instructions file，再读当前任务对应的 SKILL.md。

## 技能索引

| 技能 | 用途 | 路径 |
|------|------|------|
| ipo-router | 项目状态评估 → 分析计划单生成。不做分析 | .claude/skills/ipo-router/SKILL.md |
| industry-scanner | 节点1：行业/业务定位三角色推演 | .claude/skills/industry-scanner/SKILL.md |
| tech-scanner | 节点2：技术/知识产权三角色推演 | .claude/skills/tech-scanner/SKILL.md |
| finance-scanner | 节点3：财务合规三角色推演 | .claude/skills/finance-scanner/SKILL.md |
| pricing-scanner | 节点4：定价/发行三角色推演 | .claude/skills/pricing-scanner/SKILL.md |

## 四节点管道

```
ipo-router → industry-scanner → tech-scanner → finance-scanner → pricing-scanner
     │              │               │               │                │
 分析计划单     行业风险矩阵    技术风险矩阵     财务风险矩阵      定价风险矩阵
                 + 节点制品      + 节点制品       + 节点制品        + 节点制品
```

### 链式调用规则

1. ipo-router 产出分析计划单后，按 plan.mode 决定执行链路
2. full-chain / pricing-focused：按节点顺序自动衔接，不等待用户确认
3. quick-scan：industry 和 tech 节点并行执行，参见 references/analysis-registry.md 并行协调规则
4. targeted-update：Router 路由到指定节点后执行
5. 每个节点产出后立即移交下游（如链路中有下一节点）

## 非协商条款（所有 agent、所有 CLI、所有请求强制生效）

1. Router 禁止做分析。只做项目状态评估 → 分析计划单 → 移交节点。
2. 禁止跳过分析计划单。无 analysis_plan (YAML)，下游节点禁止启动。
3. 未知状态默认为 full-chain，不猜测用户意图。
4. 超范围请求明确拒绝，不尝试"帮忙做一点"。
5. 禁止分析计划单未覆盖的节点被触发。
6. 数值判断必须有搜索结果或用户提供的材料作为依据。
7. 角色禁止视角切换（买方不替 Pre-IPO 投资人说话，舆论不帮企业公关）。
8. 禁止生成包含外部依赖的交付物（关键数据必须内联摘要、禁止本地绝对路径）。
9. 制品传递必须使用注册表定义的 schema（references/artifact-schemas.md），不得自创字段。
10. 分析路径唯一事实源为 references/analysis-registry.md——不得在 skill 文件中重复定义路径规则。
11. 数值论断必须锚定数据所属期（data_as_of）。市场环境类数据时效 ≤ 6 个月，禁止以抓取时间冒充数据所属期，禁止凭记忆输出市场统计。

## 单一事实源

- 分析路径定义：`references/analysis-registry.md`
- 制品 schema 定义：`references/artifact-schemas.md`
- 角色定义：`references/roles/*.md`
- 质量门禁定义：`references/guardrails/quality-gates.md`
- 降级策略定义：`references/guardrails/degradation-paths.md`
- 跨维度传染矩阵：`references/contagion-matrix.md`（C1-C9，含叠加规则§6）
- 前瞻信号监测框架：`references/signal-watchlist.md`（含优先级矩阵§3.6、逆转信号§3.7、执行力代理§3.8）
- 输出模板（Markdown）：`references/templates/risk-matrix-template.md`
- 输出模板（HTML）：`references/templates/risk-matrix-template.html`（自包含，内联 CSS）

所有 skill 文件引用以上文档，不自行定义路径、schema、角色、门禁。

## 知识库（基准库）

`knowledge/` 为内建基准库——搜索失败或数据时效不足（D1/D4 降级）时的兜底依据。使用规则见 `knowledge/README.md`。子目录：
- `industry-benchmarks/` — 新股发行环境基准、可比估值快照方法与实例（基准日期 2026-08）
- `policy-tracker/` — IPO 审核/现场检查统计基准（基准日期 2026-08）
- `case-library/` — 历史 IPO 案例库（待填充）
