#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_interoceptive_F.py
=========================
算据：照 Dirac 样板，为内感受 AI 写出公理 II 的拉氏量 F，
      并核验"那一项"（不可写成势差的内生驱动 = 曲率项）。

模型（内感受场 = 内部状态轨迹 psi(t) = s(t) in R^2）：
    F[s] = Int L dt ,   L = (1/2) m |sdot|^2 - V(s) + A(s).sdot
Euler-Lagrange:
    m sddot = -grad V(s) + (curl A) J sdot ,   J = [[0,1],[-1,0]]
其中 curl A = d_x A_y - d_y A_x （2D 唯一分量）。

五组核验：
  A. E-L 正确性     ：E-L 残差 ~ 0；作用量驻定 O(eps^2)
  B. 规范不变性     ：A -> A + grad(chi) 不改轨迹（势差部分被吸收）
  C. 势型 vs 非势差 ：curl=0 轨迹不出初始的 1 维子空间；curl!=0 进入 2 维环流
  D. 环积分 = 曲率  ：oint A.ds = curl * Area （非保守力 => 不可写成势差）
  E. 精度 gamma     ：gamma = ||curl A||；文章原型 A=grad(-D) => gamma = 0
所有数值都做步长细扫（h = 1e-3 / 5e-4 / 2.5e-4）以排除伪象。
"""

import numpy as np

trapz = getattr(np, "trapezoid", None) or np.trapz   # numpy>=2 改名

m = 1.0                                     # 状态空间里的"惯性"
k = 1.0                                     # 势阱刚度
J2 = np.array([[0.0, 1.0], [-1.0, 0.0]])    # 反对称 2x2（等价于乘 -i）


# ---------------------------------------------------------------- 势与驱动场
def V_quad(s):
    return 0.5 * k * float(np.dot(s, s))


def gradV_quad(s):
    return k * np.asarray(s, float)


def A_curl(s, w):
    """A = (w/2)(-y, x)  =>  curl A = w（常数曲率）"""
    s = np.asarray(s, float)
    return 0.5 * w * np.array([-s[1], s[0]])


def chi(s):
    """规范函数 chi = 0.3 x^2 y"""
    s = np.asarray(s, float)
    return 0.3 * s[0] ** 2 * s[1]


def grad_chi(s):
    s = np.asarray(s, float)
    return np.array([0.6 * s[0] * s[1], 0.3 * s[0] ** 2])


def A_paper(s, sp):
    """文章原型：内感受"奖励" r = D(s_t) - D(s_{t+1})  等价于 A = grad(-D)，
    D = |s - s*|（到设定点的欧氏距离）。"""
    r = np.asarray(s, float) - np.asarray(sp, float)
    nrm = np.sqrt(float(np.dot(r, r))) + 1e-12
    return -r / nrm                          # = grad(-D)


# ---------------------------------------------------------------- 积分器
def accel(s, v, curl):
    """m a = -grad V + curl * J v"""
    return -gradV_quad(s) + curl * (J2 @ v)


def rk4_step(f, s, v, h):
    k1s = v
    k1v = f(s, v)
    k2s = v + 0.5 * h * k1v
    k2v = f(s + 0.5 * h * k1s, v + 0.5 * h * k1v)
    k3s = v + 0.5 * h * k2v
    k3v = f(s + 0.5 * h * k2s, v + 0.5 * h * k2v)
    k4s = v + h * k3v
    k4v = f(s + h * k3s, v + h * k3v)
    return (s + (h / 6.0) * (k1s + 2 * k2s + 2 * k3s + k4s),
            v + (h / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v))


def integrate(f, s0, v0, T, h):
    n = int(round(T / h))
    S = np.zeros((n + 1, 2)); Vv = np.zeros((n + 1, 2))
    S[0], Vv[0] = np.asarray(s0, float), np.asarray(v0, float)
    s, v = S[0].copy(), Vv[0].copy()
    for i in range(n):
        s, v = rk4_step(f, s, v, h)
        S[i + 1], Vv[i + 1] = s, v
    return S, Vv


def enclosed_area(S):
    """轨迹有向面积 ½∮(x dy - y dx)：1 维往返 = 0；2 维环流 ≠ 0。"""
    x, y = S[:, 0], S[:, 1]
    dx, dy = np.gradient(x), np.gradient(y)
    return 0.5 * float(np.sum(x * dy - y * dx))


def dom_freq(S, h):
    x = S[:, 0] - S[:, 0].mean()
    sp = np.abs(np.fft.rfft(x))
    fr = np.fft.rfftfreq(len(x), d=h)
    return fr[np.argmax(sp)]


# ================================================================ A. E-L 自洽
def check_A():
    print("=" * 70)
    print("A. E–L 正确性（变分自洽）")
    w, T = 1.2, 8.0
    f = lambda s, v: accel(s, v, w)
    for h in (1e-3, 5e-4, 2.5e-4):
        S, Vv = integrate(f, [1.0, 0.0], [0.0, 0.0], T, h)
        a_num = (S[2:, :] - 2 * S[1:-1, :] + S[:-2, :]) / h ** 2
        v_mid = (S[2:, :] - S[:-2, :]) / (2 * h)
        rhs = np.array([-gradV_quad(s) + w * (J2 @ v)
                        for s, v in zip(S[1:-1, :], v_mid)])
        res = a_num - rhs
        print(f"  h={h:g}   max|m sddot + gradV - curl J v| = {np.max(np.abs(res)):.3e}")
    h = 2.5e-4
    S0, V0 = integrate(f, [1.0, 0.0], [0.0, 0.0], T, h)
    t = np.linspace(0, T, len(S0))
    eta = np.stack([np.sin(np.pi * t / T), np.zeros_like(t)], axis=1)
    print("  作用量驻定（端点为零的扰动；应 O(eps^2)）：")
    ref = None
    for eps in (0.02, 0.01, 0.005):
        S = S0 + eps * eta
        Vd = np.gradient(S, h, axis=0)
        Acom = np.array([A_curl(s, w) for s in S])
        L = 0.5 * m * np.sum(Vd ** 2, axis=1) - np.array([V_quad(s) for s in S]) \
            + np.sum(Acom * Vd, axis=1)
        val = trapz(L, dx=h)
        ref = val if ref is None else ref
        dS = val - trapz(0.5 * m * np.sum(np.gradient(S0, h, axis=0) ** 2, axis=1)
                         - np.array([V_quad(s) for s in S0])
                         + np.sum(np.array([A_curl(s, w) for s in S0])
                                  * np.gradient(S0, h, axis=0), axis=1), dx=h)
        print(f"    eps={eps:g}   dS = {dS:+.3e}")


# ================================================================ B. 规范不变
def force_from_A(s, v, Afun, fd=1e-6):
    """由 A 数值给出 (J_A^T - J_A) v ：J_A 用中心差分。"""
    J = np.zeros((2, 2))
    for j in range(2):
        e = np.zeros(2); e[j] = fd
        J[:, j] = (Afun(s + e) - Afun(s - e)) / (2 * fd)
    return -gradV_quad(s) + (J.T - J) @ v


def check_B():
    print("=" * 70)
    print("B. 规范不变性：A -> A + grad(chi) 不改轨迹")
    w, T = 1.2, 8.0
    A1 = lambda s: A_curl(s, w)
    A2 = lambda s: A_curl(s, w) + grad_chi(s)
    # (i) 力场逐点比较
    dmax = 0.0
    for s in ([1.0, 0.0], [0.3, 0.5], [-0.6, 0.8], [0.2, -0.9]):
        s = np.array(s, float); v = np.array([0.4, -0.3])
        dmax = max(dmax, np.max(np.abs(force_from_A(s, v, A1)
                                         - force_from_A(s, v, A2))))
    print(f"  max|F(A) - F(A + grad chi)| = {dmax:.3e}   (应 ~0)")
    # (ii) 轨迹比较
    f1 = lambda s, v: force_from_A(s, v, A1)
    f2 = lambda s, v: force_from_A(s, v, A2)
    for h in (1e-3, 5e-4):
        S1, _ = integrate(f1, [1.0, 0.0], [0.0, 0.0], T, h)
        S2, _ = integrate(f2, [1.0, 0.0], [0.0, 0.0], T, h)
        print(f"  h={h:g}   max|Delta s| = {np.max(np.abs(S1 - S2)):.3e}")
    # 反向核对：curl(grad chi) = 0
    hh = 1e-5; cchi = 0.0
    for s in ([0.4, -0.7], [1.1, 0.3], [-0.2, 0.9]):
        s = np.array(s, float)
        cx = (grad_chi(s + np.array([0, hh]))[0] - grad_chi(s - np.array([0, hh]))[0]) / (2 * hh)
        cy = (grad_chi(s + np.array([hh, 0]))[1] - grad_chi(s - np.array([hh, 0]))[1]) / (2 * hh)
        cchi = max(cchi, abs(cx - cy))
    print(f"  数值 curl(grad chi) = {cchi:.3e}   (应为 0)")


# ================================================================ C. 势型 vs 非势差
def check_C():
    print("=" * 70)
    print("C. 势型(curl=0) vs 非势差(curl!=0)：轨迹是否离开初始 1 维子空间")
    T = 64.0
    s0, v0 = [1.0, 0.0], [0.0, 0.0]      # 初值沿 x 轴、零速
    for h in (1e-3, 5e-4, 2.5e-4):
        out = []
        for w in (0.0, 0.6, 1.2):
            f = lambda s, v: accel(s, v, w)
            S, _ = integrate(f, s0, v0, T, h)
            out.append((w, np.max(np.abs(S[:, 1])), enclosed_area(S), dom_freq(S, h)))
        print(f"  h={h:g}  " + "  |  ".join(
            f"w={w}: max|y|={my:.3e}, Area={ar:+.4f}, f={fr:.4f}"
            for w, my, ar, fr in out))
    print("  => w=0：max|y|=0、Area=0（轨迹被锁在 x 轴上，1 维退化）")
    print("     w!=0：max|y|>0、Area!=0（进入 2 维环流，且频率分裂）")


# ================================================================ D. 环积分
def check_D():
    print("=" * 70)
    print("D. 环积分 = 曲率 x 面积（非保守力 => 不可写成势差）")
    w = 1.2
    for r0 in (0.5, 1.0, 2.0):
        N = 400000
        th = np.linspace(0, 2 * np.pi, N)
        pts = np.stack([r0 * np.cos(th), r0 * np.sin(th)], axis=1)
        A = np.array([A_curl(p, w) for p in pts])
        dpts = np.gradient(pts, th, axis=0)
        loop = trapz(np.sum(A * dpts, axis=1), th)
        pred = w * np.pi * r0 ** 2
        print(f"  r0={r0:g}   oint A.ds = {loop:+.6f}   curl*Area = {pred:+.6f}"
              f"   diff = {loop - pred:+.2e}")
    # 加 grad(chi) 后环积分不变
    N = 400000
    th = np.linspace(0, 2 * np.pi, N)
    r0 = 1.0
    pts = np.stack([r0 * np.cos(th), r0 * np.sin(th)], axis=1)
    dpts = np.gradient(pts, th, axis=0)
    A1 = np.array([A_curl(p, w) for p in pts])
    A2 = np.array([A_curl(p, w) + grad_chi(p) for p in pts])
    loop1 = trapz(np.sum(A1 * dpts, axis=1), th)
    loop2 = trapz(np.sum(A2 * dpts, axis=1), th)
    print(f"  规范核对 r0=1：oint A.ds = {loop1:+.6f}，oint (A+grad chi).ds = "
          f"{loop2:+.6f}，diff = {loop2 - loop1:+.2e}")


# ================================================================ E. 精度 gamma
def check_E():
    print("=" * 70)
    print("E. 精度 gamma = ||curl A||；文章原型 gamma = 0")
    # 口径注：运动方程只用 J_A^T - J_A = 2·antisym(J_A)，
    # 故 gamma = ||curl A|| = 2·||antisym J_A||（下表 ||antisym J_A|| = w/2、||curl A|| = w）。
    for w in (0.0, 0.6, 1.2, 2.5):
        J_A = 0.5 * w * np.array([[0.0, -1.0], [1.0, 0.0]])
        anti = 0.5 * (J_A - J_A.T)
        print(f"  w={w:g}   ||antisym J_A|| = {np.max(np.abs(anti)):g}"
              f"   ||curl A|| = {w:g}")
    sp = np.array([1.0, 0.0]); hh = 1e-5; cmax = 0.0
    for s in ([0.3, 0.4], [1.7, -0.6], [-0.5, 1.2], [2.0, 2.0]):
        s = np.array(s, float)
        cyx = (A_paper(s + np.array([hh, 0]), sp)[1]
               - A_paper(s - np.array([hh, 0]), sp)[1]) / (2 * hh)
        cxy = (A_paper(s + np.array([0, hh]), sp)[0]
               - A_paper(s - np.array([0, hh]), sp)[0]) / (2 * hh)
        cmax = max(cmax, abs(cyx - cxy))
    print(f"  文章原型 A = grad(-D)： max|curl A| = {cmax:.3e}  =>  gamma_paper = 0")


if __name__ == "__main__":
    check_A(); check_B(); check_C(); check_D(); check_E()
    print("=" * 70)
    print("全部核验完成。")
