# Claude Code Skill 制作技术综合分析报告

> 基于四个仓库的系统性研究：
> 1. **FolioPulse** — 投资标的推荐引擎
> 2. **Credence-Global** — 国际固收信用分析引擎
> 3. **Credence-China** — 中国固收信用分析引擎
> 4. **Baker-Street** — Sherlock 多视角分析框架

---

## 目录

1. [核心发现](#1-核心发现)
2. [四项目架构对比](#2-四项目架构对比)
3. [Skill 制作核心模式](#3-skill-制作核心模式)
4. [复杂分析逻辑的编码技术](#4-复杂分析逻辑的编码技术)
5. [反模式与常见问题](#5-反模式与常见问题)
6. [推荐采纳的技术清单](#6-推荐采纳的技术清单)

---

## 1. 核心发现

### 1.1 四个项目形成了一条清晰的进化链

```
FolioPulse (简单)  →  Credence-China (成熟)  →  Credence-Global (国际化)  →  Baker-Street (元技能)
   3个skill              4个skill                   4个skill                   1个元skill
   3个pipeline阶段        4个pipeline阶段            4个pipeline阶段            4个phase
   单角色                 6个角色(M0-M5)             6个角色                   7个persona
   1条工作路径            16条工作路径               16条工作路径               动态
   公开数据              公开+外部数据               公开+外部数据              研究+搜索
   引擎文档独立           引擎文档→skill引用          引擎文档→skill引用          prompt→子agent
```

### 1.2 最关键的发现：所有四个项目共享同一套底层架构哲学

这套哲学包含以下几个层次：

| 层次 | 模式 | 成熟度 |
|------|------|--------|
| **架构层** | 多阶段管道 + 结构化制品传递 + 单一事实源 | 高度成熟 |
| **知识层** | engine/ 文档作为知识库 + skill 作为执行器 | 成熟 |
| **流程层** | 路由→分析→报告→质检的四段链 | 成熟 |
| **质量层** | 门禁校验 + 自愈回退 + 反漂移铁律 | 中高 |
| **编排层** | 链式调用 + 自动化过渡 + 确认点注入 | 中等 |

---

## 2. 四项目架构对比

### 2.1 FolioPulse — 入门级但完整的 Skill 系统

**结构：**
```
AGENTS.md                          ← 全局编排器 + 技能索引 + 反漂移铁律
├── .claude/skills/
│   ├── profile-intake/SKILL.md    ← 客户画像摄入（预检 + 4问路由）
│   ├── recommend-engine/SKILL.md  ← 推荐引擎（5步管道）
│   └── recommend-qa/SKILL.md      ← 质检+交付（5门禁 + 自愈回退 + 2段交付）
├── engine/                        ← 单一事实源（评分框架、过滤规则、适当性矩阵）
├── src/                           ← Python可执行实现（加载engine/配置）
├── templates/                     ← HTML交付物模板
└── profiles/                      ← 默认配置
```

**关键数字：** 3个skill、4阶段管道、7项反漂移铁律、5步推荐管道、5项门禁

**最佳模式：**
- **§0 预检协议**：提问前先扫描已有信息，只问缺失的
- **进度签章行**：每步管道输出 `[n/5] 步骤名: {metrics}` 格式的签章
- **自愈回退**：质检失败→自动退回→修正→重新质检（一轮自动，超限才暴露给用户）
- **残留占位符扫描**：交付物生成后搜索 `{` 字符确保无未替换占位符

### 2.2 Credence-China — 最成熟的领域分析 Skill 系统

**结构（比FolioPulse显著膨胀）：**
```
AGENTS.md                          ← 全局编排器 + 防漂移铁律
dev/
├── .claude/skills/
│   ├── credit-analysis-router/    ← 四问路由→16条工作路径
│   ├── fixed-income-credit-analysis/ ← 按路径单执行分析
│   ├── credit-report-builder/     ← 分析产物→交付报告
│   └── credit-qa-verifier/        ← 预交付质量门
├── engine/
│   ├── engine-overview.md         ← 引擎总览
│   ├── mosaic-engine.md           ← 马赛克引擎（碎片数据拼图）
│   ├── dual-track-methodology.md  ← 双轨交叉验证
│   ├── industry-framework.md      ← 10维度行业评分
│   ├── lgfv-framework.md          ← 城投债专属（中国特有）
│   ├── m2/m3/m5-framework.md      ← 角色专属框架
│   ├── concentration-framework.md ← 五维集中度
│   ├── contagion-matrix.md        ← 跨行业传染
│   ├── ...（共20+个框架文档）
│   └── audits/                    ← 15+次质量审计报告
├── templates/                     ← 19种报告模板
├── src/                           ← Python scorer实现
├── tests/                         ← 全面测试
├── validation/                    ← 验证walkthrough
└── version/                       ← 版本打包（含完整skill包）
```

**关键数字：** 4个skill、16条工作路径、13+行业、19种报告模板、20+引擎文档、15+次审计

**最佳模式（超越FolioPulse的创新）：**

1. **工作路径注册表（Work Path Registry）** — 16条路径的单一事实源，每条路径定义：角色、对象、深度、引擎阅读顺序、质量门禁、模板。路由skill只做匹配，不做分析。

2. **路径战术手册（Path Playbooks）** — 每条工作路径有独立的执行契约文件（如 `WP-CS-01.md`），明确规定：触发条件、必读文档、执行步骤、维度词汇表、输出形状。这是"把决策树编码为文档"的最高形式。

3. **四段链式契约（Pipeline Contract）** — `pipeline-contract.md` 定义了四个阶段的制品字段形状和链式边。`path_id` 作为贯穿各段的 join key。

4. **马赛克引擎的信号密度门禁**：
   - 关键维度信号密度 <20% → 禁止输出数值评分
   - 加权平均密度 <50% → 禁止输出最终评级
   - 密度 50-80% → 允许评级但标"中等置信度"并拓宽区间 ±1 notch
   - 完整性报告为强制输出

5. **系统性审计文化** — `dev/engine/audits/` 包含15+次结构化质量审计，覆盖：能力审查、闭包检查、一致性审计、金融分析审计、量化审计、评级机构对标审计、风险管理标准审计等。

6. **版本管理体系** — `version/` 目录包含完整的发布包（skill包+引擎文档+模板+源码），`scripts/promote.py` 实现版本晋升。

7. **可执行编排器** — `src/pipeline.py` 从 `pipeline-contract.md` 读取阶段定义，仅对接线路径调用编码引擎。引擎文档为规范源，scorer 为其可执行实现，`tests/test_engine_doc_parity.py` 对账。

### 2.3 Credence-Global — 国际化版本

与 Credence-China 结构相同，但有以下差异：
- 移除了 LGFV（城投）框架
- 采用 GICS 19 行业分类替代中国13行业
- 六大国际分析范式（P1-P6）替代中国特定框架
- S&P/Moody's/Fitch 评级对齐
- IFRS/US GAAP 框架
- 6个国际买方角色

**版本差异显著：** Global 是 v0.0.1（早期），China 是 v0.10.4（成熟）。这反映了"先做深中国市场→再国际化"的演进策略。

### 2.4 Baker-Street (Sherlock) — 元技能：一个 skill 编排多个 agent

**结构：**
```
.claude/skills/sherlock/
├── skill.md                       ← 主编排器（5阶段管道，约1000行）
├── personas/                      ← 7个认知角色
│   ├── holmes.md                  ← 演绎推理
│   ├── watson.md                  ← 常识归纳
│   ├── moriarty.md                ← 对抗分析
│   ├── adler.md                   ← 社会情感智力
│   ├── lestrade.md                ← 证据实用主义
│   ├── hound.md                   ← 恐惧与偏见检测
│   └── mycroft.md                 ← 系统思维
├── scout-prompt.md                ← 斥候agent prompt（问题分解）
├── research-prompt.md             ← 研究agent prompt（事实收集）
├── quantitative-agent-prompt.md   ← 量化分析agent prompt
├── judge.md                       ← LLM-as-Judge评分
├── validate.md                    ← 验证套件
├── tools/analysis/                ← Python工具（stats.py, simulation.py等）
├── test-cases/                    ← 6个测试用例
└── platforms/                     ← 跨平台适配器
```

**关键数字：** 1个元skill、7个persona、5个phase、3层合成、CUR质量指标

**独特创新：**

1. **多Agent编排** — skill.md 不是给单个LLM执行的指令，而是给"主控LLM"的编排剧本——告诉它如何派发子agent、如何收集结果、如何合成。这是 skill 概念的最高级用法。

2. **认知角色差异化** — 7个persona各有独立的认知姿态、核心问题、方法论、盲点、输出格式。差异化不是通过修改同一段prompt实现的，而是从完全不同的认知哲学出发。

3. **三层合成架构**：
   - Layer 1: 冲突挖掘（Conflict Mining）— 比较每对persona的产出
   - Layer 1.5: 冲突反驳（Rebuttal）— 让冲突双方互相回应
   - Layer 2: 盲点合成（Blind Spot Synthesis）— 收集所有persona承认的盲点
   - Layer 3: 行动路径（Action Pathway）— 三级时间维度

4. **定量质量指标** — CUR (Claim Uniqueness Ratio) 测量persona重叠度，反谄媚比 (anti-sycophancy ratio) 确保足够多的反面证据。

5. **诚实机制** — 当CUR > 0.8且零冲突时，框架主动告知用户"多视角分析可能没有增加显著价值"。当反驳失败时，标注"反驳未维持"而非编造。

6. **Plugin分发** — 通过 `.claude-plugin/plugin.json` + `install.js` 实现跨平台安装。

---

## 3. Skill 制作核心模式

### 3.1 三层架构模式（最核心的模式）

所有四个项目都使用严格的三层分离：

```
┌─────────────────────────────────────────┐
│  AGENTS.md / CLAUDE.md                  │  ← 全局编排层
│  "这个项目是什么、有哪些skill、怎么串联"   │
├─────────────────────────────────────────┤
│  .claude/skills/*/SKILL.md              │  ← Skill执行层
│  "怎么做：步骤、工具、护栏、输出schema"    │
├─────────────────────────────────────────┤
│  engine/*.md / references/*.md          │  ← 知识/规则层
│  "知道什么：阈值、权重、矩阵、分类法"      │
└─────────────────────────────────────────┘
```

**为什么有效：**
- Skill文件保持精简（Credence-Global的fixed-income-credit-analysis从初始1000+行瘦身到约150行，细节下沉到references/）
- 规则变更只需要改engine文档，不需要改skill
- 同一套规则可被多个skill引用
- LLM token消耗可控——只加载当前路径需要的文档

### 3.2 管道+制品传递模式

```
Skill A ──YAML artifact──→ Skill B ──YAML artifact──→ Skill C
  ↑                            ↑                           ↑
  path_id贯穿各段，作为join key
```

**关键设计决策：**
- 制品格式统一为YAML（结构化、人类可读、LLM友好）
- 每个skill定义其输出schema
- path_id/ profile_id 作为贯穿标识符
- 某些过渡自动化（S1→S2），某些需要用户确认（S3→S4）

### 3.3 单一事实源 + 反漂移模式

```
铁律：阈值、权重、评级映射只存在于 engine/*.md
Skill文件：引用 "engine/scoring-framework.md §3.2"
Python代码：engine_loader.py 从markdown提取YAML → 运行时加载
```

**实施机制：**
- AGENTS.md 声明反漂移铁律（FolioPulse有7+1条，Credence有5+1条）
- engine_loader.py 抛出 `EngineDocError("引擎未定义")` 当文档缺失
- 测试验证：`test_engine_doc_parity.py` 对账引擎文档与scorer实现
- 一致性检查：`consistency_check.py` 扫描数值重复定义

### 3.4 工作路径路由模式（复杂分析的核心）

这是Credence项目最先进的模式：

```
用户输入（模糊/复合）
    │
    ▼
credit-analysis-router (SKILL.md)
    │ 四问协议：角色/对象/深度/数据
    │ 查 work-path-registry.md
    ▼
Path Sheet (YAML)
    │ path_id, engine_reading_order, quality_gates, templates
    ▼
fixed-income-credit-analysis (SKILL.md)
    │ 读取 path-playbooks/{path_id}.md
    │ 按 engine_reading_order 读取引擎文档
    │ 执行分析步骤
    ▼
Analysis Artifact (YAML)
    │
    ▼
credit-report-builder → credit-qa-verifier
```

**work-path-registry.md 条目示例：**
```yaml
WP-CS-01:
  role: credit-selector
  object: single-issuer
  depth: L2
  status: active
  engine_reading_order:
    - dev/engine/industry-framework.md
    - dev/engine/mosaic-engine.md
    - dev/engine/dual-track-methodology.md
  quality_gates:
    - "Signal Density (mosaic-engine.md §4.3)"
    - "Veto (industry-framework.md §5)"
    - "Cross-Validation (dual-track-methodology.md §4)"
  templates: [type1, type2, type14]
```

### 3.5 多Agent编排模式（Baker-Street特有）

```
skill.md (主控LLM)
    │
    ├── Phase 0: 斥候Agent (问题分解)
    │
    ├── Phase 1: 研究Agent × N (事实收集)
    │       └── 编译共享事实库
    │       └── 收集定量分析需求
    │       └── 执行定量分析Agent
    │
    ├── Phase 2: Persona Agent × 7 (独立推理)
    │       └── 每个从共享事实库获取证据
    │       └── 每个收到定量分析包
    │       └── Baseline Agent (无persona对照组)
    │
    └── Phase 3: 合成
            └── 冲突挖掘 → 反驳 → 盲点合成 → 行动路径
```

**核心创新：**
- Persona作为可插拔的"认知滤镜"
- 共享事实库确保所有persona使用相同的证据基础
- Baseline agent作为对照组衡量框架增益
- 反驳机制模拟学术同行评议
- **两轮推理（v0.6关键创新）**：实测发现当所有persona共享定量分析包时，CUR从0.52骤降到0.45（同质化）。修复方案：第一轮persona独立起草（无定量包）→第二轮用定量包修订，每个结论标注 `[DATA: CONFIRMED/REVISED/UNSUPPORTED]`。修复后CUR恢复到均值0.622
- **Agent超时预算校准**：基于实测数据设定（研究600s, persona 360s, revision 300s, scout/rebuttal 240s）
- **实测指标**：agent失败率从7.7%优化到3.1%，persona崩溃率0%，反驳成功率100%，反谄媚比11-20%维持

---

## 4. 复杂分析逻辑的编码技术

### 4.1 决策树 → 工作路径注册表

**问题：** 信用分析有大量分支逻辑——不同角色、不同对象、不同深度需要完全不同的分析流程。

**解决方案：** 不把决策树编码在skill prompt里（会爆炸），而是编码在 `work-path-registry.md` 的声明式表格中。Router skill只做"提取特征→查表→匹配路径"。

```yaml
# 16条路径，每条定义了完整的分析路线
WP-CS-01: { role: credit-selector, object: single-issuer, depth: L2 }
WP-PM-01: { role: portfolio-manager, object: single-issuer, depth: L2 }
WP-RO-01: { role: risk-officer, object: portfolio, depth: L2 }
# ...
```

### 4.2 多维度评分 → 范式+维度+金字塔

**问题：** 不同行业的信用分析重点完全不同——银行的信用分析不适用于科技公司。

**解决方案：**
1. 先将行业映射到6个范式（P1-P6）
2. 每个范式有独立的10维度权重模板（D1-D10各1-5分）
3. 每个范式有独立的4层金字塔（L1最重要→L4最次要）
4. 一票否决条件在各行业框架的§5定义

```
行业分类 → 范式确定(6选1) → 维度权重(10维×范式特定) → 金字塔评分(4层) → 评级映射(18级)
```

### 4.3 交叉验证 → 双轨+冲突裁决矩阵

**问题：** 单一分析轨道可能产生系统性偏见。

**解决方案：**
- 轨A（基本面）：定性+定量评分
- 轨B（市场信号）：信用利差/波动率/资金流/评级迁移
- 两轨独立运行，然后交叉对撞
- 冲突裁决矩阵明确优先级（一致增强、分歧时A优先、一致削弱）

```
轨A positive + 轨B positive → 互证增强，评分+0.5
轨A positive + 轨B negative → 轨A优先，标注"市场信号分歧"
轨A negative + 轨B positive → 轨A优先，标注"市场信号先行"
轨A negative + 轨B negative → 互证削弱，评分-0.5
```

### 4.4 数据不确定性 → 马赛克引擎的信号密度门禁

**问题：** 公开数据总是不完整的，但LLM倾向于忽略数据缺失。

**解决方案：**
- 将"数据缺失"本身编码为风险信号
- 用信号密度（有效数据点/总数据点）作为置信度代理
- 低于阈值时强制限制输出（不能给数值评分、不能给最终评级）
- 完整性报告为所有分析的强制输出

这是"让LLM承认自己不知道"的最强机制。

### 4.5 质量保证 → 门禁+质检+审计

**三层质量机制：**

1. **门禁（Gates）**：分析过程中的硬性检查点（信号密度、否决条件、交叉验证）
2. **质检（QA）**：交付前的系统性复核（5门禁检查、自愈回退、一票否决）
3. **审计（Audit）**：离线质量评估（一致性审计、评级机构对标、从业者可用性审计）

---

## 5. 反模式与常见问题

### 5.1 重量级问题（最严重）

**表现：**
- Credence-China 有 20+ 引擎文档、19 种报告模板、15+ 审计报告
- 每条工作路径需要阅读 3-10 个引擎文档
- AGENTS.md 本身就有数百行

**影响：**
- LLM context window 消耗巨大
- 初次使用需要大量阅读
- 维护负担重——一个阈值变更需要审计所有引用

**缓解策略（项目中观察到的）：**
- SKILL.md 瘦身（Credence从1000+行瘦到约150行）
- 按路径加载（只读 engine_reading_order 中列出的文档）
- 细节下沉到 references/（不常用的细节不占主prompt）

### 5.2 过度工程化

**表现：**
- 定义了很多框架但可能从未被执行（如Credence-Global的很多框架标注v0.0.1）
- 路径战术手册非常详细，但LLM可能无法严格遵循每一步
- 版本管理复杂，但实际发布包可能很少有人安装

**建议：**
- 从最小可行路径开始，逐步扩展
- 先验证核心路径的LLM执行质量，再增加新路径
- 用实际使用数据驱动框架扩展，而非预先设计

### 5.6 Credence-China 特有发现

**28个版本22天**：从 v0.1.0 (7月7日) 到 v0.10.4-release (7月29日)，平均每天1.3个版本。

**14次审计报告**：`dev/engine/audits/` 包含14次结构化质量审计，覆盖能力审查、量化审计（21个统计问题，Bootstrap CI/FDR/ADF/Newey-West）、评级机构对标（Moody's/S&P/Fitch差距分析）、从业者可用性审计、风险管理标准合规（Basel/COSO）。

**M0-M5六角色框架**：中国版特有承销（M2）、交易（M3）、融资顾问（M5）三个专属框架，超越典型全球信用分析的覆盖范围。

**诚实缺口文化**：明确记录的数据缺失包括——无Z-spread/OAS/凸性/买卖价差（国内债市基础设施限制）、区县级城投财政数据不可靠、无公开违约回收数据库。量化审计自评"18/21问题在文档中修复，0%已编码"。

**核心矛盾**：方法论深度极高（11,467行文档），但编码覆盖率极低（仅6个已编码引擎）。自评为"方法论验证"阶段，尚未到达MVP。

### 5.3 紧耦合问题

**表现：**
- Skill文件通过精确路径引用引擎文档（`dev/engine/mosaic-engine.md §4.3`）
- 引擎文档重命名/重组节会破坏所有引用
- 跨文档的版本一致性缺乏自动化保证

**缓解策略（部分实现）：**
- `consistency_check.py` 扫描重复定义
- `tests/` 中有些测试验证文档引用
- 但没有自动化的交叉引用验证（§锚点是否真实存在）

### 5.4 语言锁定

FolioPulse和Credence-China全部中文，Credence-Global全部英文。国际化需要完全重写skill和引擎文档。这是领域特定的固有限制。

### 5.5 提示缓存未充分利用

虽然引擎文档设计成"按需加载"，但没有显式的缓存策略说明。多次调用相同路径时，引擎文档可能被重复发送到LLM。

---

## 6. 推荐采纳的技术清单

### 🔴 核心必学（强烈推荐）

| # | 技术 | 来源 | 说明 |
|---|------|------|------|
| 1 | **三层架构分离** | 全部 | AGENTS.md编排 + SKILL.md执行 + engine/知识 |
| 2 | **单一事实源+反漂移** | 全部 | 所有数值定义在engine/，skill只引用不定义 |
| 3 | **管道+结构化制品传递** | FolioPulse, Credence | YAML制品作为skill间通信协议 |
| 4 | **工作路径路由** | Credence | Router skill → 注册表 → Path Sheet → 执行 |
| 5 | **信号密度门禁** | Credence | "不知道"本身作为风险信号，低于阈值禁止输出 |
| 6 | **双轨交叉验证** | Credence | 独立轨道并行分析→冲突裁决矩阵 |
| 7 | **自愈回退循环** | FolioPulse | QA失败→自动退回修正→重新质检 |
| 8 | **残留占位符扫描** | FolioPulse | 生成后搜索 `{` 确保无未替换模板变量 |

### 🟡 进阶推荐（按需采纳）

| # | 技术 | 来源 | 说明 |
|---|------|------|------|
| 9 | **路径战术手册** | Credence | 每条路径独立的执行契约文件 |
| 10 | **进度签章行** | FolioPulse | `[n/5] 步骤名: {metrics}` 格式 |
| 11 | **多Agent编排** | Baker-Street | skill编排多个子agent的剧本 |
| 12 | **Persona差异化** | Baker-Street | 独立认知姿态+核心问题+盲点+输出格式 |
| 13 | **冲突反驳机制** | Baker-Street | 冲突双方互相回应→合成判断 |
| 14 | **CUR质量指标** | Baker-Street | 测量persona重叠度 |
| 15 | **框架增益评估** | Baker-Street | Baseline对照组衡量框架是否真的增加了价值 |
| 16 | **诚实失败机制** | Baker-Street | 框架无效时主动告知用户 |

### 🟢 基础设施（工程实践）

| # | 技术 | 来源 | 说明 |
|---|------|------|------|
| 17 | **引擎加载器** | FolioPulse, Credence | Markdown→YAML提取→运行时加载 |
| 18 | **对账测试** | Credence | `test_engine_doc_parity.py` 确保doc与code一致 |
| 19 | **一致性检查脚本** | 全部 | 扫描数值重复定义和违反单一事实源 |
| 20 | **版本打包** | Credence-China | version/目录 + promote脚本 |
| 21 | **Plugin分发** | Baker-Street | plugin.json + install.js 跨平台安装 |
| 22 | **跨平台适配器** | Baker-Street, Credence | codex.md / antigravity.json / cursor.json |
| 23 | **工具名抽象层** | Baker-Street | tool-map.json 映射通用名→平台API，persona/research/scout prompt零平台依赖 |
| 24 | **降级即设计模式** | Baker-Street | 每个phase有显式的部分失败/超时/空输出处理，系统优雅降级而非崩溃或幻觉 |
| 25 | **实测驱动架构演进** | Baker-Street | CUR崩溃测量→两轮推理重构，超时预算从实测agent时长校准 |

---

## 附录：四个项目的Skill系统对比表

| 维度 | FolioPulse | Credence-China | Credence-Global | Baker-Street |
|------|-----------|---------------|-----------------|-------------|
| Skill数量 | 3 | 4 | 4 | 1（元skill） |
| Pipeline阶段 | 4 | 4 | 4 | 4（phase） |
| 管道过渡 | 自动+确认点 | 自动+确认点 | 自动+确认点 | Phase顺序 |
| 工作路径数 | 1 | 16 | 16 | 动态 |
| 角色/Persona | 1（RM） | 6（M0-M5） | 6（国际角色） | 7+baseline |
| 引擎文档数 | 8 | 20+ | 20+ | N/A（prompt体系） |
| 模板数 | 7 | 19 | 18 | 0 |
| Python代码 | 有 | 有 | 有 | 有（工具脚本） |
| 测试覆盖 | 最小 | 全面 | 全面 | 中等 |
| 审计体系 | 无 | 15+次审计 | 无 | 验证套件 |
| 版本管理 | 无 | 有（version/） | 有 | 有（ROADMAP） |
| 跨平台 | 有限 | 有适配器 | 有适配器 | 有adapter+plugin |
| 语言 | 中文 | 中文 | 英文 | 英文+中文 |
| 成熟度 | 生产就绪 | v0.10.4 | v0.0.1（早期） | 生产就绪 |
| 复杂度 | ★★☆ | ★★★ | ★★★ | ★★★ |

---

*报告生成日期：2026-07-29*
*分析方法：直接阅读GitHub API获取的核心文件 + FolioPulse子agent深度分析*
