# 冒烟测试记录 — 场景 3:快速扫描(quick-scan)

- **日期**:2026-08-07(T0)
- **测试人**:Claude(扮演 ipo-router + industry-scanner + tech-scanner)
- **模拟用户输入**:"有个项目想做科创板,帮我看一下行业和技术靠不靠谱——公司叫宇树科技,做四足和人形机器人的。"
- **执行范围**:ipo-router → industry + tech 两节点(并行,串行模拟);finance / pricing 禁止触发

---

## 1. ipo-router 阶段

### §0 项目状态预检(仅从输入提取,未提问)

| 信息项 | 提取结果 |
|--------|---------|
| 项目阶段 | 早期洽谈("有个项目想做科创板") |
| 已有材料 | 无 |
| 关注重点 | 行业 + 技术("行业和技术靠不靠谱") |
| 上次推演 | 无 |

### §1 路径匹配

- 用户请求为"快速可行性判断"(立项前筛选),关注节点恰好为 industry + tech → 匹配 **quick-scan / QUICK-SCAN**,depth=quick。
- 推理备注:输入未命中 §1 字面触发词("快速看看/初步判断/立项"),靠语义推理匹配;targeted-update(single-node)与本场景(两节点)不匹配,quick-scan 是唯一节点集合为 [industry, tech] 的路径。

### §2 确认与计划单产出(模拟用户确认)

```yaml
analysis_plan:
  plan_id: "PLAN-20260807-001"
  project_name: "宇树科技"
  mode: "quick-scan"
  path_id: "QUICK-SCAN"
  nodes: [industry, tech]
  depth: "quick"
  previous_run_id: null
  previous_artifacts: {}
  existing_materials: []
  generated_at: "2026-08-07T10:00:00+08:00"
```

---

## 2. 并行执行说明(检查点 3 依据)

- 按 analysis-registry.md §并行执行协调:Router 向两节点传入**相同** analysis_plan;tech-scanner 在 quick-scan 下**无上游依赖**,未读取 industry 制品;两节点各自独立搜索、独立分析。
- 本测试为单线程串行模拟(先 industry 后 tech),执行中验证:tech 节点全程未引用 industry 的任何结论,并行协调规则(启动/独立性/汇聚/部分失败/深度)五条均明确、可直接指导真实并行。
- 搜索轮次记账:industry 节点 3 轮(每角色 1 轮),tech 节点 3 轮(每角色 1 轮),合计 6 轮,符合 quick 深度"每角色 1-2 轮"。

---

## 3. 节点 1:industry-scanner

### Step 0 时间锚定

- T0 = 2026-08-07,写入所有 generated_at。
- 查询全部带时间限定词:"宇树科技 融资 估值 IPO 上市辅导 2026" / "人形机器人 四足机器人 行业市场规模 出货量 2026 最新" / "宇树科技 争议 质疑 价格 2026 最新新闻"。

### Step 1 角色加载

已读取 pre-ipo-investor.md / buy-side.md / media.md。

### Step 2 三角色风险条目(quick:每角色 ≥1)

