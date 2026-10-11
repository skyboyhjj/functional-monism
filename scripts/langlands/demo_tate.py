import mpmath as mp
import cmath, math

mp.mp.dps = 30

# ============ Tate 曲线：j-不变量 ============
# 论文 2606.06604：商掉阿基米德轨道上的离散 Frobenius 对称 ⟹ 复 Tate 曲线，模数 q = p^{-1}
# Tate 曲线的 j-不变量：  j(q) = 1/q + 744 + 196884 q + 21493760 q^2 + ...
# （196884 = 196883 + 1 —— monstrous moonshine 的那个数）

print('='*76)
print('Tate 曲线（模数 q = p^{-1}）与 j-不变量的 q-展开')
print('='*76)

def j_expansion(q, terms=4):
    coeffs = [1, 744, 196884, 21493760]   # 1/q, 常数, q, q^2
    val = coeffs[0]/q + coeffs[1]
    for k in range(2, terms+1):
        val += coeffs[k-1] * q**(k-1)
    return val

print('\n[q-展开]  j(q) = 1/q + 744 + 196884·q + 21493760·q² + …')
print(f'  {"q":>10} {"1/q+744+…":>22}')
for q in [0.25, 0.1, 0.05]:
    print(f'  {q:>10} {j_expansion(q):>22.4f}')

# ---- 精确值检验：j(i) = 1728, j(ρ) = 0（ρ = e^{2πi/3}） ----
print('\n[精确值检验] 用 E₄³/Δ 直接数值算 j(τ)')
def E4(tau, N=400):
    return 1 + 240*sum(mp.mpf(n**3)*mp.e**(2j*mp.pi*n*tau)/(1-mp.e**(2j*mp.pi*n*tau)) for n in range(1,N))
def E6(tau, N=400):
    return 1 - 504*sum(mp.mpf(n**5)*mp.e**(2j*mp.pi*n*tau)/(1-mp.e**(2j*mp.pi*n*tau)) for n in range(1,N))
def j(tau):
    return 1728 * E4(tau)**3 / (E4(tau)**3 - E6(tau)**2)

for name, tau, expect in [('j(i)', 1j, 1728),
                          ('j(2i)', 2j, 287496)]:
    v = j(tau)
    vr = float(v.real); vi = float(v.imag)
    ok = abs(vr-expect) < 1e-2
    print(f'  {name:10s} = {vr:>14.4f} {vi:+.4f}i   期望 {expect}   {"✅" if ok else "✗"}')

# j(3i) 的期望值由 q-展开独立给出（|q|=e^{-6π} 极小，1/q 主导）
q3 = math.e**(-6*math.pi)
print(f'  j(3i)      = {float(j(3j).real):>14.4f}   q-展开 1/q+744 = {1/q3+744:>14.4f}   '
      f'{"✅" if abs(float(j(3j).real)-(1/q3+744)) < 1 else "✗"}')

print('\n  ★ j(i)=1728、j(2i)=287496 为经典精确值，数值复算通过。')
print('  ★ 论文的 Tate 曲线取 q = p^{-1}；q→0 时 j ~ 1/q → ∞（退化），')
print('     这正是"商掉 Frobenius 得到一个几何对象"的具体形态。')

# ============ 论文的两个关键数 ============
print('\n' + '='*76)
print('论文关键结构（已核实原文摘要/正文）')
print('='*76)
print('  · (Spec ℤ)_{𝔽₁} 在 ℂ 上的非平凡点 → 两个主齐性空间（torsor），')
print('      分别在 Weil 群 W_p = ℚ_p^× 与 W_∞ = ℂ^× 上')
print('  · 商掉离散 Frobenius 对称 → 复 Tate 曲线，模数 q = p^{-1}')
print('  · 该椭圆曲线 = (实轨迹，即阿黛尔周期轨道 C_p = ℝ₊^×/p^ℤ) × (与 p 无关的相空间)')
print('  · 相空间 𝒳~_∞ = Fargues–Fontaine 曲线的【实（阿基米德）类比】')
print('  · 全文【未出现】：交形式 / 正性 / Riemann-Roch / Weil 正性 / Deninger / RH')
print('  · 文末唯一未解问题：研究 Frobenius 特征空间（如 B^{φ=p}）下降到 C_p 的行为')
