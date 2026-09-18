import numpy as np, cmath
import mpmath as mp
mp.mp.dps = 30
np.set_printoptions(precision=6, suppress=True)

# ============================================================
# R2 · Part A：函数域 —— 「序（有限计数）⟹ 谱（α）」
#   完全有限、精确、可算法化
# ============================================================
def legendre(v,p):
    v %= p
    if v == 0: return 0
    return 1 if pow(v,(p-1)//2,p) == 1 else -1

def count_points(p,a,b):
    n = 1                          # 无穷远点
    for x in range(p):
        r = (x*x*x + a*x + b) % p
        l = legendre(r,p)
        n += 1 if l == 0 else (2 if l == 1 else 0)
    return n

def gf_mul(A,B,p,irr,k):
    res = [0]*(2*k-1)
    for i in range(k):
        for j in range(k):
            res[i+j] = (res[i+j] + A[i]*B[j]) % p
    for d in range(2*k-2, k-1, -1):
        c = res[d]
        if c:
            res[d] = 0
            for j in range(k):
                res[d-k+j] = (res[d-k+j] - c*irr[j]) % p
    return res[:k]

def count_points_ext(p,k,irr,a,b):
    elems = []
    for n in range(p**k):
        v = n; e = []
        for _ in range(k):
            e.append(v % p); v //= p
        elems.append(e)
    sq = set()
    for e in elems:
        s = gf_mul(e,e,p,irr,k)
        sq.add(tuple(s))
    n = 1
    for e in elems:
        x3 = gf_mul(gf_mul(e,e,p,irr,k), e, p, irr, k)
        ae = [(a*ee) % p for ee in e]
        fx = [(x3[i] + ae[i] + (b if i==0 else 0)) % p for i in range(k)]
        if tuple(fx) in sq:
            n += 2 if any(fx) else 1
    return n

print('='*84)
print('R2 · Part A：函数域 —— 一个有限计数 ⟹ 谱（α），有限精确可反演')
print('='*84)
curves = [(1,1),(-1,0),(0,1),(1,0),(2,1),(-2,1),(3,1),(1,3)]
print(f'\n  {"p":>4} {"(a,b)":>9} {"N₁":>5} {"a_p":>5} {"α₁":>26} {"|α|":>11} {"√p":>9} {"Hankel⪰0":>9}')
ok = tot = 0
for p in [5,7,11,13,17,19,23,29,31,37,41,43]:
    for (a,b) in curves:
        if (4*a**3+27*b**2) % p == 0: continue
        N = count_points(p,a,b); ap = p+1-N
        disc = ap*ap-4*p
        if disc >= 0:
            r = disc**0.5; al = [(ap+r)/2, (ap-r)/2]
        else:
            r = (-disc)**0.5; al = [complex(ap/2, r/2), complex(ap/2, -r/2)]
        S = [2.0, float(ap)]
        for kk in range(2,7):
            S.append(ap*S[-1] - p*S[-2])        # Newton 递推
        V = np.array([[al[0]**i for i in range(3)], [al[1]**i for i in range(3)]])
        H = V.conj().T @ V                      # M_ij = Σ_l conj(α_l^i)·α_l^j
        ev = np.linalg.eigvalsh(H)
        psd = ev.min() > -1e-8*max(1.0, abs(ev).max())
        hasse = abs(abs(al[0]) - p**0.5) < 1e-9
        tot += 1; ok += (hasse and psd)
        print(f'  {p:>4} {str((a,b)):>9} {N:>5} {ap:>5} {str(al[0])[:26]:>26} {abs(al[0]):>11.6f} {p**0.5:>9.6f} {str(psd):>9}')
print(f'\n  |α|=√p（曲线的 RH）且 Hankel 矩矩阵 ⪰ 0 ： {ok}/{tot} 全部通过 ✅')

# ---- A'：独立核验（真去数 F_{p²}） ----
print('\n  [A′ 独立核验] 不去推断，直接数 𝔽_{p²} 上的点，看是否等于 α₁²+α₂² 的预测')
checks = [(5,2,[2,0,1],1,1), (7,2,[1,0,1],1,1)]   # p,k,irr=[c0,c1,...,ck]
for (p,k,irr,a,b) in checks:
    N1 = count_points(p,a,b); ap = p+1-N1
    pred_a2 = ap*ap - 2*p
    N2 = count_points_ext(p,k,irr,a,b)
    N2_pred = p**2 + 1 - pred_a2
    print(f'    p={p}, E:y²=x³+x+1 :  N₂(实算)={N2:>5}   预测 p²+1−(a_p²−2p)={N2_pred:>5}   {"✅" if N2==N2_pred else "✗"}')

# ============================================================
# R2 · Part B：数域 —— 矩发散 ⟹ Newton 恒等式无从启动
# ============================================================
print('\n'+'='*84)
print('R2 · Part B：数域 —— 矩 Σγ^{2n} 发散 ⟹ 有限反演不可能')
print('='*84)
NZ = 200
gam = np.array([float(mp.im(mp.zetazero(k))) for k in range(1,NZ+1)])
print(f'\n  取前 {NZ} 个零点：γ₁={gam[0]:.6f} … γ_{NZ}={gam[-1]:.4f}')
print(f'\n  曲线情形  S_k = Σα^k       有界（|α|=√q）          ⟹ Newton 可用 ✅')
print(f'  数域情形  S_' + '{2n}' + ' = Σγ^{2n}     随 T³logT 发散        ⟹ Newton 无从启动 ✗')
print(f'\n  {"n":>3} {"Σ_{k≤50} γ^{2n}":>18} {"Σ_{k≤100} γ^{2n}":>18} {"Σ_{k≤200} γ^{2n}":>20}')
for n in [1,2,3]:
    a50 = np.sum(gam[:50]**(2*n)); a100 = np.sum(gam[:100]**(2*n)); a200 = np.sum(gam**(2*n))
    print(f'  {n:>3} {a50:>18.4e} {a100:>18.4e} {a200:>20.4e}')
print('\n  平滑律：  Σ_{γ<T} γ² ≈ ∫₀^T t² (1/2π)[log(t/2πe)+1] dt  ~  T³ log T/(6π)  ⟶  ∞')
for T in [50,100,200,500,1000]:
    f = lambda t: t*t*(1/(2*mp.pi))*(mp.log(t/(2*mp.pi*mp.e))+1)
    approx = mp.quad(f,[mp.mpf('1e-9'), T])
    print(f'     T={T:>5}:  预测 Σγ² ≈ {float(approx):.4e}')

print('\n  ⟹ 关键：几何侧只能给出 Σ_γ h(γ)，其中 h 必须【衰减】。')
print('     h=γ^{2n} 不衰减 ⟹ 矩【根本不是几何侧的数据】⟹ Newton 恒等式无从启动。')

# ============================================================
print('\n'+'='*84)
print('R2 · Part C：正性的角色')
print('='*84)
print('''  曲线：正性（|α|=√p / Hodge 指标）【自动成立】，矩矩阵 ⪰0（Part A 实测），
         ⟹ 谱是一个【有限正测度】⟹ Newton 反演稳定。
  ζ  ：正性 = Weil 正性 ⟺ 谱是一个【正测度】⟺ RH ——【未证】。
        ⟹ 带限/正则化反演要成为定理，恰恰需要它。

  ⟹ 结论：S2（序⟹谱）在函数域 = 有限问题（已解决）；
           在数域 = 无穷维 + 需要正性，而正性就是 RH。''')
