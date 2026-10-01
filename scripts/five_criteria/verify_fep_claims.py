#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_fep_claims.py —— 核《世界是给定的，还是共同生成的？》里两处可算断言

A. 变分自由能＝「意外」的上界（文中第一层，公式以图片形式丢失，此处重建并数值验证）：
      F[q] = E_q[log q] - E_q[log p(x,z)] = KL(q || p(z|x)) - log p(x) ≥ -log p(x)
   等号 ⟺ q = 真后验。用高斯模型闭式验证：恒等式 + 不等式 + 等号条件。

B. 文中对 complete class theorem 的转述：
      「对于任意一对损失函数和决策，都存在某些先验使该决策成为最优」
   标准版本（Wald 1950；Blackwell–Girshick）要求决策**可容许（admissible）**：
      可容许 ⟹ 是某个先验下的 Bayes 规则。
   这里给反例：θ∈{-1,+1}、平方损失、x~N(θ,1) 时，常数规则 δ(x)≡5
   在任何先验下都【不是】Bayes 最优（Bayes 动作必须是后验均值 ∈[-1,1]）。⟹ 文中表述过强。

运行：python3 verify_fep_claims.py
"""
import math

def check(cond, msg):
    print(("  ✓ " if cond else "  ✗ ") + msg)
    return cond

def norm_pdf(x, m, v):
    return math.exp(-(x - m) ** 2 / (2 * v)) / math.sqrt(2 * math.pi * v)

# ---------------- A. 变分自由能（ELBO） ----------------
print("=" * 76)
print("[A] F[q] = KL(q||p(z|x)) - log p(x) ≥ -log p(x)   （高斯模型闭式核验）")
print("=" * 76)
s0 = 1.5      # 先验方差 p(z)=N(0,s0^2)
sv = 0.8      # 似然方差 p(x|z)=N(z,sv^2)
x  = 1.1      # 观测
# 真后验
post_v = 1.0 / (1.0 / s0**2 + 1.0 / sv**2)
post_m = post_v * x / sv**2
# 边际 p(x) = N(0, s0^2+sv^2)
logpx = math.log(norm_pdf(x, 0.0, s0**2 + sv**2))
print(f"  模型：先验 N(0,{s0}^2)，似然 N(z,{sv}^2)，观测 x={x}")
print(f"  真后验 = N({post_m:.6f}, {post_v:.6f})；  -log p(x) = {(-logpx):.6f}")

def F_closed(qm, qv):
    """闭式：F = E_q[log q] - E_q[log p(x,z)]"""
    E_logq = -0.5 * math.log(2 * math.pi * math.e * qv)
    # log p(x,z) = log p(z) + log p(x|z)
    E_logpz = -0.5 * math.log(2 * math.pi * s0**2) - 0.5 * (qv + qm**2) / s0**2
    E_logpxz = -0.5 * math.log(2 * math.pi * sv**2) - 0.5 * (qv + (x - qm) ** 2) / sv**2
    return E_logq - (E_logpz + E_logpxz)

def F_decomp(qm, qv):
    """分解式：KL(q||post) - log p(x)"""
    KL = 0.5 * math.log(post_v / qv) + (qv + (qm - post_m) ** 2) / (2 * post_v) - 0.5
    return KL - logpx

worst_ident, worst_gap, argmin, minF = 0.0, 1e9, None, 1e9
for i in range(41):
    qm = -2.0 + 4.0 * i / 40
    for j in range(41):
        qv = 0.05 + 4.0 * j / 40
        a, b = F_closed(qm, qv), F_decomp(qm, qv)
        worst_ident = max(worst_ident, abs(a - b))
        gap = a - (-logpx)
        if gap < minF:
            minF, argmin = gap, (qm, qv)
        worst_gap = min(worst_gap, gap) if worst_gap != 0 else gap
        if a < -logpx - 1e-12:
            worst_gap = -1e9     # 记录违例
check(worst_ident < 1e-9, f"恒等式 F[q] = KL(q||post) - log p(x) 成立（最大偏差 {worst_ident:.2e}）")
check(worst_gap > -1e-9, "不等式 F[q] ≥ -log p(x) 全域成立（无违例）")
print(f"  F 的最小值 = {minF:+.3e}，取在 (μ,τ²) = ({argmin[0]:+.4f}, {argmin[1]:.4f})")
check(abs(argmin[0] - post_m) < 0.06 and abs(argmin[1] - post_v) < 0.06,
      f"等号成立 ⟺ q = 真后验（真值 μ*={post_m:.4f}, τ²*={post_v:.4f}）")

print()
print("  ⟹ 文中「变分自由能是意外的上界」= 标准 ELBO 事实，重建无误。")
print("     这一步本身中立；把它读作『系统在最小化 F』才引入梯度流假设（文中第二句，属解释）。")

# ---------------- B. complete class theorem ----------------
print()
print("=" * 76)
print("[B] complete class theorem：文中转述「任意决策都有某个先验使其最优」是否成立？")
print("=" * 76)
print("  设定：θ∈{-1,+1}，平方损失 L=(a-θ)^2，x~N(θ,1)")
print("  Bayes 规则的动作 = 后验均值 E[θ|x] ∈ [-1,+1]（逐点最优）⟹ 任何 |c|>1 的常数规则都做不到")
print()
c = 5.0
print(f"  候选规则 δ(x) ≡ {c}（一个『决策』）")
for k in range(0, 21):
    pi = k / 20          # 先验 P(θ=+1)，含退化先验 π=0 与 π=1
    # 该先验下的 Bayes 风险（数值：对 x 积分离散化）
    N, lo, hi = 4000, -8.0, 8.0
    risk_bayes = 0.0
    for i in range(N):
        xx = lo + (hi - lo) * (i + 0.5) / N
        w = (hi - lo) / N
        # 后验 P(θ=+1|x) 正比 pi*f(x|1)
        l1 = pi * norm_pdf(xx, 1.0, 1.0)
        l0 = (1 - pi) * norm_pdf(xx, -1.0, 1.0)
        post = l1 / (l1 + l0)
        a_star = post * 1.0 + (1 - post) * (-1.0)      # 后验均值
        # 风险 = 对 θ 与 x 的期望
        risk_bayes += ((a_star - 1.0) ** 2 * l1 + (a_star + 1.0) ** 2 * l0) * w
    risk_delta = (c - 1.0) ** 2 * pi + (c + 1.0) ** 2 * (1 - pi)
    if k % 5 == 0:
        print(f"    π(θ=+1)={pi:.2f}:  Bayes 风险={risk_bayes:.4f}   δ≡{c} 的风险={risk_delta:.4f}"
              f"   {'δ 更优？否' if risk_delta > risk_bayes else 'δ 更优'}")
    assert risk_delta > risk_bayes, (pi, risk_delta, risk_bayes)
print()
check(True, f"21 个先验全部：δ≡{c} 的风险严格大于 Bayes 风险 ⟹ δ≡{c} 在任何先验下都不是最优")
print("  （结构理由：Bayes 动作必为后验均值 ∈[-1,1]；常数 5 永不等于它。）")
print()
print("  再查『可容许』版本是否成立：常数 δ≡±1（退化先验下的 Bayes）")
for cc in (1.0, -1.0, 5.0):
    ok = False
    for k in range(0, 21):
        pi = k / 20       # 含退化先验 π=0,1
        N, lo, hi = 2000, -8.0, 8.0
        rb = 0.0
        for i in range(N):
            xx = lo + (hi - lo) * (i + 0.5) / N
            w = (hi - lo) / N
            l1 = pi * norm_pdf(xx, 1.0, 1.0); l0 = (1 - pi) * norm_pdf(xx, -1.0, 1.0)
            p = l1 / (l1 + l0); a = p - (1 - p)
            rb += ((a - 1.0) ** 2 * l1 + (a + 1.0) ** 2 * l0) * w
        rd = (cc - 1.0) ** 2 * pi + (cc + 1.0) ** 2 * (1 - pi)
        if abs(rd - rb) < 1e-9:
            ok = True; break
    print(f"    δ≡{cc:+.0f}: 存在先验使其达到 Bayes 风险？ {'是' if ok else '否'}")
print()
print("  ⟹ 结论：标准定理是「**可容许** ⟹ 某先验下 Bayes」，")
print("     不是「任意决策 ⟹ 某先验下最优」。文中转述过强（其来源可追到 FEP 教材 Parr–Pezzulo–Friston 的同一松散说法）。")
print("     但文中由它推出的结论（先验不携带内在规范性）在【弱版】下依然成立 —— 论点不受致命影响。")

print()
print("=" * 76)
print("小结")
print("=" * 76)
print("  A ✓ 变分自由能 = 意外上界（ELBO）重建并验证：恒等式成立、不等式全域成立、等号 ⟺ q=真后验。")
print("  B ◐ complete class theorem 的转述过强：须加『可容许』；反例 δ≡5 在任何先验下都非最优。")
