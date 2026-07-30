---
name: finance-scanner
description: >
  Gatekeeper 节点3：财务合规三角色推演。接收上游技术制品和分析计划单，
  从三个外部视角分析收入确认质量、关联交易复杂度、现金流质量和
  财务数据内在一致性。
---

## 用途

对发行人的财务数据进行三个外部视角的压力测试。
重点不是"合不合规"（那是审计师的事），而是"买方信不信"和"媒体会不会质疑"。

## 前置条件

- 分析计划单（analysis_plan YAML）
- 上游 node_artifact（来自 industry-scanner 和 tech-scanner）
- 无分析计划单 → 拒绝启动（非协商条款 N2）

## 分析边界

**✅ 本节点负责：**
- 收入确认政策与行业惯例的差异分析
- 关联交易的复杂度与公允性信号
- 应收账款质量与经营现金流健康度
- 研发资本化政策的合理性（与同行业对比）
- 财务数据的内在一致性（是否存在调节痕迹的信号）
- 客户/供应商集中度风险

**❌ 本节点不负责：**
- 行业增长逻辑验证（→ industry-scanner，仅引用）
- 技术先进性和研发成果评估（→ tech-scanner，仅引用）
- 估值倍数选取和定价判断（→ pricing-scanner）
- 审计级别的合规鉴证（这不是审计系统）

## 执行流程

### Step 1: 加载角色与上游制品

1. 读取 `references/roles/pre-ipo-investor.md`
2. 读取 `references/roles/buy-side.md`
3. 读取 `references/roles/media-watchdog.md`
4. 读取上游 industry-scanner 和 tech-scanner 的 node_artifact
5. 不重复搜索行业和技术数据——仅搜索财务相关数据

### Step 2: 三角色并行分析

三个角色各自独立分析。按各角色搜索策略搜索财务相关数据。

每个角色产出风险条目列表（deep: ≥5条/角色, standard: ≥3条, quick: ≥1条）。
条目格式严格遵循 `references/artifact-schemas.md §S3 risk_entry`。
node 字段固定为 `"finance"`。

### Step 3: 汇聚与冲突标注

同 industry-scanner（Step 3）。

### Step 4: 质量门禁

同 industry-scanner（Step 4），按 `references/guardrails/quality-gates.md` 逐项检查。

### Step 5: 降级处理

同 industry-scanner（Step 5），按 `references/guardrails/degradation-paths.md`。

## 输出

### 1. 节点结论制品（给下游节点）

```yaml
node_artifact:
  node: "finance"
  generated_at: "{ISO 8601}"
  plan_id: "{plan_id}"
  summary:
    overall_rating: "favorable|neutral|cautious|red-flag"
    key_finding: "一句话核心判断"
  role_consensus:
    agreed_risks: []
    conflicts: []
  data_freshness:
    search_quality: "rich|adequate|sparse"
    key_data_gaps: []
```

### 2. 风险矩阵报告

按 `references/templates/risk-matrix-template.md` 格式输出。

## 链式调用

- **上游**：tech-scanner + industry-scanner（引用行业和技术结论）
- **下游**：pricing-scanner（全链路模式下自动衔接）

## 护栏

- 禁止重复分析行业和技术问题（引用上游制品即可）
- 禁止出具审计意见或合规鉴证
- 禁止在没有 inline_summary 的情况下输出风险条目
- 买方视角尤其重要：关注"财务质量可持续性"而非"合规性"
