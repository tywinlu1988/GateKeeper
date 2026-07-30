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

### 源码安装

```bash
# 克隆仓库
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
│   ├── roles/                   # 三角色定义
│   ├── guardrails/              # 质量门禁、非协商条款、降级策略
│   └── templates/               # 风险矩阵输出模板
├── knowledge/                   # 知识库插槽（当前预留给未来 A 方案）
└── docs/                        # 文档
```

## 许可证

MIT License
