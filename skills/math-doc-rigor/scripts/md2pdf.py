#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用 md -> PDF 流水线（批量）：
  md ──(抽取 LaTeX)──> MathJax(node) ──> 内嵌 SVG
     ──markdown2──> HTML ──weasyprint──> PDF
用法:
  python3 md2pdf.py [--outdir DIR] a.md b.md ...
公式约定: 块级 $$...$$ ; 行内 $`...`$ 或 $...$ ; 渲染失败自动回退纯文本。
"""
import sys, os, re, json, subprocess, tempfile

import markdown2
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
TEX2SVG = os.path.join(HERE, "tex2svg.js")
NODE_PATH = os.environ.get("MATHJAX_NODE_PATH") or os.path.join(HERE, "node_modules")

# 历史遗留的损坏行修复
FIXES = {
    "如 $`F`$` 的复杂度 / `$`\\gamma`$）": "如 F 的复杂度 / γ）",
}

CSS = """
@page { size: A4; margin: 1.9cm 1.7cm; }
body { font-family: 'Noto Serif CJK SC', serif; line-height: 1.8; font-size: 11pt; color:#111; }
h1 { font-size: 19pt; margin: 0 0 .35em; }
h2 { font-size: 14pt; margin: 1.25em 0 .5em; border-bottom: 1.5px solid #ddd; padding-bottom:.2em; }
h3 { font-size: 12.5pt; margin: 1em 0 .4em; }
h4 { font-size: 11.5pt; }
hr { border:none; border-top:1px solid #e0e0e0; margin:1em 0; }
table { border-collapse: collapse; width: 100%; margin: .6em 0; }
th, td { border: 1px solid #999; padding: 4px 7px; font-size: 10pt; vertical-align: top; }
th { background: #f2f2f2; }
blockquote { color:#555; border-left:3px solid #ccc; padding-left:10px; margin:.6em 0; }
code { background:#f4f4f4; padding:0 3px; font-family: monospace; }
pre { background:#f6f6f6; padding:6px 8px; font-size:9pt; overflow-wrap:anywhere; }
.disp { text-align:center; margin: 12px 0; }
svg { vertical-align: baseline; }
img { max-width: 82%; height: auto; display: block; margin: 10px auto; }
"""

MATH_BLOCK = re.compile(r"\$\$(.+?)\$\$", re.S)
MATH_BT = re.compile(r"\$`(.+?)`\$", re.S)
MATH_PLAIN = re.compile(r"(?<!\$)\$(?!\$)([^$]+?)(?<!\$)\$(?!\$)")


def extract(md):
    items = []

    def add(tex, display):
        items.append({"id": len(items), "tex": tex.strip(), "display": display})
        return f"@@MATH{len(items)-1}@@"

    md = MATH_BLOCK.sub(lambda m: add(m.group(1), True), md)
    md = MATH_BT.sub(lambda m: add(m.group(1), False), md)
    md = MATH_PLAIN.sub(lambda m: add(m.group(1), False), md)
    return md, items


def render_svgs(items):
    if not items:
        return {}
    with tempfile.TemporaryDirectory() as d:
        i = os.path.join(d, "in.json"); o = os.path.join(d, "out.json")
        json.dump({"items": items}, open(i, "w", encoding="utf-8"))
        env = dict(os.environ); env["NODE_PATH"] = NODE_PATH
        subprocess.run(["node", TEX2SVG, i, o], env=env, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return json.load(open(o, encoding="utf-8"))


def fix_svg(svg):
    # ex -> em (x0.5)，让 weasyprint 正确缩放
    return re.sub(r'(width|height)="([-\d.]+)ex"',
                  lambda m: f'{m.group(1)}="{float(m.group(2))*0.5:.4f}em"', svg)


def convert(src, dst):
    t = open(src, encoding="utf-8").read()
    for k, v in FIXES.items():
        t = t.replace(k, v)
    t, items = extract(t)
    svgs = render_svgs(items)
    html = markdown2.markdown(t, extras=["tables", "fenced-code-blocks", "strike"])

    n_ok = 0
    # 先处理独立成段的块公式
    def repl_disp(m):
        nonlocal n_ok
        idx = int(m.group(1)); s = svgs.get(str(idx), "")
        if not s:
            return f'<p class="disp">{items[idx]["tex"]}</p>'
        n_ok += 1
        return f'<div class="disp">{fix_svg(s)}</div>'

    html = re.sub(r"<p>@@MATH(\d+)@@</p>", repl_disp, html)

    def repl_any(m):
        nonlocal n_ok
        idx = int(m.group(1)); s = svgs.get(str(idx), "")
        if not s:
            return items[idx]["tex"]
        n_ok += 1
        return fix_svg(s)

    html = re.sub(r"@@MATH(\d+)@@", repl_any, html)

    full = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html}</body></html>"
    # base_url 让文档里的相对图片路径（如 figures/xxx.png）能被解析
    HTML(string=full, base_url=os.path.dirname(os.path.abspath(src)) + "/").write_pdf(dst)
    return len(items), n_ok


def main():
    args = sys.argv[1:]
    outdir = None
    if "--outdir" in args:
        k = args.index("--outdir"); outdir = args[k + 1]; del args[k:k + 2]
    files = args
    os.makedirs(outdir, exist_ok=True) if outdir else None
    ok = fail = 0
    for f in files:
        base = os.path.splitext(os.path.basename(f))[0] + ".pdf"
        dst = os.path.join(outdir, base) if outdir else os.path.splitext(f)[0] + ".pdf"
        try:
            n, nok = convert(f, dst)
            print(f"  [ok] {os.path.basename(f):<48} 公式 {nok}/{n}  -> {base}")
            ok += 1
        except Exception as e:
            print(f"  [FAIL] {os.path.basename(f)}: {e}")
            fail += 1
    print(f"\n完成: 成功 {ok}, 失败 {fail}")


if __name__ == "__main__":
    main()
