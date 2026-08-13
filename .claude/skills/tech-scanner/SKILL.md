---
name: tech-scanner
description: >
  Use when 持有 Gatekeeper 分析计划单（analysis_plan YAML）且链路
  路由到 tech 节点时需要执行该节点推演时。不独立触发——无分析
  计划单时拒绝启动。分析范围与流程详见正文，勿凭本描述执行。
---

## 用途

对发行人的技术实力和知识产权进行三个外部视角的压力测试。

## 前置条件

- 分析计划单（analysis_plan YAML）
- quick-scan 模式：无上游依赖（与 industry-scanner 并行执行）
- full-chain / targeted-update / pricing-focused 模式：上游 node_artifact（来自 industry-scanner）——引用其行业判断，不做重复分析
- 无分析计划单 → 拒绝启动（非协商条款 N2）
- **N2 例外**：用户手动指定 `path_id` 和 `node` 时允许跳过 Router 直接启动（见 references/guardrails/non-negotiables.md N2）

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

> 本技能中所有 `references/...` 路径均相对于 Gatekeeper **项目根目录**（非本技能所在目录）。

### Step 0: 时间锚定（强制，先于一切搜索）

1. 确定当前日期 T0（以系统日期为准），写入所有制品的 `generated_at`。
2. 所有搜索查询必须带时间限定词：`"{主题} {T0年份}"`、`"{主题} 最新/TTM/近12个月"`。禁止发送无时间限定的市场环境类查询。
3. 市场环境类数据（破发率、估值倍数、审核/撤回统计、发行制度、融资热度）：仅接受 `data_as_of` 距 T0 ≤ 6 个月的来源作为"当前"论断依据。
4. 每条证据必须填写 `data_as_of`（数据所属期）——旧研报今天被抓取，`data_as_of` 仍填其发表期，禁止以抓取时间冒充。
5. 搜到的数据超出时效阈值 → 触发降级 D4（references/guardrails/degradation-paths.md）。
6. **先搜后查库**：`knowledge/` 基准库仅在本节点实时搜索完成后才允许查阅引用；基准证据 `source_type=baseline`，禁止单独进入执行摘要/TOP 风险/评级依据（G7）。
7. 所有查询（含未命中的）逐条写入 `node_artifact.search_log`；每角色查询次数须达 depth 要求（次数标准与一手披露要求见 references/analysis-registry.md 深度级别定义）。

### Step 1: 加载角色与上游制品

1. 读取 `references/roles/pre-ipo-investor.md`
2. 读取 `references/roles/buy-side.md`
3. 读取 `references/roles/media.md`
4. 如非 quick-scan 模式：读取上游 industry-scanner 的 node_artifact（引用 `summary.key_finding` 和 `data_freshness`）
5. 不重复搜索行业数据——仅搜索技术相关数据

### Step 2: 三角色并行分析

三个角色各自独立分析。按各角色搜索策略搜索技术相关数据。

每个角色产出风险条目列表（deep: ≥5条/角色, standard: ≥3条, quick: ≥1条）。
条目格式严格遵循 `references/artifact-schemas.md §S3 risk_entry`。
node 字段固定为 `"tech"`。

### Step 2.5: 前瞻信号生成

同 industry-scanner（Step 2.5），按 `references/signal-watchlist.md` 生成（含 time_window / priority_tier / execution_proxy 新字段）。

### Step 3: 汇聚与冲突标注

同 industry-scanner（Step 3）。

### Step 3.5: 传染检测

同 industry-scanner（Step 3.5），对照 `references/contagion-matrix.md`。

### Step 4: 质量门禁

同 industry-scanner（Step 4）：按 `references/guardrails/quality-gates.md` **全部**门禁逐项检查（当前为 G1-G9，含 G1.5 信号完备、G1.6 交叉信号一致性、G1.7 异议角色加权、G7 时效合规、G8 模板合规、G9 监控判定合规）。

### Step 5: 降级处理

同 industry-scanner（Step 5），按 `references/guardrails/degradation-paths.md`（D1 搜索不可用 / D2 数据稀疏 / D3 数据矛盾 / D4 数据时效不足）。

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

### 2. 风险矩阵条目（给终端节点）

本节点产出 node_artifact + risk_entries 即止。面向用户的三个工作流产物（内核风险清单 / 发行定价备忘录 / 督导期监控表）由 pricing 终端节点整合四节点制品产出（v0.5.0，模板见 references/templates/）。

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