```yaml
- id: "RISK-industry-pre-ipo-investor-001"
  node: "industry"
  role: "pre-ipo-investor"
  risk_level: "high"
  claim: "IPO 发行估值约 420 亿元较 2025 年 6 月 C 轮 120 亿元一年翻 3.5 倍,而 2026Q1 营收增速放缓至 +10.5%、扣非净利同比 -52.6%,Pre-IPO 轮次安全垫被快速透支,解禁退出面临压价风险。"
  evidence:
    primary_source:
      url: "https://www.jjckb.cn/20260604/656852a6036e46788efdb2e9696fc9b0/c.html"
      access_type: "public"
      captured_at: "2026-08-07T10:05:00+08:00"
      data_as_of: "2026-06"
    inline_summary: "经参报道:宇树 IPO 发行估值约 420 亿元,拟募资 42.02 亿元;此前 C 轮(2025-06)估值约 120 亿元;2026Q1 营收 4.21 亿元(+10.5%),扣非净利 0.40 亿元(-52.6%)。"
    key_data_points:
      - metric: "IPO 发行估值 vs C 轮估值"
        value: "420 亿 vs 120 亿(12 个月 3.5 倍)"
      - metric: "2026Q1 营收增速 / 扣非净利增速"
        value: "+10.5% / -52.6%"
  rationale: "Pre-IPO 视角只关心退出:估值倍数一年内急剧抬升而基本面增速换挡,意味着 C/C+ 轮投资人相对发行价的账面浮盈依赖上市后情绪维持,解禁时若增速未修复,退出回报被压缩。发生概率:中。"
  potential_impact: "解禁窗口遇增速持续放缓 → 股价低于发行价,C 轮 120 亿估值仍有安全垫但回报倍数大幅低于预期,退出周期拉长。"
  suggested_response: "保荐机构应在发行定价论证中准备增速换挡的解释口径,并向 Pre-IPO 股东提示锁定期内的业绩跟踪节点。"
  signal_watchlist:
    risk_statement: "估值透支叠加增速换挡的退出风险"
    time_window: {category: "market", duration: "2-4Q", abs: "2026Q4-2027Q2"}
    priority_tier: "T2"
    positive_signals:
      - {signal: "季度营收增速重回 30% 以上", threshold: "连续 2 季度 >30%", data_source: "定期报告", implication: "增长故事修复,估值支撑增强"}
      - {signal: "人形机器人工业场景订单落地", threshold: "工业类收入占比 >20%", data_source: "招股书更新/年报分部披露", implication: "需求结构从展示型转向生产型"}
    negative_signals:
      - {signal: "营收增速连续放缓", threshold: "连续 2 季度 <15%", data_source: "定期报告", implication: "增速换挡固化为趋势,发行估值失去支撑"}
      - {signal: "上市后破发", threshold: "连续 20 交易日低于发行价", data_source: "行情数据", implication: "解禁退出直接受损"}
    what_must_go_right:
      - {action: "在解禁前兑现工业/商用场景的规模化订单", success_indicator: "工业场景收入占比逐季上升"}

- id: "RISK-industry-buy-side-001"
  node: "industry"
  role: "buy-side"
  risk_level: "medium"
  claim: "人形机器人需求以文娱商演(36.8%)和科研教育(24.6%)为主,工业制造仅 9.2%,叠加单机价格三年降幅超 70%,行业呈'量增价减'的通缩结构,3-5 年持有逻辑尚未被生产性需求验证。"
  evidence:
    primary_source:
      url: "https://www.askci.com/news/chanye/20260629/090933278269537366861022.shtml"
      access_type: "public"
      captured_at: "2026-08-07T10:06:00+08:00"
      data_as_of: "2026-06"
    inline_summary: "中商产业研究院/IDC(2026-06):2025 年中国人形机器人出货 1.44 万台(全球 84.7%),2026 年预测 3.8 万台;应用结构文娱商演 36.8%、科研教育 24.6%、工业制造 9.2%;单机均价 2023 年 59 万 → 2025 年 16 万。"
    key_data_points:
      - metric: "2025 应用结构(工业制造占比)"
        value: "9.2%"
      - metric: "单机均价降幅(2023→2025)"
        value: "59 万→16 万(-70%+)"
  rationale: "买方关心 3-5 年持有价值:展示型需求天花板低且复购弱,价格通缩意味着'出货第一'不等于'收入/利润第一';风险为结构性而非一次性。"
  potential_impact: "若工业场景 2-3 年内不放量,收入增速将持续落后于出货增速,上市后估值倍数系统性下修,复制部分'智能硬件第一股'的估值回归路径。"
  suggested_response: "在募投与成长性论证中区分'出货量增长'与'生产性场景收入增长'两条曲线,避免以出货量单一叙事支撑估值。"

- id: "RISK-industry-media-001"
  node: "industry"
  role: "media"
  risk_level: "high"
  claim: "'73 天过会 + 420 亿估值 + 人形机器人第一股'的标签组合已引发广泛争议,叠加'跳舞拳击被质疑没用''半马翻车'等舆论事件,发行人的行业叙事极易被媒体解构为'表演型机器人泡沫'。"
  evidence:
    primary_source:
      url: "https://finance.ifeng.com/c/8tkHUUW1TVQ"
      access_type: "public"
      captured_at: "2026-08-07T10:07:00+08:00"
      data_as_of: "2026-07"
    inline_summary: "凤凰财经(2026-07)《宇树科技73天过会估值420亿,为何引发广泛争议?》;此前已有'机器人跳舞拳击被质疑没用,王兴兴回应''半马翻车'等传播事件(2025-2026)。"
    key_data_points:
      - metric: "过会速度引发的争议报道"
        value: "73 天过会 + 420 亿估值成为财经媒体议题"
  rationale: "媒体视角找'不想让人知道的事':估值争议 + 实用性质疑是最容易被放大的两个叙事缺口;媒体标题模拟:《420 亿的宇树,除了后空翻还会什么?》"
  potential_impact: "传播路径:财经媒体估值质疑 → 社交媒体报道'表演机器人'梗化 → 做空/自媒体深挖增速换挡,发行窗口舆情承压,上市后股价波动放大。"
  suggested_response: "保荐机构应预判发行期舆情议题清单,准备工业场景订单、科研客户复购等可验证事实材料。"
  signal_watchlist:
    risk_statement: "估值与实用性双重舆论质疑"
    time_window: {category: "market", duration: "2-4Q", abs: "2026Q4-2027Q2"}
    priority_tier: "T3"
    positive_signals:
      - {signal: "主流财经媒体出现正向深度报道", threshold: "发行后季度内 ≥2 篇聚焦工业落地", data_source: "财经媒体监测", implication: "叙事重心从估值转向基本面"}
      - {signal: "标志性工业客户公开背书", threshold: "≥1 家头部制造企业公开采购", data_source: "公司公告/客户新闻稿", implication: "'表演型'标签被事实稀释"}
    negative_signals:
      - {signal: "做空报告或质疑性深度报道", threshold: "≥1 篇引发交易所关注函", data_source: "媒体/交易所披露", implication: "舆论风险升级为监管关注"}
      - {signal: "负面舆情事件二次发酵", threshold: "类似'半马翻车'事件再现并登热搜", data_source: "社交媒体监测", implication: "实用性质疑固化"}
    what_must_go_right:
      - {action: "用可验证的工业/商用交付案例替换表演型传播素材", success_indicator: "媒体报道关键词中'工业/量产'占比上升"}
```

