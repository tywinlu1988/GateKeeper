---
name: industry-scanner
description: >
  Gatekeeper 节点1：行业/业务定位三角色推演。接收分析计划单，
  从 Pre-IPO 投资人、买方、舆论三个外部视角分析行业天花板、
  竞争格局、政策环境和"硬科技"属性。产出节点制品 + 风险矩阵。
---

## 用途

对发行人的行业定位和业务描述进行三个外部视角的压力测试。

## 前置条件

- 分析计划单（analysis_plan YAML，来自 ipo-router）
- 无分析计划单 → 拒绝启动（非协商条款 N2）

## 分析边界

**✅ 本节点负责：**
- 赛道天花板与增长驱动力评估
- 竞争格局与发行人市场地位分析
- 行业政策环境与监管趋势判断
- "硬科技"属性的市场认知检验
- 行业定位是否经得起买方和舆论质疑

**❌ 本节点不负责：**
- 核心技术先进性细节评估（→ tech-scanner）
- 收入确认合规性判断（→ finance-scanner）
- 发行估值判断（→ pricing-scanner）
- 任何形式的最终过会概率判断

## 执行流程

### Step 1: 加载角色与数据

1. 读取 `references/roles/pre-ipo-investor.md`
2. 读取 `references/roles/buy-side.md`
3. 读取 `references/roles/media.md`
4. 按每个角色的搜索策略，并行搜索行业相关数据

### Step 2: 三角色并行分析

三个角色各自独立分析。共享搜索到的底层数据，但按各自的认知立场独立解读。

每个角色产出风险条目列表（deep: ≥5条/角色, standard: ≥3条, quick: ≥1条）。
条目格式严格遵循 `references/artifact-schemas.md §S3 risk_entry`。

### Step 2.5: 前瞻信号生成

对每条 Critical/High 风险条目，按 `references/signal-watchlist.md` 生成信号清单。新增字段：
- `time_window`：按风险类别选择窗口（customer 2-4Q / tech 4-8Q / profit 4-8Q）
- `priority_tier`：标注 T1（结构级）/ T2（趋势级）/ T3（事件级）
- `execution_proxy`：可选，管理层执行力代理（不计分）
- `reversal_signal`：仅在 C9 范式冲击时使用

### Step 3: 汇聚与冲突标注

1. 合并三个角色的风险条目
2. 识别共识风险
3. 识别角色冲突，标注冲突类型
4. 角色间风险等级对比 → 若某角色 ≥ 其他角色 +2 档 → 按 G1.7 异议加权

### Step 3.5: 传染检测

对照 `references/contagion-matrix.md` 检查跨维度传染信号。
若触发 → node_artifact 中添加 `contagion_alert` 字段。
叠加检查 → 若 ≥2 条通道同时负向 → 按 §6 叠加规则计算放大因子。

### Step 4: 质量门禁

按 `references/guardrails/quality-gates.md` 逐项检查：
  - G1: 角色完备（每角色条目 ≥ depth 要求）
  - G1.5: 信号完备（Critical/High 风险必须有 signal_watchlist）
  - G1.6: 交叉信号一致性（跨层级冲突按 T1>T2>T3 处理）
  - G1.7: 异议角色加权（角色间风险 ≥2 档偏差时触发）
  - G2: 来源多样（不同条目不同 URL）
  - G3: 证据内联（每条有 inline_summary）
  - G4: 枚举合规（node/role/risk_level/id 格式）
  - G5: 角色锚定（rationale 与角色立场一致）
  - G6: 自包含（无本地路径、无裸 URL 依赖）

不通过 → 按门禁定义处理 → 重新生成（最多一次）。
两次仍不通过 → 触发降级策略（references/guardrails/degradation-paths.md）。

### Step 5: 降级处理

搜索失败/数据不足时按 degradation-paths.md 降级运行：
  - D1: 搜索不可用 → 标注 SEARCH_UNAVAILABLE
  - D2: 数据稀疏 → 降低要求 + confidence: low
  - D3: 数据矛盾 → 保留矛盾双方

## 输出

### 1. 节点结论制品（给下游节点）

```yaml
node_artifact:
  node: "industry"
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

### 2. 风险矩阵报告（给用户）

默认按 `references/templates/risk-matrix-template.md` 格式输出 Markdown。
如需自包含 HTML 报告，按 `references/templates/risk-matrix-template.html` 格式输出（内联 CSS，可独立分发，满足非协商条款 N8）。

### 3. 制品新鲜度

记录本节点制品的生成时间戳，纳入全局 artifact_freshness。

## 链式调用

- **下游**：tech-scanner（全链路和快速扫描模式下自动衔接）
- **制品传递**：node_artifact YAML 传递给 tech-scanner
- 如果 analysis_plan.mode = "pricing-focused"：制品传递给 pricing-scanner

## 护栏

- 禁止跨节点分析（不判断技术细节、财务合规、估值合理性）
- 禁止在没有 inline_summary 的情况下输出风险条目
- 所有枚举值必须使用 schema 定义的选项
- 角色输出必须符合其"认知立场"和"你绝对不是谁"锚定
