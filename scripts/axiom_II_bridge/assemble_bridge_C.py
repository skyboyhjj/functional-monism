#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
assemble_bridge_C.py
====================
公理 II 的桥：内感受（幅度/势差型）× 五行（相位/矢势型） = C 系统。

核心命题（本步最有价值的一条）：
    对 2D 线性场 M x ：
        curl(Mx) = 0  <=>  M 对称  <=> 势差型 = 纯幅度（梯度流/伸缩）
        curl(Mx) != 0 <=>  M 反对称 <=> 矢势型 = 旋转/相位
    => 公理 II 的桥（相位 <-> 幅度）就是「矢势项 <-> 势差项」的桥。

五组核验：
  1. 2x2 分解定理：M = S(对称) + A(反对称)；curl(Mx) = -2 A12
  2. 生成元：反对称 exp 旋转（保长）；对称 exp 伸缩（变长）
  3. 三态对照：单相位（守恒）/ 单幅度（衰减到死）/ 组装（极限环）
  4. 组装不免费：线性组装（螺旋入 0）不够；须非线性饱和
  5. Z5（五行）等变耦合把相位钉到 72 度倍数
"""
import numpy as np
from scipy.linalg import expm


def rk4_c(f, z0, T, h):
    n = int(round(T / h))
    z = complex(z0)
    for _ in range(n):
        k1 = f(z)
        k2 = f(z + .5 * h * k1)
        k3 = f(z + .5 * h * k2)
        k4 = f(z + h * k3)
        z = z + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return z


# ================================================================ 1 分解定理
def check1():
    print("=" * 72)
    print("1. 2x2 分解定理：M = S(对称,势差型) + A(反对称,矢势型)")
    M = np.array([[0.4, -1.3], [0.7, -0.2]])
    S = 0.5 * (M + M.T)
    A = 0.5 * (M - M.T)
    print(f"  ||S|| = {np.max(np.abs(S)):.4f}  (势差型/幅度)"
          f"   ||A|| = {np.max(np.abs(A)):.4f}  (矢势型/相位)")
    curl = M[1, 0] - M[0, 1]
    print(f"  curl(Mx) = {curl:.4f}  = -2*A12 = {-2 * A[0, 1]:.4f}   OK")
    print("  => curl=0 <=> 对称(幅度);  curl!=0 <=> 反对称(相位)")


# ================================================================ 2 生成元
def check2():
    print("=" * 72)
    print("2. 反对称 = 旋转生成元(保长); 对称 = 伸缩生成元(变长)")
    J = np.array([[0, -1], [1, 0]])          # 反对称
    Sd = np.array([[1.0, 0], [0, -1]])       # 无迹对称
    v = np.array([1.0, 0.6])
    for th in (0.5, 1.5, 3.0):
        R = expm(th * J)
        print(f"  th={th:<4} ||exp(thJ)v|| = {np.linalg.norm(R @ v):.6f}"
              f"  (守恒)   det = {np.linalg.det(R):.6f}")
    for th in (0.5, 1.5, 3.0):
        E = expm(th * Sd)
        print(f"  th={th:<4} ||exp(thS)v|| = {np.linalg.norm(E @ v):.6f}"
              f"  (伸缩，不守恒)")


# ================================================================ 3 三态
def check3():
    print("=" * 72)
    print("3. 三态对照（z in C）：五行(相位) / 内感受(幅度) / 组装")
    mu, l, w = 1.0, 1.0, 1.0
    z0, T, h = 0.3 + 0j, 60.0, 1e-3
    zP = rk4_c(lambda z: 1j * w * z, z0, T, h)                     # 五行：纯相位
    zA = rk4_c(lambda z: mu * z - l * abs(z) ** 2 * z, z0, T, h)   # 内感受：纯幅度
    zB = rk4_c(lambda z: (mu + 1j * w) * z - l * abs(z) ** 2 * z, z0, T, h)
    rstar = np.sqrt(mu / l)
    print(f"  单相位(五行)   |z(T)| = {abs(zP):.6f}  arg = {np.degrees(np.angle(zP)) % 360:.1f} 度  (守恒；只转)")
    print(f"  单幅度(内感受) |z(T)| = {abs(zA):.6f}  arg = {np.degrees(np.angle(zA)):.1f} 度  (定点，静止)")
    print(f"  组装           |z(T)| = {abs(zB):.6f}  arg = {np.degrees(np.angle(zB)) % 360:.1f} 度  (极限环 r*={rstar:.4f})")
    print("  => 单幅度给静止稳态；单相位给幅度不定的纯转；组装才有『活的节律』")


# ================================================================ 4 不免费
def check4():
    print("=" * 72)
    print("4. 组装不免费：线性不够(螺旋入0)，须非线性饱和")
    mu, l, w = 1.0, 2.0, 1.0
    z0, T, h = 1.0 + 0j, 60.0, 1e-3
    zL = rk4_c(lambda z: (mu + 1j * w - l) * z, z0, T, h)              # 线性组装
    zN = rk4_c(lambda z: (mu + 1j * w) * z - l * abs(z) ** 2 * z, z0, T, h)
    print(f"  线性组装 (mu+iw-l)z   |z(T)| = {abs(zL):.3e}   (螺旋入 0)")
    print(f"  非线性组装            |z(T)| = {abs(zN):.6f}   (极限环 r*={np.sqrt(mu / l):.4f})")


# ================================================================ 5 Z5 钉相
def check5():
    print("=" * 72)
    print("5. Z5（五行）等变耦合 kappa*zbar^4 把相位钉到 72 度倍数")
    mu, om, ka, ga = 1.0, 0.5, 2.0, 1.0
    f = lambda z: ((mu + 1j * om) * z - abs(z) ** 2 * z
                   + ka * np.conj(z) ** 4 - ga * abs(z) ** 4 * z)
    for z0 in (1.2 + 0.1j, 1.5 - 0.7j, 0.9 + 0.4j):
        z = rk4_c(f, z0, 120.0, 2e-4)
        th = np.degrees(np.angle(z)) % 72
        print(f"  z0={z0}  ->  r = {abs(z):.4f},  相位 mod 72 = {th:.3f} 度")
    print("  => 幅度(内感受)把相位(五行)钉到 5 个离散值（Z5 锁相）")


if __name__ == "__main__":
    check1(); check2(); check3(); check4(); check5()
    print("=" * 72)
    print("完成。")
