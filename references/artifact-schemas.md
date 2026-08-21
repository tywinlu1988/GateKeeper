# 制品 Schema 定义（Artifact Schemas）

> 单一事实源。所有阶段间传递的 YAML 制品格式仅在此文件中定义。

## S1: 分析计划单（Analysis Plan）

```yaml
# Schema: analysis_plan
# 产出者：ipo-router
# 消费者：所有 scanner 节点
analysis_plan:
  plan_id: "PLAN-{YYYYMMDD}-{3位序号}"    # 必填，格式强制
  project_name: ""                          # 必填
  mode: "full-chain|targeted-update|pricing-focused|quick-scan|monitoring-run"  # 必填，枚举
  path_id: "FULL-CHAIN|TARGETED-UPDATE|PRICING-FOCUSED|QUICK-SCAN|MONITORING-RUN"  # 必填，枚举，对应 analysis-registry
  nodes: []                                 # 必填，枚举值：industry|tech|finance|pricing
                                            # monitoring-run 模式允许空数组（不触发分析节点）
  depth: "deep|standard|quick"              # 必填，枚举；monitoring-run 填 "quick" 占位
  previous_run_id: null                     # 可选，关联上次推演
  previous_artifacts: {}                    # 可选，已有节点制品的引用
  existing_materials: []                    # 可选，用户提供的材料路径列表
  user_stated_status: ""                    # 可选，用户陈述的项目状态要点（原话）。仅作路由输入，不作事实依据；
                                            # 节点发现实况不符时在 S2 data_freshness.status_correction 标注
  generated_at: ""                          # 必填，ISO 8601

# 枚举约束
# mode: 仅允许 full-chain, targeted-update, pricing-focused, quick-scan
# nodes[]: 每个元素仅允许 industry, tech, finance, pricing
# depth: 仅允许 deep, standard, quick
# plan_id 格式: PLAN-YYYYMMDD-NNN（NNN 为 3 位零填充数字）
```

## S2: 节点结论制品（Node Artifact）

```yaml
# Schema: node_artifact
# 产出者：每个 scanner 节点
# 消费者：下游 scanner 节点（按链路顺序）
node_artifact:
  node: "industry|tech|finance|pricing"     # 必填，枚举
  generated_at: ""                           # 必填，ISO 8601
  plan_id: ""                                # 必填，关联分析计划单
  summary:
    overall_rating: "favorable|neutral|cautious|red-flag"  # 必填，枚举
    key_finding: ""                          # 必填，一句话核心判断
  role_consensus:
    agreed_risks: []                         # 三角色共识风险
    conflicts:                               # 角色间冲突
      - topic: ""
        pre_ipo_view: ""
        pre_ipo_basis: ""                    # 该角色观点的数据/逻辑依据
        buy_side_view: ""
        buy_side_basis: ""
        media_view: ""
        media_basis: ""
        conflict_type: "assumption|weighting|interpretation"  # 枚举
  contagion_alert: "none|watch|active|critical"  # 可选，传染检测结果（Step 3.5，见 contagion-matrix.md §4）
  superposition:                              # 可选，传染叠加（≥2 通道同时负向时填写，见 contagion-matrix.md §6）
    active_channels: []                       # 负向激活通道 ID 列表（如 ["C2","C5"]）
    alert_level: "watch|active|critical"      # v0.5.0 起定性化：通道数 1→watch、2-3→active、≥4→critical；
                                              # 数值放大因子（1.5×/2.0×）无实证校准，已弃用
  search_log:                                 # 必填，每角色搜索留痕（审计依据，G1 检查）
    - role: "pre-ipo-investor|buy-side|media"
      queries:
        - q: ""                               # 实际发出的查询词
          searched_at: ""                     # ISO 8601
          hits: 0                             # 有效数据点数
  market_snapshot: {}                         # pricing 节点必填（Step 1.5 八项必查表，每项含 as_of 与结果）；
                                              # 其他节点省略。缺失 → G1 不通过
  data_freshness:
    search_quality: "rich|adequate|sparse"   # 必填，枚举
    key_data_gaps: []                        # 缺失的关键数据点
    status_correction: ""                    # 可选，节点搜索发现的项目实况与用户陈述不符时的校正说明

# 枚举约束
# node: 仅允许 industry, tech, finance, pricing
# overall_rating: 仅允许 favorable, neutral, cautious, red-flag
# conflict_type: 仅允许 assumption, weighting, interpretation
# search_quality: 仅允许 rich, adequate, sparse
# contagion_alert: 仅允许 none, watch, active, critical
```

## S3: 风险矩阵条目（Risk Entry）

