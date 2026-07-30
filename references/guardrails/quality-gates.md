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
