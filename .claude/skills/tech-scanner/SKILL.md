---
name: tech-scanner
description: >
  Gatekeeper 节点2：技术/知识产权三角色推演。接收上游行业制品和分析计划单，
  从三个外部视角分析核心技术先进性、知识产权完整性、研发投入质量和
  技术依赖风险。
---

## 用途

对发行人的技术实力和知识产权进行三个外部视角的压力测试。

## 前置条件

- 分析计划单（analysis_plan YAML）
- 上游 node_artifact（来自 industry-scanner）——引用其行业判断，不做重复分析
- 无分析计划单 → 拒绝启动（非协商条款 N2）

## 分析边界

**✅ 本节点负责：**
- 核心技术先进性（与行业基准对比）
- 知识产权完整性（专利覆盖范围、潜在诉讼风险）
- 研发投入质量（真研发 vs 资本化包装的识别信号）
- 技术依赖风险（核心人员流失、供应商锁定、技术授权到期）
- 技术路线的市场认可度（买方和舆论如何看待该技术）

**❌ 本节点不负责：**
- 行业天花板和市场空间判断（→ industry-scanner，仅引用其结论）
- 研发费用的会计处理合规性（→ finance-scanner）
- 技术对估值倍数的影响量化（→ pricing-scanner）
- 任何形式的技术专利法律意见

## 执行流程

### Step 1: 加载角色与上游制品

1. 读取 `references/roles/pre-ipo-investor.md`
2. 读取 `references/roles/buy-side.md`
3. 读取 `references/roles/media-watchdog.md`
4. 读取上游 industry-scanner 的 node_artifact（引用 `summary.key_finding` 和 `data_freshness`）
5. 不重复搜索行业数据——仅搜索技术相关数据

### Step 2: 三角色并行分析

三个角色各自独立分析。按各角色搜索策略搜索技术相关数据。

每个角色产出风险条目列表（deep: ≥5条/角色, standard: ≥3条, quick: ≥1条）。
条目格式严格遵循 `references/artifact-schemas.md §S3 risk_entry`。
node 字段固定为 `"tech"`。

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
  node: "tech"
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

### 3. 制品新鲜度

更新 tech 节点的时间戳。

## 链式调用

- **上游**：industry-scanner（引用其行业结论，不重复分析）
- **下游**：finance-scanner（全链路模式下自动衔接）
- 如果 analysis_plan.mode = "quick-scan"：无下游（快速扫描到此结束）

## 护栏

- 禁止重复分析行业问题（引用上游制品即可）
- 禁止跨节点分析（不判断财务合规、估值合理性）
- 禁止在没有 inline_summary 的情况下输出风险条目
- 角色输出必须符合其锚定规则
