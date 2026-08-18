# 质量门禁（Quality Gates）

> 每个 Scanner 节点完成后必须通过以下门禁。任一门禁失败 → 标注失败原因 → 重新生成或触发降级。

## G1: 角色完备（Role Completeness）

**规则**：depth=deep（full-chain / pricing-focused）：每个角色 ≥ 5 条风险条目。
       depth=standard（targeted-update）：每个角色 ≥ 3 条。
       depth=quick（quick-scan）：每个角色 ≥ 1 条。
**搜索留痕完备（v0.4.1 新增，v0.4.5 补一手披露验收与单一事实源）**：`search_log` 必填，每角色独立查询次数与深度对应（**次数标准见 analysis-registry 深度级别定义——唯一事实源，此处不复制**），
       且查询词须带时间限定词（Step 0）。**deep 深度下每角色 ≥1 条查询命中一手披露模板**（招股书申报稿 / 问询函回复 / 发行公告，见 roles 查询模板）。
       pricing 节点另须 `market_snapshot` 八项齐全（每项含 as_of 与结果）。
**反凑数规则（v0.4.2 新增）**：
       - 三角色的 search_log 完全雷同（同查询词 + 同时间戳）视为一次查询，不重复计数——共享查询只允许存在，不允许充数
       - 每角色至少 2 条**角色独有查询**，且与该角色搜索策略匹配（如舆论角色必须有负面/诉讼/质疑类查询）
       - 实测反例：pricing 节点三角色 search_log 逐字相同（同词/同时间戳/同 hits）——一次执行复制三份，判定不合规
**制品-日志对账（v0.4.4 新增）**：过程日志/汇报中的任何统计数字（条目数、查询次数、门禁结果）必须与落盘制品一致。
       实测反例：日志声称"51 条风险条目、48 次查询、门禁全过"，制品实为 40 条且 finance/pricing 无 search_log——日志与制品不一致视同 G1 不通过。
**不通过处理**：标注数据不足的角色，**必须在 node_artifact 中显式记录** `confidence: low` 及缺口说明（哪个角色差几条/几次查询）——静默放行视同门禁未执行（v0.4.4 强化）。

## G1.5: 信号完备（Signal Completeness）

**规则**：每条 risk_level = critical 或 high 的风险条目，必须附带 signal_watchlist（≥2 条正向信号 + ≥2 条负向信号 + ≥1 条 what_must_go_right）。信号设计须遵循可观测、有阈值、有时效、有含义、双面对称五原则。
**不通过处理**：标注 `signal_incomplete`，要求补充信号清单。最多重试一次。

## G1.6: 交叉信号一致性（Cross-Signal Consistency）

**规则**：当同一风险条目的 signal_watchlist 中包含跨优先级层级（T1 vs T2/T3）且方向相反的信号时，按 `references/signal-watchlist.md §3.6` 的优先级冲突处理规则执行。T1 信号优先于 T3，被覆盖信号标注 `overridden_by_T1`。冲突处理结果须在 risk_entry 中记录。
**不通过处理**：不做拒绝——仅标注 `cross_signal_conflict: true` 并列出覆盖理由。覆盖后的风险等级以主导信号为准。

## G1.7: 异议角色加权（Dissenting-Role Escalation）

**规则**：汇聚步骤完成后，若角色 A 的 risk_level ≥ 角色 B 和 C 的 risk_level + 2 档（如 A=Critical, B/C=Low），触发异议加权——该角色此条判断权重 ×1.5，在风险矩阵中置顶，在 conflicts 中标注 `dissenting_view: {role}` 和 `amplified: true`。
**设计依据**：GateKeeper 系统性低估风险幅度（方向正确，量级保守）。当某一角色给出显著高于其他角色的风险等级时，值得额外关注。
**不通过处理**：不做拒绝——信息增强，仅标注升级。

## G2: 来源多样（Source Diversity）

**规则**：同一角色内不同风险条目使用不同 primary_source URL。
       同一 URL 最多支撑 2 条风险条目。
**不通过处理**：合并同源条目，标注 `source_concentration: high`。

## G3: 证据内联（Evidence Inline）

**规则**：每条风险条目必须有 `evidence.inline_summary` 字段，且非空。
       裸 URL（有 primary_source.url 但无 inline_summary）视为不通过。
       深度 deep 下另须 `key_data_points[].source_ref` 逐条填写（指向 search_log 中对应查询，如 "buy-side#2"；
       无法追溯时填 [UNLOGGED]）——数字追溯链是审阅者核验出处的前提（实测反例：weak 模型某轮 finance/pricing
       制品 source_ref 使用 0 处，大量数字无法核实出处）。
**不通过处理**：拒绝通过，要求补充内联摘要。最多重试一次。

