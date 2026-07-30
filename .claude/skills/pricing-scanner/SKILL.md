---
name: pricing-scanner
description: >
  Gatekeeper 节点4：定价/发行三角色推演。接收上游制品和分析计划单，
  从三个外部视角分析可比估值区间、发行定价合理性、破发风险和
  估值故事的市场可信度。这是全链路推演的终点。
---

## 用途

对发行定价进行三个外部视角的压力测试。
三个角色在定价节点天然对立——Pre-IPO 投资人想要安全垫，买方嫌贵，舆论盯着"割韭菜"——这正是本节点的价值所在。

## 前置条件

- 分析计划单（analysis_plan YAML，来自 ipo-router）
- 上游 node_artifact（根据路径模式：full-chain 需 industry + tech + finance；pricing-focused 需 industry）
- 无分析计划单 → 拒绝启动（非协商条款 N2）

## 分析边界

**✅ 本节点负责：**
- 可比公司估值区间与发行人定位
- 发行价相对于可比公司的溢价/折价分析
- Pre-IPO 轮次估值的安全垫测算
- 破发风险评估（基于可比公司上市后表现）
- 买方可能提出的估值质疑
- 舆论可能发起的定价争议

**❌ 本节点不负责：**
- 行业赛道判断（→ industry-scanner，仅引用）
- 技术先进性论证（→ tech-scanner，仅引用）
- 财务数据真实性验证（→ finance-scanner，仅引用）
- 给出具体的发行价建议（这是承销商的工作）
- DCF 模型构建（这是分析师的工作）

## 执行流程

### Step 1: 加载角色与上游制品

1. 读取 `references/roles/pre-ipo-investor.md`
2. 读取 `references/roles/buy-side.md`
3. 读取 `references/roles/media-watchdog.md`
4. 读取上游 node_artifact（行业 + 技术 + 财务 或仅行业，取决于路径模式）
5. 不重复搜索行业/技术/财务数据——仅搜索估值相关数据

### Step 2: 三角色并行分析

三个角色各自独立分析估值问题。按各角色搜索策略搜索估值相关数据。

**定价节点的三角色分工特别说明：**

- **Pre-IPO 投资人**：计算估值安全垫。对比 Pre-IPO 轮次估值 vs 预期发行价区间，搜索同轮次退出回报率基准
- **买方**：分析发行价相对于可比公司的合理性。搜索可比公司 PS/PE/PEG，反推发行价隐含增速
- **舆论**：搜索高市盈率发行争议案例、实控人套现记录、定价争议的常见质疑模式

每个角色产出风险条目列表（deep: ≥5条/角色, standard: ≥3条, quick: ≥1条）。
条目格式严格遵循 `references/artifact-schemas.md §S3 risk_entry`。
node 字段固定为 `"pricing"`。

### Step 3: 汇聚与冲突标注

1. 合并三个角色的风险条目
2. 识别共识风险（≥2 个角色关注的同一话题）
3. 识别角色冲突（同一话题的不同解读）
4. 特别关注定价节点特有的三角色对立——不要强行调和
5. 标注冲突类型：assumption / weighting / interpretation

### Step 4: 质量门禁

按 `references/guardrails/quality-gates.md` 逐项检查：
  - G1: 角色完备（每角色条目 ≥ depth 要求）
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

### 1. 节点结论制品（终端节点——无下游传递）

```yaml
node_artifact:
  node: "pricing"
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

### 2. 风险矩阵报告（全链路最终输出）

按 `references/templates/risk-matrix-template.md` 格式输出。
如果为全链路模式，报告包含所有四个节点的 artifact_freshness 汇总。

## 链式调用

- **上游**：依路径模式而定
  - full-chain: industry → tech → finance → pricing
  - pricing-focused: industry → pricing
- **本节点为终端节点**：无下游传递

## 护栏

- 禁止给出具体发行价格建议
- 禁止构建完整 DCF/财务模型
- 禁止重复分析行业/技术/财务问题（引用上游制品）
- 三个角色的估值分歧是核心价值——不要强行调和
- 冲突标注优先展示定价节点特有的三角色对立
