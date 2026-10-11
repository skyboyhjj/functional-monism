import numpy as np

print('='*76)
print('演示 A：Newton 多边形 vs Hodge 多边形（弱可容许不等式 t_H ≤ t_N）')
print('='*76)
print()
print('  φ-模的斜率 λ_i（递增） ⟹ Newton 折线 t_N(i) = λ_1+…+λ_i（下凸包）')
print('  Hodge–Tate 权 h_i（递增） ⟹ Hodge 折线 t_H(i) = h_1+…+h_i')
print('  弱可容许（Mazur）：  t_H(i) ≤ t_N(i)  ∀i，端点相等')
print()

def poly(vals):
    out=[0]
    for x in vals: out.append(out[-1]+x)
    return out

cases = [
    ('椭圆曲线 · 好约化 · ordinary',      [0,1],     [0,1]),
    ('椭圆曲线 · 好约化 · supersingular', [0,1],     [0.5,0.5]),
    ('椭圆曲线 · 坏约化 · 乘法(tame)',     [0,1],     [0.5,0.5]),
]
for name, ht, nw in cases:
    tH = poly(sorted(ht)); tN = poly(sorted(nw))
    ok = all(a <= b+1e-12 for a,b in zip(tH,tN)) and abs(tH[-1]-tN[-1])<1e-12
    print(f'  {name}')
    print(f'     HT 权 {sorted(ht)}  ⟹ t_H = {tH}')
    print(f'     斜率   {sorted(nw)}  ⟹ t_N = {tN}')
    print(f'     t_H ≤ t_N 且端点相等 ? {"✅ 弱可容许条件成立" if ok else "✗"}')
    print()

print('  要点：')
print('   · supersingular：t_H=(0,0,1) 严格落在 t_N=(0,1/2,1) 之下 ⟹ 中间有"空隙"')
print('   · 这个不等式是【逐点比较】——是"序"，不是二次型的定号。')

print()
print('='*76)
print('演示 B：交错型（skew-symmetric）不可能"正定"')
print('='*76)
print()
print('  Weil 配对 / Poincaré 配对是交错的（反对称）。')
print('  一个实交错型 A（Aᵀ = −A）的特征值恒为【纯虚】±iλ：')
print()
for n in [2,4]:
    rng = np.random.default_rng(7)
    M = rng.normal(size=(n,n))
    A = M - M.T                      # 反对称
    w = np.linalg.eigvals(A)
    print(f'  n={n}: 特征值 = ' + ', '.join(f'{v.real:+.3f}{v.imag:+.3f}i' for v in w))
    print(f'        实部最大值 = {max(abs(v.real) for v in w):.2e}  ⟹ 特征值纯虚 ⟹ 无实特征值')
print()
print('  ⟹ 「xᵀAx > 0 ∀x≠0」（正定）对交错型【恒不成立】（因为 xᵀAx ≡ 0）。')
print('     这正是"数域一侧的正性"为什么难：')
print('     函数域的"交形式"是【对称型】（可正定）；')
print('     而数域的 Poincaré/Weil 配对是【交错型】（恒不定号）。')
print()
# 直接验证 x^T A x = 0
A = np.array([[0,1],[-1,0]], dtype=float)
x = np.array([1.0,2.0])
print(f'  例：A=[[0,1],[-1,0]], x=(1,2):  xᵀAx = {x@A@x:.1f}  （恒为 0）')
print()
print('='*76)
print('结论')
print('='*76)
print('  • B^{φ=p} 一线上的"正性" = 斜率/凸性/序（ℚ_p 值域，不可序）⟹ 结构上产生不了"定号"')
print('  • 自然配对是交错型 ⟹ 恒不定号')
print('  • ⟹ 它不是缺掉的那一半，只是"序那一半"的候选载体')