```yaml
# Schema: risk_entry
# 产出者：每个 scanner 节点（每个角色产出多条）
# 消费者：最终用户（内核风险清单 / 发行定价备忘录 / 督导期监控表；critical+unpriced 条目另生成 S5 预测记录）
risk_entry:
  id: "RISK-{node}-{role}-{3位序号}"        # 必填，格式强制
  node: "industry|tech|finance|pricing"      # 必填，枚举
  role: "pre-ipo-investor|buy-side|media"    # 必填，枚举
  risk_level: "critical|high|medium|low"     # 必填，枚举
  claim: ""                                   # 必填，一句话风险主张
  evidence:
    primary_source:
      source_type: "search|baseline|material"   # 必填，枚举：实时搜索 | knowledge/ 基准库 | 用户提供材料
      url: ""                                # 可选（搜索不可用时可为空）
      access_type: "public|internal|paywall"  # 必填，枚举
      captured_at: ""                         # 必填，ISO 8601（抓取时间）
      data_as_of: ""                          # 必填，YYYY-MM 或 YYYY-Qn（数据所属期）
    inline_summary: ""                        # 必填，内联证据摘要
    key_data_points:                          # 必填（至少1条）
      - metric: ""                            # 必填
        value: ""                             # 必填
        comparison: ""                        # 可选
        source_ref: ""                        # deep 必填 / standard·quick 可选，指向 search_log 中对应查询（如 "buy-side#2"）；
                                            # 无法追溯到任何已执行查询时填 [UNLOGGED]
  rationale: ""                               # 必填，为什么这个角色关注
  potential_impact: ""                        # 必填，风险发生的影响推演
  suggested_response: ""                      # 必填，保荐机构可执行动作（含动词与对象；禁止"关注XX""加强管理"等空泛表述）
  priced_in: "priced-in|partially|unpriced|unknown"  # 必填（v0.5.0），市场定价状态：219x 已隐含的预期属于 priced-in；
                                              # 判定必须附推导依据（如"发行 PE 隐含 35%+ 增速，增速放缓已被定价"）
  response_owner: "保荐代表人|内核|发行人|资本市场部|督导团队|联合体"  # 必填（v0.5.0），应对动作责任归属
  response_deadline: ""                       # 必填（v0.5.0），如"问询回复前|发行前|上市后6个月"
  signal_watchlist:                           # 可选，risk_level=critical|high 时必填（见 signal-watchlist.md §1 模板）
    risk_statement: ""
    time_window: {}
    priority_tier: "T1|T2|T3"
    positive_signals: []
    negative_signals: []
    what_must_go_right: []
    execution_proxy: {}                       # 可选，管理层执行力代理（不计分）

# 枚举约束
# node: 仅允许 industry, tech, finance, pricing
# role: 仅允许 pre-ipo-investor, buy-side, media
# risk_level: 仅允许 critical, high, medium, low
# id 格式: RISK-{node}-{role}-NNN（NNN 为 3 位零填充数字）
#   {role} 段必须等于 role 字段的完整枚举值：pre-ipo-investor | buy-side | media。
#   禁止缩写（RISK-pricing-pre-ipo-001 违规；合法为 RISK-pricing-pre-ipo-investor-001）。
# access_type: 仅允许 public, internal, paywall
# priced_in: 仅允许 priced-in, partially, unpriced, unknown。
#   全部 unknown 视为 G1 不通过；priced-in 判定必须附推导依据（G5）。
# source_type: 仅允许 search, baseline, material。
#   baseline（knowledge/ 基准库）证据的使用限制见 quality-gates.md G7——
#   禁止单独进入执行摘要/TOP 风险/评级依据，且引用前必须在 search_log 中有对应的实时搜索尝试。
# data_as_of: 数据内容所描述的时间点/期间（YYYY-MM 或 YYYY-Qn），
#   禁止以 captured_at（抓取时间）冒充。2023 年研报今天被抓取，
#   data_as_of 仍须填 2023 年对应期。历史案例引用须如实标注其发生期。
#   聚合多篇统计时，data_as_of 填统计期末（非报道日）。
#   时效阈值由 quality-gates.md G7 定义。
```

## S5: 预测记录（Prediction Record，v0.7.0 新增）

<!-- 编号说明：制品新鲜度追踪（Artifact Freshness）为历史上未编号的第四类制品，故本 schema 顺延编号 S5 -->

