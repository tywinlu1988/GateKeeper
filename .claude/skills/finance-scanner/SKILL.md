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
- **N2 例外**：用户手动指定 `path_id` 和 `node` 时允许跳过 Router 直接启动（见 references/guardrails/non-negotiables.md N2）

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

> 本技能中所有 `references/...` 路径均相对于 Gatekeeper **项目根目录**（非本技能所在目录）。

### Step 0: 时间锚定（强制，先于一切搜索）

1. 确定当前日期 T0（以系统日期为准），写入所有制品的 `generated_at`。
2. 所有搜索查询必须带时间限定词：`"{主题} {T0年份}"`、`"{主题} 最新/TTM/近12个月"`。禁止发送无时间限定的市场环境类查询。
3. 市场环境类数据（破发率、估值倍数、审核/撤回统计、发行制度、融资热度）：仅接受 `data_as_of` 距 T0 ≤ 6 个月的来源作为"当前"论断依据。
4. 每条证据必须填写 `data_as_of`（数据所属期）——旧研报今天被抓取，`data_as_of` 仍填其发表期，禁止以抓取时间冒充。
5. 搜到的数据超出时效阈值 → 触发降级 D4（references/guardrails/degradation-paths.md）。
6. **先搜后查库**：`knowledge/` 基准库仅在本节点实时搜索完成后才允许查阅引用；基准证据 `source_type=baseline`，禁止单独进入执行摘要/TOP 风险/评级依据（G7）。
7. 所有查询（含未命中的）逐条写入 `node_artifact.search_log`；每角色查询次数须达 depth 要求（deep ≥3，含 ≥1 次一手披露查询——招股书申报稿/问询函/发行公告）。

### Step 1: 加载角色与上游制品

1. 读取 `references/roles/pre-ipo-investor.md`
2. 读取 `references/roles/buy-side.md`
3. 读取 `references/roles/media.md`
4. 读取上游 industry-scanner 和 tech-scanner 的 node_artifact
5. 不重复搜索行业和技术数据——仅搜索财务相关数据

### Step 2: 三角色并行分析

三个角色各自独立分析。按各角色搜索策略搜索财务相关数据。

每个角色产出风险条目列表（deep: ≥5条/角色, standard: ≥3条, quick: ≥1条）。
条目格式严格遵循 `references/artifact-schemas.md §S3 risk_entry`。
node 字段固定为 `"finance"`。

### Step 2.5: 前瞻信号生成

同 industry-scanner（Step 2.5），按 `references/signal-watchlist.md` 生成（含 time_window / priority_tier / execution_proxy 新字段）。

### Step 3: 汇聚与冲突标注

同 industry-scanner（Step 3）。

### Step 3.5: 传染检测

同 industry-scanner（Step 3.5），对照 `references/contagion-matrix.md`。财务节点特别关注 C1（行业→财务）和 C5（财务→定价）通道。

### Step 4: 质量门禁

同 industry-scanner（Step 4）：按 `references/guardrails/quality-gates.md` **全部**门禁逐项检查（当前为 G1-G8，含 G1.5 信号完备、G1.6 交叉信号一致性、G1.7 异议角色加权、G7 时效合规、G8 模板合规）。

### Step 5: 降级处理

同 industry-scanner（Step 5），按 `references/guardrails/degradation-paths.md`（D1 搜索不可用 / D2 数据稀疏 / D3 数据矛盾 / D4 数据时效不足）。

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

默认按 `references/templates/risk-matrix-template.md` 格式输出 Markdown。
如需自包含 HTML 报告，**以 `references/templates/risk-matrix-template.html` 为底本填充**——禁止从零自行设计 HTML/CSS；输出必须保留模板标记注释（G8 验证）。HTML 生成必须遵循 `references/templates/html-assembly.md` 组装协议（Write 分块 + cat 拼接；禁止 Bash heredoc / 依赖 python 渲染）。

## 链式调用

- **上游**：tech-scanner + industry-scanner（引用行业和技术结论）
- **下游**：pricing-scanner（全链路模式下自动衔接）

## 护栏

- 禁止重复分析行业和技术问题（引用上游制品即可）
- 禁止出具审计意见或合规鉴证
- 禁止在没有 inline_summary 的情况下输出风险条目
- 买方视角尤其重要：关注"财务质量可持续性"而非"合规性"
