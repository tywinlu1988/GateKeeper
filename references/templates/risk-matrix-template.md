# 风险矩阵输出模板

> 所有 Scanner 节点最终输出的统一格式。模板字段对应 artifact-schemas.md §S3 risk_entry。

---

# Gatekeeper 风险矩阵

<!-- GateKeeper-Template: risk-matrix-template.md —— 输出报告必须保留本标记（G8 模板合规验证依据） -->

**项目**：{project_name}　**计划**：{plan_id}　**节点**：{node_name}　**深度**：{depth}　**生成时间**：{generated_at}

---

## 执行摘要

> {exec_verdict}

| 节点 | 评级 | 风险数 |
|------|------|--------|
| 行业/业务定位 | {industry_rating} | {industry_risk_count} |
| 技术/知识产权 | {tech_rating} | {tech_risk_count} |
| 财务合规 | {finance_rating} | {finance_risk_count} |
| 定价/发行 | {pricing_rating} | {pricing_risk_count} |

**风险分布**：🔴Critical {critical_count}　🟠High {high_count}　🟡Medium {medium_count}　🟢Low {low_count}

**TOP 3-5 风险**：
1. {exec_top1}
2. {exec_top2}
3. {exec_top3}
（可选 4-5. {exec_top4_5}）

**关键数据**：
- {exec_data1}
- {exec_data2}
- {exec_data3}

---

## 节点总结

**综合评级**：{overall_rating}

**核心发现**：{key_finding}

**数据质量**：{search_quality} | **缺失数据**：{data_gaps}

---

## 角色共识风险

> 以下风险被多个角色共同关注，推演可信度最高。

{agreed_risks_section}

| ID | 风险主张 | 风险等级 | 共识角色 | 关键数据 | 建议应对 |
|----|---------|---------|---------|---------|---------|
| {id} | {claim} | {risk_level} | {roles} | {key_data_summary} | {suggested_response} |

---

## 角色冲突标注

> 以下话题存在角色间分歧。分歧类型：假设冲突(assumption) / 权重冲突(weighting) / 解读冲突(interpretation)

{conflicts_section}

**冲突话题**：{topic}

| 角色 | 观点 | 依据 |
|------|------|------|
| Pre-IPO 投资人 | {pre_ipo_view} | {pre_ipo_basis} |
| 买方 | {buy_side_view} | {buy_side_basis} |
| 舆论 | {media_view} | {media_basis} |

---

## Pre-IPO 投资人视角

> 此角色关注：退出路径清晰度、估值安全垫、上市确定性对投资回报的影响
> 风险等级：🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low

| ID | 风险主张 | 等级 | 关键数据 | 退出影响 | 来源时效 | 建议应对 |
|----|---------|------|---------|---------|---------|---------|
{pre_ipo_entries}

---

## 上市后买方视角

> 此角色关注：上市后增长可持续性、财务质量、估值合理性
> 风险等级：🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low

| ID | 风险主张 | 等级 | 关键数据 | 股价影响推演 | 可比案例 | 建议应对 |
|----|---------|------|---------|------------|---------|---------|
{buy_side_entries}

---

## 舆论/媒体视角

> 此角色关注：可能引发负面报道的争议话题、隐藏风险、信息披露薄弱点
> 风险等级：🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low

| ID | 风险主张 | 等级 | 媒体标题模拟 | 类似案例 | 传播路径 | 建议应对 |
|----|---------|------|------------|---------|---------|---------|
{media_entries}

---

## 关键论断时效清单

> 本报告全部数值型关键论断的数据所属期（data_as_of）。由 pricing-scanner Step 4.5 生成。
> 时效状态：✅ 时效内 / ⚠️ 超期但已按 D4 标注（已移出结论位）/ ❌ 违规（不应出现）

| 论断 | 数值 | data_as_of | 来源 | 时效状态 |
|------|------|-----------|------|---------|
{claim_freshness_rows}

---

## 制品新鲜度

| 节点 | 最后更新 | 状态 | 距今 |
|------|---------|------|------|
| 行业定位 | {industry_generated_at} | {industry_status} | {industry_age} |
| 技术/IP | {tech_generated_at} | {tech_status} | {tech_age} |
| 财务合规 | {finance_generated_at} | {finance_status} | {finance_age} |
| 定价/发行 | {pricing_generated_at} | {pricing_status} | {pricing_age} |

---

*报告由 Gatekeeper v0.6.1 生成 · 所有数据均内联摘要，可独立分发*
*知识来源：实时搜索 + 基准库（knowledge/） · 搜索质量：{search_quality}*
