# Gatekeeper — Pre-IPO 保荐承销外部视角推演 Skill 包

> **设计日期**：2026-07-30
> **状态**：设计完成，待实现计划
> **一句话**：为科创板 IPO 保荐承销机构提供 Pre-IPO 投资人、上市后买方、舆论三个外部视角的结构化推演，覆盖全链路四个关键节点。

---

## 1. 产品定位

### 1.1 目标用户

从事科创板 IPO 保荐和发行的投资机构（券商投行部）。

### 1.2 核心场景

- **项目开始前的全链路推演**：在正式启动 IPO 流程前，用三个外部视角系统性地压力测试项目
- **过程中多节点的更新细化**：随项目推进、新数据到达，对特定节点进行局部更新推演

### 1.3 核心价值

帮保荐机构跳出内部视角，提前看到 Pre-IPO 投资人、上市后买方、舆论三方可能提出的挑战，减少"内核会上被问倒""反馈回复中被动""发行后破发被质疑"的风险。

---

## 2. 整体架构

### 2.1 三层分离

```
AGENTS.md                              ← 全局编排 + 非协商条款 + 输出模板
│
├── .claude/skills/                    ← Skill 执行层（怎么做）
│   ├── ipo-router/SKILL.md
│   ├── industry-scanner/SKILL.md
│   ├── tech-scanner/SKILL.md
│   ├── finance-scanner/SKILL.md
│   └── pricing-scanner/SKILL.md
│
├── references/                        ← 知识/规则层（知道什么）
│   ├── analysis-registry.md
│   ├── artifact-schemas.md
│   ├── roles/
│   │   ├── pre-ipo-investor.md
│   │   ├── buy-side.md
│   │   └── media-watchdog.md
│   ├── templates/
│   │   └── risk-matrix-template.md
│   └── guardrails/
│       ├── non-negotiables.md
│       ├── quality-gates.md
│       └── degradation-paths.md
│
└── knowledge/                         ← 未来 A 方案知识库插槽（当前空）
    ├── industry-benchmarks/
    ├── case-library/
    └── policy-tracker/
```

### 2.2 编排模式

- **入口**：Router 负责项目状态评估、路径匹配、分析计划单生成
- **全链路**：行业 → 技术 → 财务 → 定价，顺序执行，制品传递
- **局部更新**：Router 根据用户指定路由到单个节点，复用已有上游制品
- **节点内部**：三角色并行分析（共享底层搜索数据，独立解读），汇聚标注冲突

### 2.3 当前阶段：B 方案（实时搜索驱动）

所有数据通过实时搜索获取。knowledge/ 目录预留给未来 A 方案（内建知识库）。

---

## 3. 分析路径注册表

```yaml
# references/analysis-registry.md

paths:
  full-chain:
    trigger: "首次全链路推演、项目初期尽调完成"
    nodes: [industry, tech, finance, pricing]
    mode: sequential
    depth: deep

  targeted-update:
    trigger: "新数据到达、局部信息更新、反馈回复后重新评估"
    nodes: ["用户指定"]
    mode: single-node
    reuse_previous_artifacts: true

  pricing-focused:
    trigger: "临近发行窗口、估值讨论"
    nodes: [industry, pricing]
    mode: sequential
    note: "跳过 tech 和 finance 节点，引用已有制品"

  quick-scan:
    trigger: "初步项目筛选、快速可行性判断"
    nodes: [industry, tech]
    mode: parallel
    depth: quick
```

---

## 4. 四个推演节点

### 4.1 行业/业务定位（industry-scanner）

**分析范围**：
- 赛道天花板与增长驱动力
- 竞争格局与发行人市场地位
- 行业政策环境与监管趋势
- "硬科技"属性是否经得起质疑

**三角色分析焦点**：

