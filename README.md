# GateKeeper

科创板 Pre-IPO 外部视角风险推演引擎。为保荐承销机构提供 Pre-IPO 投资人、上市后买方、舆论三方视角的结构化风险评估。

## 功能概述

GateKeeper 围绕科创板 IPO 保荐承销场景，覆盖从行业定位到发行定价的四个关键推演节点：

| 节点 | 技能 | 分析范围 |
|------|------|---------|
| **入口路由** | `ipo-router` | 项目状态评估 → 路径匹配 → 生成分析计划单 |
| **行业/业务定位** | `industry-scanner` | 赛道天花板、竞争格局、政策环境、"硬科技"属性 |
| **技术/知识产权** | `tech-scanner` | 核心技术先进性、IP 完整性、研发投入质量、技术依赖 |
| **财务合规** | `finance-scanner` | 收入确认质量、关联交易、现金流、财务内在一致性 |
| **定价/发行** | `pricing-scanner` | 可比估值、定价合理性、破发风险、估值故事可信度 |

每个节点由三个外部角色（Pre-IPO 投资人、上市后买方、舆论媒体）并行分析，各自按独立认知立场搜索、解读、输出风险条目，最终汇聚为风险矩阵报告。

## 分析路径

| 路径 | 触发场景 | 执行节点 |
|------|---------|---------|
| **full-chain** | 首次全链路推演、尽调完成 | industry → tech → finance → pricing |
| **pricing-focused** | 临近发行窗口、估值讨论 | industry → pricing |
| **targeted-update** | 新数据到达、局部信息更新 | 用户指定节点 |
| **quick-scan** | 初步项目筛选、快速评估 | industry + tech（并行） |

## 使用方式

### 通过 npx（推荐）

```bash
npx github:tywinlu1988/GateKeeper
```

### 源码安装

```bash
git clone https://github.com/tywinlu1988/GateKeeper.git
cd GateKeeper
```

然后在 Claude Code 中打开该目录，`.claude/skills/` 下的所有技能将自动被发现和加载。

### 快速开始

在 Claude Code 中描述你的 Pre-IPO 项目情况：

```
> 帮我评估一下某科技公司，计划明年申报科创板，目前刚完成股改
```

系统将通过 ipo-router 匹配分析路径，依次执行各节点推演，输出结构化风险矩阵报告。

## 核心特性

### 风险推演引擎

- **5 技能管道**：ipo-router → industry → tech → finance → pricing，顺序执行，制品传递
- **三角色并行分析**：Pre-IPO 投资人（退出视角）、上市后买方（持有视角）、舆论媒体（负面挖掘视角）
- **4 条分析路径**：full-chain / pricing-focused / targeted-update / quick-scan

### 前瞻信号监测（v0.2.0+）

- 每条重大风险附带信号清单：正向信号（风险缓解）、负向信号（风险兑现）、必须做对的事
- 信号优先级矩阵（v0.3.0）：T1 结构级 > T2 趋势级 > T3 事件级，避免短期噪音干扰长期判断
- 弹性时间窗口（v0.3.0）：按风险类别差异化（客户 2-4Q / 技术 4-8Q / 利润 4-8Q）

### 跨维度传染分析（v0.2.0+）

- 9 条传染通道（C1-C9）：追踪风险在行业→技术→财务→定价间的级联传导
- 多路径叠加放大（v0.3.0）：≥2 通道同时激活时 1.5× 放大，≥3 通道 2.0× 放大
- C9 外部范式飞跃通道（v0.3.0）：低概率极端事件的监测与逆转信号处理

### 质量体系

- 10 条非协商条款（防漂移）
- 9 道质量门禁（含 G1.5 信号完备、G1.6 交叉信号一致性、G1.7 异议角色加权）
- 3 条降级策略（搜索不可用 / 数据稀疏 / 结果矛盾）
- 管理层执行力代理指标（v0.3.0）：辅助判断，不参与评分

## 项目结构

```
├── AGENTS.md                    # 全局编排、技能索引、非协商条款
├── .claude/skills/              # 技能执行层
│   ├── ipo-router/SKILL.md
│   ├── industry-scanner/SKILL.md
│   ├── tech-scanner/SKILL.md
│   ├── finance-scanner/SKILL.md
│   └── pricing-scanner/SKILL.md
├── references/                  # 知识/规则层
│   ├── analysis-registry.md     # 分析路径注册表
│   ├── artifact-schemas.md      # 制品 Schema 定义
│   ├── contagion-matrix.md      # 跨维度传染矩阵（C1-C9 + 叠加规则）
│   ├── signal-watchlist.md      # 前瞻信号监测框架（T1-T3 + 逆转信号）
│   ├── roles/                   # 三角色定义
│   ├── guardrails/              # 质量门禁（G1-G6 + G1.5/1.6/1.7）
│   └── templates/               # 风险矩阵输出模板（MD + HTML）
├── knowledge/                   # 知识库插槽（预留给未来 A 方案）
└── docs/                        # 文档
```

## 许可证

MIT License
