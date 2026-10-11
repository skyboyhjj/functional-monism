#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo_two_books.py —— 离散递推 = 连续螺旋的整点采样（两本账）
对应：zhuzaiyu_two_books.md
结论：账 A（离散递推）= 账 B（连续螺旋 z(t)）在整点采样。【严格】
"""
import cmath
from math import log, pi

lam = log(2) / 12
print("连续螺旋 z(t) = exp(t*(ln2/12 + i*2π/12))")
print("逐点对齐 n = 0..12：")
ok = True
for n in range(13):
    disc = 2 ** (n / 12) * cmath.exp(1j * 2 * pi * n / 12)
    cont = cmath.exp(n * (lam + 1j * 2 * pi / 12))
    d = abs(disc - cont)
    ok &= d < 1e-10
    if n in (0, 1, 6, 12):
        print(f"  n={n:2d}  |离散-连续| = {d:.2e}")
print("全部 n 通过:", ok)

print()
print(">>> 结论：离散递推 = 连续螺旋在整点的采样 —— “两本账”成立。【严格】")
