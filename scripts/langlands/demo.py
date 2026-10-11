import mpmath as mp
mp.mp.dps = 30

# ---------- 算术侧：von Mangoldt 求和 ----------
def Lambda(n):
    """von Mangoldt: Lambda(p^k)=log p, 其余=0"""
    m = n
    for p in mp.primefactors(n) if hasattr(mp, 'primefactors') else []:
        pass
    # 手写因子分解
    N = n
    d = 2
    facs = []
    while d * d <= N:
        if N % d == 0:
            facs.append(d)
            while N % d == 0:
                N //= d
        d += 1
    if N > 1:
        facs.append(N)
    if len(set(facs)) == 1 and len(facs) > 0:
        return mp.log(facs[0])
    return mp.mpf(0)

def psi_arith(x):
    return sum((Lambda(n) for n in range(2, int(x) + 1)), mp.mpf(0))

# ---------- 谱侧：显式公式（零点求和）----------
def psi_spec(x, zeros):
    x = mp.mpf(x)
    base = x - mp.log(2 * mp.pi) - mp.log(1 - x ** -2) / 2
    tot = mp.mpf(0)
    for g in zeros:
        rho = mp.mpf('0.5') + 1j * g
        tot += 2 * mp.re(mp.power(x, rho) / rho)
    return base - tot

# ---------- 取零点 ----------
print('取前 40 个非平凡零点（ρ = 1/2 + iγ）…')
zeros = [mp.im(mp.zetazero(k)) for k in range(1, 41)]
print('  γ1..γ5 =', [mp.nstr(z, 6) for z in zeros[:5]])

X = 100
exact = psi_arith(X)
print(f'\n=== x = {X} ===')
print(f'算术侧  ψ(x) = Σ Λ(n)         = {mp.nstr(exact, 12)}')

print('\n谱侧（零点求和）逐段收敛：')
for k in [5, 10, 20, 30, 40]:
    v = psi_spec(X, zeros[:k])
    err = abs(v - exact)
    print(f'  用前 {k:2d} 个零点: {mp.nstr(v, 12):>16}   误差 {mp.nstr(err, 4)}')

# 再取一个 x 检验
for X2 in [50, 200]:
    e2 = psi_arith(X2)
    z2 = [mp.im(mp.zetazero(k)) for k in range(1, 61)]
    v2 = psi_spec(X2, z2)
    print(f'\nx = {X2}:  算术侧 {mp.nstr(e2,10)}  |  谱侧(60 零点) {mp.nstr(v2,10)}  |  误差 {mp.nstr(abs(v2-e2),4)}')

# ---------- 附：Weil 二次型的结构（f = g*g* ⟹ f̂ = |ĝ|² ≥ 0）----------
print('\n=== Weil 二次型结构演示 ===')
print('取高斯 g(t) = exp(-t²/2)，检验 f = g*g* 的傅里叶变换 ≡ |ĝ|² ≥ 0：')
for t in [-3, -1, 0, 1, 3]:
    t = mp.mpf(t)
    ghat = mp.sqrt(2 * mp.pi) * mp.e ** (-t ** 2 / 2)   # 高斯自傅里叶
    fhat = ghat ** 2
    print(f'   t = {mp.nstr(t,3):>5}   ĝ(t) = {mp.nstr(ghat,8):>14}   f̂(t)=|ĝ|² = {mp.nstr(fhat,8):>14}   ≥0 ✓')
