#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
langlands_into_the_bridge.py
============================
把「朗兰兹」那一格接进同一个桥（相位 <-> 幅度 = 矢势 <-> 势差）。

桥的回顾：
    矢势型(反对称,curl!=0) = 相位/环流 ;  势差型(对称,curl=0) = 幅度/定号
    组装: ż = (mu+i*om)z - l|z|^2 z  ,  极限环 = 「幅度钉死 |z|=r*、相位自由」

朗兰兹的接法（本步）：
    相位端 = p-adic / Connes 的 scaling 流 / zeta-cycle（圆，长 log p）
    幅度端 = archimedean / Weil 正性（定号）
    RH 读法： s = sigma + i t （sigma=幅度, t=相位）
             RH <=> sigma 全被钉到 1/2、t 自由  <=> 极限环结构

四组核验：
  1. 组装极限环：幅度钉死（|z|->r*）+ 相位自由（theta 增长）
  2. zeta 零点：相位谱（虚部，自由无界） + 零点计数无界
  3. 显式公式：局部(素数) = 整体(零点) —— 桥的"恒等式"侧
  4. 局部 Euler 积发散：定号非局部
"""
import numpy as np
import mpmath as mp
mp.mp.dps = 25


def rk4_c(f, z0, T, h):
    n = int(round(T / h)); z = complex(z0)
    for _ in range(n):
        k1 = f(z); k2 = f(z + .5 * h * k1)
        k3 = f(z + .5 * h * k2); k4 = f(z + h * k3)
        z = z + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return z


# ================================================================ 1 极限环
def check1():
    print("=" * 72)
    print("1. 组装极限环：幅度钉死、相位自由")
    mu, l, om = 1.0, 1.0, 1.0
    rstar = np.sqrt(mu / l)
    for z0 in (0.30 + 0j, 2.50 + 0j, 1.0 + 1.6j):
        z = rk4_c(lambda z: (mu + 1j * om) * z - l * abs(z) ** 2 * z, z0, 60.0, 1e-3)
        print(f"  z0={z0}  ->  |z| = {abs(z):.6f} (r*={rstar})   "
              f"arg = {np.degrees(np.angle(z)) % 360:7.2f} 度 (自由)")
    print("  => |z| 被钉到 r*（幅度），arg(相位) 自由 —— 极限环")


# ================================================================ 2 zeta 零点
def check2():
    print("=" * 72)
    print("2. zeta 零点：相位谱（虚部 gamma，自由）+ 计数无界")
    gams = [mp.zetazero(k).imag for k in range(1, 6)]
    print("  前 5 个零点虚部 gamma_k =",
          ", ".join(mp.nstr(g, 6) for g in gams))
    print("  (Riemann–Siegel 独立算法已核验到 t~1e12 都在 sigma=1/2；")
    print("   本条只作『相位自由』的展示，不是 RH 的证明)")
    N = 200
    G = [mp.zetazero(k).imag for k in range(1, N + 1)]
    print(f"  {'T':>6}{'N(T)实测':>10}{'(T/2pi)log(T/2pi e)':>24}")
    for T in (50, 100, 200, 400):
        na = sum(1 for g in G if g <= T)
        est = T / (2 * mp.pi) * mp.log(T / (2 * mp.pi * mp.e))
        print(f"  {T:>6}{na:>10}{mp.nstr(est, 8):>24}")
    print("  => 相位(零点虚部)自由、无界 —— 零点无穷多")


# ================================================================ 3 显式公式
def check3():
    print("=" * 72)
    print("3. 显式公式：局部(素数) = 整体(零点) —— 桥的『恒等式』侧")
    h = lambda r: mp.e ** (-(r ** 2) / 2)
    g = lambda u: mp.sqrt(2 * mp.pi) / (2 * mp.pi) * mp.e ** (-(u ** 2) / 2)

    def vM(n):
        m = n
        for d in range(2, n + 1):
            if m % d == 0:
                while m % d == 0:
                    m //= d
                return mp.log(d) if m == 1 else 0.0
        return 0.0

    Nz = 120
    LHS = 2 * mp.fsum(h(mp.zetazero(k).imag) for k in range(1, Nz + 1))
    arch = mp.quad(lambda r: h(r) * mp.re(mp.digamma(mp.mpf(1) / 4 + 1j * mp.mpf(r) / 2)),
                   [-mp.inf, 0, 0, mp.inf]) / (2 * mp.pi)
    ps = mp.fsum(vM(n) / mp.sqrt(n) * g(mp.log(n))
                 for n in range(2, 4001) if vM(n) != 0)
    RHS = arch + 2 * h(1j / 2) - g(0) * mp.log(mp.pi) - 2 * ps
    print(f"  |LHS(零点, N={Nz}) - RHS(arch+素数)| = {mp.nstr(abs(LHS - RHS), 4)}")
    print("  => 两半相等（等式，免费）；缺的是它的【符号】")


# ================================================================ 4 局部积
def check4():
    print("=" * 72)
    print("4. 局部 Euler 积发散：定号不是局部量")
    def primes(n):
        s = np.ones(n + 1, bool); s[:2] = False
        for i in range(2, int(n ** .5) + 1):
            if s[i]:
                s[i * i::i] = False
        return np.nonzero(s)[0]
    for P in (100, 1000, 10000, 100000):
        p = primes(P).astype(float)
        print(f"  P={P:>6}  prod(1-p^-1/2)^-2 = {np.prod((1 - p ** -0.5) ** -2):.4e}")


# ================================================================ 5 桥的两端
def check5():
    print("=" * 72)
    print("5. 朗兰兹接进桥：两端映射")
    rows = [
        ("相位/环流(矢势)", "p-adic / scaling 流 H=x d_x", "zeta-cycle 圆(长 log p)", "好"),
        ("幅度/定号(势差)", "archimedean / Weil 正性", "Connes-Consani 2021 已证", "好"),
        ("桥(合拢)", "Delta=H(1+H) 自伴 谱实", "全部 places 合成", "缺"),
    ]
    print(f"  {'端':<16}{'数学对象':<28}{'现状':<26}")
    for r in rows:
        print(f"  {r[0]:<16}{r[1]:<28}{r[2]:<26}")


if __name__ == "__main__":
    check1(); check2(); check3(); check4(); check5()
    print("=" * 72)
    print("完成。")
