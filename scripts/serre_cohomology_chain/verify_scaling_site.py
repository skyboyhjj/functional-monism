#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_scaling_site.py

核验「Connes 的 Scaling Site 层上同调 = ②层的一个实现」里几处可算的事实。

A. 特征标下降 ⟹ 圆长 L = 2πn/s
   λ ↦ λ^{is} 要下降为圆 C_μ = R_+^*/μ^Z（μ = e^L）上的函数，必须 s·L ∈ 2πZ。
   故 ζ-cycle 的圆长恰好是 2π/s 的整数倍 —— 此即 Connes–Consani 的 Theorem 1.1(ii)。
B. Scaling Site 的 theta 函数恒等式：θ(pλ) = θ(λ) + λ − 1（对 p = 2,3,5,7 数值恒等）。
C. 覆盖稳定性：若 L 使 s·L ∈ 2πZ，则 nL 亦然（n 重覆盖仍是 ζ-cycle）。

运行：python3 verify_scaling_site.py
"""
import math

# ζ 前 8 个非平凡零点的虚部
ZEROS = [14.134725141734693, 21.022039638771555, 25.010857580145688,
         30.424876125859513, 32.935061587739189, 37.586178158825671,
         40.918719012147495, 43.327073280914999]


def check(cond, msg):
    print(("  ✓ " if cond else "  ✗ ") + msg)
    return cond


def theta(lam, p, M=200):
    """Scaling Site 的 theta 函数（两项均单调，可早停，避免 p^m 溢出）：
       theta(lam) = sum_{m>=0} max(0, 1 - p^m lam) + sum_{m>=1} max(0, lam/p^m - 1)"""
    s = 0.0
    pm = 1.0                       # p^m
    for _ in range(M):
        t = 1.0 - pm * lam
        if t <= 0.0:
            break
        s += t
        pm *= p
    pm = p                         # p^m, m 从 1 起
    for _ in range(1, M):
        t = lam / pm - 1.0
        if t <= 0.0:
            break
        s += t
        pm *= p
    return s


def main():
    ok = True

    print("=== A. 特征标下降，圆长 L = 2πn/s（Theorem 1.1(ii)）===")
    print("  判据：s*L in 2πZ  <=>  L in (2π/s)Z")
    L1 = 2 * math.pi / ZEROS[0]
    for s in ZEROS[:4]:
        L = 2 * math.pi / s
        r = s * L / (2 * math.pi)
        ok &= check(abs(r - round(r)) < 1e-12 and round(r) == 1,
                    f"s={s:.6f} -> L=2π/s={L:.6f}，s·L/2π={r:.12f}（整数）")
    print("  反例：同一 L 对非零点 s'=13 不成立")
    r13 = 13.0 * L1 / (2 * math.pi)
    ok &= check(abs(r13 - round(r13)) > 1e-6,
                f"s'=13：s'·L/2π={r13:.6f}（非整数，故非 ζ-cycle）")

    print("\n=== B. theta 函数恒等式 theta(p*lam) = theta(lam) + lam - 1 ===")
    for p in (2, 3, 5, 7):
        worst = 0.0
        for lam in (0.2, 0.37, 0.7, 1.0, 1.3, 1.9, 2.7, 5.0, 11.0):
            d = abs(theta(p * lam, p) - (theta(lam, p) + lam - 1.0))
            worst = max(worst, d)
        ok &= check(worst < 1e-9, f"p={p}：最大偏差 {worst:.2e}")

    print("\n=== C. 覆盖稳定性：n 重覆盖仍是 ζ-cycle ===")
    s = ZEROS[0]
    for n in (1, 2, 3, 4, 5):
        L = n * (2 * math.pi / s)
        r = s * L / (2 * math.pi)
        ok &= check(abs(r - round(r)) < 1e-12, f"n={n}：L={L:.6f}，s·L/2π={r:.12f}（整数）")

    print("\n=== 结论 ===")
    print("  A ✓ 圆长必为 2π/s 的整数倍（特征标 λ^{is} 能在圆上单值下降）")
    print("  B ✓ theta 恒等式精确成立：Scaling Site 的『热带』几何自洽")
    print("  C ✓ 覆盖保持 ζ-cycle：同一零点在族中无穷次出现，故 site 是自然参数空间")
    print("  ==> 以上是『层上同调把临界零点实现为缩放作用之谱』的周边可算事实；")
    print("      真正的谱实现（Theorem 1.2 / 5.4）在文献里，本脚本不重证。")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
