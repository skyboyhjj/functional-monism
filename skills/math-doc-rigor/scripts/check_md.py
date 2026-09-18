#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
渲染安全体检：检查 Markdown 数学文档在 GitHub(MathJax) 与 PDF 导出下的常见隐患。
用法: python3 check_md.py 文档.md [更多.md ...]
退出码: 0 = 干净, 1 = 有隐患（便于批量时聚合）。

检查项
  1. 块公式含中文 —— MathJax 对 CJK 退化成 <text>，PDF 端不可靠
  2. 行内公式：每行至多 1 个 / $ 须配对
  3. 风险宏 \\tag \\boxed \\overset \\underset \\xrightarrow
  4. 相对图片文件是否存在
  5. 缺字形字符 —— md2pdf.py 字体栈（Noto CJK / DejaVu）无 emoji 字体，
     ✅(U+2705) ❌(U+274C) 之类会**静默消失**；改用 ✓(U+2713) ✗(U+2717)
  6. 粗体断裂 —— ** 未按 CommonMark flanking 规则配对时会**字面输出星号**
     （典型：** 紧跟在全角标点前，如 `是**「定号型」记账**`）
"""
import re
import sys
import os
import glob
import unicodedata

CJK = re.compile(r"[\u4e00-\u9fff]")
RISKY = ["\\tag", "\\xrightarrow", "\\overset", "\\boxed", "\\underset"]
IMG = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

# --------------------------------------------------------------------------
# 5) 缺字形字符
# --------------------------------------------------------------------------
# 无 emoji 字体时可粗检的区间；U+2700-27BF 里 ✓(2713)/✗(2717) 有字形，故豁免
EMOJI_OK = {0x2713, 0x2717}          # ✓ ✗
NO_GLYPH_RANGES = [
    (0x1F000, 0x1FAFF),   # 各类 emoji / 象形符号
    (0x1F1E6, 0x1F1FF),   # 区域指示符（国旗）
    (0x2600, 0x26FF),     # 杂项符号（☀ ★ ⚠ …）
    (0x2700, 0x27BF),     # 装饰符号（✅ 2705 / ❌ 274C / ❓ …）
    (0x2B00, 0x2BFF),     # 杂项箭头与符号（⭐ ⬛ …）
    (0xFE0F, 0xFE0F),     # 变体选择符-16
    (0x200D, 0x200D),     # 零宽连接符（emoji 序列）
]

FONT_GLOBS = (
    "/usr/share/fonts/**/NotoSerifCJK*.ttc",
    "/usr/share/fonts/**/NotoSansCJK*.ttc",
    "/usr/share/fonts/**/Noto*CJK*.otf",
    "/usr/share/fonts/**/DejaVu*.ttf",
    "/usr/share/fonts/**/DejaVu*.ttc",
)


_CMAPS = []
_CMAPS_READY = False


def _load_cmaps():
    """加载字体 cmap 做精确字形覆盖检查；缺 fontTools/字体则返回 None。

    结果缓存到模块级：批量体检几十个文件时只解析一次字体（否则约 3 秒/文件）。
    """
    global _CMAPS, _CMAPS_READY
    if _CMAPS_READY:
        return _CMAPS or None
    _CMAPS_READY = True
    try:
        from fontTools.ttLib import TTFont, TTCollection
    except ImportError:
        return None
    paths = []
    for pat in FONT_GLOBS:
        paths.extend(glob.glob(pat, recursive=True))
    if not paths:
        return None
    cmaps = []
    for p in paths:
        try:
            if p.lower().endswith(".ttc"):
                for f in TTCollection(p).fonts:
                    cmaps.append(f.getBestCmap())
            else:
                cmaps.append(TTFont(p, fontNumber=0).getBestCmap())
        except Exception:
            continue
    _CMAPS = cmaps
    return _CMAPS or None


def _is_emoji(ch):
    o = ord(ch)
    if o in EMOJI_OK:
        return False
    return any(lo <= o <= hi for lo, hi in NO_GLYPH_RANGES)


def missing_glyphs(text, cmaps):
    """返回 [(char, count)]：在当前字体栈下没有字形的非 ASCII 字符。"""
    miss = []
    for ch in set(text):
        if ord(ch) < 0x80 or ch in "\n\r\t":
            continue
        if cmaps is not None:
            if not any(ord(ch) in m for m in cmaps):
                miss.append((ch, text.count(ch)))
        elif _is_emoji(ch):
            miss.append((ch, text.count(ch)))
    return sorted(miss, key=lambda kv: -kv[1])


# --------------------------------------------------------------------------
# 6) 粗体断裂（CommonMark flanking）
# --------------------------------------------------------------------------
ASCII_PUNCT = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")


def _is_punct(c):
    return c in ASCII_PUNCT or unicodedata.category(c).startswith("P")


def _is_space(c):
    return c.isspace()


def _mask_code(t):
    """把围栏/行内/缩进代码替换成等长的中性占位字符，避免把代码里的 ** 当成粗体。

    占位符必须满足两条：
      · 保留 \\n —— 否则行号漂移，报错会指向错误的行；
      · 用非空白、非标点字符（"x"）—— 因为 CommonMark 的 flanking 判定区分
        "空白"和"标点"，掩码成空格会把代码前后的定界符语义改掉，造出假报错。
    """
    def blank(m):
        return re.sub(r"[^\n]", "x", m.group(0))
    t = re.sub(r"```.*?```", blank, t, flags=re.S)
    t = re.sub(r"~~~.*?~~~", blank, t, flags=re.S)
    t = re.sub(r"`[^`\n]*`", blank, t)

    # 缩进代码块（4 空格/制表符起始）：仅当上一非空行是空行或同样是缩进行
    # —— 这样列表项的续行（前面是 "- xxx"）不会被误判成代码块
    lines = t.split("\n")
    prev_blank = True
    for k, ln in enumerate(lines):
        if ln[:1] in (" ", "\t") and ln.strip():
            indent = len(ln) - len(ln.lstrip(" \t"))
            if indent >= 4 and (prev_blank or lines[k - 1][:1] in (" ", "\t")):
                lines[k] = " " * indent + "x" * (len(ln) - indent)
                continue
        prev_blank = not ln.strip()
    return "\n".join(lines)


def find_broken_bold(text):
    """按 CommonMark flanking 规则模拟 ** 配对，返回 [(行号, 原因)]。"""
    m = _mask_code(text)
    out, stack = [], []
    for r in re.finditer(r"(?<!\*)\*{2}(?!\*)", m):
        i = r.start()
        before = m[i - 1] if i > 0 else "\n"
        after = m[i + 2] if i + 2 < len(m) else "\n"
        # 左定界：后面不是空白，且（后面非标点 或 前面是空白/标点）
        left = (not _is_space(after)) and (
            (not _is_punct(after)) or _is_space(before) or _is_punct(before)
        )
        # 右定界：前面不是空白，且（前面非标点 或 后面是空白/标点）
        right = (not _is_space(before)) and (
            (not _is_punct(before)) or _is_space(after) or _is_punct(after)
        )
        if right and stack:
            stack.pop()                      # 正常闭合
        elif right and not left:
            out.append((m[:i].count("\n") + 1, "孤立闭合 **"))   # 能闭合却无开符
        elif left:
            stack.append(i)                  # 开符入栈
        # 两侧皆不可开/闭 → 字面量（如 `2 ** 3`），忽略
    for i in stack:
        out.append((m[:i].count("\n") + 1, "开符未闭合 **"))
    return sorted(set(out))


# --------------------------------------------------------------------------


def check(path):
    raw = open(path, encoding="utf-8").read()
    # 扫描 1~4、6 走掩码文本（代码块/行内代码里的内容不算数）；
    # 扫描 5（缺字形）走原文——因为代码块在 PDF 里照样按文本渲染，照样会丢字形。
    t = _mask_code(raw)
    issues = []

    # 1) 块公式含中文（MathJax 会渲染失败）
    blk = re.findall(r"\$\$(.*?)\$\$", t, re.S)
    bad = [b.strip() for b in blk if CJK.search(b)]
    if bad:
        issues.append("块公式含中文 %d 处（必须清零）" % len(bad))
        for b in bad[:3]:
            issues.append("    ↳ %s" % b[:90])

    # 2) 行内公式：每行至多 1 个；须配对（反引号写法 $`...`$ 不参与计数）
    clean = re.sub(r"\$\$.*?\$\$", "", t, flags=re.S)
    clean = re.sub(r"\$`[^`]*`\$", "", clean)
    clean = re.sub(r"`[^`]*`", "", clean)
    multi = odd = 0
    for line in clean.split("\n"):
        c = line.count("$")
        if c >= 4:
            multi += 1
        elif c % 2 == 1:
            odd += 1
    if multi:
        issues.append("%d 行含 >=2 个行内公式（每行至多 1 个）" % multi)
    if odd:
        issues.append("%d 行 $ 不配对" % odd)

    # 3) 风险宏
    for mac in RISKY:
        if mac in t:
            issues.append("风险宏 %s" % mac)

    # 4) 相对图片是否存在
    for m in IMG.finditer(t):
        p = m.group(1).strip()
        if p.startswith(("http://", "https://", "data:")):
            continue
        full = os.path.join(os.path.dirname(os.path.abspath(path)), p)
        if not os.path.exists(full):
            issues.append("图片缺失 %s" % p)

    # 5) 缺字形字符（原文，不掩码）
    cmaps = _load_cmaps()
    miss = missing_glyphs(raw, cmaps)
    if miss:
        issues.append("缺字形字符 %d 种（PDF 里会静默消失）：" % len(miss))
        for ch, n in miss[:12]:
            try:
                nm = unicodedata.name(ch)
            except ValueError:
                nm = "?"
            issues.append("    ↳ %r U+%04X %s  x%d" % (ch, ord(ch), nm[:44], n))
        issues.append("    ↳ 修法：emoji 改 ✓/✗（有字形）或改纯文字")
    if cmaps is None:
        issues.append("!注: 未装 fontTools 或缺 CJK 字体，字形检查仅按 emoji 区间粗检"
                      "（精确覆盖请 pip install fonttools）")

    # 6) 粗体断裂
    broken = find_broken_bold(raw)
    if broken:
        lines = sorted({ln for ln, _ in broken})
        issues.append("粗体 ** 断裂 %d 处（PDF 里会字面显示星号）：" % len(lines))
        for ln in lines[:6]:
            line_text = raw.split("\n")[ln - 1].strip()
            issues.append("    ↳ L%d: %s" % (ln, line_text[:80]))
        issues.append("    ↳ 修法：把 ** 移到空格之后的词首（见 render-rules 规则 11）")

    return issues, len(blk), raw.count("$`")


def main():
    files = sys.argv[1:]
    if not files:
        print("用法: python3 check_md.py 文档.md [...]")
        sys.exit(2)
    total = 0
    for f in files:
        try:
            issues, nblk, nbt = check(f)
        except UnicodeDecodeError as e:
            print("[!] %s  解码失败（非法 UTF-8 字节）: %s" % (os.path.basename(f), e))
            total += 1
            continue
        name = os.path.basename(f)
        if issues:
            total += len(issues)
            print("[!] %s  (块公式 %d, 反引号行内 %d)" % (name, nblk, nbt))
            for it in issues:
                print("      - %s" % it)
        else:
            print("[ok] %s  (块公式 %d, 反引号行内 %d)" % (name, nblk, nbt))
    print("\n合计隐患: %d" % total)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
