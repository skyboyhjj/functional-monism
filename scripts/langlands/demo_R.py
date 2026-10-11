import numpy as np
import mpmath as mp
np.set_printoptions(precision=5, suppress=True)
mp.mp.dps = 20

# ============================================================
# R：在 GL₁ 上构造一个"用 t = log[·]"的自伴算子，查其谱是否含 ζ 零点
# ============================================================
# 设计（自我说明）：
#   账 B（算术侧）：素数测度  μ(t) = Σ_{n≥2} Λ(n)/n^{1/2} · δ(t − log n)
#                   —— 它的"自变量"正是乘法变量 t = log（这就是 t = log[ε] 的同胞）
#   显式公式说的就是：μ 的"谱"（傅里叶侧）落在 ζ 的零点上
#   ⟹ 构造 μ 的【自相关核】 C(s) = Σ_{m,n} Λ(m)Λ(n)/√(mn) · K(s − log(m/n))
#      —— 这是一个【对称（自伴）核】，其谱密度应在 γ_n 处出现峰
# ============================================================

def Lambda(n):
    N=n; d=2; facs=[]
    while d*d<=N:
        if N%d==0:
            facs.append(d)
            while N%d==0: N//=d
        d+=1
    if N>1: facs.append(N)
    return np.log(facs[0]) if facs and len(set(facs))==1 else 0.0

NMAX = 2000
ns = [n for n in range(2, NMAX+1)]
lam = np.array([Lambda(n) for n in ns])
w = lam/np.sqrt(ns)                      # 权重 Λ(n)/√n
L = np.log(ns)                            # ★ 乘法变量 t = log n

print('='*76)
print('R：用乘法变量 t = log n 构造自伴对象，检验其谱是否落在 ζ 零点上')
print('='*76)
print(f'\n  素数测度：μ(t) = Σ Λ(n)/√n · δ(t − log n)，  n ≤ {NMAX}')
print(f'  非零项个数：{int((w>0).sum())}')
print(f'  t 的范围：log 2 = {L[0]:.4f} … log {NMAX} = {L[-1]:.4f}')

# ---- 1. 自相关核的"谱密度" ----
# C(s) = Σ_{m,n} w_m w_n K(s − (L_m − L_n))，取高斯核 K
# 其傅里叶变换（谱密度）在 γ 处应有峰
print('\n[1] 自相关核的谱密度  S(γ) = |Σ_n w_n e^{−i γ L_n}|²  ×  高斯窗')
def S(gamma, sigma=1.0):
    """prime-side 谱密度（加高斯窗平滑）"""
    return abs(np.sum(w * np.exp(-1j*gamma*L) * np.exp(-(L-L.mean())**2/(2*sigma**2))))**2

gammas = np.linspace(0, 60, 6001)
Svals = np.array([S(g) for g in gammas])
# 找峰
peaks = []
for i in range(1, len(gammas)-1):
    if Svals[i] > Svals[i-1] and Svals[i] > Svals[i+1] and Svals[i] > 0.02*Svals.max():
        peaks.append(gammas[i])
# 合并邻近峰
merged=[]
for p in peaks:
    if not merged or p-merged[-1] > 1.5: merged.append(p)

zeros = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178,
         40.918719, 43.327073, 48.005151, 49.773832, 52.970321, 56.446248, 59.347044]
print(f'\n  峰位置（prime-side 谱密度）：{ [round(p,2) for p in merged[:8]] }')
print(f'  ζ 前 8 个零点 γ_n        ：{ [round(z,2) for z in zeros[:8]] }')
print()
hit = 0
for z in zeros[:6]:
    d = min(abs(z-p) for p in merged) if merged else 99
    print(f'    γ={z:8.4f}   最近峰距 {d:6.3f}   {"✅" if d < 0.5 else "（不吻合）"}')
    hit += (d < 0.5)
print(f'\n  命中 {hit}/6')

# ---- 2. 自伴矩阵：Gram 型 ----
print('\n[2] 自伴矩阵（Gram 型）：M_{kl} = Σ_n w_n² · K(L_k − L_n) · K(L_l − L_n)')
print('    取 N 个探针中心 t_k = log k（k ≤ 100），高斯核')
K = lambda s: np.exp(-s**2/(2*1.0**2))
Ks = [k for k in range(2, 101)]
centers = np.log(Ks)
Mm = np.zeros((len(Ks), len(Ks)))
for i,a in enumerate(centers):
    for j,b in enumerate(centers):
        Mm[i,j] = np.sum(w**2 * K(a-L) * K(b-L))
ev = np.linalg.eigvalsh(Mm)
print(f'    矩阵规模 {Mm.shape}，实对称 ⟹ 谱全实（自伴）')
print(f'    最大 5 个特征值：{np.round(ev[::-1][:5],4)}')
print(f'    最小特征值 = {ev[0]:.3e}   ⟹ {"半正定（自伴正型）✅" if ev[0] > -1e-10 else "有负特征值"}')

# ---- 3. 诚实判定 ----
print('\n' + '='*76)
print('诚实判定')
print('='*76)
print('  • 自伴性：✅ 构造天然对称（核对称）⟹ 谱全实。')
print('  • 谱是否 = ζ 零点？ 见上面 [1] 的峰位对照。')
print('  • 关键：谱密度确实只在"素数测度的自相关"上看到结构，')
print('    而把峰精确定位到 γ_n 需要【显式公式】——即需要把 archimedean 项补齐。')
print('    这正说明：**构造是可行的，但"谱=零点"是显式公式的【产物】，不是构造的直接输出**。')
print('  ⟹ 想把它变成"自伴算子谱 = 零点"，缺的正是显式公式里的 archimedean 部分，')
print('     而那一部分的对偶化 = Weil 正性 = RH。')