### Step 3 汇聚与冲突标注

- 共识风险:三角色均指向"增长质量与估值的匹配问题"(pre-ipo 从退出、买方从持有、媒体从叙事)。
- 冲突 1 条:
  - topic: "行业需求真实性的严重度"
  - pre_ipo_view: "高——直接影响解禁退出定价"(依据:420 亿估值 vs 增速换挡)
  - buy_side_view: "中——结构性问题但有 3-5 年修复窗口"(依据:工业场景占比 9.2%、预测出货高增)
  - media_view: "高——叙事层面最易被攻击"(依据:已有争议报道与质疑事件)
  - conflict_type: "weighting"
- G1.7 异议加权检查:无角色等级 ≥ 其他角色 +2 档 → 不触发。

### Step 3.5 传染检测

- C2(industry→pricing):"行业增速换挡质疑 → 可比估值下调"信号存在;pricing 不在本次链路,仅记录。
- C7(external→all):特斯拉 Optimus 2026 年产能目标 5-10 万台、国内智元(2025 出货 5168 台)等竞争加剧 → 存在早期外部冲击信号,标注 `contagion_alert`。
- 叠加检查:仅 1 条通道(C7)偏负向,未达 ≥2 条 → 不启动 §6 放大。

### Step 4 质量门禁(逐项)

| 门禁 | 结果 | 说明 |
|------|------|------|
| G1 角色完备 | 通过 | quick 深度 3/3 角色各 1 条 |
| G1.5 信号完备 | 通过 | 2 条 high(pre-ipo-001、media-001)均附 signal_watchlist(2+2+1) |
| G1.6 交叉信号一致 | 通过(N/A) | 无跨层级反向信号 |
| G1.7 异议加权 | 通过(N/A) | 无 ≥2 档分歧 |
| G2 来源多样 | 通过 | 每角色 1 条,URL 互不相同 |
| G3 证据内联 | 通过 | 3 条 inline_summary 均非空 |
| G4 枚举合规 | 通过 | node/role/risk_level/id 格式全部合规 |
| G5 角色锚定 | 通过 | rationale 分别锚定退出/持有/舆论立场,无视角切换 |
| G6 自包含 | 通过 | 无本地路径、无裸 URL(均配 inline_summary) |
| G7 时效合规 | 通过,未触发 | 市场环境类 data_as_of 2026-06/2026-07,距 T0 ≤2 个月(≤6 个月阈值) |

