# Gatekeeper 冒烟测试记录 — 场景 2（定向更新 targeted-update）

- **测试日期**：2026-08-07（T0 = 2026-08-07，与场景 1 同日午后执行）
- **测试性质**：合规性+端到端测试（扮演 Gatekeeper 系统：ipo-router + finance-scanner）
- **测试用例**：回归基准项目"频准激光"（688826）
- **模拟用户输入**："上次推演 PLAN-20260807-001，频准激光刚披露了新的财务数据（2026 年半年报），帮我重新跑一下财务节点。"
- **外部调用**：真实执行。WebSearch ×4（standard 深度，财务主题限定）。
- **前次制品来源**：`scenario-1.md`（PLAN-20260807-001 的 industry/tech/finance/pricing node_artifact）
- **重要实况发现**：用户称"刚披露 2026 年半年报"，真实搜索确认**正式半年报尚未披露**——最新财务数据为 ①2026-07-30 业绩预告（H1 营收 2.3-2.6 亿、归母净利 9000 万-1.05 亿）②2026Q1 实际数（营收 1.01 亿 +55.21%）。Router 按 N1 不核实用户陈述；finance 节点将"预告≠正式半年报"作为数据状态事实处理（P1 类问题复现）。

---

## 0. ipo-router（路由，禁止分析）

**§0 项目状态预检**：上次推演=PLAN-20260807-001（用户明示 plan_id）；关注重点=财务节点（"重新跑一下财务节点"）；已有材料=新财务数据（用户陈述"2026 半年报"）；项目阶段=已推演后局部更新。

**§1 路径匹配**：对照 analysis-registry.md——trigger"新数据到达"+"局部信息更新"+用户指定节点 → `targeted-update`（path_id=TARGETED-UPDATE，mode=single-node，depth=standard，reuse_previous_artifacts=true）。无"定价/估值/快速"关键词，不触发 pricing-focused/quick-scan；非首次，不默认 full-chain。

**产出分析计划单（§S1 合规）**：

```yaml
analysis_plan:
  plan_id: "PLAN-20260807-002"
  project_name: "频准激光"
  mode: "targeted-update"
  path_id: "TARGETED-UPDATE"
  nodes: [finance]
  depth: "standard"
  previous_run_id: "PLAN-20260807-001"
  previous_artifacts:
    industry:
      plan_id: "PLAN-20260807-001"
      generated_at: "2026-08-07T10:20:00+08:00"
      overall_rating: "cautious"
      key_finding: "量子激光器细分国产龙头（国内市占率16.85%）卡位高景气赛道，但核心市场仅约1亿美元量级且收入深度绑定科研经费，天花板与需求结构是行业定位的两大硬伤。"
    tech:
      plan_id: "PLAN-20260807-001"
      generated_at: "2026-08-07T10:50:00+08:00"
      overall_rating: "cautious"
      key_finding: "技术路线差异化经国家级项目验证、无实际诉讼，但15%核心部件依赖美日进口、专利组合偏外围改进、研发绝对投入仅为龙头1/6，'全链条自研'叙事存在可攻击缝隙。"
  existing_materials: ["2026年半年报（用户陈述，实况为业绩预告+Q1实际数）"]
  generated_at: "2026-08-07T14:00:00+08:00"
```

计划单无分析结论字段（N1 合规）。按链式调用规则移交 finance-scanner——**唯一被触发节点**；tech-scanner、pricing-scanner 未调用。

---

## 1. 节点 3：finance-scanner（targeted-update，depth=standard）

**Step 0 时间锚定**：T0=2026-08-07；查询带"2026/最新"限定词；财务/经营类阈值 ≤18 个月（≥2025-02）；每条证据填 data_as_of。

**Step 1 加载角色与上游制品**：三角色文件已读；industry + tech 制品经 previous_artifacts 引用（key_finding 作为分析上下文：收入绑定科研经费→回款节奏；天花板质疑→H1 增速解读）。**本轮 4 轮搜索全部为财务主题**（业绩预告、应收/现金流、毛利率/存货、分红补流争议），未发起任何行业规模/技术/专利/估值类查询。

**Step 2 三角色分析**（standard：每角色 3 条，共 9 条；搜索轮次：pre-ipo 2 轮 / buy-side 2 轮 / media 1 轮复用，合计 4 轮覆盖三角色主题）。