| 角色 | 核心问题 | 搜索重点 |
|------|---------|---------|
| Pre-IPO 投资人 | 赛道天花板够不够高？退出窗口什么时候？ | 同行业 IPO 退出案例、赛道融资热度变化 |
| 买方 | 上市后 3-5 年还能不能增长？ | 可比公司收入增速、行业渗透率、TAM 测算 |
| 舆论 | 是不是"伪硬科技"？有没有政策红利嫌疑？ | 行业争议事件、政策敏感标签、科创板定位争议案例 |

**不负责**：收入确认合规（→ finance）、核心技术先进性细节（→ tech）、估值判断（→ pricing）

### 4.2 技术/知识产权（tech-scanner）

**分析范围**：
- 核心技术先进性（与行业基准对比）
- 知识产权完整性（专利覆盖、潜在诉讼）
- 研发投入质量（真研发 vs 资本化包装）
- 技术依赖风险（核心人员、供应商、授权）

**三角色分析焦点**：

| 角色 | 核心问题 | 搜索重点 |
|------|---------|---------|
| Pre-IPO 投资人 | 技术壁垒是否真实？会不会上市后技术被替代？ | 技术路线竞争动态、核心技术人员的竞业情况 |
| 买方 | 研发投入是真研发还是资本化包装？ | 研发费用率 vs 同行、专利质量（引用数/授权率）、技术迭代周期 |
| 舆论 | 核心技术是否自主可控？有没有专利诉讼？ | 专利纠纷、技术来源争议、"卡脖子"标签、产学研关联交易 |

**不负责**：行业天花板（→ industry）、研发费用会计处理合规性（→ finance）、技术对估值的影响（→ pricing）

### 4.3 财务合规（finance-scanner）

**分析范围**：
- 收入确认政策与行业惯例对比
- 关联交易复杂度与公允性
- 应收账款与现金流质量
- 研发资本化政策的合理性
- 财务数据的内在一致性（是否存在调节痕迹）

**三角色分析焦点**：

| 角色 | 核心问题 | 搜索重点 |
|------|---------|---------|
| Pre-IPO 投资人 | 收入和利润真实性有没有硬伤？会不会补税？ | 税务处罚记录、同行业财务暴雷案例 |
| 买方 | 财务质量是否可持续？有没有调节痕迹？ | 应收账款周转天数 vs 同行、经营现金流/净利润比值趋势、大客户依赖 |
| 舆论 | 应收账款异常？关联交易复杂？ | 关联方资金占用、大额异常交易、供应商/客户重叠 |

**不负责**：行业增长逻辑（→ industry）、研发成果评估（→ tech）、估值倍数选取（→ pricing）

### 4.4 定价/发行（pricing-scanner）

**分析范围**：
- 可比公司估值区间与发行人定位
- 发行价相对于可比公司的溢价/折价
- Pre-IPO 轮次估值的安全垫分析
- 破发风险评估
- 买方可能提出的估值质疑

**三角色分析焦点**：

| 角色 | 核心问题 | 搜索重点 |
|------|---------|---------|
| Pre-IPO 投资人 | 估值有没有安全垫？破发概率多大？ | 同轮次估值对比、解禁后股价表现、科创板破发率统计 |
| 买方 | 发行价相对于可比公司贵不贵？ | 可比 PS/PE/PEG、发行价隐含增速反推、机构询价区间 |
| 舆论 | 定价是否合理？有没有"割韭菜"嫌疑？ | 高市盈率发行争议案例、发行人/实控人的套现记录、媒体对定价的质疑模式 |

**不负责**：行业选择（→ industry）、技术判断（→ tech）、财务数据真实性（→ finance）

---

## 5. 三个外部角色定义

### 5.1 Pre-IPO 投资人

