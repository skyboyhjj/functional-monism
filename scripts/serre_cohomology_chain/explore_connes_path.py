#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""核验 Connes–Consani 路线（2026, ζ-cycles）中的三个可算断言：
  ① 算子 Δ = H(1+H)（H = x∂_x，scaling 生成元）的谱 = {(z−1/2)²−1/4 | ζ(z)=0}
     且"该谱为负 ⟺ RH"（推论 4.3）
  ② ζ-cycle 的圆长 L = log μ 与临界零点 s 的关系：L = 2π/s 的整数倍（定理 1.1(ii)）
  ③ Σ_μ 的尺度不变性（ζ-cycle 定义所依赖）"""
import mpmath as mp
mp.mp.dps = 25

def hdr(s): print("=" * 74); print(s); print("=" * 74)

# ---------------------------------------------------------------- ①
hdr("核验①  Δ = H(1+H) 的谱（H = x∂_x）—— 与 ζ 零点的对应")
print("  映射：z ↦ λ = (z − 1/2)² − 1/4")
print(f"  {'k':>3} {'z_k = 1/2 + iγ':>26} {'λ_k':>26} {'Re(λ_k)':>12}")
for k in range(1, 8):
    z = mp.zetazero(k)
    lam = (z - mp.mpf(1) / 2) ** 2 - mp.mpf(1) / 4
    print(f"  {k:>3} {mp.nstr(z, 18):>26} {mp.nstr(lam, 18):>26} {mp.nstr(lam.real, 10):>12}")
print()
print("  ⟹ 临界零点 Re(z)=1/2 ⟹ λ = (iγ)² − 1/4 = −γ² − 1/4 < 0  【恒为负】")
print()

# ---------------------------------------------------------------- ①'
hdr("核验①'  若存在【非临界】零点 β≠1/2，谱会怎样？")
print("  关键在【虚部】：Im(λ) = 2(β − 1/2)·γ")
print("  ⟹ λ ∈ ℝ  ⟺  β = 1/2（零点在临界线上）")
print(f"  {'β':>6} {'γ':>10} {'Im(λ)':>14} {'λ∈ℝ?':>7} {'λ 值':>26}")
for beta in ['0.5', '0.55', '0.7']:
    for gamma in ['14.134725']:
        z = mp.mpf(beta) + 1j * mp.mpf(gamma)
        lam = (z - mp.mpf(1) / 2) ** 2 - mp.mpf(1) / 4
        print(f"  {beta:>6} {gamma:>10} {mp.nstr(lam.imag, 8):>14} "
              f"{'是' if abs(lam.imag) < 1e-12 else '否':>7} {mp.nstr(lam, 20):>26}")
print()
print("  ⟹ 正确的等价链是：")
print("     RH ⟺ 所有非平凡零点满足 β = 1/2 ⟺ Im(λ) = 0（谱为【实数】）")
print("     且此时 λ = −γ² − 1/4 ≤ −1/4（实、且严格为负）")
print("  ⟹ 更准确的表述：'谱为实数（因而落在 (−∞, −1/4]）⟺ RH'")
print("     —— RH 被化归为【谱实性/正性】，这正是 Hilbert–Pólya 式陈述")

# ---------------------------------------------------------------- ②
hdr("核验②  ζ-cycle 的圆长 L = 2π/s（定理 1.1(ii)）")
print(f"  {'k':>3} {'s = γ_k':>14} {'L = 2π/s':>14}")
for k in [1, 2, 3, 5]:
    s = mp.zetazero(k).imag
    L = 2 * mp.pi / s
    print(f"  {k:>3} {mp.nstr(s, 10):>14} {mp.nstr(L, 10):>14}")
print("  ⟹ 每个临界零点 s 给出一个长度 2π/s 的圆；这些圆是 ζ-cycle 的候选")
print("     注意：L 随 γ 增大而减小 —— 高零点对应【短】圆")

# ---------------------------------------------------------------- ③
hdr("核验③  Σ_μ 的尺度不变性（ζ-cycle 定义所依赖）")
mu = mp.mpf('2.5')
K = 400
def Sigma(g, u):
    return mp.fsum(g(u * mu ** k) for k in range(-K, K + 1))
print("  ⚠️ 前提：必须 f(0) = 0，否则 Σ_μ 发散")
print("     （若 f(0) ≠ 0，k→−∞ 时 f(μ^k u) → f(0) ≠ 0，求和发散）")
print("     —— 这正是原文要求 f ∈ S₀^ev（满足 f(0)=0=∫f）的原因")
print()
g = lambda x: x * x * mp.e ** (-x * x)          # 满足 g(0) = 0 ✓
u0 = mp.mpf('1.7')
a, b = Sigma(g, u0), Sigma(g, u0 * mu)
print(f"  μ = {mu},  g(x) = x²·exp(−x²)（满足 g(0)=0）,  u₀ = {u0}")
print(f"  Σ_μ g(u₀)   = {mp.nstr(a, 20)}")
print(f"  Σ_μ g(μ u₀) = {mp.nstr(b, 20)}")
print(f"  差 = {mp.nstr(abs(a-b), 6)}  ⟹ {'✓ 尺度不变' if abs(a-b) < mp.mpf('1e-18') else '✗'}")
print("  ⟹ Σ_μ 把 u 与 μu 等同 ⟹ 它活在一个【圆】R₊*/μ^ℤ 上")
print("     这就是 ζ-cycle 的几何载体：一个长度 L = log μ 的圆")

hdr("小结：Connes 路线的三步结构")
print("  ① 整体作用   ：H = x∂_x（scaling 流），算子 Δ = H(1+H)")
print("  ② 装配       ：通过 trace map E（Hochschild 同调）把局部数据装进 L²(C)")
print("     ★ 关键积分：∫_{R₊*} E(f)(u) u^{−iz} d*u = ζ(1/2 − iz) ψ(z)")
print("  ③ 正性问题   ：Δ 的谱为【实数（从而 ≤ −1/4）】⟺ RH —— 这一步【仍未证】")
print()
print("  本路线把 RH 精确转化为：'某个自伴（或近自伴）算子的谱落在实轴上'")
print("  —— 即：把'零点位置'变成了'谱的实性'。这正是它最贴总纲'正性'之处。")
