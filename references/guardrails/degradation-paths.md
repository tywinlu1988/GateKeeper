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