### Step 5 降级

无触发(搜索质量 adequate)。

### 节点制品

```yaml
node_artifact:
  node: "industry"
  generated_at: "2026-08-07T10:30:00+08:00"
  plan_id: "PLAN-20260807-001"
  summary:
    overall_rating: "cautious"
    key_finding: "赛道地位(四足全球 60-70% 份额、人形出货全球第一)真实且稀缺,但 420 亿发行估值建立在增速换挡与展示型需求结构之上,行业定位经得起'有没有'的质疑、经不起'值不值'的质疑。"
  role_consensus:
    agreed_risks: ["增长质量与估值匹配问题(增速换挡+需求结构偏展示型)"]
    conflicts:
      - topic: "行业需求真实性的严重度"
        pre_ipo_view: "高——影响解禁退出定价"
        pre_ipo_basis: "420 亿发行估值 vs 2026Q1 增速 +10.5%"
        buy_side_view: "中——结构性但存在修复窗口"
        buy_side_basis: "工业场景占比仅 9.2%,但 2026 出货预测高增"
        media_view: "高——叙事层面最易被攻击"
        media_basis: "73 天过会估值争议报道 + 实用性质疑事件"
        conflict_type: "weighting"
  contagion_alert: ["C7 早期信号:特斯拉 Optimus 2026 量产目标 5-10 万台,国内智元等对手密集融资(2026 年前三月赛道融资超 200 亿元)"]
  data_freshness:
    search_quality: "adequate"
    key_data_gaps: ["发行后实际募资/中签率数据尚未产生", "2026Q2 财务数据未披露"]
```

---

## 4. 节点 2:tech-scanner(与 industry 并行,未读取 industry 制品)

### Step 0 时间锚定

- T0 = 2026-08-07;查询带时间限定词:"宇树科技 全栈自研 专利数量 研发投入 2026 招股书" / "宇树科技 人形机器人 技术路线 特斯拉Optimus 对比 2026" / "宇树科技 技术质疑 开源 核心技术人员 2026 最新"(第 3 轮未返回摘要,媒体角色复用本节点第 1 轮共享底层数据,符合 Step 2"共享搜索到的底层数据")。

### Step 1 角色加载

已读取三角色文件;quick-scan 模式无上游制品依赖(符合前置条件)。

### Step 2 三角色风险条目(quick:每角色 ≥1)

