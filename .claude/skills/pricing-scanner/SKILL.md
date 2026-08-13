---
name: pricing-scanner
description: >
  Use when 持有 Gatekeeper 分析计划单（analysis_plan YAML）且链路
  路由到 pricing 节点时需要执行该节点推演时。不独立触发——无分析
  计划单时拒绝启动。分析范围与流程详见正文，勿凭本描述执行。
---

## 用途

对发行定价进行三个外部视角的压力测试。
三个角色在定价节点天然对立——Pre-IPO 投资人想要安全垫，买方嫌贵，舆论盯着"割韭菜"——这正是本节点的价值所在。

## 前置条件

- 分析计划单（analysis_plan YAML，来自 ipo-router）
- 上游 node_artifact（根据路径模式：full-chain 需 industry + tech + finance；pricing-focused 需 industry）
- 无分析计划单 → 拒绝启动（非协商条款 N2）
- **N2 例外**：用户手动指定 `path_id` 和 `node` 时允许跳过 Router 直接启动（见 references/guardrails/non-negotiables.md N2）

## 分析边界

**✅ 本节点负责：**
- 可比公司估值区间与发行人定位
- 发行价相对于可比公司的溢价/折价分析
- Pre-IPO 轮次估值的安全垫测算
- 破发风险评估（按下述二分框架，禁止单一历史外推）
- 买方可能提出的估值质疑
- 舆论可能发起的定价争议

**定价风险的二分框架（强制）：**
- **首日/短期破发风险**：由市场制度环境决定（发行节奏、询价规则、近 12 个月破发统计），以 Step 1.5 的市场环境基准快照为准——禁止用历史破发潮统计或可比公司旧表现推断当前首日概率
- **上市后 6-24 个月估值回归风险**：由基本面与传染通道决定（C2 行业→定价、C5 财务→定价），这是三角色推演的主战场
- 两者分别评估、分别成条，不得互相替代，不得混用证据

**❌ 本节点不负责：**
- 行业赛道判断（→ industry-scanner，仅引用）
- 技术先进性论证（→ tech-scanner，仅引用）
- 财务数据真实性验证（→ finance-scanner，仅引用）
- 给出具体的发行价建议（这是承销商的工作）
- DCF 模型构建（这是分析师的工作）

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
4. 读取上游 node_artifact（行业 + 技术 + 财务 或仅行业，取决于路径模式）
5. 不重复搜索行业/技术/财务数据——仅搜索估值相关数据

### Step 1.5: 市场环境基准快照（强制，先于三角色分析）

逐项查询并填写下表。每一项都必须记录 `as_of`（数据所属期）与**来源 URL**；任何一项 `as_of` 距 T0 > 6 个月 → 按 G7/D4 处理，且该项结论禁止进入执行摘要和 TOP 风险。**每项必须填具体数值——"估计""极低""较高"等无量表述视同未查（G1 不通过）**。

| # | 必查项 | 查询模板 | as_of | 数值结果 | 来源 URL |
|---|--------|---------|-------|---------|---------|
| 1 | 近 12 个月新股首日破发率 | "A股 新股 首日破发 {T0年份}" | | | |
| 2 | 近 12 个月新股首日平均涨幅 | "科创板 新股 首日涨幅 {T0年份}" | | | |
| 3 | 可比公司当前估值（逐家） | "{可比公司名} 市盈率 TTM 最新" | | | |
| 4 | IPO 审核/现场检查近期统计 | "IPO 现场检查 撤回率 {T0年份}" | | | |
| 5 | 发行制度与询价规则现状 | "科创板 发行制度 {T0年份}" | | | |
| 6 | 发行人发行结果公告（若已发行/已定价） | "{发行人} 发行结果公告 / 网上申购倍数 / 实际募资" | | | |

- 第 6 项条件触发：只要发行人已完成定价或发行，**必须**查实际发行结果（实际募资、超募金额、认购倍数、弃购率）——禁止使用发行前的预测数（预测超募≠实际超募）

- 可比估值必须取**最新交易日 TTM**，禁止使用历史一致预期、静态 PE 或超过 6 个月前的研报数字
- **可比估值双来源规则（v0.4.3 新增）**：每家可比公司须满足其一——(a) ≥2 个独立来源一致；或 (b) 1 个来源 + 「总市值 ÷ TTM 净利润」交叉计算验证，两者都记入快照表。单一来源且未交叉验证的数值不得进入快照
- 多平台估值数据冲突时（差异 > 20%）：以主流行情终端最新 TTM 为准，可用「总市值 ÷ TTM 净利润」交叉验证，并按 D3 保留冲突双方记录
- **聚合数字可复算（v0.4.3 新增）**：可比均值/区间等聚合数字必须能从快照表列出的分项直接复算——禁止出现与分项对不上的均值（实测反例：三家可比 117/206/107x 却得出"均值 190.22x"）
- 「近 12 个月」类统计的查询词可用 "{主题} 近一年" 变体补充年份查询；聚合多篇统计时 `as_of` 填**统计期末**（非报道日）
- 快照全部完成后才进入三角色分析；快照数据是首日破发风险判断的**唯一**环境依据

