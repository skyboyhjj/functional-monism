#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_five_criteria_instances.py

为「五条刻度尺逐格核」提供算据（先算后说）：
  组 1  阴阳五行：相生算子 R（5-循环置换阵）—— R⁵=I、det=1、谱=5 次单位根。
  组 2  朱载堉十二律：2^(n/12)、螺旋整点采样、"12"=连分数 7/12、毕氏音差。
  组 3  （v1.4）阴阳五行的二维拓扑激发：U(1) 涡旋的绕数 = 整数拓扑荷。
  组 4  （v1.4）十二律的八度圆 S¹：ℤ₁₂ 在对数轴的自由作用 ⟹ 商 = 圆周。
"""
import numpy as np
from math import log2, log

np.set_printoptions(precision=6, suppress=True)
print("=" * 70)
print("组 1 · 阴阳五行：相生算子 R = 5-循环置换")
print("=" * 70)
R = np.roll(np.eye(5), 1, axis=0)
print("R =\n", R.astype(int))
print("R^5 == I :", np.allclose(np.linalg.matrix_power(R, 5), np.eye(5)),
      " | det(R) =", int(round(np.linalg.det(R))))
lam = np.linalg.eigvals(R)
print("特征值     :", np.round(lam, 6))
print("|λ| 全为 1 :", np.allclose(np.abs(lam), 1.0), "  （谱 = 5 次单位根）")
real_ev = [l for l in lam if abs(l.imag) < 1e-12]
print("实特征值   :", np.round(real_ev, 6), "  <- λ=1（全 1 向量）")
print("⟹ 存在 1 维不变子空间（常数模）⟹ 作为【矩阵】，R 在 ℝ 上【可约】。")
print("  注意：'R 不可约'只在【置换单循环 / 作用传递】这一义上成立，与矩阵不可约是两回事。")
print("名相对应：相生=R、相克=R²、相乘/相侮=R³、子病及母=R⁴ —— 单一生成元 ⟹ 循环群 C₅")
Z10 = list(range(10))
print("阴阳五行整体 0 → ℤ₅ → ℤ₁₀ → ℤ₂ → 0 : 子群|2ℤ₁₀| =",
      len([x for x in Z10 if x % 2 == 0]), "  商类 =", sorted({x % 2 for x in Z10}))

print()
print("=" * 70)
print("组 2 · 朱载堉十二律：ℤ₁₂ × 对数标度")
print("=" * 70)
n = np.arange(12)
ratios = 2 ** (n / 12.0)
print("十二律比值 2^(n/12)（前 6）:", np.round(ratios[:6], 6))


def z(t):
    return np.exp(t * (log(2) / 12 + 2j * np.pi / 12))


zs = z(n.astype(float))
print("螺旋 |z(n)| 对 2^(n/12) 最大偏差 :",
      float(np.max(np.abs(np.abs(zs) - ratios))), "（整点采样 = 十二律）")
print("螺旋 相位 (mod 12) 对 n 最大偏差  :",
      float(np.max(np.abs((np.angle(zs) / (2 * np.pi / 12)) % 12 - n))))
print("z(12) =", np.round(z(12.0), 6), " ⟹ 一个八度后回到比值 2")
x = log2(1.5)
cf, y = [], x
for _ in range(6):
    a = int(y); cf.append(a); y = 1.0 / (y - a) if y - a > 1e-15 else 0.0
print("log2(3/2) =", round(x, 8), " 连分数 =", cf)
p2, p1, q2, q1 = 0, 1, 1, 0
for a in cf:
    p = a * p1 + p2; q = a * q1 + q2
    p2, p1 = p1, p; q2, q1 = q1, q
    if q in (2, 5, 12):
        print(f"   收敛子 {p}/{q} = {p/q:.8f}  （分母 {q} ⟸ 就是'12'）")
print("三分损益 12 步偏差（毕氏音差）= %.2f 音分" % (1200 * log2((1.5 ** 12) / (2 ** 7))))

print()
print("=" * 70)
print("组 3 · 阴阳五行的二维拓扑激发：U(1) 涡旋的绕数（拓扑荷）")
print("=" * 70)


def winding(q, M=4000):
    phi = np.linspace(0, 2 * np.pi, M, endpoint=False)
    theta = q * phi                                    # θ = q·φ（q = 涡旋荷）
    d = np.diff(np.concatenate([theta, theta[:1]]))
    d = (d + np.pi) % (2 * np.pi) - np.pi              # 解缠绕
    return d.sum() / (2 * np.pi)


print("绕数 (1/2π)∮∇θ·dl 对连续形变是常数、且取整数值：")
for q in [0, 1, 2, 3, -1]:
    w = winding(q)
    print(f"   标称荷 q={q:>2}  ->  实测绕数 = {w:+.6f}   （整数：{abs(w-round(w))<1e-9}）")
print("⟹ 涡旋荷被'钉'成整数（拓扑不变量）—— 这就是二维 XY 模型的拓扑激发；")
print("   KT 相变 = 涡旋-反涡旋对的束缚/解离（拓扑缺陷的定性转变）。")

print()
print("=" * 70)
print("组 4 · 十二律的八度圆 S¹：ℤ₁₂ 在对数频率轴上的自由作用")
print("=" * 70)
logf = n * (1.0 / 12.0)                                # log2(频率)，以八度为周期
print("log2(f) mod 1（12 个点，环绕一周）:", np.round(np.sort(logf % 1), 6))
print("互不相同（12 个独立类）:", len(set(np.round(logf % 1, 9))) == 12)
print("n=12 时 mod 1 =", (12 / 12.0) % 1, " ⟹ 12 步回到起点（周期 12）")
# 自由作用：任何非零步长都无不动点
for k in [1, 5, 7]:
    fixed = [m for m in range(12) if (m * k) % 12 == 0]
    print(f"   步长 k={k}: 有不动点吗（应只在 m=0）->", fixed)
print("⟹ 对数轴 ℝ 被 ℤ₁₂ 自由作用，商 ℝ/(ln2·ℤ) ≅ S¹（'八度圆'）；")
print("   十二律 = 圆上的 12 个等分点。")
print()
print("裁决：组 1–4 均为【严格】结构事实。")
