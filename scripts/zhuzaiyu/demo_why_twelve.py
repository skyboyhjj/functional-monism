#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo_why_twelve.py —— “12” 从哪来？log2(3/2) 的连分数最佳逼近
对应：zhuzaiyu_constant_check.md（重构部分）
结论：“12” = log2(3/2) 的收敛项 7/12 的分母。【严格】
"""
from math import log2

x = log2(1.5)
print(f"log2(3/2) = {x:.12f}")

a = []; y = x
for _ in range(8):
    i = int(y); a.append(i); y -= i
    if y == 0: break
    y = 1 / y
print("连分数:", a)

print("收敛项 p/q（m 个五度 ≈ n 个八度）：")
p2, p1, q2, q1 = 0, 1, 1, 0
for ai in a:
    p = ai * p1 + p2; q = ai * q1 + q2
    print(f"  {p}/{q} = {p/q:.10f}   误差 {abs(p/q - x)*1200:.3f} 音分")
    p2, p1 = p1, p; q2, q1 = q1, q

print()
print(">>> 结论：7/12 是 log2(3/2) 的极佳逼近 —— 十二律的“12”。【严格】")
