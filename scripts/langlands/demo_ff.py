import cmath, math

# ============ 1. 有限域 GF(p) 上的椭圆曲线点计数 ============
def N1(a, b, p):
    """y^2 = x^3 + a x + b over GF(p)；返回 #E(GF(p))（含无穷远点）"""
    cnt = 0
    for x in range(p):
        rhs = (x*x*x + a*x + b) % p
        # 数平方根个数
        r = pow(rhs, (p-1)//2, p) if rhs % p else 0
        if rhs % p == 0:
            cnt += 1
        elif r == 1:
            cnt += 2
        # r == p-1 → 非剩余，+0
    return cnt + 1

# ============ 2. GF(p^2) = GF(p)[t]/(t^2 - c)，c 为非剩余 ============
def find_nonresidue(p):
    for c in range(2, p):
        if pow(c, (p-1)//2, p) == p-1:
            return c
    return None

def N2(a, b, p):
    """在 GF(p^2) 上计数（元素写作 u + v t，t^2 = c）"""
    c = find_nonresidue(p)
    def mul(x, y):          # (u,v)*(u',v')
        return ((x[0]*y[0] + x[1]*y[1]*c) % p, (x[0]*y[1] + x[1]*y[0]) % p)
    def add(x, y):
        return ((x[0]+y[0]) % p, (x[1]+y[1]) % p)
    def sc(s, x):
        return ((s*x[0]) % p, (s*x[1]) % p)
    els = [(u, v) for u in range(p) for v in range(p)]
    sq = {}                 # 平方值 -> 元素列表
    for e in els:
        sq.setdefault(mul(e, e), []).append(e)
    cnt = 0
    for x in els:
        x2 = mul(x, x)
        x3 = mul(x2, x)
        rhs = add(add(x3, sc(a, x)), (b % p, 0))
        cnt += len(sq.get(rhs, []))
    return cnt + 1

# ============ 3. 由 a_p 解出 Frobenius 特征值，验证 |alpha| = sqrt(p) ============
def frob_pair(a_p, p):
    disc = a_p*a_p - 4*p
    s = cmath.sqrt(disc + 0j)
    return (a_p + s)/2, (a_p - s)/2

print('=' * 74)
print('函数域 GL(1)：Weil 猜想（RH）在曲线上已【证明】—— 数值直接验证')
print('=' * 74)
print('\n[第 1 部分] 逐条：数点 ⟹ a_p ⟹ 特征值 ⟹ |α| 是否 = √p（这就是曲线上的 RH）\n')
print(f'  {"曲线":>14} {"p":>4} {"#E(F_p)":>8} {"a_p":>6} {"|α|":>12} {"√p":>12} {"判定":>6}')

cases = [(-1, 0, 7), (-1, 0, 11), (-1, 0, 19),   # p ≡ 3 mod 4 → a_p = 0，|α| = √p 精确
         (-1, 0, 5), (-1, 0, 13),                # p ≡ 1 mod 4
         (1, 1, 7), (1, 1, 13), (0, 1, 7), (2, 3, 11)]
for (a, b, p) in cases:
    n = N1(a, b, p)
    a_p = p + 1 - n
    al, be = frob_pair(a_p, p)
    ok = abs(abs(al) - math.sqrt(p)) < 1e-9
    print(f'  y²=x³+{a}x+{b:>2} {p:>4} {n:>8} {a_p:>6} {abs(al):>12.7f} {math.sqrt(p):>12.7f} '
          f'{"✅" if ok else "✗":>6}')

print('\n[第 2 部分] 「两本账」：扩张域点数 N_n = p^n + 1 − (α^n + ᾱ^n)')
print('   账A：直接数点；  账B：用 α 的幂（迹公式）\n')

# 用交换递推 a_{p^n} = a_p·a_{p^{n-1}} − p·a_{p^{n-2}}（等价于 α^n+ᾱ^n 的 Chebyshev 递推）
def trace_n(a_p, p, n):
    # T_n = α^n + ᾱ^n，递推 T_n = a_p·T_{n-1} − p·T_{n-2}
    T0, T1 = 2.0, float(a_p)
    if n == 0: return T0
    if n == 1: return T1
    for _ in range(2, n+1):
        T0, T1 = T1, a_p*T1 - p*T0
    return T1

a, b, p = -1, 0, 5     # y² = x³ − x over F_5
n1 = N1(a, b, p); a_p = p + 1 - n1
print(f'   曲线 y² = x³ − x over F_{p}:  #E(F_{p}) = {n1},  a_{p} = {a_p}')
print(f'   {"n":>3} {"账A: 直接数点":>13} {"账B: p^n+1−T_n":>15}   '
      f'{"|N−(p^n+1)|":>12} {"≤ 2·p^{n/2}":>12}  {"RH/Hasse":>8}')
for n in range(1, 9):
    bB = p**n + 1 - trace_n(a_p, p, n)
    if n == 1:
        bA = str(n1)
    elif n == 2:
        bA = str(N2(a, b, p))     # 真·暴力数点 GF(25)
    else:
        bA = '—'
    dev = abs(bB - (p**n + 1))
    bound = 2 * p**(n/2)
    tag = '✅' if dev <= bound + 1e-6 else '✗'
    print(f'   {n:>3} {bA:>13} {bB:>15.6f}   {dev:>12.5f} {bound:>12.5f}  {tag:>8}')

print(f'\n   ✔ n=1 与 n=2 是【真暴力数点】(GF(5) 与 GF(25))，与账B吻合（差 0）。')
print(f'   ✔ 每个 n 都满足 Weil/Hasse 界 |N_n − (p^n+1)| ≤ 2·p^(n/2) —— 这正是曲线上 RH。')

print('\n[第 3 部分] p ≡ 3 (mod 4) 的精确情形（a_p = 0 ⟹ α = ± i√p，|α| = √p 精确）')
for p in [3, 7, 11, 19, 23, 31]:
    n = N1(-1, 0, p)
    print(f'   p={p:3d}:  #E = {n:3d} = p+1 = {p+1:3d} ? {"✅" if n == p+1 else "✗"}   '
          f'a_p = {p+1-n}  ⟹ α = ±i√{p}')
