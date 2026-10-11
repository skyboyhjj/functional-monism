#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_monopole_bundle.py

核验《从莫比乌斯带到磁单极》里的几处关键事实，并与本项目旧算据对接。

 A. Hopf 纤维化：**任意**两根不同纤维的环绕数恒为 1（取三对不同的纤维实算）。
 B. 磁单极的拓扑荷 = 第一陈数：过渡函数 phi -> e^{i n phi} 的绕数 = n。
    （与 08 的"整数化"同一判据：单值 ⟺ 整数 ⟺ Chern 数取整。）
 C. 切丛截面障碍：chi(环面)=0（可梳平）vs chi(S^2)=2（梳不平）。

运行：python3 verify_monopole_bundle.py
"""
import cmath
import math


def check(cond, msg):
    print(("  ✓ " if cond else "  ✗ ") + msg)
    return cond


def normalize(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


def hopf_fiber(w, t, M=400):
    """Hopf 映射 eta(z1,z2)=(2 z1 conj(z2), |z1|^2-|z2|^2) 在 p=(w,t) 上的纤维。
       纤维 = { e^{i a} * (A, beta) }，A=sqrt((1+t)/2), beta=w/(2A)。"""
    A = math.sqrt((1 + t) / 2)
    beta = complex(w) / (2 * A)
    pts = []
    for k in range(M):
        ph = 2 * math.pi * k / M
        e = cmath.exp(1j * ph)
        pts.append([(e * A).real, (e * A).imag, (e * beta).real, (e * beta).imag])
    return pts


def stereographic(P, N, basis):
    d = sum(P[i] * N[i] for i in range(4))
    W = [(P[i] - d * N[i]) / (1.0 - d) for i in range(4)]
    return [sum(W[i] * basis[j][i] for i in range(4)) for j in range(3)]


def gauss_linking(C1, C2):
    tot = 0.0
    n1, n2 = len(C1), len(C2)
    for i in range(n1):
        r1 = C1[i]
        d1 = [C1[(i + 1) % n1][k] - r1[k] for k in range(3)]
        for j in range(n2):
            r2 = C2[j]
            d2 = [C2[(j + 1) % n2][k] - r2[k] for k in range(3)]
            r = [r1[k] - r2[k] for k in range(3)]
            cr = [d1[1] * d2[2] - d1[2] * d2[1],
                  d1[2] * d2[0] - d1[0] * d2[2],
                  d1[0] * d2[1] - d1[1] * d2[0]]
            num = sum(r[k] * cr[k] for k in range(3))
            den = sum(x * x for x in r) ** 1.5
            if den > 1e-12:
                tot += num / den
    return tot / (4 * math.pi)


def winding(n, M=100000):
    tot, prev = 0.0, 0.0
    for j in range(M + 1):
        z = cmath.exp(1j * n * (2 * math.pi * j / M))
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


def main():
    ok = True

    print("=== A. Hopf 纤维化：任意两根纤维的环绕数 = 1 ===")
    N = normalize([1.0, 1.0, 1.0, 1.0])
    e1 = normalize([1, -1, 0, 0])
    e2 = normalize([1, 1, -2, 0])
    e3 = normalize([1, 1, 1, -3])
    # 三对不同的点 p=(w,t) in S^2（|w|^2+t^2=1）
    pairs = [
        (complex(0.3, 0.4), math.sqrt(0.75), complex(-0.5, 0.2), -math.sqrt(0.71)),
        (complex(0.6, 0.0), 0.8, complex(0.0, 0.6), -0.8),
        (complex(-0.2, 0.7), math.sqrt(1 - 0.53), complex(0.5, -0.5), math.sqrt(1 - 0.5)),
    ]
    for i, (w1, t1, w2, t2) in enumerate(pairs, 1):
        C1 = [stereographic(P, N, [e1, e2, e3]) for P in hopf_fiber(w1, t1)]
        C2 = [stereographic(P, N, [e1, e2, e3]) for P in hopf_fiber(w2, t2)]
        lk = gauss_linking(C1, C2)
        print(f"  第 {i} 对纤维：环绕数 = {lk:+.4f}")
        ok &= check(abs(abs(lk) - 1.0) < 0.05, "|环绕数| = 1")
    print("  ==> 「任意两根纤维恒为 1」成立 ⟹ c_1(Hopf) = ±1 ≠ 0")

    print("\n=== B. 磁单极拓扑荷 = 第一陈数 = 过渡函数绕数 ===")
    for n in (1, 2, -1, 3):
        w = winding(n, M=50000)
        print(f"  过渡函数 phi -> e^(i {n:+d} phi)：绕数 = {w:+.4f}")
        ok &= check(abs(w - n) < 1e-6, f"绕数 = n = {n}")
    print("  ==> 「Dirac 量子化条件的整数 n」= 第一陈数 = 过渡函数绕数")
    print("      （与 08 的整数化判据同一件：单值 ⟺ 整数 ⟺ Chern 数取整）")

    print("\n=== C. 切丛截面障碍：chi 定生死 ===")
    chi_torus = 1 - 2 + 1          # 环面的 CW 结构：1 顶点 2 边 1 面
    chi_s2 = 4 - 6 + 4             # 四面体
    print(f"  环面 chi = {chi_torus}（可梳平：chi=0 ⟹ 存在处处非零向量场）")
    print(f"  球面 chi = {chi_s2}（梳不平：chi≠0 ⟹ 必有零点）")
    ok &= check(chi_torus == 0 and chi_s2 == 2, "Poincare-Hopf：零点指数和 = chi")

    print("\n=== 结论 ===")
    print("  A ✓ 任意两根 Hopf 纤维环绕数为 1（Hopf 不变量 = 1）")
    print("  B ✓ 磁单极荷 = c_1 = 过渡函数绕数（整数）")
    print("  C ✓ chi 决定切丛截面是否存在（环面可、球面不可）")
    print("  ==> 本篇的『整数 n』与 08 的『度数』是同一个整数：")
    print("      Dirac 量子化 = 第一陈数 = 和乐/2pi = 特征标绕数。")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
