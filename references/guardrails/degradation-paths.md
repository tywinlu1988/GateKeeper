# 降级策略（Degradation Paths）

> 当搜索失败、数据不足、或结果矛盾时，各节点按以下策略降级运行。降级不做自动裁决——始终保留原始信息，标注降级原因。

## D0: 降级标注的状态转移

降级标注（D1-D4）跨计划单追踪时使用三种状态：
- **open**：标注产生，问题未消解
- **narrowed**：新数据部分消解（如冲突区间收窄、时效缺口缩小）——在 inline_summary 中说明消解程度
- **resolved**：新数据完全消解——移除标注，在制品中记录 `degradation_resolved: {type, resolved_at, by_plan_id}`

后续推演遇到前次标注时必须给出状态判定，禁止无限期原样延续。

## D1: 搜索不可用（Search Unavailable）

**触发条件**：WebSearch 工具调用失败、超时、或返回空结果达 3 次以上。
**降级行为**：
- 所有风险条目标注 `[SEARCH_UNAVAILABLE]`
- 优先引用 `knowledge/` 基准库（引用时 data_as_of 填基准日期，规则见 knowledge/README.md），其次基于用户提供的材料（existing_materials 字段）做分析
- 如果基准库无覆盖且用户未提供任何材料 → 输出空风险矩阵，标注 `analysis_blocked: no_search_and_no_materials`
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

## D4: 数据时效不足（Stale Data）

**触发条件**：搜索成功、结果不稀疏，但可用来源的 `data_as_of` 超出 G7 时效阈值（典型：命中旧研报、旧一致预期、旧统计周期）。D1-D3 均不覆盖此情形。
**降级行为**：
- 强制一轮带当前年份/「最新」/「TTM」限定词的补充搜索
- 仍无时效合格数据 → 查 `knowledge/` 基准库是否有覆盖；有 → 引用基准（data_as_of 填基准日期），节点 confidence 降为 low
- 基准库也无覆盖 → 该数值论断标注 `[STALE_DATA: as_of=YYYY-MM]`，节点 confidence 降为 low
- **时效不合格的数据禁止写入执行摘要、TOP 3 风险和 overall_rating 的判断依据**——仅可保留在条目正文中并带标注。旧数据可以进附录，不能进结论位
- 禁止用参数记忆（训练知识）填补时效缺口；若某论断只能依赖记忆，标注 `[MEMORY_ONLY: 未经当前搜索验证]`，同样禁止进结论位