## G4: 枚举合规（Enum Compliance）

**规则**：所有条目的以下字段必须在枚举值范围内：
       - `node`: industry | tech | finance | pricing
       - `role`: pre-ipo-investor | buy-side | media
       - `risk_level`: critical | high | medium | low
       - `id`: 格式 RISK-{node}-{role}-{seq}（seq 为 3 位数字），且 **{role} 段必须等于 role 字段的完整枚举值**——禁止缩写（实测反例：`RISK-pricing-pre-ipo-001` 用缩写 pre-ipo 冒充枚举值 pre-ipo-investor，却自评 G4 通过；ID 是跨节点/跨计划单追溯的主键，缩写会使对账与状态转移失效）
**不通过处理**：拒绝通过，返回修正后的条目。

## G5: 角色锚定与可执行性（Role Anchoring + Actionability）

**规则**：每条风险的 `rationale` 字段阐述的理由必须与该角色的认知立场一致。
       检查方式：rationale 中的关键词是否与角色的"核心问题"和"搜索重点"匹配。
       买方说"上市后估值合理性"= 通过。买方说"Pre-IPO 退出机制"= 不通过。
**可执行性（v0.5.0 新增）**：
       - `suggested_response` 必须是保荐机构可执行动作（含动词与对象），"关注XX""加强管理""提高警惕"等空泛表述视为不通过
       - `priced_in` 判定必须附推导依据（如"发行 PE 隐含 35%+ 增速"），拍脑袋判定视为不通过
       - `response_owner` / `response_deadline` 必填
**概率语义分型（v0.7.0 新增——全体系数值论断的唯一语义规则，适用于所有产物，非仅风险条目）**：
       每个数值型论断必须先自报类型，按类型受检。禁止跨类型混用（C 型判断冒充 A 型统计 = 频准激光"破发概率 50-65%"事故）。
       - **A 型·描述性统计**（对已发生事实的观察，如破发率 12%、撤回率 2.5%）：四要件不变——样本量、统计区间起止时间、来源 URL、data_as_of，四缺一删除该数字；叠加 G7 时效
       - **B 型·基准率外推**（把 cohort 统计直接用作预测，如"参照 2026H1 科创板 68 只零破发，首日破发概率≈0"）：在 A 型四要件之上加两件——①参照类显式（"参照类 = 2026H1 科创板全部新股"）②可交换性假设显式（本标的与参照类无系统性差异的成立/不成立说明）；**存在 regime 变化证据时必须降置信并标注**（如智元案：用 2026H1 港股数据外推 Q4 上市，而 7 月打新环境已转冷）
       - **C 型·主观判断预测**（基准率+个案调整，如"本标的破发概率 15%"）：数值**只允许出现在 S5 预测记录及报告「预测与验证计划」区块**，正文叙述一律用三档速记。S5 内强制：base_rate_ref（锚定的 B 型基准）+ 偏离理由（一句话）+ 点估计（允许附区间表达不确定度）
       - **D 型·隐含反推**（对假设的算术，如"当前定价隐含 2026 营收 +281%"）：非概率，参数显式标注为假设（v0.5.0 既有规则，不变）
       - **三档速记数值锚**：低 = 5-20% / 中 = 20-50% / 高 = 50-80%——三档是展示层速记，与 C 型点估计可互译；禁止在三档语义下夹带无锚百分比
       - **S5 可证伪性检查**：每条 prediction_record 必须具备 claim（可证伪陈述）+ resolution_criteria（数据源+判定规则）+ resolution_window（验证窗口），缺一直接判不通过；`scored: false` 合法但必须附理由——禁止为凑评分把不可测陈述强行数值化
**不通过处理**：标注 `role_drift_detected` 或 `response_not_actionable`，重新生成该条目。

## G6: 自包含（Self-Containment）

**规则**：输出报告不得包含：
       - 本地绝对路径（如 `/home/user/project/...`、`file:///...`）
       - 外部 CSS/JS 引用（如 `<link rel="stylesheet" href="...">`）
       - 仅裸 URL 作为证据（必须有 inline_summary）
**不通过处理**：标注违规位置，要求修正。

## G7: 时效合规（Time Validity）

**规则**：每条风险条目的 `evidence.primary_source.data_as_of` 必填，且与论断性质匹配：
       - **市场环境类论断**（破发率、估值倍数、审核/撤回统计、发行制度、市场情绪、融资热度）：`data_as_of` 距 `generated_at` ≤ 6 个月
       - **财务/经营类论断**（财报数据、经营指标、客户结构、市场规模、市占率、行业增速）：≤ 18 个月
       - **历史案例引用**（claim 中明确表述为历史事件的）：豁免时效阈值，但 `data_as_of` 仍须如实填写其发生期
