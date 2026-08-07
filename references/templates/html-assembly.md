# HTML 报告组装协议（HTML Assembly Protocol）

> 设计来源：v0.4.2 弱模型实测中，HTML 报告生成成为最大执行瓶颈——Bash heredoc 引号冲突、
> python 运行时不可用（exit 49）、单次巨型 Write 截断，最终靠反复试错才摸索出可行路径。
> 本协议把该可行路径固化为标准做法，消除试错成本。

## 禁止事项

1. **禁止用 Bash heredoc / echo / printf 写 HTML 内容**——HTML 中的引号、反引号、`$` 与 shell 必然冲突
2. **禁止依赖 python/node 渲染脚本**——执行环境可能没有运行时或禁止执行（实测 `python3 -c "print('hello')"` 都被拒绝）
3. **禁止单次 Write 超过 ~400 行的 HTML**——弱模型长文件输出易截断，截断的 HTML 无法修复只能重写

## 标准做法：Write 分块 + cat 拼接

```
0. Read  references/templates/risk-matrix-template.html   # 必须以官方模板为底本（G8），禁止从零自行设计
1. Write  report_head.html   # 模板的 <!DOCTYPE>、<style>、报告头，填执行摘要、评级总览
2. Write  report_nodes.html  # 四个节点的风险条目表格（节点 1-2）
3. Write  report_nodes2.html # 节点 3-4（如需再分）
4. Write  report_tail.html   # 关键论断时效清单、制品新鲜度、页脚
5. Bash: cat report_head.html report_nodes.html report_nodes2.html report_tail.html > 最终报告.html
6. 验证：最终文件非空、以 </html> 结尾、保留模板标记注释 <!-- GateKeeper-Template: ... -->、包含 G8 要求的三个固定区块
```

## 规则

- 每个分块以完整标签边界切分（不在 `<table>` 中间断块）
- 拼接顺序必须与 G8 固定区块顺序一致
- 分块中间产物保留在输出目录，不删除——它们是审计证据
- 拼接后若验证失败（缺 `</html>`、缺固定区块），只重写对应分块再重新拼接，不重写整个文件
- Markdown 报告（默认输出）不适用本协议——MD 可直接单次 Write
