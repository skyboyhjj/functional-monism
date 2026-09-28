#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""探索"局部 ⇏ 整体"的精确性质：
   究竟是【信息不足】，还是【装配方式缺失】？
   核验两条：(A) 有限域：零点可直接读出（装配是自动的）；
             (B) 数域：Newton 恒等式所需的幂和 Σγ^{2n} 随 n 爆炸（无限维）。"""
import mpmath as mp
mp.mp.dps = 25

def hdr(s): print("=" * 74); print(s); print("=" * 74)

# ---------------------------------------------------------------- A 有限域
hdr("A  有限域侧：装配是【自动】的 —— 零点直接从局部数据读出")
for (p, a) in [(101, -2), (1009, -30)]:
    # P(T) = 1 - a T + p T^2
    roots = mp.polyroots([p, -a, 1])          # 注意 polyroots 按升幂/降幂需确认
    r = sorted(roots, key=lambda z: abs(z))
    print(f"  p={p:>5}, a_p={a:>4}:  P(T) = 1 − ({a})T + {p}T²")
    for z in r:
        print(f"      根 T = {mp.nstr(z, 8)}   |T| = {mp.nstr(abs(z), 8)}   1/√p = {mp.nstr(p**-0.5, 8)}")
    print(f"      检查 |T| = 1/√p ? {mp.nstr(abs(r[0]), 6)} vs {mp.nstr(p**-0.5, 6)}")
print("  ⟹ 零点 = 一个【次数固定】的多项式的根：有限、可直接写出、可代数求解 ✓")
print("     局部数据(a_p) ⟹ 整体(零点) 这一步【不需要额外构造】")

# ---------------------------------------------------------------- B 数域
hdr("B  数域侧：Newton 恒等式所需的幂和 —— 看它是否收敛")
N = 300
print(f"  取 Riemann ζ 的前 {N} 个零点 γ_k（mpmath 实算）…")
gam = [mp.zetazero(k).imag for k in range(1, N + 1)]
print(f"  γ_1 = {mp.nstr(gam[0], 8)},  γ_{N} = {mp.nstr(gam[-1], 8)}")
print()
print("  幂和  S_{2n} = Σ γ^{2n}：")
for n in [1, 2, 3, 4]:
    S = sum(g ** (2 * n) for g in gam)
    print(f"    n={n}:  S_2n = {mp.nstr(S, 6)}")
print()
print("  关键：零点均匀分布（密度 dN/dT ~ log T / 2π），故整体幂和")
print("        Σ_γ γ^{2n}  ~  ∫_0^∞ T^{2n} · (log T / 2π) dT   →  【发散】")
print()
print("  而 Newton 恒等式要把 ζ 的零点当作某个'特征多项式的根'：")
print("        e_k = (1/k!) · det[...]  ← 需要 S_1, S_2, …, S_k 全部【有限】")
print("  ⟹ S_{2n} 发散 ⇒ Newton 恒等式【无法启动】⇒ 不存在有限次的特征多项式")
print("  ⟹ 必须换成一个【无限维】的对象（算子/流/圆作用）来承载这些零点")

hdr("C  结论：断点的性质究竟是什么？")
print("  ✗ 不是'信息不足'：收敛域内的值【唯一确定】解析延拓（若延拓存在）")
print("       —— 信息在理论上不缺，况且两边都是可数无穷。")
print("  ✓ 是【装配方式缺失】：")
print("       · 有限域：局部因子自动装配成一个【有限多项式】(有理函数)")
print("       · 数域  ：局部因子只能装配成一个【无穷 Euler 积】，")
print("                 而它整体上【没有一个有限对象】可承载零点位置")
print("  ✓ 所以真正的断点是：'把局部装配成整体'的那一步，")
print("     在数域需要一个【新的整体层对象】—— 而它至今没有被造出来。")
print()
print("  ⟹ 三条'整体层'路线恰是三种装配方案：")
print("      Deninger : 装配成 Frobenius 流 Θ 的正则化行列式 det_reg(s−Θ)")
print("      Connes   : 装配成 adele class space 的 scaling 算子（迹公式）")
print("      Hesselholt: 装配成 THH 的 S¹-作用之 Tate 构造（TP）")
print("    三者的共同点：用【一个整体作用】替代【无穷多个局部 Frobenius】。")
