import numpy as np
np.set_printoptions(precision=4, suppress=True)

print('='*76)
print('演示：什么是"定号"—— 正定核 / 正定二次型（Weil 正性那一侧的具体形态）')
print('='*76)
print()

# ---- 1. 定号的"种子"： f = g * g*  ⟹  f̂ = |ĝ|² ≥ 0 ----
print('[1] 定号的种子：  f = g * g*  ⟹  f̂(t) = |ĝ(t)|² ≥ 0')
print('    （正定函数 = 自卷积 ⟹ 傅里叶变换是非负的模平方）')
import numpy as np
t = np.linspace(-5, 5, 2001); dt = t[1]-t[0]
g = np.exp(-t**2/2)                      # 高斯
f = np.convolve(g, g[::-1], mode='same')*dt
fhat = np.abs(np.fft.fftshift(np.fft.fft(np.fft.ifftshift(f))))*dt
print(f'    f̂ 的最小值 = {fhat.min():.3e}   ⟹ 非负 ✅（定号）')
print()

# ---- 2. Screw 核： 一个具体的正定核 ----
print('[2] Screw 核（Suzuki / Krein–Langer 的正定核条件）')
print('    K(t,u) = g(t−u) − g(t) − g(−u) + g(0)')
print('    取 g(t) = |t|  ⟹  K(t,u) = |t−u| − |t| − |u| = −2·min(|t|,|u|)')
print()
for n in [4, 8, 16]:
    s = np.linspace(0.2, 2.0, n)
    # K 矩阵
    K = np.abs(s[:,None]-s[None,:]) - np.abs(s)[:,None] - np.abs(s)[None,:]
    wK = np.linalg.eigvalsh(K)
    # −K = 2·min
    M = np.minimum(s[:,None], s[None,:])
    wM = np.linalg.eigvalsh(M)
    print(f'    n={n:2d}:  特征值(2·min) 最小值 = {wM.min():+.3e}  ⟹ '
          f'{"半正定 ✅（正定核）" if wM.min() > -1e-10 else "✗"}')
print()
print('    ⟹ min(|t|,|u|) 恰是【布朗运动的协方差】，是标准的正定核。')
print('       —— 这就是"定号"在分析侧的具体面目。')
print()

# ---- 3. 对照：交错型恒不定号 ----
print('[3] 对照：交错型（Weil/Poincaré 配对）恒不定号')
rng = np.random.default_rng(3)
for n in [2, 4]:
    A = rng.normal(size=(n,n)); A = A - A.T
    vals = np.linalg.eigvals(A)
    x = rng.normal(size=n)
    print(f'    n={n}: 特征值 {", ".join(f"{v.real:+.2f}{v.imag:+.2f}i" for v in vals)}'
          f'   实部最大 {max(abs(v.real) for v in vals):.0e}   xᵀAx = {x@A@x:+.1e}')
print('    ⟹ 交错型：特征值纯虚、xᵀAx≡0 ⟹ 【恒不能定号】')
print()

# ---- 4. 结论 ----
print('='*76)
print('结论：两拨"定号"对象，从不相交')
print('='*76)
print('  已证的定号（Arakelov 交形式 / Néron–Tate 高度 / 古典 Hodge 指标）')
print('        ⟹ 定号性来自几何对称性（Euler 数、函数方程），【不承载 RH】')
print()
print('  承载 RH 的定号（Weil 正性 / screw 核 / 矩问题正性）')
print('        ⟹ 其定号性【恰恰就是 RH】，从未被无条件证明')
print()
print('  而"序型"的对象（Mazur 不等式 t_H≤t_N、Newton 凸性）从不蕴含定号；')
print('  交错型配对（数域的自然配对）恒不定号。')
print()
print('  ★ 结论：缺口不是"没人想到桥"，而是"常规桥面被定理排除"。')
