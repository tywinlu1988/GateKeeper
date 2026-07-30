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

## 并行执行协调（quick-scan 特有）

quick-scan 的 `mode: parallel` 表示 industry-scanner 和 tech-scanner **同时启动**而非串行等待。

### 协调规则

1. **启动**：Router 同时发起 industry-scanner 和 tech-scanner 调用，传入相同的 `analysis_plan`
2. **独立性**：两节点各自独立搜索、独立分析——quick-scan 模式下 tech-scanner 不等待 industry 制品（无上游依赖）
3. **汇聚**：两节点都完成后，合并输出：
   - industry 风险矩阵 + tech 风险矩阵 → 单一报告
   - 不做节点间冲突标注（quick-scan 无此要求）
   - artifact_freshness 同时记录两个节点的时间戳
4. **部分失败处理**：若一个节点失败（搜索不可用/数据不足），另一节点正常产出；失败节点按 D1/D2 降级策略标注，不阻塞成功节点
5. **深度调整**：两节点均使用 depth=quick，每角色 ≥ 1 条目即可
