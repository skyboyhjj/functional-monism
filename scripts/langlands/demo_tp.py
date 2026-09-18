import numpy as np
import mpmath as mp
np.set_printoptions(precision=4, suppress=True)

print('='*76)
print('演示：路 (b) 的唯一现成线索 —— 「凸性/序 ⟹ 正定」在特殊情形【确实是定理】')
print('='*76)
print()

# ---- 1. 全正性：Toeplitz 核的所有子式 ≥ 0 ----
print('[1] 全正性（total positivity）：所有子式 ≥ 0')
print('    PF 函数 Λ  ⟹  Toeplitz 核 T_Λ = (Λ(i−j)) 全正')
print('    取 Λ(x) = exp(−x²)（高斯，经典 PF 函数）')
print()

def all_minors_nonneg(A, maxk=None):
    from itertools import combinations
    n = A.shape[0]; maxk = maxk or n
    worst = float('inf')
    for k in range(1, maxk+1):
        for r in combinations(range(n), k):
            for c in combinations(range(n), k):
                d = np.linalg.det(A[np.ix_(r,c)])
                worst = min(worst, d)
    return worst

for n in [4, 6]:
    idx = np.arange(n)
    T = np.exp(-(idx[:,None]-idx[None,:])**2)
    w = all_minors_nonneg(T, maxk=min(n,4))
    print(f'    n={n}: 所有 ≤4 阶子式的最小值 = {w:.3e}   {"✅ 全正" if w > -1e-10 else "✗"}')

print()
print('[2] Pólya 定理：φ 偶、递减、凸  ⟹  φ̂ ≥ 0（正定核）')
print('    —— 这是"凸性 ⟹ 正定"在分析侧的【一条真定理】')
print()
for name, phi in [('exp(−x²)（高斯）',  lambda x: np.exp(-x**2)),
                  ('exp(−|x|)（指数）', lambda x: np.exp(-np.abs(x))),
                  ('1/(1+x²)（Cauchy）', lambda x: 1/(1+x**2))]:
    x = np.linspace(-40, 40, 8193); dx = x[1]-x[0]
    f = phi(x)
    # 数值傅里叶变换（应 ≥ 0）
    F = np.real(np.fft.fftshift(np.fft.fft(np.fft.ifftshift(f)))) * dx
    print(f'    {name:20s}  min φ̂ = {F.min():+.3e}   {"✅ ≥0（正定）" if F.min() > -1e-3 else "✗"}')
print()
print('    ⟹ 在这些情形里，"凸性/单调序" 确实【蕴含】了正定。')
print('       但注意：这是【实轴上的标量函数】情形。')

print()
print('[3] ★ 但它到不了算术情形 —— 三处断裂')
print('    ① 定义域：Pólya/全正性活在【实轴上】；B^{φ=p} 活在 ℚ_p（不可序）')
print('    ② 对象：这里是【标量函数的核】；数域要的是【Weil 二次型在 adele 类的空间上】')
print('    ③ 定理：Serre/Deninger 已证"实系数 Weil 上同调不存在"，切断了上同调式迁移')
print()
print('='*76)
print('结论')
print('='*76)
print('  • 「序 ⟹ 定号」不是空想 —— 在【实轴标量】情形有真定理（Pólya / PF / 全正性）')
print('  • 但从"实轴标量核"到"数域上的 Weil 二次型"，中间三处断裂')
print('  • ⟹ 路 (b) 不是"无机制"，而是"机制存在但迁移不过去"')