```yaml
# Schema: prediction_record
# 产出者：pricing 节点（Step 4.7，终端节点统一汇总 P1/P2/P3）
# 消费者：最终报告「预测与验证计划」区块；predictions.yaml（artifacts/，只增不改）
# 设计依据：事前预测可靠性是项目核心定位——预测必须在结果出来之前以可评分格式锁定，
#   否则永远无法校准（天气预报原则：不能在下雨后才修正观测数据）。
prediction_record:
  prediction_id: "P-{plan_id}-{3位序号}"    # 必填，格式强制
  type: "P1|P2|P3"                          # 必填，枚举：P1 首日方向 / P2 回归方向 / P3 风险兑现
  claim: ""                                  # 必填，可证伪陈述（二元或分类），禁止含糊表述
  forecast: 0.15                             # scored=true 必填，点估计概率（0-1）；允许附 range 字段表达不确定度
  range: ""                                  # 可选，如 "0.10-0.20"
  base_rate_ref: ""                          # 必填，锚定的 B 型基准（基准库条目或快照项 + 数值）
  deviation_rationale: ""                    # 必填，一句话偏离理由（因何相对基准上调/下调）
  horizon: "listing_day|6m|12m|event_driven" # 必填，枚举，决定报告区块的分类
  resolution_criteria:
    source: ""                               # 必填，判定数据源（如"东财行情"）
    rule: ""                                 # 必填，判定规则（如"上市首日收盘价 < 发行价 判真"）
  resolution_window: ""                      # 必填，验证时点/窗口（如"上市日 T""上市满 6 个月"）
  scored: true                               # 必填；false 合法但须附 unscored_reason
  unscored_reason: ""                        # scored=false 时必填
  linked_risk_id: ""                         # P3 必填，指向内核清单条目 RISK-{node}-{role}-{seq}

# 枚举约束
# type: 仅允许 P1, P2, P3
#   P1 首日方向：horizon=listing_day，每次推演强制 1 条；格式按基准率信息量分条件（v0.7.1；阈值量化 v0.7.2）——
#     **基准率退化判定（唯一标准）：近 12 个月市场首日破发率 <5% 或 >95%**（方向预测技巧分趋零）
#     基准率退化（如科创板零破发 regime）→ regime 复述 + 幅度带预测
#     （claim 为"首日涨幅相对 regime 均值：显著低于/持平/显著高于"）；
#     基准率未退化（如港股 18C 首日破发率 ~25-30%）→ 保留破发/平盘/上涨三分类方向预测
#   P2 回归方向：上市后价格回归区间带，horizon=6m 或 12m，每次推演强制 ≥1 条；
#     判定参照分 regime（v0.8.0，依据 ipo-cohort-backtest F4）——
#     热 regime（首日破发率 <5%）→ 相对**首日收盘价** <80% 判真（热 regime 破发行价无区分度：24/25 仍在发行价上方）；
#     非热 regime → 相对**发行价** <80% 判真（冷 regime 破发行率基准 40%）
#   P3 风险兑现：内核清单中 critical + unpriced 条目逐条二值化（兑现/未兑现），horizon 逐条定
# horizon: 仅允许 listing_day, 6m, 12m, event_driven
# forecast 为 C 型主观判断预测——数值概率只允许出现在本 schema 与报告「预测与验证计划」区块（G5 概率语义分型）
# predictions.yaml 只增不改：已落盘的预测记录禁止事后修改，判定结果写入独立的 resolutions 记录
```

## S6: 判定记录（Resolution Record，v0.8.0 新增）

```yaml
# Schema: resolution_record
# 产出者：事件驱动判定 / resolution-sweep（流程见 references/validation-protocol.md）
# 消费者：评分与差距分析（gap-analysis）；算法卡健康报告
resolution_record:
  resolution_id: "RES-{prediction_id}"       # 必填，格式强制
  prediction_id: "P-{plan_id}-{3位序号}"      # 必填，指向 S5 记录
  verdict: "true|false|insufficient|expired" # 必填，枚举
  resolved_at: ""                            # 必填，ISO 8601 判定时间
  resolution_source: ""                      # 必填，判定数据来源（如"东财行情""披露易招股书"）
  observed_value: ""                         # 必填，实际观测值
  criteria_check: ""                         # 必填，"规则原文 vs 实际观测值"的显式比较说明
  brier: 0.0                                 # verdict=true/false 且 scored=true 时必填，(forecast − outcome)²，真=1 假=0
  base_rate_brier: 0.0                       # 同上，regime 基准率预测的 Brier（技巧分 = 1 − brier/base_rate_brier）
  note: ""                                   # insufficient/expired 必填原因

# verdict 枚举
#   true / false：按 resolution_criteria.rule 判定成立 / 不成立
#   insufficient：判定窗口到达但数据不足（附原因；禁止临时改口径后判定）
#   expired：预测前提失效（如 P1 regime_note 重锚条款触发——基准率已跨越退化阈值，原预测作废不计分）
# resolutions.yaml 只增不改；expired/insufficient 不计分但计入覆盖率统计
```

## 制品新鲜度追踪（Artifact Freshness）

```yaml
# Schema: artifact_freshness
# 产出者：每次推演完成后更新
artifact_freshness:
  industry:
    generated_at: ""                          # ISO 8601 或 null
    status: "fresh|stale|not_run"             # 枚举
    age_days: 0                               # 整数，not_run 时为 null
  tech:
    generated_at: ""
    status: "fresh|stale|not_run"
    age_days: 0
  finance:
    generated_at: ""
    status: "fresh|stale|not_run"
    age_days: 0
  pricing:
    generated_at: ""
    status: "fresh|stale|not_run"
    age_days: 0

# 新鲜度规则
# generated_at = null → not_run
# status 判定（按优先级）：
#   1. 本次推演中重跑过的节点 → fresh（age_days 从最新 generated_at 计）
#   2. targeted-update 中未被重跑的节点 → stale（语义为"非本次实测"，不论 age_days）
#   3. age_days <= 3 → fresh
#   4. age_days > 3 → stale
# 注：stale 有两种成因——"时间过期"（age_days 超期）与"被新推演取代"（superseded）。
#     报告中建议标注成因：stale(age) / stale(superseded)。
```
