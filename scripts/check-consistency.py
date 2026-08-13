#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gatekeeper 发布前一致性自检。

历史 bug 驱动（每项检查对应一次真实事故）：
  C1 版本统一   —— v0.5.1/v0.5.2 两次版本漂移：AGENTS/README/模板页脚不同步
  C2 计数引用   —— v0.5.0 快照扩至八项但 S2/G1 仍写"六项"；N/G/D 数量与 README 宣称不符
  C3 单一事实源 —— AGENTS 曾漏列 non-negotiables.md 与 final-report.html
  C4 交叉引用   —— 全库 references/ 路径必须可解析
  C5 模板标记   —— 输出模板必须含 GateKeeper-Template（G8 验证依据）

用法：python scripts/check-consistency.py
退出码：0 = 通过；1 = 存在不一致
"""
import io, os, re, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
errors = []

def read(p):
    return io.open(p, encoding='utf-8').read()

def warn(msg):
    errors.append(msg)
    print('    [X]', msg)

def ok(msg):
    print('    [OK]', msg)

ZH = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
def num(s):
    return int(s) if s.isdigit() else ZH.get(s, -1)

# ---------- C1 版本统一 ----------
print('[C1] 版本统一')
agents = read('AGENTS.md')
m = re.search(r'\*\*版本\*\*：v(\d+\.\d+\.\d+)', agents)
ver = m.group(1) if m else None
if not ver:
    warn('AGENTS.md 未找到版本号')
else:
    carriers = {
        'README.md': r'\*\*当前版本：v(\d+\.\d+\.\d+)\*\*',
        'references/templates/final-report.html': r'GateKeeper v(\d+\.\d+\.\d+) · 三产物合一',
        'references/templates/risk-matrix-template.html': r'GateKeeper v(\d+\.\d+\.\d+) · 数据内联',
        'references/templates/risk-matrix-template.md': r'报告由 Gatekeeper v(\d+\.\d+\.\d+) 生成',
        'references/templates/kernel-risk-checklist.md': r'Gatekeeper v(\d+\.\d+\.\d+) · 内核风险清单',
        'references/templates/pricing-memo.md': r'Gatekeeper v(\d+\.\d+\.\d+) · 发行定价备忘录',
        'references/templates/supervision-monitor.md': r'Gatekeeper v(\d+\.\d+\.\d+) · 督导期监控表',
        'references/templates/monitoring-report.md': r'Gatekeeper v(\d+\.\d+\.\d+) · 督导期监控告警清单',
    }
    for p, pat in carriers.items():
        if not os.path.exists(p):
            warn('版本载体缺失: %s' % p)
        else:
            mm = re.search(pat, read(p), flags=re.IGNORECASE)
            if not mm:
                warn('版本页脚缺失或格式变化: %s' % p)
            elif mm.group(1) != ver:
                warn('版本不一致: %s -> v%s（期望 v%s）' % (p, mm.group(1), ver))
    if not errors:
        ok('全部载体一致 v%s' % ver)

# ---------- C2 计数引用 ----------
print('[C2] 计数引用一致')
ps = read('.claude/skills/pricing-scanner/SKILL.md').split('\n')
tbl_idx = next(i for i, l in enumerate(ps) if l.strip().startswith('|') and '必查项' in l)
rows = 0
for l in ps[tbl_idx + 2:]:
    mm = re.match(r'\|\s*(\d+)\s*\|', l.strip())
    if mm and int(mm.group(1)) == rows + 1:
        rows += 1
    elif l.strip().startswith('|'):
        continue
    else:
        break
if rows < 1:
    warn('Step 1.5 快照表解析失败（项数=%d）' % rows)
else:
    checks = [
        ('references/artifact-schemas.md', r'market_snapshot:.*?Step 1\.5\s*([\d一二三四五六七八九十]+)项必查', 'S2 注释'),
        ('references/guardrails/quality-gates.md', r'market_snapshot`\s*([\d一二三四五六七八九十]+)项齐全', 'G1 门禁'),
    ]
    for p, pat, label in checks:
        mm = re.search(pat, read(p), flags=re.S)
        if not mm:
            warn('%s 未找到快照项数引用' % p)
        elif num(mm.group(1)) != rows:
            warn('%s 引用"%s项" 与 Step 1.5 实际 %d 项不符（%s）' % (p, mm.group(1), rows, label))
    if not errors:
        ok('快照 %d 项，两处引用一致' % rows)

# N 条款数量
nn = read('references/guardrails/non-negotiables.md')
n_count = len(re.findall(r'^## N\d+', nn, flags=re.M))
a_lines = agents.split('\n')
a_start = next(i for i, l in enumerate(a_lines) if '## 非协商条款' in l)
a_end = next(i for i, l in enumerate(a_lines) if i > a_start and l.startswith('## '))
a_count = len([l for l in a_lines[a_start:a_end] if re.match(r'^\d+\. ', l)])
if n_count != a_count:
    warn('非协商条款数量不一致: non-negotiables=%d, AGENTS=%d' % (n_count, a_count))
else:
    ok('非协商条款 N1-N%d 一致' % n_count)

# 门禁数量
gq = read('references/guardrails/quality-gates.md')
g_nums = [int(x) for x in re.findall(r'^## G(\d+)(?:\.\d+)?', gq, flags=re.M)]
g_max = max(g_nums)
g_total = len(re.findall(r'^## G\d+', gq, flags=re.M))
for p in glob.glob('.claude/skills/*/SKILL.md'):
    for mm in re.finditer(r'当前为 G1-G(\d+)', read(p)):
        if int(mm.group(1)) != g_max:
            warn('%s 写"G1-G%d" 但门禁实际到 G%d' % (p, int(mm.group(1)), g_max))
rm = re.search(r'(\d+) 道质量门禁', read('README.md'))
if rm and int(rm.group(1)) != g_total:
    warn('README 宣称 %s 道门禁，实际 %d 道（G1-G%d 含 G1.5/1.6/1.7）' % (rm.group(1), g_total, g_max))
if not errors:
    ok('门禁 G1-G%d（共 %d 道），scanner 引用一致' % (g_max, g_total))

# 降级数量（D0 为状态转移元规则，不计入降级路径）
dp = read('references/guardrails/degradation-paths.md')
d_count = len(re.findall(r'^## D[1-9]\d*', dp, flags=re.M))
rd = re.search(r'(\d+) 条降级策略', read('README.md'))
if rd and int(rd.group(1)) != d_count:
    warn('README 宣称 %s 条降级，实际 %d 条' % (rd.group(1), d_count))
if not errors:
    ok('降级策略 D1-D%d（共 %d 条）一致' % (d_count, d_count))

# ---------- C3 单一事实源完整 ----------
print('[C3] AGENTS 单一事实源完整')
listed = set(re.findall(r'`(references/[^`]+)`', agents))
actual = set()
for root, dirs, files in os.walk('references'):
    for fn in files:
        actual.add('/'.join(root.split(os.sep)) + '/' + fn)
for p in sorted(listed):
    if '*' in p:
        if not glob.glob(p):
            warn('AGENTS 列出的通配路径无匹配: %s' % p)
    elif not os.path.exists(p):
        warn('AGENTS 列出但不存在的文件: %s' % p)
for p in sorted(actual):
    if p not in listed and not any(p.startswith(l.split('*')[0]) for l in listed if '*' in l):
        warn('references/ 存在但未列入 AGENTS 单一事实源: %s' % p)
if not errors:
    ok('%d 个 references 文件全部在列' % len(actual))

# ---------- C4 交叉引用有效 ----------
print('[C4] 全库 references/ 引用可解析')
ref_pat = re.compile(r'references/[A-Za-z0-9_\-/]+\.(?:md|html)')
seen = set()
for p in (glob.glob('.claude/skills/*/SKILL.md') + glob.glob('references/**/*.md', recursive=True)
          + glob.glob('references/**/*.html', recursive=True) + ['AGENTS.md', 'README.md', 'docs/smoke-test-log.md']):
    if not os.path.exists(p):
        continue
    for m in ref_pat.findall(read(p)):
        seen.add(m)
missing = sorted(r for r in seen if not os.path.exists(r))
if missing:
    for r in missing:
        warn('失效引用: %s' % r)
else:
    ok('%d 个引用路径全部可解析' % len(seen))

# ---------- C5 模板标记 ----------
print('[C5] 输出模板标记在位')
tpls = [f for f in sorted(os.listdir('references/templates')) if f != 'html-assembly.md']
for f in tpls:
    if 'GateKeeper-Template' not in read('references/templates/' + f):
        warn('模板缺失标记: references/templates/%s' % f)
if not errors:
    ok('%d 个模板全部含 GateKeeper-Template' % len(tpls))

# ---------- 汇总 ----------
print()
if errors:
    print('自检失败：%d 处不一致' % len(errors))
    sys.exit(1)
else:
    print('自检通过：C1-C5 全部一致')
    sys.exit(0)
