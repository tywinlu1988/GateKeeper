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
  mode: "full-chain|targeted-update|pricing-focused|quick-scan"  # 必填，枚举
  path_id: ""                               # 必填，对应 analysis-registry 中的 path_id
  nodes: []                                 # 必填，枚举值：industry|tech|finance|pricing
  depth: "deep|standard|quick"              # 必填，枚举
  previous_run_id: null                     # 可选，关联上次推演
  previous_artifacts: {}                    # 可选，已有节点制品的引用
  existing_materials: []                    # 可选，用户提供的材料路径列表
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
        buy_side_view: ""
        media_view: ""
        conflict_type: "assumption|weighting|interpretation"  # 枚举
  data_freshness:
    search_quality: "rich|adequate|sparse"   # 必填，枚举
    key_data_gaps: []                        # 缺失的关键数据点

# 枚举约束
# node: 仅允许 industry, tech, finance, pricing
# overall_rating: 仅允许 favorable, neutral, cautious, red-flag
# conflict_type: 仅允许 assumption, weighting, interpretation
# search_quality: 仅允许 rich, adequate, sparse
```

## S3: 风险矩阵条目（Risk Entry）

```yaml
# Schema: risk_entry
# 产出者：每个 scanner 节点（每个角色产出多条）
# 消费者：最终用户（风险矩阵报告）
risk_entry:
  id: "RISK-{node}-{role}-{3位序号}"        # 必填，格式强制
  node: "industry|tech|finance|pricing"      # 必填，枚举
  role: "pre-ipo-investor|buy-side|media"    # 必填，枚举
  risk_level: "critical|high|medium|low"     # 必填，枚举
  claim: ""                                   # 必填，一句话风险主张
  evidence:
    primary_source:
      url: ""                                # 可选（搜索不可用时可为空）
      access_type: "public|internal|paywall"  # 必填，枚举
      captured_at: ""                         # 必填，ISO 8601
    inline_summary: ""                        # 必填，内联证据摘要
    key_data_points:                          # 必填（至少1条）
      - metric: ""                            # 必填
        value: ""                             # 必填
        comparison: ""                        # 可选
  rationale: ""                               # 必填，为什么这个角色关注
  potential_impact: ""                        # 必填，风险发生的影响推演
  suggested_response: ""                      # 必填，建议应对策略

# 枚举约束
# node: 仅允许 industry, tech, finance, pricing
# role: 仅允许 pre-ipo-investor, buy-side, media
# risk_level: 仅允许 critical, high, medium, low
# id 格式: RISK-{node}-{role}-NNN（NNN 为 3 位零填充数字）
# access_type: 仅允许 public, internal, paywall
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
# age_days <= 3 且 status = fresh → fresh
# age_days > 3 → stale
# generated_at = null → not_run
```
