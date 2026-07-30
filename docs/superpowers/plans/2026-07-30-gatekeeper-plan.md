# Gatekeeper Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 5-skill Pre-IPO external-perspective analysis system (Gatekeeper) for STAR Market IPO sponsorship, with three external roles (Pre-IPO investor, buy-side, media) performing structured risk assessment across four nodes (industry, tech, finance, pricing).

**Architecture:** Three-layer separation — AGENTS.md orchestrates, 5 SKILL.md files execute pipeline stages, references/ holds role prompts, templates, guardrails, and schemas. Real-time search-driven (Plan B) with knowledge/ directory reserved for future Plan A.

**Tech Stack:** Markdown skill files, YAML schemas, Claude Code Agent SDK. No Python code — pure prompt-driven analysis.

## Global Constraints

- All skills must ≤ 200 lines each
- All numeric thresholds/weights/enum values must live only in references/ files — never duplicated in skills
- No analysis without an Analysis Plan Sheet (YAML artifact from Router)
- Every risk entry must have inline_summary (self-contained, no bare URL dependency)
- All outputs must use enumerated values only (node/role/risk_level)
- Role prompts must include "what you are NOT" anchor lists
- knowledge/ directory created but left empty (future Plan A slot)

---

## File Structure Map

```
D:\sandbox\
├── AGENTS.md                              ← Task 2: Global orchestrator
├── .claude/
│   └── skills/
│       ├── ipo-router/
│       │   └── SKILL.md                   ← Task 7: Entry router
│       ├── industry-scanner/
│       │   └── SKILL.md                   ← Task 8: Node 1
│       ├── tech-scanner/
│       │   └── SKILL.md                   ← Task 9: Node 2
│       ├── finance-scanner/
│       │   └── SKILL.md                   ← Task 10: Node 3
│       └── pricing-scanner/
│           └── SKILL.md                   ← Task 11: Node 4
├── references/
│   ├── guardrails/
│   │   ├── non-negotiables.md             ← Task 3
│   │   ├── quality-gates.md              ← Task 3
│   │   └── degradation-paths.md          ← Task 3
│   ├── analysis-registry.md              ← Task 4
│   ├── artifact-schemas.md               ← Task 4
│   ├── roles/
│   │   ├── pre-ipo-investor.md           ← Task 5
│   │   ├── buy-side.md                   ← Task 5
│   │   └── media.md                      ← Task 5
│   └── templates/
│       └── risk-matrix-template.md        ← Task 6
└── knowledge/
    ├── industry-benchmarks/
    │   └── .gitkeep                       ← Task 1
    ├── case-library/
    │   └── .gitkeep                       ← Task 1
    └── policy-tracker/
        └── .gitkeep                       ← Task 1
```

---

### Task 1: Create directory structure

**Files:**
- Create: `knowledge/industry-benchmarks/.gitkeep`
- Create: `knowledge/case-library/.gitkeep`
- Create: `knowledge/policy-tracker/.gitkeep`

**Interfaces:**
- Consumes: nothing
- Produces: directory structure for all subsequent tasks

- [ ] **Step 1: Create all directories**

```bash
mkdir -p D:/sandbox/.claude/skills/ipo-router
mkdir -p D:/sandbox/.claude/skills/industry-scanner
mkdir -p D:/sandbox/.claude/skills/tech-scanner
mkdir -p D:/sandbox/.claude/skills/finance-scanner
mkdir -p D:/sandbox/.claude/skills/pricing-scanner
mkdir -p D:/sandbox/references/guardrails
mkdir -p D:/sandbox/references/roles
mkdir -p D:/sandbox/references/templates
mkdir -p D:/sandbox/knowledge/industry-benchmarks
mkdir -p D:/sandbox/knowledge/case-library
mkdir -p D:/sandbox/knowledge/policy-tracker
```

- [ ] **Step 2: Create .gitkeep files for knowledge/ directories**

```bash
touch D:/sandbox/knowledge/industry-benchmarks/.gitkeep
touch D:/sandbox/knowledge/case-library/.gitkeep
touch D:/sandbox/knowledge/policy-tracker/.gitkeep
```

- [ ] **Step 3: Verify structure**

```bash
find D:/sandbox/.claude D:/sandbox/references D:/sandbox/knowledge -type d | sort
```

Expected: 15 directories exist.

- [ ] **Step 4: Commit**

```bash
git add knowledge/ .claude/ references/
git commit -m "feat: scaffold Gatekeeper directory structure"
```

---

### Task 2: Create AGENTS.md — Global orchestrator

**Files:**
- Create: `AGENTS.md`

**Interfaces:**
- Consumes: reference paths from file structure (Task 1)
- Produces: global non-negotiable rules, skill index, pipeline overview, output template reference. All downstream skill files reference this.

- [ ] **Step 1: Write AGENTS.md**

```markdown
# AGENTS.md — Gatekeeper 跨 CLI 通用入口

**项目**：Gatekeeper（科创板 Pre-IPO 外部视角推演引擎）
**版本**：v0.1.0
**一句话**：为科创板 IPO 保荐承销机构提供 Pre-IPO 投资人、上市后买方、舆论三个外部视角的结构化风险推演。

> 任何 agent CLI 都从这里开始：先读你的 instructions file，再读当前任务对应的 SKILL.md。

## 技能索引

| 技能 | 用途 | 路径 |
|------|------|------|
| ipo-router | 项目状态评估 → 分析计划单生成。不做分析 | .claude/skills/ipo-router/SKILL.md |
| industry-scanner | 节点1：行业/业务定位三角色推演 | .claude/skills/industry-scanner/SKILL.md |
| tech-scanner | 节点2：技术/知识产权三角色推演 | .claude/skills/tech-scanner/SKILL.md |
| finance-scanner | 节点3：财务合规三角色推演 | .claude/skills/finance-scanner/SKILL.md |
| pricing-scanner | 节点4：定价/发行三角色推演 | .claude/skills/pricing-scanner/SKILL.md |

## 四节点管道

```
ipo-router → industry-scanner → tech-scanner → finance-scanner → pricing-scanner
     │              │               │               │                │
 分析计划单     行业风险矩阵    技术风险矩阵     财务风险矩阵      定价风险矩阵
                 + 节点制品      + 节点制品       + 节点制品        + 节点制品