### Step 2: 三角色并行分析

三个角色各自独立分析估值问题。按各角色搜索策略搜索估值相关数据。

**定价节点的三角色分工特别说明：**

- **Pre-IPO 投资人**：计算估值安全垫。对比 Pre-IPO 轮次估值 vs 预期发行价区间，搜索同轮次退出回报率基准
- **买方**：分析发行价相对于可比公司的合理性。搜索可比公司 PS/PE/PEG，反推发行价隐含增速
- **舆论**：搜索高市盈率发行争议案例、实控人套现记录、定价争议的常见质疑模式

每个角色产出风险条目列表（deep: ≥5条/角色。pricing-scanner 仅运行在 deep 深度下）。
条目格式严格遵循 `references/artifact-schemas.md §S3 risk_entry`。
node 字段固定为 `"pricing"`。

### Step 2.5: 前瞻信号生成

同 industry-scanner（Step 2.5），按 `references/signal-watchlist.md` 生成（含 time_window / priority_tier / execution_proxy 新字段）。

### Step 3: 汇聚与冲突标注

1. 合并三个角色的风险条目
2. 识别共识风险（≥2 个角色关注的同一话题）
3. 识别角色冲突（同一话题的不同解读）
4. 特别关注定价节点特有的三角色对立——不要强行调和
5. 标注冲突类型：assumption / weighting / interpretation

### Step 3.5: 传染检测

同 industry-scanner（Step 3.5），对照 `references/contagion-matrix.md`。定价节点特别关注 C2（行业→定价）和 C5（财务→定价）通道。

### Step 4: 质量门禁

同 industry-scanner（Step 4）：按 `references/guardrails/quality-gates.md` **全部**门禁逐项检查（当前为 G1-G8，含 G1.5 信号完备、G1.6 交叉信号一致性、G1.7 异议角色加权、G7 时效合规、G8 模板合规）。

不通过 → 按门禁定义处理 → 重新生成（最多一次）。
两次仍不通过 → 触发降级策略（references/guardrails/degradation-paths.md）。

### Step 4.5: 关键论断时效自检（终端节点强制，先于报告输出）

作为全链路终端节点，pricing-scanner 在输出最终报告前必须完成：

1. 扫描最终报告全部内容，列出**所有数值型关键论断**（执行摘要、TOP 3 风险、各节点 key_finding、关键数据区中的每一个数字）
2. 逐条填写「关键论断时效清单」：论断 | 数值 | data_as_of | 来源 | 时效状态（✅ 时效内 / ⚠️ 超期但已标注 / ❌ 违规）
3. 凡触发 G7 时效阈值且未按 D4 标注的 → 判定 ❌ → 回炉：带当前年份限定词重新验证；无法验证 → 按 D4 移出结论位
4. **一致性核对（v0.4.3 新增）**：逐字扫描执行摘要、TOP 风险、关键数据、各节点 key_finding——凡出现被 D4/[STALE_DATA] 标注的论断数值，删除或改写该处表述。清单判定与报告正文必须一致，禁止"判而不行"
5. 该清单作为报告固定区块输出（见输出模板「关键论断时效清单」节）——它是接收方核验报告事实时效的唯一入口

设计来源：频准激光初版报告的三处事实漂移（破发概率、可比 PE、撤回率）均由人工事后核查发现。本步骤将事后人工核查制度化为输出前的强制自检。

### Step 5: 降级处理

搜索失败/数据不足时按 degradation-paths.md 降级运行：
  - D1: 搜索不可用 → 标注 SEARCH_UNAVAILABLE
  - D2: 数据稀疏 → 降低要求 + confidence: low
  - D3: 数据矛盾 → 保留矛盾双方
  - D4: 数据时效不足 → 补搜 → 基准库兜底 → [STALE_DATA] 标注且禁入结论位

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

默认按 `references/templates/risk-matrix-template.md` 格式输出 Markdown。
如需自包含 HTML 报告，**以 `references/templates/risk-matrix-template.html` 为底本填充**（内联 CSS）——禁止从零自行设计 HTML/CSS；输出必须保留模板标记注释（G8 验证）。HTML 生成必须遵循 `references/templates/html-assembly.md` 组装协议（Write 分块 + cat 拼接；禁止 Bash heredoc / 依赖 python 渲染）。
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
- 禁止用历史破发率或旧可比估值推断当前首日破发概率——首日判断只能以 Step 1.5 快照为依据
- 三个角色的估值分歧是核心价值——不要强行调和
- 冲突标注优先展示定价节点特有的三角色对立
