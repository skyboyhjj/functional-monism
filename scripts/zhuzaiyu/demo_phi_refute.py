#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demo_phi_refute.py —— 【证伪记录】φ / 斐波那契并不“耦合”十二律
对应：zhuzaiyu_constant_check.md（找反例）
结论：φ 与十二律无精确关系；斐波那契不是同一序列。【严格否定】
（本脚本是“失败记录”性质：记录一个被证伪的声称，如同 demo_R.py。）
"""
from math import log2, sqrt

phi = (1 + sqrt(5)) / 2
print("=== φ 与十二律 ===")
print(f"  φ = {phi:.12f}")
print(f"  log2(φ) = {log2(phi):.12f}")
print(f"  φ 的律位 = {log2(phi)*12:.4f}   <- 非整数")
print("  推导：若 2^(n/12)=φ，则 φ^12=2^n；φ 是二次代数数、2^n 是有理数 ⟹ 不可能。")

print()
print("=== 斐波那契 vs 十二律 ===")
f = [1, 1]
for _ in range(12):
    f.append(f[-1] + f[-2])
print(f"  斐波那契相邻比  -> {f[-1]/f[-2]:.6f}  (趋 φ = 1.618...)")
print(f"  十二律比        -> {2.0:.6f}  (趋 2)")
print("  两组比值不同 ⟹ 不是同一序列。")

print()
print(">>> 结论：两处“耦合”均不成立；“姑洗=黄金分割点”是数值巧合。【严格否定】")
