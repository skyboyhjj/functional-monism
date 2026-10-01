#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_evidence_appendix.py

把两份算据脚本汇编成 notes/five_criteria_evidence_appendix.md
（供不收 .py 的平台入库）。
用法：在仓库根运行  python3 scripts/five_criteria/make_evidence_appendix.py
BASE 取本脚本的上两级目录（即仓库根）。
"""
import os
import re

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SCRIPTS = [
    ("scripts/five_criteria/verify_shaping_vs_five_criteria.py", "算据 A · 势整形：策略层 vs 动力学层"),
    ("scripts/five_criteria/verify_five_criteria_instances.py", "算据 B · 五实例刻度尺：阴阳五行 · 十二律 · 涡旋 · 八度圆"),
]
OUT = os.path.join(BASE, "notes", "five_criteria_evidence_appendix.md")

head = """# 附录 · 「五条形式判据」算据汇编

> **配套**：`five_criteria_mechanism_landed.md`（v1.4）
> **说明**：平台不收 `.py`，故把两份算据脚本汇编于此（与原文件**逐字节一致**）。
> **定位**：`notes/` 批注稿附录。

---

"""

body = []
checks = []
for rel, title in SCRIPTS:
    txt = open(os.path.join(BASE, rel), encoding="utf-8").read()
    checks.append((rel, len(txt.encode("utf-8")), len(txt.splitlines())))
    body.append(f"## {title}\n\n`{rel}`\n\n```python\n{txt}```\n\n")

doc = head + "".join(body)
doc += "\n---\n\n## 自校验（与源文件逐字节一致）\n\n| 源文件 | 字节 | 行数 |\n| :-- | --: | --: |\n"
for rel, nb, nl in checks:
    doc += f"| `{rel}` | {nb} | {nl} |\n"

open(OUT, "w", encoding="utf-8", newline="\n").write(doc)

blocks = re.findall(r"```python\n(.*?)```", doc, flags=re.S)
ok = all(blk == open(os.path.join(BASE, rel), encoding="utf-8").read()
         for rel, blk in zip([s[0] for s in SCRIPTS], blocks))
print("wrote:", OUT)
print("bytes:", len(doc.encode("utf-8")), " lines:", doc.count("\n"))
print("code blocks byte-identical to sources:", ok)
