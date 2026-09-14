#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 axioms/ 与 notes/ 目录下 Markdown 文档的 GitHub 网页端显示格式问题。

已知 bug 与对应规则（详见 PROJECT_CONTEXT.md「公理/笔记显示格式自动检查」）：

  [ERROR] \\operatorname           GitHub 禁用该宏，须改用 \\mathrm
  [ERROR] $$...$$ 跨行              KaTeX 报 "Can't use function '$' in math mode"，须合并单行
  [ERROR] 行内公式 $...$ 含 LaTeX 命令但未反引号包裹   MathJax 解析失败，须写 $`...`$
  [ERROR] 加粗右闭合失效（右括号后紧跟汉字）  CommonMark 加粗不成立，须改 <strong>…</strong>
  [WARN ] \\boxed{ 后多余 \\;       建议删除冗余空距命令

用法：
  python scripts/check_display_format.py [文件或目录 ...]
  不带参数时默认检查 axioms/ 与 notes/ 目录（递归 *.md）。
  发现 ERROR 时退出码为 1（供 pre-commit 拦截）。
"""

import argparse
import re
import sys
from pathlib import Path

ERROR = "ERROR"
WARN = "WARN"

# \operatorname —— GitHub 限制宏
RE_OPERATORNAME = re.compile(r"\\operatorname")
# \boxed{\; —— 冗余空距命令
RE_BOXED_SEMI = re.compile(r"\\boxed\{\s*\\;")
# 加粗右闭合失效：`**...右括号...**` 的结尾 `**` 后紧跟汉字（右括号后跟汉字使右-flanking 失效）
RIGHT_BRACKETS = "）】」』》)]}"


def is_cjk(ch):
    cp = ord(ch)
    return (0x3400 <= cp <= 0x4DBF) or (0x4E00 <= cp <= 0x9FFF) or (0xF900 <= cp <= 0xFAFF)


def find_bold_rightflank(line):
    """返回「加粗结尾 ** 前是右括号且后紧跟汉字」的结尾 ** 列号（0-based）列表。"""
    out = []
    i = 0
    n = len(line)
    in_bold = False
    while i < n - 1:
        if line[i] == "*" and line[i + 1] == "*":
            if not in_bold:
                in_bold = True
            else:
                prev = line[i - 1] if i > 0 else ""
                nxt = line[i + 2] if i + 2 < n else ""
                if prev in RIGHT_BRACKETS and nxt and is_cjk(nxt):
                    out.append(i)
                in_bold = False
            i += 2
        else:
            i += 1
    return out


def find_unwrapped_inline(line):
    """返回 (起始列0, 公式内容) 列表：未反引号包裹且含 LaTeX 命令的行内公式。"""
    out = []
    n = len(line)
    i = 0
    while i < n:
        if line[i] != "$":
            i += 1
            continue
        nxt = line[i + 1] if i + 1 < n else ""
        if nxt == "$":            # 块级 $$，交给 find_issues 处理
            i += 2
            continue
        if nxt == "`":            # 已包裹 $`...`$，跳过到结尾
            j = line.find("`$", i + 1)
            i = (j + 2) if j != -1 else i + 1
            continue
        j = line.find("$", i + 1)  # 未包裹行内，找结尾 $
        if j == -1:
            i += 1
            continue
        content = line[i + 1:j]
        if "\\" in content:
            out.append((i, content.strip()))
        i = j + 1
    return out


def find_issues(path):
    lines = Path(path).read_text(encoding="utf-8", errors="replace").split("\n")
    issues = []
    in_code = False
    open_dollar_line = None  # 未闭合 $$ 的起始行号（1-based）

    for idx, raw in enumerate(lines):
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        lineno = idx + 1

        for m in RE_OPERATORNAME.finditer(line):
            issues.append((ERROR, lineno, m.start() + 1,
                           "禁用宏 \\operatorname（GitHub 报 macros not allowed），请改用 \\mathrm"))

        for m in RE_BOXED_SEMI.finditer(line):
            issues.append((WARN, lineno, m.start() + 1,
                           "\\boxed{ 后存在冗余空距命令 \\;，建议删除"))

        for col in find_bold_rightflank(line):
            issues.append((ERROR, lineno, col + 1,
                           "加粗「**」右闭合失效（右括号后紧跟汉字），请改用 <strong>…</strong>"))

        for col, content in find_unwrapped_inline(line):
            issues.append((ERROR, lineno, col + 1,
                           "行内公式含 LaTeX 命令但未反引号包裹，请写为 $`…`$：" + content))

        # 块级 $$ 跨行检测
        j = 0
        while True:
            k = line.find("$$", j)
            if k == -1:
                break
            if open_dollar_line is None:
                open_dollar_line = lineno
            else:
                if open_dollar_line != lineno:
                    issues.append((ERROR, open_dollar_line, 1,
                                   "块级公式 $$…$$ 跨行（KaTeX 报 Can't use function '$' in math mode），请合并为单行"))
                open_dollar_line = None
            j = k + 2

    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description="检查 axioms/notes 的 Markdown 显示格式")
    parser.add_argument("paths", nargs="*", help="文件或目录；缺省检查 axioms/ 与 notes/")
    args = parser.parse_args(argv)

    targets = args.paths or ["axioms", "notes"]
    files = []
    for t in targets:
        p = Path(t)
        if p.is_dir():
            files.extend(sorted(p.rglob("*.md")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"[skip] 目标不存在: {t}", file=sys.stderr)

    all_issues = []
    for f in files:
        for iss in find_issues(f):
            all_issues.append((str(f),) + iss)

    n_err = sum(1 for x in all_issues if x[1] == ERROR)
    n_warn = sum(1 for x in all_issues if x[1] == WARN)

    for path, kind, lineno, col, msg in all_issues:
        print(f"{path}:{lineno}:{col}: [{kind}] {msg}")

    print(f"\n共检查 {len(files)} 个文件：{n_err} 个 ERROR，{n_warn} 个 WARN")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())