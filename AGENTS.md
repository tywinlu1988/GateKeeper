# AGENTS.md — Gatekeeper 跨 CLI 通用入口

**项目**：Gatekeeper（拟 IPO 标的事前调研推演引擎）
**版本**：v0.8.7
**一句话**：对拟 IPO 标的进行事前外部视角调研推演，产出内核风险清单与发行定价备忘录（附督导期监控表）。核心价值在发行/上市之前的预测；分析透镜是三角色；决策标准符合投资人与股票市场第一性。

## 定位原则（2026-08-17 定位修订）

1. **事前预测是唯一核心价值**。本项目的价值在标的发行/上市之前的调研推演；事后"调整观测"没有决策价值——天气预报不能在下雨后才修正观测数据。
2. **禁止逐案例持续追踪**。个案事后跟进样本偏差过大，不构成方法论改进依据。case-library 仅作引擎回归测试基准（RED-GREEN），不新增追踪型案例。
3. **事后数据仅以队列级形式回流**。方法论校准依赖全量 cohort 统计（基准库：全市场破发率/审核统计/可比估值），而非单一企业的事后表现。
4. **督导期监控为附属能力**。monitoring-run 保留可用，但不属于核心定位，暂缓投入——事前预测可靠性（可评分、可校准）未建立前，不扩展服务覆盖。
5. **机制准入门槛（v0.7.0）**。任何新机制提案必须回答"它防的是哪一次真实观察到的失败"，且新增一处须同时提议退役一处——防止机制只增不减、体系复杂化失控。

> 任何 agent CLI 都从这里开始：先读你的 instructions file，再读当前任务对应的 SKILL.md。

## 技能索引

| 技能 | 用途 | 路径 |
|------|------|------|
| ipo-router | 项目状态评估 → 分析计划单生成。不做分析 | .claude/skills/ipo-router/SKILL.md |
| industry-scanner | 节点1：行业/业务定位三角色推演 | .claude/skills/industry-scanner/SKILL.md |
| tech-scanner | 节点2：技术/知识产权三角色推演 | .claude/skills/tech-scanner/SKILL.md |
| finance-scanner | 节点3：财务合规三角色推演 | .claude/skills/finance-scanner/SKILL.md |
| pricing-scanner | 节点4：定价/发行三角色推演 | .claude/skills/pricing-scanner/SKILL.md |
| monitor-runner | 督导期信号监控执行器（monitoring-run 路径，非分析节点；**附属能力，暂缓投入**）。不做四节点分析，只做信号比对与告警 | .claude/skills/monitor-runner/SKILL.md |

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
5. monitoring-run（附属路径）：引用前次推演的督导期监控表执行信号比对（monitor-runner），要求 previous_run_id，无制品拒绝执行
6. 每个节点产出后立即移交下游（如链路中有下一节点）

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
12. 规则文件只读。执行体禁止修改 AGENTS.md / references/ / .claude/skills/ / knowledge/ 下任何文件；发现规则缺陷时记录 rule_defect 并报告用户，不得自行修复。版本号 bump、tag、Release 是用户专属动作。

## 单一事实源

- 分析路径定义：`references/analysis-registry.md`
- 制品 schema 定义：`references/artifact-schemas.md`
- 非协商条款定义：`references/guardrails/non-negotiables.md`
- 角色定义：`references/roles/*.md`
- 质量门禁定义：`references/guardrails/quality-gates.md`
- 降级策略定义：`references/guardrails/degradation-paths.md`
- 跨维度传染矩阵：`references/contagion-matrix.md`（C1-C9，含叠加规则§6）
- 前瞻信号监测框架：`references/signal-watchlist.md`（含优先级矩阵§3.6、逆转信号§3.7、执行力代理§3.8）
- 首发推断算法卡（冻结版本，v0.8.0）：`references/prediction-algorithm/*.md`
- 校验协议（判定/盲测/差距分析，v0.8.0）：`references/validation-protocol.md`
- 输出模板（Markdown）：`references/templates/risk-matrix-template.md`（⚠️ v0.7.0 起 DEPRECATED，仅供历史对照）
- 输出模板（HTML）：`references/templates/risk-matrix-template.html`（⚠️ v0.7.0 起 DEPRECATED，仅供历史对照）
- HTML 组装协议：`references/templates/html-assembly.md`（Write 分块 + cat 拼接；禁止 heredoc/python 渲染）
- 工作流产物模板（v0.5.0 主交付物）：`references/templates/kernel-risk-checklist.md`、`references/templates/pricing-memo.md`、`references/templates/supervision-monitor.md`
- 最终报告模板（v0.5.1 起主交付物）：`references/templates/final-report.html`（三产物 + 预测与验证计划合一自包含 HTML；分拆件为上面三个 MD；v0.7.0 起第四区块为 S5 预测记录汇总）
- 监控告警清单模板（v0.6.0）：`references/templates/monitoring-report.md`（monitoring-run 路径产物）

所有 skill 文件引用以上文档，不自行定义路径、schema、角色、门禁。

## 知识库（基准库）

`knowledge/` 为内建基准库——搜索失败或数据时效不足（D1/D4 降级）时的兜底依据。使用规则见 `knowledge/README.md`。子目录：
- `industry-benchmarks/` — 新股发行环境基准、可比估值快照方法与实例（基准日期 2026-08）；**科创板 IPO 全样本回测底座**（ipo-cohort-backtest.md，n=98，2026-08-20 首批）
- `policy-tracker/` — IPO 审核/现场检查统计基准（基准日期 2026-08）
- `case-library/` — 历史 IPO 案例库（**仅作引擎回归测试基准**，不做事后追踪）：频准激光（688826，科创板，含失败模式清单）、宇树科技（688836，科创板，含市场第一性要素）、智元机器人（港股 18C，含港股口径差异与数据缺口提示）、长江存储（长存控股，科创板已受理，周期顶点上市与贱卖极端样本）