```
认知立场："能不能上市、退出赚多少"

核心问题：
1. 退出路径是否清晰？预计何时解禁？
2. 当前轮次估值相对最终发行价有多少安全垫？
3. 上市确定性如何？主要障碍是什么？
4. 锁定期条款是否合理？有没有回购风险？
5. 历史同轮次类似项目的退出回报率？

搜索策略：
- 搜索：科创板退出案例、解禁后股价表现、同轮次估值对比
- 不搜索：上市后长期持有回报分析、行业深度研报、可比公司 DCF

立场锚定：
- 你绝对不是监管审核员——不说"不符合某条规定"
- 你绝对不是买方分析师——不关心上市后 3 年的持有收益
- 你绝对不是企业顾问——不帮企业想解决方案

输出风险时，每一判断必须对应：
1. 具体的退出影响（延迟？压价？解禁时破发？）
2. 可量化的数据依据（估值差额、时间成本）
```

### 5.2 上市后买方

```
认知立场："上市后值不值得买"

核心问题：
1. 增长驱动力是否可持续？3-5 年后这家公司还值得持有吗？
2. 财务质量是否真实？有没有调节痕迹？
3. 管理层能力和诚信如何？
4. 竞争格局是否在恶化？
5. 目前隐含的估值是否合理？

搜索策略：
- 搜索：可比公司 3-5 年财务趋势、增长驱动力可持续性、管理层履历与历史争议
- 不搜索：Pre-IPO 退出机制、锁定期条款、一级市场估值

立场锚定：
- 你绝对不是保荐机构——不说"这个问题可以解释"
- 你绝对不是 Pre-IPO 投资人——不关心解禁时能不能赚钱退出
- 你绝对不是监管审核员——不判断是否符合上市条件

输出风险时，每一判断必须对应：
1. 对上市后 1-3 年股价表现的具体影响推演
2. 可对比的同行业案例或数据点
```

### 5.3 舆论/媒体

```
认知立场："有什么不想让人知道的"

核心问题：
1. 发行人的"故事"中哪些部分最容易被质疑？
2. 有没有隐藏的关联交易、利益输送、历史污点？
3. 核心技术/产品的宣传是否有夸大成分？
4. 实控人/管理层的历史是否有争议？
5. 行业/政策标签是否经得起推敲（"硬科技""国产替代"等）？

搜索策略：
- 搜索：行业争议事件、政策敏感词、发行人与实控人相关的负面新闻/诉讼/处罚
- 不搜索：估值数据、财务指标、投资回报计算

立场锚定：
- 你绝对不是企业公关——不给应对方案，只挖问题
- 你绝对不是投资人——不判断是否值得投资
- 你不做合规判断——不引用法条，只报道"外界可能怎么看"

输出风险时，每一判断必须对应：
1. 一句可能的媒体标题（帮助保荐机构感受冲击力）
2. 类似争议事件的真实案例引用
```

---

## 6. 制品 Schema

### 6.1 分析计划单（Router 产出）

```yaml
analysis_plan:
  plan_id: "PLAN-{YYYYMMDD}-{seq}"
  project_name: ""
  mode: "full-chain | targeted-update | pricing-focused | quick-scan"
  nodes: [industry, tech, finance, pricing]
  depth: "deep | standard | quick"
  previous_run_id: null
  previous_artifacts: {}
  existing_materials: []
  generated_at: "{timestamp}"
```

### 6.2 节点结论制品（节点产出，传递给下游）

```yaml
node_artifact:
  node: "industry|tech|finance|pricing"
  generated_at: "{timestamp}"
  summary:
    overall_rating: "favorable|neutral|cautious|red-flag"
    key_finding: "一句话核心判断"
  role_consensus:
    agreed_risks: []
    conflicts:
      - topic: ""
        pre_ipo_view: ""
        buy_side_view: ""
        media_view: ""
        conflict_type: "assumption|weighting|interpretation"
  data_freshness:
    search_quality: "rich|adequate|sparse"
    key_data_gaps: []
```

### 6.3 风险矩阵条目（每个节点最终产出）