```yaml
- id: "RISK-tech-pre-ipo-investor-001"
  node: "tech"
  role: "pre-ipo-investor"
  risk_level: "medium"
  claim: "截至 2026-01 境内发明专利仅 20 项(占境内专利 11.83%),其中 11 项为 2025 年 3 月后突击申请,专利护城河单薄,上市后若遭专利诉讼或被快速模仿,将直接侵蚀退出估值。"
  evidence:
    primary_source:
      url: "https://finance.sina.cn/stock/ssgs/2026-03-27/detail-inhsmnzp9517235.d.html?vt=4"
      access_type: "public"
      captured_at: "2026-08-07T10:35:00+08:00"
      data_as_of: "2026-01"
    inline_summary: "新浪证券据招股书(披露截止 2026-01-31):境内外专利合计 262 项,境内发明专利仅 20 项(11.83%),其中 11 项为 2025 年 3 月后申请;优必选授权专利 2790 项、越疆 709 项;招股书自述'因技术保密专利申请较少,可能难以有效防范侵权'。"
    key_data_points:
      - metric: "境内发明专利数 vs 同行"
        value: "20 项 vs 优必选 2790 项(总)、越疆 709 项"
  rationale: "Pre-IPO 视角:专利单薄本身不阻塞上市(已过会),但锁定期内一旦爆发专利战(参照敏芯股份 IPO 期遭歌尔诉讼的历史案例,as_of 2019-2023),退出时点与价格都会被拖入诉讼周期。发生概率:中。"
  potential_impact: "核心专利诉讼 → 解禁期不确定性上升 → 退出窗口被迫后移或折价退出。"
  suggested_response: "保荐机构应核查 FTO 分析与核心人员竞业安排,并将诉讼风险纳入锁定期内跟踪事项。"

- id: "RISK-tech-buy-side-001"
  node: "tech"
  role: "buy-side"
  risk_level: "high"
  claim: "公司技术路线为'小脑优先、成本领先',通用具身大模型('大脑')尚未规模化应用于产品,研发费用率约 7.73% 远低于优必选 35.1%、越疆 26.7%;若行业竞争焦点从运动控制转向具身智能,'硬件先行'壁垒的 3-5 年可持续性存疑。"
  evidence:
    primary_source:
      url: "https://xueqiu.com/1290568231/389223677"
      access_type: "public"
      captured_at: "2026-08-07T10:36:00+08:00"
      data_as_of: "2026-06"
    inline_summary: "2026Q2 对比研报:宇树走'运动控制优先'路线(自研电机扭矩密度 45Nm/kg、执行器成本为 Optimus 约 1/3),但招股书确认具身大模型未规模化应用;2025 年前三季度研发费用率 7.73%(优必选 35.1%);拟募资 42.02 亿中约 48%(20.22 亿)投向智能机器人模型研发,补强'大脑'。"
    key_data_points:
      - metric: "研发费用率对比"
        value: "7.73% vs 优必选 35.1%、越疆 26.7%"
      - metric: "募投中模型研发占比"
        value: "20.22 亿 / 42.02 亿(约 48%)"
  rationale: "买方视角:技术路线的可持续性决定 3-5 年持有价值——运动控制壁垒是'现在时',具身大模型是'将来时';公司自己用 48% 募资补'大脑'等于官方承认短板。风险为结构性。"
  potential_impact: "若 2027-2028 年行业范式转向'大脑定义机器人',宇树可能从'技术领先者'被重估为'硬件代工厂',估值倍数从科技股向制造业回归(可比参照:特斯拉 Optimus 端到端 AI 路线 vs 宇树多传感器+运控路线)。"
  suggested_response: "持续跟踪募投项目里程碑(具身大模型上车时点、泛化能力评测),将其作为持有决策的核心跟踪变量。"
  signal_watchlist:
    risk_statement: "技术路线偏向'小脑','大脑'缺位的可持续性风险"
    time_window: {category: "tech", duration: "4-8Q", abs: "2027Q3-2028Q3"}
    priority_tier: "T1"
    positive_signals:
      - {signal: "自研具身大模型规模化上车", threshold: "≥1 款量产机型搭载并公开演示泛化任务", data_source: "新品发布/招股更新", implication: "技术路线短板补齐,壁垒从运控扩展到智能"}
      - {signal: "研发费用率显著提升且投向模型", threshold: "年研发费用率 >12% 且模型投入占比 ≥30%", data_source: "定期报告", implication: "资源投放与'补大脑'叙事一致"}
    negative_signals:
      - {signal: "竞争对手端到端方案量产落地", threshold: "Optimus/Figure 等泛化任务能力公开评测显著领先", data_source: "第三方评测/拆解报告", implication: "行业范式转向'大脑',运控壁垒贬值"}
      - {signal: "募投模型项目延期", threshold: "里程碑延期 ≥2 个季度", data_source: "募集资金使用公告", implication: "'补大脑'执行力存疑"}
    what_must_go_right:
      - {action: "按期交付具身大模型并证明任务泛化能力", success_indicator: "第三方泛化任务评测进入第一梯队"}
    execution_proxy:
      commitment_history: "历史出货承诺兑现良好(2025 出货 5500 台全球第一)"
      launch_track_record: "G1/H1/R1 多代产品按时发布,2026 春晚亮相"
      pre_ipo_milestones: "辅导→过会→注册 73 天完成,执行力强"

- id: "RISK-tech-media-001"
  node: "tech"
  role: "media"
  risk_level: "medium"
  claim: "招股书 22 次提及'全栈自研',但研发费用仅为优必选 1/9、境内发明专利仅 20 项,'叙事强度 vs 投入强度'的落差已被新浪证券等媒体点破,存在二次发酵空间。"
  evidence:
    primary_source:
      url: "https://www.163.com/dy/article/KP1VKEE405568W0A.html"
      access_type: "public"
      captured_at: "2026-08-07T10:37:00+08:00"
      data_as_of: "2026-03"
    inline_summary: "《招股书22次提及"全栈"自研 研发费用仅为优必选的九分之一》(2026-03)直接对比叙事与投入;类似拆解报道还有中邮证券 G1 拆解(2026-03)显示减速器齿轮等来自外部供应商。"
    key_data_points:
      - metric: "'全栈'提及次数 vs 研发投入对比"
        value: "22 次 vs 研发费用为优必选 1/9"
  rationale: "媒体视角:'全栈自研'是发行人最想让人知道的标签,而'研发费用 1/9、专利 20 项、减速器齿轮外采'是最不想让人知道的对比——标题模拟:《宇树的"全栈自研",全在哪里?》"
  potential_impact: "传播路径:拆解报告 → 财经媒体引用 → 自媒体二次创作'伪全栈'话题,叠加估值争议形成组合质疑。"
  suggested_response: "保荐机构应统一'全栈自研'口径边界(自研环节清单 vs 外采环节清单),避免绝对化表述被逐一证伪。"
```