```

### 链式调用规则

1. ipo-router 产出分析计划单后，按 plan.mode 决定执行链路
2. full-chain / pricing-focused：按节点顺序自动衔接，不等待用户确认
3. targeted-update / quick-scan：Router 路由到指定节点后执行
4. 每个节点产出后立即移交下游（如链路中有下一节点）

## 非协商条款（所有 agent、所有 CLI、所有请求强制生效）

1. Router 禁止做分析。只做项目状态评估 → 分析计划单 → 移交节点。
2. 禁止跳过分析计划单。无 analysis_plan (YAML)，下游节点禁止启动。
3. 未知状态默认为 full-chain，不猜测用户意图。
4. 超范围请求明确拒绝，不尝试"帮忙做一点"。
5. 禁止分析计划单未覆盖的节点被触发。
6. 数值判断必须有搜索结果或用户提供的材料作为依据。
7. 角色禁止视角切换（买方不替 Pre-IPO 投资人说话，舆论不帮企业公关）。
8. 禁止生成包含外部依赖的交付物（关键数据必须内联摘要、禁止本地绝对路径）。
9. 制品传递必须使用注册表定义的 schema（references/artifact-schemas.md），不得自创字段。
10. 分析路径唯一事实源为 references/analysis-registry.md——不得在 skill 文件中重复定义路径规则。

## 单一事实源

- 分析路径定义：`references/analysis-registry.md`
- 制品 schema 定义：`references/artifact-schemas.md`
- 角色定义：`references/roles/*.md`
- 质量门禁定义：`references/guardrails/quality-gates.md`
- 降级策略定义：`references/guardrails/degradation-paths.md`
- 输出模板：`references/templates/risk-matrix-template.md`

所有 skill 文件引用以上文档，不自行定义路径、schema、角色、门禁。

## 知识库（未来 A 方案）

`knowledge/` 目录预留给未来内建知识库，当前为空。子目录：
- `industry-benchmarks/` — 行业估值基准
- `case-library/` — 历史 IPO 案例库
- `policy-tracker/` — 科创板政策动态
```

- [ ] **Step 2: Verify file content**

```bash
grep -c "非协商条款" AGENTS.md
grep -c "单一事实源" AGENTS.md
grep -c "skill" AGENTS.md
```

Expected: non-zero counts for all three.

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md
git commit -m "feat: add AGENTS.md with global orchestrator and non-negotiables"
```

---

### Task 3: Create guardrails (non-negotiables, quality gates, degradation paths)

**Files:**
- Create: `references/guardrails/non-negotiables.md`
- Create: `references/guardrails/quality-gates.md`
- Create: `references/guardrails/degradation-paths.md`

**Interfaces:**
- Consumes: AGENTS.md non-negotiable clause definitions
- Produces: non-negotiables.md (expanded with violation responses), quality-gates.md (6 gates with pass/fail criteria), degradation-paths.md (3 scenarios with specific behaviors). Consumed by all 5 skills and all 3 role definitions.

- [ ] **Step 1: Write non-negotiables.md**

```markdown
# 非协商条款（Non-Negotiables）

> 此文件是 AGENTS.md 非协商条款的详细展开。每个条款定义了违反时的处理方式。

## N1: Router 禁止做分析

**规则**：ipo-router 只做项目状态评估和路径匹配。任何需要搜索、判断、打分的行为均不属于 Router 职责。
**违反响应**：下游节点检测到 Router 产出的分析计划单中包含评分、推荐、结论等分析内容 → 拒绝执行，要求 Router 重新生成纯计划单。
**检查方式**：分析计划单的 YAML schema 只包含路径/节点/模式字段，不含 `assessment`/`rating`/`recommendation` 字段。含此类字段的计划单直接拒绝。

## N2: 无分析计划单则禁止启动

**规则**：所有 Scanner 节点在收到显式的 analysis_plan YAML 之前禁止启动分析。
**违反响应**：Scanner 提示"未收到分析计划单，请先通过 ipo-router 生成"。
**例外**：用户手动指定 `path_id` 和 `node` 时可以跳过 Router 直接启动。

## N3: 未知默认为 full-chain

**规则**：当无法判断用户意图时，Router 默认选择 full-chain 路径，不猜测也不跳过。
**违反响应**：N/A（此规则防止 Router 偷懒跳过节点）。

## N4: 超范围请求明确拒绝

**规则**：当用户请求不属于 Gatekeeper 覆盖范围（如"帮我写招股书""做 DCF 模型""审查法律合同"），明确告知边界。
**违反响应**：禁止尝试"帮忙做一点"。输出格式：`[OUT_OF_SCOPE] 本系统不覆盖 {具体请求}。Gatekeeper 覆盖范围：科创板 IPO 行业/技术/财务/定价四个节点的外部视角风险推演。`

## N5: 禁止未注册节点被触发

**规则**：仅 industry/tech/finance/pricing 四个节点可被触发。任何其他节点名称直接拒绝。
**违反响应**：提示"节点 {name} 不在注册表中。可选节点：industry, tech, finance, pricing。"

## N6: 数值判断必须有依据

**规则**：任何数值判断（如"估值偏高 30%"）必须有搜索结果 URL 或用户提供的材料作为依据。
**违反响应**：质量门禁 G4 检查：无来源的数值判断 → 标注 [UNCITED] 而非输出该判断。

## N7: 角色禁止视角切换

**规则**：每个角色必须严格保持其认知立场。"你不是谁"清单定义了禁止切换的方向。
**违反响应**：质量门禁 G5 检查：角色产出的风险条目中，rationale 字段与该角色认知立场不一致 → 标注角色漂移，重新生成。

## N8: 自包含交付物

**规则**：所有交付物可独立分发，接收方无需访问本系统任何文件。关键数据必须内联摘要，禁止仅提供裸 URL。
**违反响应**：质量门禁 G6 检查：无 inline_summary 的风险条目 → 拒绝通过。

## N9: 制品 Schema 合规

**规则**：所有制品传递必须使用 references/artifact-schemas.md 定义的 schema。
**违反响应**：含未注册字段的制品 → 截断非标字段，标注 schema 不合规。

## N10: 路径定义单一事实源

**规则**：分析路径的唯一定义位置为 references/analysis-registry.md。Skill 文件只引用，不定义路径规则。
**违反响应**：一致性检查脚本会发现重复定义并报错。
```

- [ ] **Step 2: Write quality-gates.md**

```markdown
# 质量门禁（Quality Gates）

> 每个 Scanner 节点完成后必须通过以下门禁。任一门禁失败 → 标注失败原因 → 重新生成或触发降级。

## G1: 角色完备（Role Completeness）

**规则**：每个角色产出 ≥ 3 条风险条目（full-chain / targeted-update 深度）。
       quick-scan 深度：每个角色 ≥ 1 条。
**不通过处理**：标注数据不足的角色，降低该节点整体置信度为 `confidence: low`。

## G2: 来源多样（Source Diversity）

**规则**：同一角色内不同风险条目使用不同 primary_source URL。
       同一 URL 最多支撑 2 条风险条目。
**不通过处理**：合并同源条目，标注 `source_concentration: high`。

## G3: 证据内联（Evidence Inline）

**规则**：每条风险条目必须有 `evidence.inline_summary` 字段，且非空。
       裸 URL（有 primary_source.url 但无 inline_summary）视为不通过。
**不通过处理**：拒绝通过，要求补充内联摘要。最多重试一次。

## G4: 枚举合规（Enum Compliance）

**规则**：所有条目的以下字段必须在枚举值范围内：
       - `node`: industry | tech | finance | pricing
       - `role`: pre-ipo-investor | buy-side | media
       - `risk_level`: critical | high | medium | low
       - `id`: 格式 RISK-{node}-{role}-{seq}（seq 为 3 位数字）
**不通过处理**：拒绝通过，返回修正后的条目。

## G5: 角色锚定（Role Anchoring）

**规则**：每条风险的 `rationale` 字段阐述的理由必须与该角色的认知立场一致。
       检查方式：rationale 中的关键词是否与角色的"核心问题"和"搜索重点"匹配。
       买方说"上市后估值合理性"= 通过。买方说"Pre-IPO 退出机制"= 不通过。
**不通过处理**：标注 `role_drift_detected`，重新生成该条目。

## G6: 自包含（Self-Containment）

**规则**：输出报告不得包含：
       - 本地绝对路径（如 `D:/sandbox/...`、`file:///...`）
       - 外部 CSS/JS 引用（如 `<link rel="stylesheet" href="...">`）
       - 仅裸 URL 作为证据（必须有 inline_summary）
**不通过处理**：标注违规位置，要求修正。
```

- [ ] **Step 3: Write degradation-paths.md**

```markdown
# 降级策略（Degradation Paths）

> 当搜索失败、数据不足、或结果矛盾时，各节点按以下策略降级运行。降级不做自动裁决——始终保留原始信息，标注降级原因。

## D1: 搜索不可用（Search Unavailable）

**触发条件**：WebSearch 工具调用失败、超时、或返回空结果达 3 次以上。
**降级行为**：
- 所有风险条目标注 `[SEARCH_UNAVAILABLE]`
- 仅基于用户提供的材料（existing_materials 字段）做分析
- 如果用户未提供任何材料 → 输出空风险矩阵，标注 `analysis_blocked: no_search_and_no_materials`
- 不编造任何数据

## D2: 搜索结果稀疏（Sparse Results）

**触发条件**：某角色在某节点的搜索结果 < 3 条有效数据点。
**降级行为**：
- 该角色的风险条目最低要求降至 1 条
- 整体节点置信度标注 `confidence: low`
- 在制品 `data_freshness.search_quality` 中标注 `sparse`
- 列出缺失的数据点类型（data_gaps 字段）

## D3: 搜索结果矛盾（Conflicting Results）

**触发条件**：同一数据点的搜索结果存在实质性矛盾（如可比公司 PS 从 5x 到 15x 不等）。
**降级行为**：
- 保留矛盾双方的数值范围
- 标注 `conflicting_sources: true`
- 不做自动裁决——让用户判断
- 在 inline_summary 中呈现矛盾："来源 A 显示 PS 5x（2026 Q1），来源 B 显示 PS 15x（2026 Q2），差异可能源于样本选择不同"
```

- [ ] **Step 4: Verify files**

```bash
grep -c "^## N" references/guardrails/non-negotiables.md
grep -c "^## G" references/guardrails/quality-gates.md
grep -c "^## D" references/guardrails/degradation-paths.md
```

Expected: N=10, G=6, D=3.

- [ ] **Step 5: Commit**

```bash
git add references/guardrails/
git commit -m "feat: add guardrails - non-negotiables, quality gates, degradation paths"
```

---

### Task 4: Create analysis registry and artifact schemas

**Files:**
- Create: `references/analysis-registry.md`
- Create: `references/artifact-schemas.md`

**Interfaces:**
- Consumes: node and role definitions from spec
- Produces: analysis-registry.md (4 paths with trigger/sequence/mode), artifact-schemas.md (3 schemas: analysis_plan, node_artifact, risk_entry). Consumed by ipo-router and all 4 scanner skills.

- [ ] **Step 1: Write analysis-registry.md**

```markdown
# 分析路径注册表（Analysis Registry）

> 单一事实源。所有分析路径的定义仅在此文件中维护。Skill 文件只引用 path_id，不定义路径规则。

## 路径定义

```yaml
paths:
  full-chain:
    path_id: "FULL-CHAIN"
    trigger:
      - "首次全链路推演"
      - "项目初期尽调完成"
      - "用户明确要求完整分析"
    nodes: [industry, tech, finance, pricing]
    mode: sequential
    depth: deep
    description: "从行业定位到定价发行的完整推演链路，前序节点制品传递给后续节点"

  targeted-update:
    path_id: "TARGETED-UPDATE"
    trigger:
      - "新数据到达"
      - "局部信息更新"
      - "反馈回复后重新评估特定方面"
    nodes: ["user-specified"]
    mode: single-node
    depth: standard
    reuse_previous_artifacts: true
    description: "用户指定节点进行局部更新推演，复用已有上游制品"

  pricing-focused:
    path_id: "PRICING-FOCUSED"
    trigger:
      - "临近发行窗口"
      - "估值讨论"
      - "定价策略评估"
    nodes: [industry, pricing]
    mode: sequential
    depth: deep
    description: "聚焦定价推演，跳过技术和财务节点，引用已有行业制品"

  quick-scan:
    path_id: "QUICK-SCAN"
    trigger:
      - "初步项目筛选"
      - "快速可行性判断"
      - "立项前快速评估"
    nodes: [industry, tech]
    mode: parallel
    depth: quick
    description: "快速扫描，行业和技术节点并行执行"
```

## 深度级别定义

| depth | 每角色最少风险条目 | 搜索轮次 | 适用场景 |
|-------|-----------------|---------|---------|
| deep | 5 | 3-4 轮 | full-chain, pricing-focused |
| standard | 3 | 2-3 轮 | targeted-update |
| quick | 1 | 1-2 轮 | quick-scan |
```

- [ ] **Step 2: Write artifact-schemas.md**

```markdown
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
```

- [ ] **Step 3: Verify schemas are consistent**

```bash
# Check that all enum values used in artifact-schemas.md are defined
grep -o "仅允许.*" references/artifact-schemas.md
# Should list all enum constraints clearly
```

- [ ] **Step 4: Commit**

```bash
git add references/analysis-registry.md references/artifact-schemas.md
git commit -m "feat: add analysis registry and artifact schemas"
```

---

### Task 5: Create three role definitions

**Files:**
- Create: `references/roles/pre-ipo-investor.md`
- Create: `references/roles/buy-side.md`
- Create: `references/roles/media.md`

**Interfaces:**
- Consumes: quality-gates.md (G5 role anchoring check), degradation-paths.md (search failure behavior)
- Produces: three role prompt files with cognitive stance, core questions, search strategy, "not you" anchors, and output requirements. Consumed by all 4 scanner skills — each scanner loads all 3 roles for parallel analysis.

- [ ] **Step 1: Write pre-ipo-investor.md**

```markdown
# Pre-IPO 投资人视角

## 认知立场

"能不能上市、退出赚多少"

## 核心问题

1. 退出路径是否清晰？预计何时解禁？
2. 当前轮次估值相对最终发行价有多少安全垫？
3. 上市确定性如何？主要障碍是什么？
4. 锁定期条款是否合理？有没有回购风险？
5. 历史同轮次类似项目的退出回报率如何？

## 搜索策略

**优先搜索**：
- 科创板同行业 IPO 退出案例（解禁后股价 vs 发行价）
- 同轮次（Pre-IPO/B轮/C轮）估值对比数据
- 赛道融资热度变化（近 12 个月融资事件和估值趋势）
- 锁定期条款的市场惯例
- 发行人/可比公司的融资历史与估值轨迹

**不搜索**：
- 上市后 3-5 年的长期持有回报分析（那是买方的事）
- 行业深度研报中的长期增长逻辑（那是买方的事）
- 企业治理结构的法律合规细节（那是保荐机构内核的事）

## "你绝对不是谁"

- 你绝对不是监管审核员——不说"不符合《科创板上市规则》第X条"
- 你绝对不是买方分析师——不说"基于 DCF 模型该股票上市后目标价 XX 元"
- 你绝对不是企业顾问——不给解决方案，只评估风险

## 输出要求

每一条风险判断必须包含：
1. **退出影响**：这个风险会如何影响退出？（延迟？压价？解禁时破发？退出失败？）
2. **量化依据**：具体的数值对比（估值差额、时间成本、同轮次回报率对比）
3. **概率判断**：基于历史类似案例，这个风险发生的概率（高/中/低）

**禁止输出的内容**：
- 对上市后股价的预测
- 对监管审核结果的预测
- 为企业"想办法解决"的建议（suggested_response 字段是从保荐机构角度写的应对策略，不是给企业的）
```

- [ ] **Step 2: Write buy-side.md**

```markdown
# 上市后买方视角

## 认知立场

"上市后值不值得买"

## 核心问题

1. 增长驱动力是否可持续？3-5 年后这家公司还值得持有吗？
2. 财务质量是否真实？有没有调节痕迹？
3. 管理层能力和诚信如何？
4. 竞争格局是否在恶化？
5. 目前隐含的估值是否合理？

## 搜索策略

**优先搜索**：
- 可比公司 3-5 年财务趋势（收入增速、利润率变化、ROE 趋势）
- 同行业上市公司的市场表现（上市后 1-3 年股价 vs 发行价）
- 管理层履历（过往任职公司的市场表现、是否有诚信争议）
- 行业竞争格局动态（新进入者、技术替代、价格战信号）
- 可比估值：PS/PE/PEG 横向对比、发行价隐含增速反推

**不搜索**：
- Pre-IPO 退出机制和锁定期条款（那是 Pre-IPO 投资人的事）
- 一级市场估值数据（那是 Pre-IPO 投资人的事）
- 监管审核关注点（那是保荐机构内核的事）

## "你绝对不是谁"

- 你绝对不是保荐机构——不说"这个问题在招股书中可以这样解释"
- 你绝对不是 Pre-IPO 投资人——不说"解禁时能不能赚钱退出"
- 你绝对不是监管审核员——不说"这个信息披露不合规"

## 输出要求

每一条风险判断必须包含：
1. **股价影响推演**：如果这个风险在上市后暴露，对 1-3 年股价走势的具体影响
2. **可比案例**：同行业类似情况的上市公司案例（公司名 + 具体数据对比）
3. **可持续性判断**：这个风险是一次性的还是结构性的？

**禁止输出的内容**：
- 对发行价的具体建议
- 对是否参与 IPO 申购的建议
- 对监管审核流程的评论
```

- [ ] **Step 3: Write media.md**

```markdown
# 舆论/媒体视角

## 认知立场

"有什么不想让人知道的"

## 核心问题

1. 发行人的"故事"中哪些部分最容易被质疑？
2. 有没有隐藏的关联交易、利益输送、历史污点？
3. 核心技术/产品的宣传是否有夸大成分？
4. 实控人/管理层的历史是否有争议？
5. 行业/政策标签是否经得起推敲（"硬科技""国产替代"等）？

## 搜索策略

**优先搜索**：
- 发行人与实控人相关的负面新闻、诉讼记录、行政处罚
- 同行业 IPO 被否/撤回案例中媒体质疑的焦点
- 科创板"伪硬科技"争议案例（被质疑技术含量不足的公司报道）
- 关联方资金往来、供应商/客户重叠、大额异常交易
- 政策敏感词触发：补贴依赖、政策红利、行业调控、环保/安全记录
- ESG 争议（劳工、环保、数据安全、消费者权益）

**不搜索**：
- 估值数据和财务指标计算（那是投资人的事）
- 投资建议和股价预测（那是投资人的事）
- 合规法条引用（那是保荐机构内核的事）

## "你绝对不是谁"

- 你绝对不是企业公关——不给应对方案、不帮忙洗白
- 你绝对不是投资人——不说"值不值得投资"
- 你绝对不是监管审核员——不引用法条做合规判断

## 输出要求

每一条风险判断必须包含：
1. **媒体标题模拟**：如果这个风险被媒体报道，标题会怎么写？（帮助保荐机构感受冲击力）
2. **类似案例引用**：历史上有没有类似的争议导致 IPO 受阻或上市后股价大跌的真实案例？
3. **传播路径推演**：这个风险可能通过什么渠道被放大？（财经媒体？社交媒体？行业论坛？做空报告？）

**禁止输出的内容**：
- 为企业提供公关应对方案
- 判断某个风险"不重要"或"不会引起关注"
- 做合规性判断（是否违反某条规定）
```

- [ ] **Step 4: Verify each role has all required sections**

```bash
for f in references/roles/*.md; do
  echo "=== $f ==="
  grep -c "认知立场" "$f"
  grep -c "核心问题" "$f"
  grep -c "搜索策略" "$f"
  grep -c "你绝对不是谁" "$f"
  grep -c "输出要求" "$f"
  grep -c "禁止输出的内容" "$f"
done
```

Expected: each file returns 1 for all 6 sections.

- [ ] **Step 5: Commit**

```bash
git add references/roles/
git commit -m "feat: add three external role definitions"
```

---

### Task 6: Create risk matrix template

**Files:**
- Create: `references/templates/risk-matrix-template.md`

**Interfaces:**
- Consumes: artifact-schemas.md (risk_entry schema)
- Produces: Markdown template for final risk matrix output. Consumed by all 4 scanner skills as the output format.

- [ ] **Step 1: Write risk-matrix-template.md**

```markdown
# 风险矩阵输出模板

> 所有 Scanner 节点最终输出的统一格式。模板字段对应 artifact-schemas.md §S3 risk_entry。

---

# Gatekeeper 风险矩阵

**项目**：{project_name}
**计划**：{plan_id}
**节点**：{node_name} | **深度**：{depth} | **生成时间**：{generated_at}

---

## 节点总结

**综合评级**：{overall_rating}

**核心发现**：{key_finding}

**数据质量**：{search_quality} | **缺失数据**：{data_gaps}

---

## 角色共识风险

> 以下风险被多个角色共同关注，推演可信度最高。

{agreed_risks_section}

| ID | 风险主张 | 风险等级 | 共识角色 | 关键数据 | 建议应对 |
|----|---------|---------|---------|---------|---------|
| {id} | {claim} | {risk_level} | {roles} | {key_data_summary} | {suggested_response} |

---

## 角色冲突标注

> 以下话题存在角色间分歧。分歧类型：假设冲突(assumption) / 权重冲突(weighting) / 解读冲突(interpretation)

{conflicts_section}

**冲突话题**：{topic}

| 角色 | 观点 | 依据 |
|------|------|------|
| Pre-IPO 投资人 | {pre_ipo_view} | {pre_ipo_basis} |
| 买方 | {buy_side_view} | {buy_side_basis} |
| 舆论 | {media_view} | {media_basis} |

---

## Pre-IPO 投资人视角

> 此角色关注：退出路径清晰度、估值安全垫、上市确定性对投资回报的影响
> 风险等级：🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low

| ID | 风险主张 | 等级 | 关键数据 | 退出影响 | 来源时效 | 建议应对 |
|----|---------|------|---------|---------|---------|---------|
{pre_ipo_entries}

---

## 上市后买方视角

> 此角色关注：上市后增长可持续性、财务质量、估值合理性
> 风险等级：🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low

| ID | 风险主张 | 等级 | 关键数据 | 股价影响推演 | 可比案例 | 建议应对 |
|----|---------|------|---------|------------|---------|---------|
{buy_side_entries}

---

## 舆论/媒体视角

> 此角色关注：可能引发负面报道的争议话题、隐藏风险、信息披露薄弱点
> 风险等级：🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low

| ID | 风险主张 | 等级 | 媒体标题模拟 | 类似案例 | 传播路径 | 建议应对 |
|----|---------|------|------------|---------|---------|---------|
{media_entries}

---

## 制品新鲜度

| 节点 | 最后更新 | 状态 | 距今 |
|------|---------|------|------|
| 行业定位 | {industry_generated_at} | {industry_status} | {industry_age} |
| 技术/IP | {tech_generated_at} | {tech_status} | {tech_age} |
| 财务合规 | {finance_generated_at} | {finance_status} | {finance_age} |
| 定价/发行 | {pricing_generated_at} | {pricing_status} | {pricing_age} |

---

*报告由 Gatekeeper v0.1.0 生成 · 所有数据均内联摘要，可独立分发*
*知识来源：实时搜索 · 搜索质量：{search_quality}*
```

- [ ] **Step 2: Verify template placeholders match schema fields**

```bash
# Check that all {placeholders} in template have corresponding schema fields
grep -oP '\{[a-z_]+\}' references/templates/risk-matrix-template.md | sort -u
```

Expected: all placeholders correspond to fields in artifact-schemas.md §S3.

- [ ] **Step 3: Commit**

```bash
git add references/templates/risk-matrix-template.md
git commit -m "feat: add risk matrix output template"
```

---

### Task 7: Create ipo-router SKILL.md

**Files:**
- Create: `.claude/skills/ipo-router/SKILL.md`

**Interfaces:**
- Consumes: AGENTS.md (non-negotiables), analysis-registry.md (path definitions), artifact-schemas.md (analysis_plan schema)
- Produces: analysis_plan YAML artifact. Consumed by all 4 scanner skills as the required entry credential.

- [ ] **Step 1: Write ipo-router SKILL.md**

```markdown
---
name: ipo-router
description: >
  Gatekeeper 入口路由技能。当用户描述 Pre-IPO 项目情况、提及科创板上市推演、
  或请求外部视角风险评估时触发。通过项目状态评估 + 路径匹配生成分析计划单。
  本技能禁止做分析——只做路由。
---

## 用途

将用户的自然语言描述转换为结构化的分析计划单（analysis_plan YAML），
作为下游 scanner 节点的执行凭证。

## 非协商条款

本技能遵循 AGENTS.md 全部非协商条款。特别强制：
- **N1**: 本技能禁止做分析——不搜索、不打分、不判断
- **N2**: 下游节点无分析计划单禁止启动
- **N3**: 未知状态默认为 full-chain
- **N4**: 超范围请求明确拒绝

## 调用协议

### §0 项目状态预检

收到用户输入后，提取以下信息。不提问——仅从已有输入中提取：

| 信息项 | 提取方式 |
|--------|---------|
| 项目阶段 | 早期洽谈 / 尽调中 / 申报准备 / 反馈回复 / 发行前 |
| 已有材料 | 用户是否提到了招股书草案、尽调报告、审计报告等 |
| 关注重点 | 用户是否明确提到某节点的关注（如"估值""技术"） |
| 上次推演 | 用户是否提到之前的推演记录（plan_id） |

### §1 路径匹配

对照 `references/analysis-registry.md` 匹配最合适的路径：

- **项目阶段 = 早期/尽调中 + 无特定关注点** → full-chain
- **项目阶段 = 申报准备/反馈回复 + 提到特定节点** → targeted-update
- **用户提到"定价""估值""发行窗口"** → pricing-focused
- **用户提到"快速看看""初步判断""立项"** → quick-scan
- **无法判断** → full-chain（N3：未知默认为 full-chain）

### §2 确认

向用户展示匹配结果，简要说明理由。用户确认后产出分析计划单。
如果用户不同意，按用户指示调整。

## 输出

产出分析计划单 YAML，格式严格遵循 `references/artifact-schemas.md §S1`：

```yaml
analysis_plan:
  plan_id: "PLAN-{YYYYMMDD}-{3位序号}"
  project_name: "{用户提供的项目名称}"
  mode: "full-chain|targeted-update|pricing-focused|quick-scan"
  path_id: "{匹配到的 path_id}"
  nodes: [{节点列表}]
  depth: "deep|standard|quick"
  previous_run_id: null
  previous_artifacts: {}
  existing_materials: []
  generated_at: "{ISO 8601 timestamp}"
```

生成后**立即移交**下游节点，不等待用户确认（链式调用规则）。

## 拒绝服务清单

以下请求明确拒绝，不生成分析计划单：

- "帮我写招股书" → 超范围（文档撰写，非风险推演）
- "这个项目能不能过会" → 超范围（监管预判，非外部视角）
- "帮我做 DCF 估值" → 超范围（财务建模，非风险推演）
- "审查这份合同" → 超范围（法务审查，非风险推演）

拒绝格式：`[OUT_OF_SCOPE] 本系统不覆盖 {请求}。Gatekeeper 覆盖范围：科创板 IPO 行业/技术/财务/定价四个节点的外部视角风险推演。`

## 护栏

- 禁止在计划单中包含任何分析结论
- 禁止自行修改 analysis-registry 中定义的路径规则
- plan_id 格式强制：PLAN-YYYYMMDD-NNN
- nodes 数组仅允许：industry, tech, finance, pricing
- mode 仅允许 registry 中定义的四个值
```

- [ ] **Step 2: Verify line count ≤ 200**

```bash
wc -l .claude/skills/ipo-router/SKILL.md
```

- [ ] **Step 3: Verify all required sections present**

```bash
grep -c "非协商条款" .claude/skills/ipo-router/SKILL.md
grep -c "调用协议" .claude/skills/ipo-router/SKILL.md
grep -c "输出" .claude/skills/ipo-router/SKILL.md
grep -c "拒绝服务清单" .claude/skills/ipo-router/SKILL.md
grep -c "护栏" .claude/skills/ipo-router/SKILL.md
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/ipo-router/SKILL.md
git commit -m "feat: add ipo-router skill"
```

---

### Task 8: Create industry-scanner SKILL.md

**Files:**
- Create: `.claude/skills/industry-scanner/SKILL.md`

**Interfaces:**
- Consumes: AGENTS.md, analysis-registry.md (depth rules), artifact-schemas.md (node_artifact + risk_entry schemas), references/roles/*.md (3 role prompts), references/guardrails/quality-gates.md, references/guardrails/degradation-paths.md, references/templates/risk-matrix-template.md
- Produces: node_artifact YAML (for downstream) + risk matrix report (for user). Consumed by: tech-scanner (next in chain), pricing-scanner (when in pricing-focused mode)

- [ ] **Step 1: Write industry-scanner SKILL.md**

```markdown
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

### Step 3: 汇聚与冲突标注

1. 合并三个角色的风险条目
2. 识别共识风险（≥2 个角色关注的同一话题）
3. 识别角色冲突（同一话题的不同解读）
4. 标注冲突类型：assumption / weighting / interpretation

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

按 `references/templates/risk-matrix-template.md` 格式输出。

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
```

- [ ] **Step 2: Verify line count ≤ 200**

```bash
wc -l .claude/skills/industry-scanner/SKILL.md
```

- [ ] **Step 3: Verify key sections**

```bash
grep -c "✅ 本节点负责" .claude/skills/industry-scanner/SKILL.md
grep -c "❌ 本节点不负责" .claude/skills/industry-scanner/SKILL.md
grep -c "质量门禁" .claude/skills/industry-scanner/SKILL.md
grep -c "降级" .claude/skills/industry-scanner/SKILL.md
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/industry-scanner/SKILL.md
git commit -m "feat: add industry-scanner skill"
```

---

### Task 9: Create tech-scanner SKILL.md

**Files:**
- Create: `.claude/skills/tech-scanner/SKILL.md`

**Interfaces:**
- Consumes: node_artifact from industry-scanner (upstream), all references (same set as industry-scanner)
- Produces: node_artifact YAML + risk matrix report. Consumed by: finance-scanner (next in chain)

- [ ] **Step 1: Write tech-scanner SKILL.md**

```markdown
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
3. 读取 `references/roles/media.md`
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
```

- [ ] **Step 2: Verify line count ≤ 200**

```bash
wc -l .claude/skills/tech-scanner/SKILL.md
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/tech-scanner/SKILL.md
git commit -m "feat: add tech-scanner skill"
```

---

### Task 10: Create finance-scanner SKILL.md

**Files:**
- Create: `.claude/skills/finance-scanner/SKILL.md`

**Interfaces:**
- Consumes: node_artifact from tech-scanner (upstream), all references
- Produces: node_artifact YAML + risk matrix report. Consumed by: pricing-scanner (next in chain)

- [ ] **Step 1: Write finance-scanner SKILL.md**

```markdown
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

### Step 1: 加载角色与上游制品

1. 读取三个角色定义
2. 读取上游 industry 和 tech 的 node_artifact
3. 不重复搜索行业和技术数据——仅搜索财务相关数据

### Step 2-5

同 industry-scanner 的 Step 2-5 流程。

node 字段固定为 `"finance"`。

## 输出

### 1. 节点结论制品

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

按 `references/templates/risk-matrix-template.md` 格式输出。

## 链式调用

- **上游**：tech-scanner + industry-scanner（引用行业和技术结论）
- **下游**：pricing-scanner（全链路模式下自动衔接）

## 护栏

- 禁止重复分析行业和技术问题（引用上游制品）
- 禁止出具审计意见或合规鉴证
- 禁止在没有 inline_summary 的情况下输出风险条目
- 买方视角尤其重要：关注"财务质量可持续性"而非"合规性"
```

- [ ] **Step 2: Verify line count ≤ 200**

```bash
wc -l .claude/skills/finance-scanner/SKILL.md
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/finance-scanner/SKILL.md
git commit -m "feat: add finance-scanner skill"
```

---

### Task 11: Create pricing-scanner SKILL.md

**Files:**
- Create: `.claude/skills/pricing-scanner/SKILL.md`

**Interfaces:**
- Consumes: node_artifact from finance-scanner (upstream, when in full-chain mode) or industry-scanner (when in pricing-focused mode), all references
- Produces: node_artifact YAML + risk matrix report. This is the terminal node — no downstream consumer.

- [ ] **Step 1: Write pricing-scanner SKILL.md**

```markdown
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

- 分析计划单（analysis_plan YAML）
- 上游 node_artifact（来自前序节点，根据路径模式不同）
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

1. 读取三个角色定义
2. 读取所有上游 node_artifact（行业 + 技术 + 财务 或仅行业，取决于路径模式）
3. 不重复搜索行业/技术/财务数据——仅搜索估值相关数据

### Step 2: 三角色并行分析

三个角色各自独立分析估值问题。对于定价节点的三角色分工特别说明：

- **Pre-IPO 投资人**：计算估值安全垫。对比 Pre-IPO 轮次估值 vs 预期发行价区间，搜索同轮次退出回报率基准
- **买方**：分析发行价相对于可比公司的合理性。搜索可比公司 PS/PE/PEG，反推发行价隐含增速
- **舆论**：搜索高市盈率发行争议案例、实控人套现记录、定价争议的常见质疑模式

每个角色产出风险条目（deep/standard: ≥5条/角色, quick: ≥3条）。
条目格式严格遵循 `references/artifact-schemas.md §S3 risk_entry`。
node 字段固定为 `"pricing"`。

### Step 3-5

同 industry-scanner 的 Step 3-5 流程。

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
```

- [ ] **Step 2: Verify line count ≤ 200**

```bash
wc -l .claude/skills/pricing-scanner/SKILL.md
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/pricing-scanner/SKILL.md
git commit -m "feat: add pricing-scanner skill"
```

---

### Task 12: Cross-reference consistency verification

**Files:**
- No new files. Verify all existing files.

**Interfaces:**
- Consumes: all files created in Tasks 1-11
- Produces: consistency report (terminal output). No new artifacts.

- [ ] **Step 1: Verify all enum values are consistent across files**

```bash
# Check that every node reference uses only: industry, tech, finance, pricing
echo "=== Checking node enum consistency ==="
grep -rn "node.*:" .claude/skills/ references/artifact-schemas.md | grep -v ".git"

# Check that every role reference uses only: pre-ipo-investor, buy-side, media
echo "=== Checking role enum consistency ==="
grep -rn "role.*:" .claude/skills/ references/artifact-schemas.md references/roles/ | grep -v ".git"

# Check that every risk_level uses only: critical, high, medium, low
echo "=== Checking risk_level enum ==="
grep -rn "risk_level" references/ | grep -v ".git"
```

- [ ] **Step 2: Verify all schema references point to existing files**

```bash
echo "=== Checking file references ==="
for ref in $(grep -ohP 'references/[a-z0-9_/.-]+\.md' .claude/skills/*/SKILL.md AGENTS.md | sort -u); do
  if [ -f "$ref" ]; then
    echo "OK: $ref"
  else
    echo "MISSING: $ref"
  fi