```yaml
risk_entry:
  id: "RISK-{node}-{role}-{seq}"
  node: "industry|tech|finance|pricing"
  role: "pre-ipo-investor|buy-side|media"
  risk_level: "critical|high|medium|low"
  claim: "一句话风险主张"
  evidence:
    primary_source:
      url: ""
      access_type: "public|internal|paywall"
      captured_at: ""
    inline_summary: |
      内联证据摘要（确保报告可独立分发，不依赖外部链接）
    key_data_points:
      - metric: ""
        value: ""
        comparison: ""
  rationale: "为什么这个角色关注这个风险"
  potential_impact: "风险一旦发生的影响推演"
  suggested_response: "建议应对策略（给保荐机构参考）"
```

---

## 7. 质量门禁

### 7.1 每节点门禁

| 门禁 | 规则 | 不通过处理 |
|------|------|-----------|
| 角色完备 | 每个角色 ≥ 3 条风险条目 | 标注数据不足的角色，降低该节点置信度 |
| 来源多样 | 不同风险条目使用不同来源 | 合并同源条目，标注来源集中度风险 |
| 证据内联 | 每条风险必须有 inline_summary | 拒绝通过，要求补充内联摘要 |
| 枚举合规 | id/node/role/risk_level 在枚举值内 | 拒绝通过，要求修正 |
| 角色锚定 | 每条风险的 rationale 与该角色认知立场一致 | 标注角色漂移，重新生成 |
| 自包含 | 无外部依赖引用（裸 URL 可接受但必须有 inline_summary） | 标注交付物自包含性不足 |

### 7.2 降级策略

| 场景 | 降级行为 |
|------|---------|
| 搜索不可用 | 标注 [SEARCH_UNAVAILABLE]，仅基于用户提供的材料分析 |
| 搜索结果稀疏（某角色 <3 条有效数据） | 降低该角色风险条目最低要求至 1 条，标注 confidence: low |
| 搜索结果矛盾 | 保留矛盾双方，标注 conflicting_sources，不做自动裁决 |
| 某角色完全无法产出 | 标注 [INSUFFICIENT_DATA]，不编造；其他角色正常产出 |

---

## 8. 防漂移体系

### 8.1 非协商条款（AGENTS.md 级别）

```
1. Router 禁止做分析。只做项目状态评估 → 分析计划单 → 移交节点。
2. 禁止跳过分析计划单。无 analysis_plan (YAML)，下游节点禁止启动。
3. 未知状态默认为 full-chain，不猜测用户意图。
4. 超范围请求明确拒绝，不尝试"帮忙做一点"。
5. 禁止分析计划单未覆盖的节点被触发。
6. 数值判断必须有搜索结果或用户材料作为依据。
7. 角色禁止视角切换（买方不替 Pre-IPO 投资人说话，舆论不帮企业公关）。
8. 禁止生成包含外部依赖的交付物（HTML 必须内联 CSS、关键数据必须内联摘要、禁止本地绝对路径）。
9. 制品传递必须使用注册表定义的 schema，不得自创字段。
```

### 8.2 节点边界（每个 Scanner skill 内）

每个节点 skill 文件显式列出：
- ✅ 本节点分析范围
- ❌ 本节点不负责的内容
- 引用上游制品的方式（只读，不重新分析）
- 输出 schema 的强制枚举值

### 8.3 角色锚定（每个角色 prompt 内）

每个角色定义：
- 认知立场（一句话）
- 核心问题（5 个）
- 搜索策略（搜什么 + 不搜什么）
- "你绝对不是谁"清单（3 项）
- 输出要求（每判断必须有对应的影响推演和数据依据）

### 8.4 输出格式锁

所有输出通过 YAML schema 的枚举值做硬约束：
- `node`: 仅允许 `industry|tech|finance|pricing`
- `role`: 仅允许 `pre-ipo-investor|buy-side|media`
- `risk_level`: 仅允许 `critical|high|medium|low`
- `id`: 强制格式 `RISK-{node}-{role}-{seq}`
- 不符合枚举值 → 拒绝通过，要求重新生成