### Pre-IPO 投资人（3 条）

**RISK-finance-pre-ipo-investor-001**（high）：H1 预告增速中枢较 Q1 实际显著回落，上市后首份定期报告即面临"高增长叙事打折"。
- evidence：业绩预告（2026-07-30 公告，data_as_of=2026-06）：H1 营收 2.3-2.6 亿（+27.58%~+44.22%）、归母净利 9000 万-1.05 亿（+26.93%~+48.08%）；Q1 实际营收 +55.21%（data_as_of=2026-03）。隐含 Q2 营收增速约 +12%~+38%（中枢约 25%），较 Q1 的 55% 明显降速。inline_summary 已含上述数值；URL：163.com/stockstar 业绩预告报道（public，captured 2026-08-07）。
- rationale：解禁退出定价依赖成长叙事持续性；首份财报落在预告下限将压缩退出估值。
- potential_impact：解禁期估值折价；suggested_response：跟踪正式半年报落点与 Q3 订单。

**RISK-finance-pre-ipo-investor-002**（medium）：应收回款质量恶化直接威胁退出期资产质量。
- evidence：2025 年末逾期未回款比例 79.40%；截至 2026-03-31 各期期后回款比例 95.47%→88.21%→24.97%；应收周转 13.33→6.37 次（data_as_of=2025-12/2026-03；来源：上交所注册稿+权衡财经报道）。
- rationale：退出测算需对减值做 haircut；科研经费拨付节奏（引 industry 制品）决定回款上限。

**RISK-finance-pre-ipo-investor-003**（low）：预告区间宽（净利 ±8%）且非审计数据，正式半年报未披露，退出测算锚点不稳。
- evidence：截至 T0 仅业绩预告（data_as_of=2026-06），正式半年报未披露（多来源确认，as_of 2026-08）。

### 买方（3 条）

**RISK-finance-buy-side-001**（high）：盈利质量结构性指标连续三年下行——净利率 40.93%→39.61%→38.15%，加权 ROE 68.56%→47.32%→39.03%；毛利率 69.21% 虽维持高位（约同行 2 倍），但增长质量边际走弱，与 H1 增速中枢下移互证。
- evidence：新浪"鹰眼预警"（data_as_of=2026-05）；Q1 毛利率 69.21%（data_as_of=2026-03）；预告增速（data_as_of=2026-06）。
- rationale：买方关心 3-5 年持有逻辑——ROE 趋势性下行是高毛利叙事的最大裂缝；可持续性判断：结构性（费用扩张+规模效应递减）。

**RISK-finance-buy-side-002**（medium，conflicting_sources: true）：现金流口径矛盾部分消解但未闭合——新数据显示 2025 全年经营现金流净额 1.91 亿＞净利 1.59 亿（经济导报，data_as_of=2025-12），支持公司宣传口径；但 2025H1 净现比仅约 36%（差额 -4540.86 万，data_as_of=2025-06）与 2026Q1 经营现金流仅 145.92 万（vs 净利 2794 万，data_as_of=2026-03）显示半年度尺度上现金流与利润持续背离。
- 处理：场景 1 的 D3 冲突（宣传口径 vs 港湾商业观察）经新数据**部分消解**——全年口径成立，但背离从"全年"收窄为"半年度/季度"问题，D3 标注保留。
- rationale：买方以 TTM 现金流验证盈利质量，半年度背离决定"利润是纸面还是现金"。

**RISK-finance-buy-side-003**（medium）：资产负债表质量待验证——存货 2.49 亿、周转 0.56-0.66 次（同行约 1.97 次）；应收 6653.96 万持续攀升；业绩预告不含资产负债表数据，正式半年报是关键验证点。
- evidence：存货/应收数据（data_as_of=2025-12）；问询回复设"关于存货"专章（data_as_of=2026-04）。

### 媒体（3 条）

