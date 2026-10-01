# -*- coding: utf-8 -*-
"""朱载堉十二律 · 实例化复算（SOP S4 侦察链支撑）"""
import cmath
from math import log, log2, sqrt, pi

line = "=" * 64

print(line)
print("A. 十二律结构：比值群 ≅ Z12 ×（八度标度）")
print(line)
for n in range(13):
    print(f"  n={n:2d}   2^(n/12) = {2**(n/12):.10f}")
print(f"  闭环 2^(12/12) = {2**(12/12)}")
print("  乘性封闭 2^(a/12)*2^(b/12)=2^((a+b)/12)  => 循环群 Z12（模八度）")

print()
print(line)
print("B. 离散递推 = 连续螺旋的整点采样（两本账）")
print(line)
lam = log(2) / 12
ok = True
for n in range(13):
    disc = 2 ** (n / 12) * cmath.exp(1j * 2 * pi * n / 12)
    cont = cmath.exp(n * (lam + 1j * 2 * pi / 12))
    ok &= abs(disc - cont) < 1e-10
print(f"  2^(n/12)*e^(i2πn/12) == exp(n*(ln2/12 + i2π/12))  for n=0..12 : {ok}")
print("  => 离散递推 = 连续流 z(x)=exp(x*(ln2/12+i2π/12)) 在整数点采样")

print()
print(line)
print("C. 【核心】‘12’从哪来？— log2(3/2) 的连分数最佳逼近")
print(line)
x = log2(1.5)
print(f"  log2(3/2) = {x:.12f}")
a = []; y = x
for _ in range(8):
    i = int(y); a.append(i); y -= i
    if y == 0: break
    y = 1 / y
print("  连分数:", a)
p_2, p_1, q_2, q_1 = 0, 1, 1, 0
print("  收敛项 p/q（= m 个五度 ≈ n 个八度）:")
for ai in a:
    p = ai * p_1 + p_2; q = ai * q_1 + q_2
    err = abs(p / q - x)
    print(f"    {p}/{q} = {p/q:.10f}   误差 {err:.3e}  ({err*1200:.3f} 音分)")
    p_2, p_1 = p_1, p; q_2, q_1 = q_1, q
print("  => 7/12 是 log2(3/2) 的极佳逼近；十二律的‘12’= 这个逼近的分母")

print()
print(line)
print("D. 【找反例】φ 与十二律：不存在精确关系")
print(line)
phi = (1 + sqrt(5)) / 2
print(f"  log2(phi) = {log2(phi):.12f}   律位 = {log2(phi)*12:.4f}（非整数）")
print("  若 2^(n/12)=φ，则 φ^12=2^n：φ 是二次代数数，φ^k 仍二次；2^n 是有理数。")
print("  => 不可能相等。【精确关系不存在】；‘姑洗=黄金点’是数值巧合。")

print()
print(line)
print("E. 三分损益 vs 十二平均律：毕氏音差与累积漂移（音分 = 1200*log2）")
print(line)
step = 1.5 / (2 ** (7 / 12))
print(f"  3/2      = {1.5:.10f}")
print(f"  2^(7/12) = {2**(7/12):.10f}")
print(f"  单步差 = {1.5 - 2**(7/12):+.6f}  ({1200*log2(step):.2f} 音分)")
comma = (1.5 ** 12) / (2 ** 7)
print(f"  12步累积 (3/2)^12 / 2^7 = {comma:.10f}  ({1200*log2(comma):.2f} 音分，毕氏音差)")
print("  => 三分损益 12 步回不到八度（差一个毕氏音差）；朱载堉用 2^(1/12) 把它‘平均’⇒ 历史要害")

print()
print(line)
print("F. 五声音阶在 Z12 中的位置")
print(line)
print("  五声(宫商角徵羽) ≈ Z12 的 {0,2,4,7,9}")
print("  五度圈以 +7 步进：", [(7 * k) % 12 for k in range(12)])
print("  （+7 步进遍历全部 12 律，因为 gcd(7,12)=1）")
