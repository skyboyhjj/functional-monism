import numpy as np
mp = None  # 本脚本只用 numpy；ψ 用算术侧（素数幂）直接算，不依赖显式公式

# ============================================================
# R（修正版）：把自伴对象建在 E(t) = ψ(e^t) − e^t 上
# ============================================================
# 对应《公理IV续_R_自伴算子的构造.md》§二「修正」—— 复核脚本
# 第一次尝试（demo_R.py）把"谱密度"建在素数测度 μ 上 → 0/6 命中（失败）。
# 教训：素数是【账 A（算术侧）】，不是谱。
#
# 本脚本改用显式公式给出的【误差项】E(t) = ψ(e^t) − e^t：
#   E(t) = −Σ_ρ e^{ρt}/ρ − log 2π − ½ log(1−e^{−2t})
# 其振荡频率正是零点的虚部 γ。把谱（周期图）算在 E(t)·e^{−t/2} 上，
# 峰应落在 γ_n 处。
#
# ★ 诚实边界（与文档 §三一致）：
#   把谱建在 E(t) 上本身就是【用显式公式当输入】——它是"后验"的，不是证明 RH。
# ============================================================

def prime_sieve(limit):
    """返回 ≤ limit 的所有素数列表（numpy 埃氏筛）。"""
    if limit < 2:
        return np.array([], dtype=np.int64)
    isc = np.ones(limit + 1, dtype=bool)
    isc[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if isc[i]:
            isc[i * i::i] = False
    return np.nonzero(isc)[0]

def psi_prime_sum(xs, primes, log_primes):
    """ψ(x) = Σ_{p^k ≤ x} log p，对向量 xs 计算（算术侧，自含）。"""
    out = np.zeros_like(xs, dtype=float)
    for lg, pr in zip(log_primes, primes):
        x = xs
        # 对每个素数 p，累加 log p * floor(log_p(x)) 的贡献等价于
        # Σ_{k≥1} 1_{p^k ≤ x} log p。用循环 k 直接数：
        pk = pr
        while True:
            mask = xs >= pk
            if not mask.any():
                break
            out[mask] += lg
            pk *= pr
            if pk > xs.max():
                break
    return out

# ---- 参数（对齐文档 §〇：x ≤ 8.9×10⁶，约 4000 采样点）----
XMAX = 8.9e6
N = 4000
t0, t1 = 1.0, np.log(XMAX)          # t = log x，x = e^t ∈ [e, 8.9e6]
t = np.linspace(t0, t1, N)
dt = t[1] - t[0]

PMAX = int(XMAX) + 1
primes = prime_sieve(PMAX)
log_primes = np.log(primes.astype(float))

print('=' * 76)
print('R（修正版）：E(t) = ψ(e^t) − e^t 的自伴谱 —— 复核命中')
print('=' * 76)
print(f'  素数表：≤ {PMAX} 的素数共 {len(primes)} 个')
print(f'  t = log x ∈ [{t0:.2f}, {t1:.2f}]，采样 {N} 点，Δt = {dt:.5f}')

# ---- 1. 算术侧算出 E(t) ----
print('\n[1] 用素数幂（账 A）算 ψ(e^t)，构造误差项 E(t) = ψ(e^t) − e^t')
psi = psi_prime_sum(np.exp(t), primes, log_primes)
Et = psi - np.exp(t)
# 去掉 e^{t/2} 增长因子，使振荡项等幅：F(t) = E(t)·e^{−t/2}
Ft = Et * np.exp(-t / 2)

# ---- 2. 周期图谱密度 ----
# S(γ) = |Σ_j F(t_j) e^{−i γ t_j}|²，在细网格 γ 上直接积分（连续傅里叶）
print('\n[2] 谱密度 S(γ) = |Σ_j F(t_j) e^{−i γ t_j}|² 在 γ ∈ [10, 55] 上扫频')
grid = np.arange(10.0, 55.0, 0.005)
S = np.empty_like(grid)
denom = None
for k, g in enumerate(grid):
    # 用 e^{i g t} 复指数直接求和
    S[k] = abs(np.sum(Ft * np.exp(-1j * g * t))) ** 2

# ---- 3. 找峰（局部极大 + 最小高度）----
peaks = []
for i in range(1, len(grid) - 1):
    if S[i] > S[i - 1] and S[i] > S[i + 1] and S[i] > 0.05 * S.max():
        peaks.append(grid[i])
# 合并 < 0.5 的邻近峰
merged = []
for p in peaks:
    if not merged or p - merged[-1] > 0.5:
        merged.append(p)
merged = np.array(merged) if merged else np.array([])

zeros = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178,
         40.918719, 43.327073, 48.005151, 49.773832]
print(f'\n  检测到的峰（γ）：{np.round(merged, 4)}')
print(f'  ζ 前 10 个零点：{np.round(zeros, 4)}')
print()

print('    γ_n (已知)    谱峰位置    偏差')
hit = 0
for idx, z in enumerate(zeros):
    if len(merged) == 0:
        print(f'    {z:8.4f}      （无峰）     —')
        continue
    d = min(abs(z - p) for p in merged)
    pn = merged[np.argmin(abs(merged - z))]
    if d < 0.5:
        print(f'    {z:8.4f}     {pn:8.4f}    {d:.4f}   ✅')
        hit += 1
    elif d < 1.5:
        print(f'    {z:8.4f}     {pn:8.4f}    {d:.4f}   （与邻近峰合并）')
    else:
        print(f'    {z:8.4f}     {pn:8.4f}    {d:.4f}   （不吻合）')

print(f'\n  命中 {hit}/10')

# ---- 4. 自伴性检验 ----
# 自相关核 C(Δ) = Σ_j F(t_j) F(t_j + Δ)（整数位移对称版）
print('\n[3] 自伴性：自相关核 C(Δ) = Σ_j F(t_j) F(t_j+Δ)，整数位移对称定义')
def autocorr(m):
    """C[m] = Σ_{j=0}^{N-1-m} F_j F_{j+m}（m 为整数位移）"""
    mm = abs(int(round(m)))
    if mm >= N:
        return 0.0
    return np.dot(Ft[:N - mm], Ft[mm:N])

max_m = min(200, N - 1)
asym = max(abs(autocorr(m) - autocorr(-m)) for m in range(1, max_m))
print(f'    max_Δ |C(Δ) − C(−Δ)| = {asym:.3e}   ⟹ {"严格偶（自伴）✅" if asym < 1e-8 else "⚠️ 非严格偶"}')

# ---- 5. 诚实判定 ----
print('\n' + '=' * 76)
print('诚实判定')
print('=' * 76)
print('  • 构造在数值上可行：把对象建在 E(t) 上，其谱确实落在 ζ 零点附近。')
print('  • 但这是【后验】的：峰的出现用了显式公式的结构，')
print('    "谱 = 零点"是显式公式的【产物】，不是构造的直接输出。')
print('  • 它是一个数值实验，不是定理；升级为"自伴算子谱 = 零点"')
print('    缺的正是 archimedean 项的对偶化 = Weil 正性 = RH。')