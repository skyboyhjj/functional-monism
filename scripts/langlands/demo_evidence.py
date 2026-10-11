import mpmath as mp
mp.mp.dps = 30

print('=' * 66)
print('演示 1：Poisson 求和 ⟹ Jacobi theta 函数方程（最根本的"两本账"）')
print('=' * 66)
print('  theta(t) = Σ_{n∈Z} exp(-π n² t)')
print('  两本账：t 侧 vs 1/t 侧；  函数方程 theta(1/t) = sqrt(t)·theta(t)')
print()

def theta(t, N=200):
    t = mp.mpf(t)
    return sum(mp.e ** (-mp.pi * n * n * t) for n in range(-N, N + 1))

print('   t      theta(t)            sqrt(t)*theta(t)     theta(1/t)         |差|')
for t in ['0.25', '0.5', '1.0', '2.0', '4.0']:
    lt = mp.log(mp.mpf(t))
    a = theta(mp.e ** lt)                 # theta(t)
    rhs = mp.e ** (lt / 2) * a            # sqrt(t)*theta(t)
    lhs = theta(mp.e ** (-lt))            # theta(1/t)
    print(f'  {t:>4}  {mp.nstr(a,12):>18}  {mp.nstr(rhs,12):>18}  {mp.nstr(lhs,12):>18}  {mp.nstr(abs(lhs-rhs),4)}')

print()
print('=' * 66)
print('演示 2：Burnside/Pólya 计数（轨道数 = 群元素不动点平均数）')
print('=' * 66)
print('  账 A（轨道侧）：6 珠 2 色的项链数（模旋转群 C6）')
print('  账 B（不动点侧）：(1/|G|) Σ_g |X^g|')
print()

from itertools import product

def necklaces_bruteforce(n, k):
    seen = set(); cnt = 0
    for x in product(range(k), repeat=n):
        if x in seen:
            continue
        cnt += 1
        for r in range(n):
            seen.add(tuple(x[(i + r) % n] for i in range(n)))
    return cnt

def burnside(n, k):
    # 轮换 6 珠中属于 r 步旋转的置换 = gcd(n,r) 个轮换
    from math import gcd
    tot = sum(k ** gcd(n, r) for r in range(n))
    return tot // n

for (n, k) in [(6, 2), (6, 3), (8, 2), (10, 2)]:
    a = necklaces_bruteforce(n, k)
    b = burnside(n, k)
    print(f'  n={n:2d}, k={k}:  账A(暴力枚举) = {a:>5}   账B(Burnside) = {b:>5}   {"✅相等" if a == b else "✗不等"}')

print()
print('=' * 66)
print('演示 3：Gauss 和（同一个数，两种算法）')
print('=' * 66)
print('  账 A： G² 通过"乘加倍换元" ⟹ G² = (-1)^((p-1)/2)·p')
print('  账 B： |G|² 通过求和 ⟹ |G|² = p')
print()
for p in [5, 7, 11, 13, 17, 19, 23]:
    G = sum(mp.e ** (2j * mp.pi * a * a / p) for a in range(p))
    A = (G.real ** 2 + G.imag ** 2)          # |G|²
    B = (p if p % 4 == 1 else -p)            # (-1)^((p-1)/2) p
    sign = 1 if p % 4 == 1 else -1
    print(f'  p={p:2d}:  |G|² = {mp.nstr(A,10):>12}  = p ? {"✅" if abs(A-p)<1e-20 else "✗"}   '
          f'Re(G²)/(p·(-1)^((p-1)/2)) = {mp.nstr(G.real,8)}  符号({sign:+d})')

print()
print('  一次恒等，两端账本：')
for p in [5, 13, 17, 29]:
    G = sum(mp.e ** (2j * mp.pi * a * a / p) for a in range(p))
    G2 = G ** 2
    pred = (p if p % 4 == 1 else -p)
    print(f'     p={p:2d}  G = {mp.nstr(G.real,10)}{"+" if G.imag>=0 else ""}{mp.nstr(G.imag,6)}i   '
          f'G² = {mp.nstr(G2.real,10)} ≈ {pred:+d}  {"✅" if abs(G2.real-pred)<1e-15 else "✗"}')