### Step 3 汇聚与冲突标注

- 共识风险:pre-ipo 与 media 均指向"专利/研发投入单薄",buy-side 指向"技术路线可持续性"——合并为同一主题"技术壁垒的深度存疑"。
- 冲突:无显著冲突(media 认为叙事落差是"medium 舆情事件",buy-side 认为路线问题是"high 结构问题",属 weighting 差异但针对的条目不同,不构成同题冲突)。
- G1.7 检查:同题无 ≥2 档分歧 → 不触发。

### Step 3.5 传染检测

- C4(tech→industry):"大脑缺位 → 竞争力丧失"为远期通道(4-8Q),当前仅有路线隐忧,无触发信号 → 观察不标注。
- C3(tech→finance):无在诉专利案件 → 不触发。
- 叠加检查:0 条通道同时负向 → 不启动放大。

### Step 4 质量门禁(逐项)

| 门禁 | 结果 | 说明 |
|------|------|------|
| G1 角色完备 | 通过 | quick 深度 3/3 角色各 1 条 |
| G1.5 信号完备 | 通过 | 1 条 high(buy-side-001)附 signal_watchlist(2+2+1,含 execution_proxy) |
| G1.6 交叉信号一致 | 通过(N/A) | 无跨层级反向信号 |
| G1.7 异议加权 | 通过(N/A) | 无 ≥2 档分歧 |
| G2 来源多样 | 通过 | 3 条 URL 互不相同,且与 industry 节点 URL 也不重复 |
| G3 证据内联 | 通过 | 3 条 inline_summary 均非空 |
| G4 枚举合规 | 通过 | node 固定 "tech",其余枚举/ID 格式合规 |
| G5 角色锚定 | 通过 | 退出/持有/舆论三立场各自锚定,无漂移 |
| G6 自包含 | 通过 | 无本地路径、无裸 URL |
| G7 时效合规 | 通过,未触发 | 经营类 data_as_of 2026-01/2026-03(≤18 个月);市场环境类 2026-06(≤6 个月) |

### Step 5 降级

无触发。媒体角色第 3 轮搜索未返回摘要,按"共享底层数据"规则以本节点已有公开报道支撑,未达 D2 标准(条目证据完整)。

### 节点制品

```yaml
node_artifact:
  node: "tech"
  generated_at: "2026-08-07T10:50:00+08:00"
  plan_id: "PLAN-20260807-001"
  summary:
    overall_rating: "cautious"
    key_finding: "运动控制与成本工程能力真实且全球领先(电机/执行器自研、BOM 成本约为 Optimus 1/3),但'全栈自研'叙事与研发投入(费率 7.73%、发明专利 20 项)存在落差,具身大模型缺位是 3-5 年最大的技术可持续性变量。"
  role_consensus:
    agreed_risks: ["技术壁垒深度存疑(专利薄 + 研发投入低 + 大脑缺位)"]
    conflicts: []
  data_freshness:
    search_quality: "adequate"
    key_data_gaps: ["募投模型项目具体里程碑时间表未公开", "境外 93 项专利的国别/类型分布未获取"]
```

---

## 5. 汇聚输出(quick-scan 合并规则)

