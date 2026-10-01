#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo_pythagorean_comma.py —— 三分损益 vs 十二平均律（毕氏音差）
对应：zhuzaiyu_constant_check.md §2.3
结论：三分损益 12 步累积偏差 = 毕氏音差 23.46 音分。【严格】
说明：音分 = 1200*log2(r)。
"""
from math import log2

step = 1.5 / (2 ** (7 / 12))
print("  3/2      =", f"{1.5:.10f}")
print("  2^(7/12) =", f"{2**(7/12):.10f}")
print(f"  单步差 = {1.5 - 2**(7/12):+.6f}   ({1200*log2(step):.2f} 音分)")

comma = (1.5 ** 12) / (2 ** 7)
print(f"  12步累积 (3/2)^12 / 2^7 = {comma:.10f}   ({1200*log2(comma):.2f} 音分，毕氏音差)")

print()
print(">>> 结论：三分损益 12 步回不到八度；朱载堉用 2^(1/12) 把偏差平均掉。【严格】")