**RISK-finance-media-001**（high）："左手分红右手补流"叙事在半年报披露窗口再发酵。
- evidence：2025 年分红 2000 万（实控人张磊持股 62.04%，个人分得约 1240 万）；账上货币资金 2.38 亿+交易性金融资产 1.15 亿、零有息负债，仍募资 2.5 亿补流（data_as_of=2025-12；报道 as_of 2026-08：观察者网、权衡财经、凤凰网等多篇在发）。
- 媒体标题模拟："账上躺 3.5 亿还要募 2.5 亿补流？频准激光半年报亮出家底"。
- 传播路径：财经媒体 IPO 解读栏目 → 社交媒体"打新"话题 → 上市后首份财报二次发酵。

**RISK-finance-media-002**（medium）："收入高增长、回款靠催收"——应收逾期 79.40%+期后回款 24.97% 是现成质疑素材，与历史 Q4 收入占比质疑（场景 1 已记录）可拼接为"收入质量"连续报道。
- evidence：同 fin-preipo-002 数据源（data_as_of=2026-03/2025-12）；标题模拟："频准激光高增长背后：近八成应收逾期未回"。

**RISK-finance-media-003**（low）：业绩预告披露于申购前一周（2026-07-30），时点易被解读为"发行护航"；若正式半年报落在下限，"上市即变脸"标题现成。
- evidence：预告公告日 2026-07-30 vs 申购日 2026-08-07（data_as_of=2026-07/08）。

### Step 2.5 前瞻信号（3 条 high 全配，G1.5）

**fin-preipo-001**（category=profit，window 4-8Q→2026Q4-2027Q2，T2）：正向①正式半年报营收/净利落在预告中枢以上（≥2.45 亿/≥9750 万）②2026Q3 营收同比增速回升至 ≥40%；负向①半年报落在下限（≤2.3 亿/≤9000 万）②连续 2 个季度同比增速 <25%；WMGR：半导体设备领域收入放量对冲科研经费节奏，Q3-Q4 订单转化可验证。

**fin-buy-001**（category=profit，window 4-8Q，T2）：正向①2026 全年净利率企稳 ≥37%②毛利率维持 67%-70% 区间且与可比公司同向；负向①单季净利率跌破 35%②毛利率同比降 ≥5pp 或独立背离行业；WMGR：费用管控+高毛利新品占比提升。

**fin-media-001**（category=regulatory，window 2-4Q→2026Q4-2027Q1，T3）：正向①正式半年报披露货币资金+理财下降、募投项目实质投入②公司公告明确补流用途进度；负向①半年报显示理财余额不降反升②再度分红或新增大额理财；WMGR：募集资金按披露用途快速投入并形成可验证产出。

### Step 3 汇聚与冲突标注

- **共识风险（≥2 角色）**：①盈利质量边际走弱（增速中枢下移+净利率/ROE 下行，pre-ipo+buy-side）；②应收/回款质量恶化（三角色）。
- **冲突**：现金流质量——全年 OCF 1.91 亿＞净利（2025-12）vs 半年度净现比 36%/Q1 仅 146 万 → 非矛盾而是"尺度差"：conflict_type=interpretation，D3 标注保留（conflicting_sources: true 于 fin-buy-002）。
- 无角色等级差 ≥2 档 → G1.7 未触发。

### Step 3.5 传染检测

- **C5（财务→定价）信号对**：应收/营收比值连续 2 期攀升（✔ 触发：887 万→6654 万、周转 13.33→6.37，as_of 2025-12/2026-03）；扣非转负（✘ 预告 +28.49%~+51.16%）；盈利低于招股书预测（N/A，预告为增长）。→ **1 条负向 → 🟡 弱传染，`contagion_alert: watch`**（与场景 1 结论一致，未升级）。
- **C1（行业→财务）**：毛利率 69.21% 远高于行业（正向）；市占率/大客户采购引用 industry 制品不重新判断（制品 staleness 见第 3 节备注）。→ 未激活。
- 负向通道=1 → 叠加因子 1.0×（§6）。

### Step 4 质量门禁（G1-G7 逐项）