- 合并 industry(3 条)+ tech(3 条)共 6 条风险条目;按协调规则**不做节点间冲突标注**。
- artifact_freshness:industry generated_at 2026-08-07T10:30 / tech 2026-08-07T10:50,同日同时记录。
- finance / pricing 节点:未触发,analysis_plan.nodes 仅含 [industry, tech],无非计划节点调用(检查点 4)。

```yaml
artifact_freshness:
  industry: {generated_at: "2026-08-07T10:30:00+08:00", status: "fresh", age_days: 0}
  tech:     {generated_at: "2026-08-07T10:50:00+08:00", status: "fresh", age_days: 0}
  finance:  {generated_at: null, status: "not_run", age_days: null}
  pricing:  {generated_at: null, status: "not_run", age_days: null}
```

---

## 6. 检查点结果汇总

| # | 检查点 | 结果 | 证据 |
|---|--------|------|------|
| 1 | Router 匹配 quick-scan 路径(path_id=QUICK-SCAN) | ✅ | 计划单 path_id=QUICK-SCAN,nodes=[industry, tech],mode=quick-scan |
| 2 | depth 标记 quick,每角色 ≥1 条目 | ✅ | depth=quick;industry 3 条 + tech 3 条,每角色恰好 1 条,G1 通过 |
| 3 | industry + tech 并行执行(非串行等待) | ✅(串行模拟) | tech 全程未读取 industry 制品;并行协调 5 条规则(启动/独立性/汇聚/部分失败/深度)明确可直接指导真实并行 |
| 4 | finance/pricing 未被触发 | ✅ | artifact_freshness 中两节点 not_run;无任何 finance/pricing 分析动作 |
| 5 | 搜索轮次受限(每角色 1-2 轮) | ✅ | industry 3 轮 + tech 3 轮,每角色 1 轮,合计 6 轮 |

## 7. v0.4.0 附加观察项

| 观察项 | 结果 | 说明 |
|--------|------|------|
| 每条证据 data_as_of 填写且格式正确 | ✅ | 6/6 条均已填,格式为 YYYY-MM(2026-01/03/06/07);旧数据均以所属期填写,未以 captured_at 冒充 |
| 无四要件的百分比概率 | ✅ 未出现 | 概率判断一律使用 高/中/低 三档;条目中的百分比(11.83%、7.73% 等)为证据数据而非概率判断 |
| G7 门禁触发记录 | 无触发(已逐项检查) | 全部 6 条均在时效阈值内(市场类 ≤6 个月、经营类 ≤18 个月),无需 D4 降级;G7 检查过程已在两节点 Step 4 留痕 |

## 8. 发现的技能文件问题清单

1. **ipo-router 内部表述矛盾(轻微)**:§2 要求"用户确认后产出分析计划单",而"输出"节要求"生成后立即移交,不等待用户确认";AGENTS.md 链式规则 2 又只说 full-chain/pricing-focused 不等待确认——quick-scan 模式下"确认"与"立即移交"的先后关系不清晰。
2. **quick-scan 触发词覆盖面不足**:§1 字面触发词("快速看看/初步判断/立项")未覆盖"帮我看一下 X 和 Y 靠不靠谱"这类常见表达;本场景靠语义推理匹配,存在漏配风险(可能落入 N3 默认 full-chain)。
3. **quick-scan 与 targeted-update 边界模糊**:当用户明确指定 industry+tech 两个节点时,quick-scan(nodes 固定两节点)与 targeted-update(nodes="user-specified",mode=single-node 但 schema 未限制 nodes 数量)存在匹配歧义,registry 未定义优先级。
4. **Step 5 降级清单遗漏 D4**:industry/tech SKILL 的 Step 0 与 G7 均引用 D4(时效降级),但 Step 5 只列 D1/D2/D3,D4 未列入降级步骤清单。
5. **risk_entry 扩展字段未回流 schema**:signal_watchlist / contagion_alert / execution_proxy 等字段在 signal-watchlist.md 和 SKILL 中使用,但 artifact-schemas.md §S2/S3 未声明这些扩展字段,与"schema 单一事实源、不得自创字段"(N9)存在张力。
6. **(非问题,验证通过)并行协调规则可执行性**:registry §并行执行协调五条规则在模拟中全部可对应到具体动作,未发现缺失环节;"不做节点间冲突标注"与各节点 Step 3 的节点内冲突标注无冲突。
