#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_shaping_vs_five_criteria.py

自查（矛盾迭代引擎·步 4「主动找反例」）：
  v1.1 稿断言：「势整形定理 = 第五条（动力学标准）的严格负判据」。

两问：
  A 策略层：势整形是否改变最优策略？          期望：不变（Ng et al. 1999）
  B 动力学层：把势整形写进动力学（梯度流）后，
             吸引子结构 / 分岔是否发生定性变化？ 期望：会（=> 第五条可能亮）
裁决：该断言是否成立。
"""
import numpy as np

np.set_printoptions(precision=4, suppress=True)

# ---------------------------------------------------------------- A 策略层
print("=" * 68)
print("A · 策略层：链式 MDP 值迭代（复现项目 verify_reward.py 的结论）")
print("=" * 68)

N = 5
GAMMA = 1.0
R_EXT = np.array([0.0, 0.0, 0.0, 0.0, 1.0])      # 右端奖励
PHI = np.array([0.0, 0.1, 0.2, 0.3, 0.5])         # 势函数


def s2_of(s, a, n=N):
    return min(max(s + a, 0), n - 1)


def solve(r_ext, phi, shaped, gamma=GAMMA, n=N, iters=5000):
    def R(s, a):
        s2 = s2_of(s, a, n)
        base = r_ext[s2]
        if shaped:
            base += gamma * phi[s2] - phi[s]
        return base
    V = np.zeros(n)
    for _ in range(iters):
        Vn = V.copy()
        for s in range(n):
            Vn[s] = max(R(s, a) + gamma * V[s2_of(s, a, n)] for a in (-1, 1))
        if np.allclose(Vn, V, atol=1e-12):
            V = Vn
            break
        V = Vn
    pol = []
    for s in range(n):
        vals = {a: R(s, a) + gamma * V[s2_of(s, a, n)] for a in (-1, 1)}
        pol.append(+1 if vals[1] > vals[-1] + 1e-12 else -1)
    return V, pol


V0, p0 = solve(R_EXT, PHI, shaped=False)
V1, p1 = solve(R_EXT, PHI, shaped=True)
print("最优策略（原始）   :", p0)
print("最优策略（势整形） :", p1)
print("策略是否相同       :", p0 == p1)
print("价值 V 是否相同    :", np.allclose(V0, V1), " (max|ΔV|=%.4f)" % np.max(np.abs(V1 - V0)))

# ---------------------------------------------------------------- B 动力学层
print()
print("=" * 68)
print("B · 动力学层：把势整形写进梯度流 ẋ=-∇(F+Φ)，看吸引子/分岔")
print("=" * 68)
print("取 F(x)=x⁴/4 - x²/2（双井：极小 ±1，极大 0）；势整形 Φ(x)=c·x")
print("梯度流：ẋ = -(x³ - x + c)；不动点 = x³ - x + c 的实根；")
print("稳定性 = 该点处 G''(x)=3x²-1 的符号（>0 稳定）")
print()
print("  c      不动点(实根)                         个数  稳定点      结构")
c_star = 2.0 / (3.0 * np.sqrt(3.0))
for c in [0.0, 0.1, 0.2, 0.38, 0.40, 0.60]:
    roots = np.roots([1.0, 0.0, -1.0, c])
    reals = sorted([r.real for r in roots if abs(r.imag) < 1e-9])
    stable = [x for x in reals if 3 * x * x - 1 > 0]
    if len(reals) == 3:
        struct = "双井(3 不动点)"
    elif len(reals) == 1:
        struct = "单井(1 不动点) <- 分岔"
    else:
        struct = "?"
    print("  %-5.2f  %-38s %d     %-12s %s" % (
        c, np.array2string(np.array(reals), precision=4), len(reals),
        np.array2string(np.array(stable), precision=3), struct))

print()
print("临界 c* = 2/(3√3) ≈ %.4f：c < c* 有 3 个不动点（但位置已移动）；" % c_star)
print("                          c > c* 只剩 1 个（鞍结分岔，结构定性改变）。")
print()
print("=" * 68)
print("裁决")
print("=" * 68)
print("A 策略层 : 势整形 --- 最优策略不变（严格，与定理一致）")
print("B 动力学层: 把 Φ 写进流后 ---")
print("    · 不动点位置随 c 连续移动（c=0.1,0.2: −1,0,1 → 已移位）")
print("    · c 超过 c* 后不动点由 3 变 1（鞍结分岔 = 定性改变）")
print("  ⟹ 「势整形不改变动力学定性」为假：它改的是【景观/吸引子】。")
print("  ⟹ 势整形定理给出的是【策略层】不变，不是【第五条·动力学标准】的不变。")
print("  ⟹ v1.1 稿把定理当第五条的严格负判据 = 层次混淆（方向亦反）。")