---

## 9. 制品新鲜度追踪

每次推演后更新制品新鲜度记录：

```yaml
artifact_freshness:
  industry:
    generated_at: "2026-07-30T10:00:00Z"
    status: "fresh|stale"
    age_days: 0
  tech:
    generated_at: "2026-07-30T10:00:00Z"
    status: "fresh"
    age_days: 0
  finance:
    generated_at: "2026-07-20T10:00:00Z"
    status: "stale"
    age_days: 10
  pricing:
    generated_at: null
    status: "not_run"
```

用户在下一次推演时了解哪些节点的结论需要更新。

---

## 10. 未来 A 方案知识库插槽

knowledge/ 目录预留三类知识库，当前为空：

| 目录 | 用途 | 示例内容 |
|------|------|---------|
| industry-benchmarks/ | 行业估值基准 | 科创板各行业 PS/PE 中枢、研发费用率基准 |
| case-library/ | 历史案例库 | 被否案例的原因归类、问询焦点统计、破发案例特征 |
| policy-tracker/ | 政策动态 | 科创板定位指引更新、行业政策变化时间线 |

知识库接入后：角色 prompt 增加"优先查阅知识库 → 知识库无覆盖再搜索"的逻辑层。references/roles/ 和 references/guardrails/ 保持不变。

---

## 11. 设计决策记录

| 决策 | 理由 | 来源经验 |
|------|------|---------|
| Router + 4 Scanner 的 5-skill 结构 | Router 不做分析，职责清晰分离 | Credence router 模式 |
| 角色 prompt 放在 references/ 而非内嵌 | 角色可独立升级，不影响 skill | Baker-Street 独立 persona 文件 |
| 分析路径声明式注册表 | 路由逻辑外化，不藏在 prompt 里 | Credence work-path-registry |
| 三角色并行而非串行 | 避免角色互相影响，保持认知独立性 | Baker-Street 并行 persona 调度 |
| 不做角色反驳循环 | 保荐场景下冲突标注比自动裁决更实用 | Baker-Street rebuttal 机制过重 |
| 制品新鲜度追踪 | 解决多次推演中"旧结论过时"的问题 | 四项均无此机制，原创新增 |
| 搜索策略差异化 | 防止三角色用相同数据得出相同结论 | Baker-Street CUR 同质化教训 |
| 质量门禁 + 降级策略 | 搜索失败是常态，需预设降级路径 | Baker-Street degradation 模式 |
| 自包含交付物 | 防止外部引用失效导致报告崩溃 | 用户实际踩坑经验 |
| "你不是谁"锚定 > "你是谁" | 角色崩塌的主要原因是视角模糊 | Baker-Street persona collapse 教训 |
| knowledge/ 预留插槽 | B→A 方案平滑升级 | Credence 的 engine/ 目录模式 |
| 防漂移体系四层挂钩 | 模型不够聪明时的最后防线 | FolioPulse + Credence 反漂移铁律 |

---

## 12. 自审查记录

### 12.1 占位符扫描
- 无 TBD、TODO 残留
- knowledge/ 目录内容明确标注"当前为空"
- 三个角色 prompt 有完整定义

### 12.2 内部一致性
- 制品 schema 中的 node/role 枚举值与角色定义、节点定义一致
- 质量门禁中的枚举检查与 schema 定义对齐
- 防漂移条款与架构设计中的非协商条款一致

### 12.3 范围检查
- 聚焦科创板 Pre-IPO 保荐承销场景
- 四个节点覆盖全链路但不溢出
- 知识库、HTML 报告等延伸功能明确标注为未来迭代

### 12.4 歧义检查
- 节点间制品 schema 明确定义
- 角色"不负责"清单消除职责模糊
- 降级策略为每种异常场景指定了具体行为
