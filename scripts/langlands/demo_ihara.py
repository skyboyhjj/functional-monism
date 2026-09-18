import numpy as np
np.set_printoptions(precision=5, suppress=True)

def eigen(A):
    return np.sort(np.linalg.eigvalsh(A))[::-1]

def check(name, A, bipartite=False):
    d = int(round(A.sum(axis=1)[0]))
    bound = 2 * np.sqrt(d - 1)
    w = eigen(A)
    # 平凡特征值：+d（总在）；二部图另有 −d
    triv = {d}
    if bipartite:
        triv.add(-d)
    nontriv = [x for x in w if all(abs(x - t) > 1e-6 for t in triv)]
    mx = max(abs(x) for x in nontriv) if nontriv else 0.0
    ok = mx <= bound + 1e-9
    print(f'  {name:12s} d={d}  2√(d−1)={bound:7.5f}  非平凡 max|λ|={mx:7.5f}  '
          f'{"✅ Ramanujan" if ok else "❌ 非 Ramanujan（图 RH 失效）"}')
    return ok

print('=' * 76)
print('Ihara zeta 的「RH」 ⟺ Ramanujan 图性质：非平凡特征值 |λ| ≤ 2√(d−1)')
print('=' * 76)

print('\n[正例 · 平凡特征值只算 +d（二部图另有 −d）]')
check('K4', np.ones((4,4)) - np.eye(4))
# Petersen
E = [(0,1),(1,2),(2,3),(3,4),(4,0),(5,7),(7,9),(9,6),(6,8),(8,5),
     (0,5),(1,6),(2,7),(3,8),(4,9)]
P = np.zeros((10,10))
for i,j in E: P[i,j]=P[j,i]=1
check('Petersen', P)
check('K5', np.ones((5,5)) - np.eye(5))
C8 = np.zeros((8,8))
for i in range(8): C8[i,(i+1)%8]=C8[(i+1)%8,i]=1
check('C8', C8)

print('\n[更正确认：K3,3 其实**是** Ramanujan（二部图的 −d 是平凡值）]')
K33 = np.zeros((6,6)); K33[:3,3:]=1; K33[3:,:3]=1
print('   K3,3 谱 =', np.round(eigen(K33),5), '  ⟹ 非平凡只有 0 ⟹ 上限 2√2=2.8284，0 ≤ 2.8284 ✅')
check('K3,3', K33, bipartite=True)

print('\n[负例 · 真正的非 Ramanujan：4-正则循环图 C_n(1,2)]')
print('   特征值 = 2cos(2πj/n) + 2cos(4πj/n)，j=0..n−1；上限 2√3 ≈ 3.4641')
print('   j=1 处取到最大非平凡值 → 2cos(2π/n)+2cos(4π/n)，随 n 增大趋近 4')
for n in [10, 14, 16, 18, 20, 30, 60]:
    A = np.zeros((n,n))
    for i in range(n):
        for s in (1,2,-1,-2):
            A[i,(i+s)%n] = 1
    d = 4; bound = 2*np.sqrt(3)
    w = eigen(A); mx = max(abs(x) for x in w if abs(abs(x)-d) > 1e-6)
    ok = mx <= bound + 1e-9
    print(f'   n={n:3d}:  非平凡 max|λ| = {mx:7.5f}   {">" if not ok else "≤"} {bound:7.5f}   '
          f'{"✅ Ramanujan" if ok else "❌ 非 Ramanujan"}')

print('\n   ⟹ 这说明 2√(d−1) 是**实质约束**：超了就是非 Ramanujan。')
print('       Alon–Boppana：任何 d-正则图族都有 liminf λ₂ ≥ 2√(d−1)。')
