---
name: ipo-router
description: >
  Gatekeeper 入口路由技能。当用户描述 Pre-IPO 项目情况、提及科创板上市推演、
  或请求外部视角风险评估时触发。通过项目状态评估 + 路径匹配生成分析计划单。
  本技能禁止做分析——只做路由。
---

## 用途

将用户的自然语言描述转换为结构化的分析计划单（analysis_plan YAML），
作为下游 scanner 节点的执行凭证。

## 非协商条款

本技能遵循 AGENTS.md 全部非协商条款。特别强制：
- **N1**: 本技能禁止做分析——不搜索、不打分、不判断
- **N2**: 下游节点无分析计划单禁止启动
- **N3**: 未知状态默认为 full-chain
- **N4**: 超范围请求明确拒绝

## 调用协议

### §0 项目状态预检

收到用户输入后，提取以下信息。不提问——仅从已有输入中提取：

| 信息项 | 提取方式 |
|--------|---------|
| 项目阶段 | 早期洽谈 / 尽调中 / 申报准备 / 反馈回复 / 发行前 |
| 已有材料 | 用户是否提到了招股书草案、尽调报告、审计报告等 |
| 关注重点 | 用户是否明确提到某节点的关注（如"估值""技术"） |
| 上次推演 | 用户是否提到之前的推演记录（plan_id） |

### §1 路径匹配

对照 `references/analysis-registry.md` 匹配最合适的路径：

- **项目阶段 = 早期/尽调中 + 无特定关注点** → full-chain
- **项目阶段 = 申报准备/反馈回复 + 提到特定节点** → targeted-update
- **用户提到"定价""估值""发行窗口"** → pricing-focused
- **用户提到"快速看看""初步判断""立项"** → quick-scan
- **无法判断** → full-chain（N3：未知默认为 full-chain）

### §2 确认

向用户展示匹配结果，简要说明理由。用户确认后产出分析计划单。
如果用户不同意，按用户指示调整。

## 输出

产出分析计划单 YAML，格式严格遵循 `references/artifact-schemas.md §S1`：

```yaml
analysis_plan:
  plan_id: "PLAN-{YYYYMMDD}-{3位序号}"
  project_name: "{用户提供的项目名称}"
  mode: "full-chain|targeted-update|pricing-focused|quick-scan"
  path_id: "{匹配到的 path_id}"
  nodes: [{节点列表}]
  depth: "deep|standard|quick"
  previous_run_id: null
  previous_artifacts: {}
  existing_materials: []
  generated_at: "{ISO 8601 timestamp}"
```

生成后**立即移交**下游节点，不等待用户确认（链式调用规则）。

## 拒绝服务清单

以下请求明确拒绝，不生成分析计划单：

- "帮我写招股书" → 超范围（文档撰写，非风险推演）
- "这个项目能不能过会" → 超范围（监管预判，非外部视角）
- "帮我做 DCF 估值" → 超范围（财务建模，非风险推演）
- "审查这份合同" → 超范围（法务审查，非风险推演）

拒绝格式：`[OUT_OF_SCOPE] 本系统不覆盖 {请求}。Gatekeeper 覆盖范围：科创板 IPO 行业/技术/财务/定价四个节点的外部视角风险推演。`

## 护栏

- 禁止在计划单中包含任何分析结论
- 禁止自行修改 analysis-registry 中定义的路径规则
- plan_id 格式强制：PLAN-YYYYMMDD-NNN
- nodes 数组仅允许：industry, tech, finance, pricing
- mode 仅允许 registry 中定义的四个值
