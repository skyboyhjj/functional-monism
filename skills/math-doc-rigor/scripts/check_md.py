#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渲染安全体检：检查 Markdown 数学文档在 GitHub(MathJax) 与 PDF 导出下的常见隐患。
用法: python3 check_md.py 文档.md [更多.md ...]
退出码: 0 = 干净, 1 = 有隐患（便于批量时聚合）。
"""
import re, sys, os

CJK = re.compile(r"[\u4e00-\u9fff]")
RISKY = ["\\tag", "\\xrightarrow", "\\overset", "\\boxed", "\\underset"]
IMG = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def check(path):
    t = open(path, encoding="utf-8").read()
    issues = []

    # 1) 块公式含中文（MathJax 会渲染失败）
    blk = re.findall(r"\$\$(.*?)\$\$", t, re.S)
    n = sum(1 for b in blk if CJK.search(b))
    if n:
        issues.append(f"块公式含中文 {n} 处（必须清零）")

    # 2) 行内公式：裸 $...$ 每行至多 1 个；反引号写法 $`...`$ 不限；$ 须配对
    clean = re.sub(r"\$\$.*?\$\$", "", t, flags=re.S)
    multi = odd = 0
    for line in clean.split("\n"):
        bare = re.sub(r"\$`[^`]*`\$", "", line)  # 反引号写法边界清晰，先剥离
        c = bare.count("$")
        if c >= 4:
            multi += 1
        elif c % 2 == 1:
            odd += 1
    if multi:
        issues.append(f"{multi} 行含 >=2 个行内公式（每行至多 1 个）")
    if odd:
        issues.append(f"{odd} 行 $ 不配对")

    # 3) 风险宏
    for mac in RISKY:
        if mac in t:
            issues.append(f"风险宏 {mac}")

    # 4) 相对图片是否存在
    for m in IMG.finditer(t):
        p = m.group(1).strip()
        if p.startswith(("http://", "https://", "data:")):
            continue
        full = os.path.join(os.path.dirname(os.path.abspath(path)), p)
        if not os.path.exists(full):
            issues.append(f"图片缺失 {p}")

    return issues, len(blk), t.count("$`")


def main():
    files = sys.argv[1:]
    if not files:
        print("用法: python3 check_md.py 文档.md [...]"); sys.exit(2)
    total = 0
    for f in files:
        issues, nblk, nbt = check(f)
        name = os.path.basename(f)
        if issues:
            total += len(issues)
            print(f"[!] {name}  (块公式 {nblk}, 反引号行内 {nbt})")
            for it in issues:
                print(f"      - {it}")
        else:
            print(f"[ok] {name}  (块公式 {nblk}, 反引号行内 {nbt})")
    print(f"\n合计隐患: {total}")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
