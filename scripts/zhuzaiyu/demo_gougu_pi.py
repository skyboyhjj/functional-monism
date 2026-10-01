#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo_gougu_pi.py —— 勾股律管（黄钟-蕤宾）与 π 密率
对应：读解 §二（原文核对）
结论：勾股算例 10√2 / 5√2 正确；密率 355/113 正确。
"""
from math import sqrt, pi

print("=== 黄钟-蕤宾（勾股）===")
print("  蕤宾倍律 = 10*sqrt(2) =", 10 * sqrt(2))
print("  蕤宾正律 =  5*sqrt(2) =", 5 * sqrt(2))
print("  回到黄正: 5sqrt2*sqrt2 =", 5 * sqrt(2) * sqrt(2), " (应 = 10)")

print()
print("=== π 近似 ===")
print(f"  约率 22/7    = {22/7:.10f}   误差 {22/7 - pi:+.3e}")
print(f"  密率 355/113 = {355/113:.10f}   误差 {355/113 - pi:+.3e}")

print()
print(">>> 结论：勾股算例与密率均正确（半严格·数值）。")