done
```

Expected: all references resolve to existing files.

- [ ] **Step 3: Verify all skill file line counts ≤ 200**

```bash
echo "=== Checking skill file sizes ==="
for f in .claude/skills/*/SKILL.md; do
  lines=$(wc -l < "$f")
  if [ "$lines" -le 200 ]; then
    echo "OK: $f ($lines lines)"
  else
    echo "OVER: $f ($lines lines - exceeds 200 limit)"
  fi
done
```

- [ ] **Step 4: Verify no duplicated definitions**

```bash
# Check that analysis path definitions only exist in registry
echo "=== Checking path definition uniqueness ==="
grep -rn "path_id\|full-chain\|targeted-update\|pricing-focused\|quick-scan" .claude/skills/ | grep -v "reference" | grep -v "引用"
# Should return nothing — skills should only reference, not define
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore: cross-reference consistency verification passed"
```

---

### Task 13: End-to-end smoke test

**Files:**
- No new files. Manual verification via CLI.

**Interfaces:**
- Consumes: all system files
- Produces: test log (manual). No code artifacts.

- [ ] **Step 1: Verify skill discovery**

```bash
ls -la .claude/skills/*/SKILL.md
```
Expected: 5 SKILL.md files listed.

- [ ] **Step 2: Verify AGENTS.md is readable as entry point**

```bash
head -5 AGENTS.md
grep "技能索引" AGENTS.md
grep "非协商条款" AGENTS.md
```

- [ ] **Step 3: Manual invocation test plan (documented, not automated)**

Run the following test scenarios manually:

1. **Full-chain test**: "帮我评估一下XX科技，计划明年申报科创板，目前刚完成股改"
   - Expect: Router matches full-chain → industry → tech → finance → pricing
   - Each node outputs risk matrix with 3 roles × ≥5 entries (deep mode)

2. **Targeted update test**: "上次推演PLAN-20260730-001，刚收到新的财务数据，帮我重新跑一下财务节点"
   - Expect: Router matches targeted-update → routes to finance-scanner only
   - Reuses previous industry/tech artifacts

3. **Quick scan test**: "有个项目想做科创板，帮我看一下行业和技术靠不靠谱"
   - Expect: Router matches quick-scan → industry + tech nodes
   - Each role ≥1 entry (quick mode)

4. **Out-of-scope rejection test**: "帮我写一份招股说明书"
   - Expect: Router response = [OUT_OF_SCOPE]

5. **Missing plan rejection test**: 直接调用 industry-scanner 而不提供分析计划单
   - Expect: Scanner rejects with "未收到分析计划单"

- [ ] **Step 4: Document results**

Record test outcomes in a test log comment on the final commit.

- [ ] **Step 5: Final commit**

```bash
git add -A
git commit -m "test: end-to-end smoke test scenarios documented"
```