**归类裁定**：市场规模/市占率/行业增速属于慢变数据，一律归"财务/经营类"（18 个月），不按市场环境类从严；只有反映"当前市场制度与情绪"的数据才适用 6 个月阈值。
**基准库证据限制（v0.4.1 新增）**：`source_type = baseline` 的证据：
       - 引用前必须在 `search_log` 中存在对应的实时搜索尝试（先搜后查库，顺序可审计）
       - 禁止单独支撑执行摘要、TOP 风险、overall_rating 的结论位——除非有同期（≤6 个月）`source_type = search` 的来源交叉确认
**时效判定清单（v0.4.1 新增，v0.4.2 强化）**：每个节点 Step 4 必须输出本节点的 G7 时效判定清单：
       每条带数值的证据一行：**论断 | data_as_of | 类别（市场/财务经营/历史案例） | 距今月数 | 阈值 | ✅/❌/D4 标注**。
       - 「距今月数」必须是**计算值**（T0 减 data_as_of，逐条算出来），不是估计——判定以距今月数与阈值的数值比较为准，禁止凭感觉判定（实测反例：as_of 2024 年报数据在 2026-08 被判"≤18 月 ✅"，实际 ~20 个月超期）
       - 清单随 node_artifact 一并产出——门禁判定必须可见，不允许"心里检查"。
**不通过处理**：拒绝通过 → 按 Step 0 的查询模板带当前年份限定词补充搜索一轮；仍无时效合格数据 → 按降级路径 D4 处理。
**回灌检查（v0.4.3 新增，v0.4.4 强化）**：D4/[STALE_DATA] 标注不是终点。完成时效判定清单后，必须逐字扫描结论位——执行摘要、TOP 风险、关键数据、各节点 key_finding、overall_rating 依据——凡出现被 D4 标注的论断数值，**删除或改写**该处表述。扫描按**数值本身**逐字进行（如 "16.85%"），不是按论断主题——同一数值在任何表述中的复用都算命中（实测反例：TOP 1 已改写，但执行摘要核心判断里 "市占第一 16.85%" 漏网）。判而不行视同门禁未通过。
**典型违规**：用 2023 年一致预期 PE 充当当前可比估值；用历史破发潮统计充当当前首日破发概率；用旧现场检查撤回率充当当前审核环境。三者均以"真 URL + 旧数据"通过 G2/G3，只有本门禁能拦截。

## G9: 监控判定合规（Monitoring Verdict Compliance，v0.6.0 新增）

**规则**：monitoring-run 的每条信号判定必须满足：
       - **检索留痕**：每条应检信号有 ≥1 次真实检索记录（查询词/时间/来源 URL，写入 monitor-run 留痕文件）
       - **数值比较**：触发/未触发判定必须列出"阈值 vs 最新值"的显式比较式；无比较的判定视为不通过
       - **三态完备**：数据不足信号显式列出并注明原因；禁止用超过 G7 时效阈值的数据冒充当前状态
**不通过处理**：标注 `signal_verdict_incomplete`，补充后重新输出。

## G8: 产物合规（Template Compliance，v0.4.2 新增，v0.4.4 强化，v0.5.0 重构为三产物）

**规则**：
1. 终端节点（pricing）必须产出**一份最终报告 + 三个分拆件**（模板见 references/templates/）：
   - **`final-report.html`（主交付物，三产物合一的自包含 HTML）**：以 final-report.html 模板为底本组装，含导航 + 四个固定区块（①内核风险清单 ②发行定价备忘录 ③督导期监控表 ④预测与验证计划——v0.7.0 新增，S5 预测记录按验证时点分类）
   - `kernel-risk-checklist.md`（内核风险清单：顶格风险精选 + 应对动作 + 责任归属 + 时限）
   - `pricing-memo.md`（发行定价备忘录：可比估值 + 隐含假设反推 + 流通结构 + 破发风险面 + 情绪位置 + 情景赔率 + 时效清单）
   - `supervision-monitor.md`（督导期监控表：信号 × 阈值 × 责任人 × 检查周期 × 触发后动作）
2. 每个产物以官方模板为底本填充，保留 `GateKeeper-Template` 标记注释
3. **交付目录组织**：最终报告与三个分拆件在根目录；全部过程文件（analysis_plan、node-*-artifact/entries、html 分块）收入 `artifacts/` 子目录——用户目录只应看到 4 个可读文件
4. 内核风险清单 ≤15 条（critical/high 优先 + unpriced 优先 + 三角色共识优先），禁止全量罗列 60+ 条
5. monitoring-run 产物（监控告警清单）同样以 monitoring-report.md 模板为底本、保留 GateKeeper-Template 标记（v0.6.1 补充）
**不通过处理**：标注缺失产物或缺失标记，要求基于模板重新生成。
