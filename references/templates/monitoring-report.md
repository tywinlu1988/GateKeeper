# 督导期监控告警清单

<!-- GateKeeper-Template: monitoring-report.md —— 产物必须保留本标记（G8 验证依据） -->

**项目**：{project_name}（{code}） ｜ **计划单**：{plan_id}（前次 {previous_run_id}） ｜ **检查时点**：{check_date} ｜ **生成**：{generated_at}
**服务环节**：上市后持续督导 ｜ **执行体**：monitor-runner（monitoring-run 路径） ｜ **应检信号**：{n} 条（按检查周期过滤）

---

## 触发告警清单

| # | 监控信号 | 阈值 | 最新值 | 比较判定 | data_as_of | 来源 | 触发后动作 | 责任人 |
|---|---------|------|--------|---------|-----------|------|-----------|--------|
{triggered_rows}

---

## 未触发概览

| # | 监控信号 | 阈值 | 最新值 | data_as_of |
|---|---------|------|--------|-----------|
{ok_rows}

---

## 数据不足清单

| # | 监控信号 | 原因 | 补查建议 |
|---|---------|------|---------|
{insufficient_rows}

---

## 下次检查建议

> 按监控表关键时点日历，下一检查窗口：{next_window}，应检信号约 {next_n} 条（{next_focus}）。

---

*Gatekeeper v0.6.0 · 督导期监控告警清单 · 判定留痕见 monitor-run-{YYYYMMDD}.yaml · 每条判定均为"阈值 vs 最新值"显式比较（G9）*
