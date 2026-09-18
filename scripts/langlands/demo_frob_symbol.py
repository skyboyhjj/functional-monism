import math

print('='*74)
print('“Frobenius 符号 = monodromy” 可算演示（Morishita 桥的两端共享同一个数据）')
print('='*74)
print('\n取 K = ℚ(i)，Gal(K/ℚ) = ℤ/2。')
print('Frobenius 符号 (K/ℚ)/p 由 p 的分裂行为决定：')
print('   p ≡ 1 (mod 4)  ⟹ p 分裂    ⟹ Frobenius = 恒等')
print('   p ≡ 3 (mod 4)  ⟹ p 惯性    ⟹ Frobenius = 非平凡元（复共轭）')
print()

def splits(p):
    """p 在 ℚ(i) 中分裂 ⟺ x² ≡ -1 (mod p) 有解 ⟺ p ≡ 1 mod 4"""
    if p == 2: return None
    has_root = any((x*x + 1) % p == 0 for x in range(p))
    return has_root

print(f'  {"p":>4} {"p mod 4":>8} {"x²≡-1 有解?":>14} {"Frobenius 符号":>18} {"p=a²+b²?":>12}')
rows=[]
for p in [3,5,7,11,13,17,19,23,29,31,37,41,43,47]:
    sp = splits(p)
    frob = 'id' if sp else '非平凡（-1）'
    # p=a^2+b^2 表示（p≡1 mod 4 时存在）
    rep = None
    for a in range(1, int(math.isqrt(p))+1):
        b2 = p - a*a
        b = math.isqrt(b2)
        if b*b == b2:
            rep = f'{a}²+{b}²'; break
    rows.append((p, p%4, sp, frob, rep))
    print(f'  {p:>4} {p%4:>8} {str(sp):>14} {frob:>18} {str(rep or "—"):>12}')

print('\n  ★ 同一个 p，三种说法完全一致：')
print('     · Frobenius 符号（算术侧）　· 分裂行为（Galois 侧）　· p = a²+b²（几何侧）')
print('    —— 这正是 Morishita 桥两端共享的那个 monodromy 数据。')

# ---- ζ_K = ζ · L(s, χ_4) 的“两本账” ----
print('\n' + '='*74)
print('两本账：ζ_K(s) = ζ(s) · L(s, χ_4)   （扩张的 zeta = 基域 zeta × 新字符 L）')
print('='*74)

def chi4(n):
    if n % 2 == 0: return 0
    return 1 if n % 4 == 1 else -1

def zeta_K(s):
    """ζ_K(s) 的 Euler 积：p=2 分支 e=2；p≡1(4) 分裂 → 两个素理想；p≡3(4) 惯性 → N=p²"""
    primes = [n for n in range(2, 3000) if all(n % d for d in range(2, int(n**.5)+1))]
    out = 1.0
    for p in primes:
        if p == 2:
            f = 1.0/(1 - p**(-s))              # (2)=𝔭²，N(𝔭)=2
        elif p % 4 == 1:
            f = 1.0/(1 - p**(-s))**2           # 分裂：(p)=𝔭𝔭'，各 N=p
        else:
            f = 1.0/(1 - p**(-2*s))            # 惯性：(p)=𝔭，N=p²
        out *= f
    return out

s = 1.5
zK_euler = zeta_K(s)
# ζ(s)·L(s,χ_4) 用 Euler 积直接算，保证可比
primes = [n for n in range(2, 3000) if all(n % d for d in range(2, int(n**.5)+1))]
def zeta_euler(s):
    o = 1.0
    for p in primes: o *= 1.0/(1 - p**(-s))
    return o
def L_euler(s):
    o = 1.0
    for p in primes:
        c = chi4(p)
        if c == 0: continue
        o *= 1.0/(1 - c*p**(-s))
    return o
zK_fact = zeta_euler(s) * L_euler(s)

print(f'   s = {s}')
print(f'   ζ_K(s) 由理想分解（Euler 积，N(𝔭) 计数） = {zK_euler:.10f}')
print(f'   ζ(s)·L(s,χ_4)（Euler 积）               = {zK_fact:.10f}')
print(f'   差 = {abs(zK_euler - zK_fact):.2e}')
print('   ⟹ 两本账一致（理想分解 vs ζ·L 因子分解）✅')
print('      —— 桥的两端共享同一个 Euler 数据（各 primse 的 Frobenius）。')

