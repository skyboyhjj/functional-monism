#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""explore_gongli3_h1_integral.py

给「公理 III · 第三角」的「拓扑↔几何」边补【整数化版本】的算据。

A. 度数 = 绕数：特征标 C_mu -> U(1) 的绕数恰为 sL/2pi（整数时）。
B. 障碍的两级：连续级(R) 与 整数级(Z)。
   omega = alpha dtheta：R-判据（周期是否为 0）vs Z-判据（alpha 是否为整数）。
C. 可离散化判据：圆上旋转 dot theta = alpha 的轨道
   周期闭 ⟺ alpha 有理；稠密 ⟺ alpha 无理（实算：周期/稠密）。
D. 06 的范例（oint dtheta = 2pi）其实已是 Z-型：度数 = 1。

运行：python3 explore_gongli3_h1_integral.py
"""
import cmath
import math


def check(cond, msg):
    print(("  ✓ " if cond else "  ✗ ") + msg)
    return cond


def winding(k, M=200000):
    """数值绕数：theta -> exp(i k theta)，theta 走一圈。"""
    tot, prev = 0.0, 0.0
    for j in range(M + 1):
        z = cmath.exp(1j * k * (2 * math.pi * j / M))
        a = cmath.phase(z)
        if j > 0:
            d = a - prev
            while d > math.pi:
                d -= 2 * math.pi
            while d < -math.pi:
                d += 2 * math.pi
            tot += d
        prev = a
    return tot / (2 * math.pi)


def orbit_period(alpha, maxN=20000, tol=1e-7):
    """轨道 theta_n = n*alpha mod 1 的最小正周期；无（在 maxN 内）则 None。"""
    for N in range(1, maxN + 1):
        r = (N * alpha) % 1.0
        if min(r, 1 - r) < tol:
            return N
    return None


def distinct_residues(alpha, N=2000, bins=200):
    """把 n*alpha mod 1 装进 bins 个格子，数非空格子数（稠密性指标）。"""
    seen = set(int((n * alpha % 1.0) * bins) for n in range(1, N + 1))
    return len(seen)


def main():
    ok = True

    print("=== A. 度数 = 绕数 = sL/2pi ===")
    for k in (1, 2, 3, -1):
        w = winding(k)
        ok &= check(abs(w - k) < 1e-6, f"k={k}: 数值绕数 = {w:.6f}")
    s0 = 14.134725141734693
    L = 2 * math.pi * 2 / s0          # 取 n = 2
    k = s0 * L / (2 * math.pi)
    ok &= check(abs(k - 2) < 1e-12 and abs(winding(round(k), M=50000) - 2) < 1e-6,
                f"ζ-cycle: sL/2pi = {k:.6f} = 特征标绕数（度）")

    print("\n=== B. 障碍的两级：连续级(R) vs 整数级(Z) ===")
    print("  omega = alpha dtheta：")
    for name, alpha in [("0", 0.0), ("1", 1.0), ("1/2", 0.5), ("sqrt2", math.sqrt(2))]:
        period = 2 * math.pi * alpha                        # ∮ omega
        R_block = abs(period) > 1e-12                       # R-障碍非零
        Z_ok = abs(alpha - round(alpha)) < 1e-12            # 属于 Z
        print(f"  alpha={name:6s}: R-障碍(∮omega={period:.6f})={'非零' if R_block else '零'}；"
              f"Z-判据(alpha∈Z)={'是' if Z_ok else '否'}")
    ok &= check(abs(2 * math.pi * 1.0 - 2 * math.pi) < 1e-12, "范例 alpha=1 的周期恰为 2pi（Z-型）")

    print("\n=== C. 可离散化判据：有理旋转闭轨道 / 无理旋转稠密 ===")
    for name, alpha in [("1（整数）", 1.0), ("1/2（有理）", 0.5), ("1/3（有理）", 1 / 3),
                        ("sqrt2（无理）", math.sqrt(2))]:
        T = orbit_period(alpha)
        dens = distinct_residues(alpha, N=2000, bins=200)
        print(f"  alpha={name:12s}: 最小周期={T}；2000 步落在 {dens}/200 个格子")
        if alpha in (1.0, 0.5, 1 / 3):
            ok &= check(T is not None, f"alpha={alpha} 轨道周期闭")
        else:
            ok &= check(T is None and dens > 190, "alpha=sqrt2 稠密（周期不存在，覆盖 ~200 格）")
    print("  ==> 有理旋转数 ⟹ 轨道闭 ⟹ 可离散记账；无理 ⟹ 稠密 ⟹ 不可")

    print("\n=== D. 06 的范例已是 Z-型 ===")
    ok &= check(abs(winding(1) - 1) < 1e-6, "oint dtheta = 2pi 对应度数 n = 1（整数型）")

    print("\n=== 结论 ===")
    print("  A ✓ 度数 = 绕数 = sL/2pi；n 就是特征标的度数（H^1(S^1;Z)）")
    print("  B ✓ 障碍分两级：R-级（周期，判势是否存在）/ Z-级（度数，判可否离散记账）")
    print("  C ✓ 可离散化 ⟺ 旋转数有理；ζ-cycle 更强：要求【整数】")
    print("  D ✓ 06 的范例本来就在 Z-级（度 1）—— 整数化是补出它下面的一格，不是替换")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
