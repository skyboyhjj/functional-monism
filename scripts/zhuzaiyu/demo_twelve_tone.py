#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo_twelve_tone.py —— 十二律比值与群结构
对应：zhuzaiyu_structure.md
结论：十二律比 = 2^(n/12)；比值群 ≅ ℤ₁₂（模八度）。【严格】
"""

print("=== 十二律比值 2^(n/12) ===")
for n in range(13):
    print(f"  n={n:2d}   2^(n/12) = {2**(n/12):.10f}")

print()
print("闭环 2^(12/12) =", 2 ** (12 / 12), "（回到八度）")
print("乘性封闭 2^(a/12)*2^(b/12) = 2^((a+b)/12)  =>  循环群 Z12（模八度）")

print()
print(">>> 结论：十二律 = 循环群 Z12 在频率对数轴上的自由作用；单一生成元 2^(1/12)。【严格】")