| 门禁 | 结果 | 说明 |
|------|------|------|
| G1 角色完备 | ✅ | standard：3 角色 ×3 条 ≥3 |
| G1.5 信号完备 | ✅ | 3 条 high（fin-preipo-001/fin-buy-001/fin-media-001）全部 ≥2正+≥2负+≥1 WMGR，含 time_window/priority_tier |
| G1.6 交叉信号一致性 | ✅（无冲突） | 无 T1 vs T3 反向信号对 |
| G1.7 异议加权 | ✅（未触发） | 同一命题无 ≥2 档分歧 |
| G2 来源多样 | ✅ | 角色内 URL 无超 2 次复用（业绩预告 163/stockstar 两源分流） |
| G3 证据内联 | ✅ | 9/9 inline_summary 非空 |
| G4 枚举合规 | ✅ | node=finance、role/risk_level/id 全部合规 |
| G5 角色锚定 | ✅ | pre-ipo 谈退出/解禁、buy-side 谈持有质量/TTM、media 谈标题/传播，无视角漂移 |
| G6 自包含 | ✅ | 无本地路径/裸 URL |
| G7 时效合规 | ✅（无触发） | 全部证据 as_of 2025-06~2026-08：财务/经营类 ≤18 个月 ✅；预告/Q1 数据 as_of 2026-03/06 距 T0 ≤5 个月；分红/货币资金 as_of 2025-12 ✅。无超期项、无"真 URL+旧数据" |

### Step 5 降级处理

- **D3 ×1**：现金流口径矛盾（fin-buy-002，conflicting_sources: true；全年 vs 半年度双口径保留，不自动裁决）。场景 1 的同主题 D3 经新数据部分消解（全年口径获证），标注延续。
- D1/D2/D4 未触发；search_quality=rich；confidence 未降级。

### 节点制品（§S2 合规）

```yaml
node_artifact:
  node: "finance"
  generated_at: "2026-08-07T14:45:00+08:00"
  plan_id: "PLAN-20260807-002"
  summary:
    overall_rating: "cautious"
    key_finding: "新财务数据（2026H1预告+Q1实际）确认增收增利无造假级信号，但隐含Q2增速中枢较Q1腰斩、净利率/ROE连续三年下行、半年度尺度现金流与利润持续背离、应收逾期率79.4%——盈利'量增质减'是本次更新的核心判断；全年现金流口径获新数据支持，场景1的D3冲突部分消解。"
  role_consensus:
    agreed_risks: ["盈利质量边际走弱（增速中枢下移+净利率/ROE下行）", "应收/回款质量恶化（逾期79.4%、期后回款24.97%）"]
    conflicts:
      - topic: "经营现金流质量的度量尺度"
        pre_ipo_view: "回款依赖经费拨付，退出期减值风险（medium）"
        pre_ipo_basis: "2025年末逾期未回款79.40%（as_of 2025-12）"
        buy_side_view: "全年口径成立但半年度背离持续（medium，D3保留）"
        buy_side_basis: "2025全年OCF 1.91亿>净利（as_of 2025-12）vs 2025H1净现比36%、2026Q1 OCF仅145.92万（as_of 2025-06/2026-03）"
        media_view: "'高增长低回款'连续报道素材现成（medium）"
        media_basis: "逾期79.40%+期后回款24.97%（as_of 2026-03）"
        conflict_type: "interpretation"
  contagion_alert: "watch"
  contagion_detail: "C5财务→定价：应收/营收连续2期攀升（1条负向信号）→弱传染；叠加通道数=1，放大因子1.0×（与PLAN-20260807-001一致，未升级）"
  data_freshness:
    search_quality: "rich"
    key_data_gaps: ["正式2026半年报未披露（仅业绩预告），资产负债表科目（存货/应收/货币资金）2026-06期数据缺失", "业绩预告无审计背书"]
```

### 更新后 artifact_freshness（本次推演完成后）

```yaml
artifact_freshness:
  industry: {generated_at: "2026-08-07T10:20:00+08:00", status: stale, age_days: 0}
  tech:     {generated_at: "2026-08-07T10:50:00+08:00", status: stale, age_days: 0}
  finance:  {generated_at: "2026-08-07T14:45:00+08:00", status: fresh, age_days: 0}
  pricing:  {generated_at: "2026-08-07T11:50:00+08:00", status: stale, age_days: 0}
```

> 备注：按 targeted-update 语义，未重跑节点标 stale（其制品基于 PLAN-20260807-001 的旧输入）。但 artifact-schemas.md 的新鲜度规则仅定义 `age_days <= 3 且 status=fresh → fresh`，本例三节点 age_days=0 同日却标 stale——规则未覆盖"被新计划单取代（superseded）"场景，见问题清单 P8。

---

## 2. 检查点结果汇总

| # | 检查点 | 结果 | 说明 |
|---|--------|------|------|
| 2-1 | Router 匹配 targeted-update（path_id=TARGETED-UPDATE） | ✅ | "新数据到达"+"用户指定节点"双 trigger 命中；mode/path_id/depth=standard 与 registry 一致 |
| 2-2 | 计划单含 previous_run_id = PLAN-20260807-001 | ✅ | 见 §0 计划单 |
| 2-3 | previous_artifacts 含 industry + tech（引用前次制品） | ✅ | 两份制品完整引用（plan_id/generated_at/rating/key_finding） |
| 2-4 | 仅 finance-scanner 被触发（tech/pricing 未调用） | ✅ | nodes=[finance]，全程无 tech/pricing 节点启动、无定价/技术类搜索 |
| 2-5 | finance 引用上游制品，未重新搜索行业/技术数据 | ✅ | 4 轮搜索全部为财务主题；行业结论（科研经费依赖→回款节奏）仅作引用 |
| 2-6 | 制品新鲜度更新（finance=fresh，其余=stale） | ✅ | 见 artifact_freshness；pricing 一并标 stale（规则语义问题见 P8） |

**总计：6/6 检查点通过。**

---

## 3. 附加观察

1. **data_as_of 规范**：9 条证据全部填写数据所属期且与抓取时间区分（如业绩预告报道 captured 2026-08-07、data_as_of=2026-06；分红数据 data_as_of=2025-12 而非报道期 2026-08）。无"抓取时间冒充所属期"。G7 未触发（无超期项）——本次更新数据天然新，未构成 G7 压力测试。
2. **G7 触发记录**：本场景 0 次触发（全部证据 as_of ≥2025-06，财务类 18 个月阈值内）。G7 的实弹检验仍依赖场景 1 的 2 次触发记录。
3. **百分比概率四要件**：本次角色概率判断全部使用高/中/低三档；条目中出现 0 处百分比形式的概率表述（增速、逾期率等为事实数据非概率判断，附数值+所属期+来源），无违规。
4. **用户陈述失真复现**：用户称"半年报已披露"，实况仅业绩预告——场景 1 问题 P1（Router 无陈述校正通道）第二次复现，升级为高频问题。本次在 existing_materials 字段做了事实备注，属于 schema 外沿用，非正式校正机制。
5. **D3 消解路径首次实测**：场景 1 的现金流 D3 冲突经新数据部分消解（全年口径获证、背离收窄为半年度尺度）——验证了"定向更新可收敛前次降级标注"的设计意图，但 degradation-paths.md 未定义 D3 的"消解/收窄"状态转移，本次靠人工判断记录（见 P9）。
6. **传染状态跨计划单延续**：C5 watch 从 PLAN-20260807-001 延续至 -002，信号对复测结果一致（仍 1 条负向），未升级未解除——传染矩阵未定义 watch 的解除条件（见 P10）。

---

## 4. 执行中发现的技能文件问题（新增；P1-P7 见场景 1）

- **P8（中）artifact_freshness 规则未覆盖"superseded"语义**。规则仅按 age_days≤3 判 fresh；targeted-update 同日重跑单一节点后，其余节点 age_days=0 却被要求标 stale，规则与 targeted-update 语义冲突，执行体只能二选一。建议增加规则："制品关联的 plan_id 非最新推演 plan_id 时，status=stale（superseded），与 age_days 无关"。
- **P9（低）降级标注无状态转移定义**。D3 冲突在新数据到达后可"消解/收窄/维持"，degradation-paths.md 未定义状态转移与记录格式，跨计划单追踪降级状态靠执行体自觉。建议为 D3/D4 增加 `resolution: resolved|narrowed|open` 字段。
- **P10（低）contagion_alert: watch 无解除条件**。传染矩阵 §4 定义了升级路径（watch→active→critical），未定义负向信号消失后 watch 如何解除，导致 watch 状态只能无限延续。建议增加"连续 2 次推演信号对全正向 → 解除 watch"。
- **P1 复现升级（中→高）**：用户陈述与公开实况不符（"半年报已披露" vs 仅业绩预告）第二次出现，Router 仍无校正通道；建议按场景 1 P1 方案在 S2 增加 `input_correction` 字段并提升优先级。
