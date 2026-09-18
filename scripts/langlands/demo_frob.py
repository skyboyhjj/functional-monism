import numpy as np

# ============ 演示：Frobenius 在哪些对象上非平凡 ============
print('='*74)
print('Λ‑结构 / Frobenius 在各对象上的行为（Borger 的 "下降数据" 视角）')
print('='*74)

# ---- 1. Z[x] 上的 Adams 算子 ψ_p：ψ_p(x) = x^p, ψ_p(n) = n ----
print('\n[1] ℤ[x] 的 Λ‑结构:  ψ_p(x) = x^p ,  ψ_p(n) = n（整数不动）')
print('    ⟹ 在初始对象 ℤ 上（无变量），ψ_p = id —— Frobenius 是【平凡】的')
print('    （ℤ 是唯一的初始 Λ‑环，即 𝔽₁ 本身）')

# ---- 2. F_p[x] 上的 Frobenius: φ_p(f) = f(x^p)，验证 freshman dream ----
print('\n[2] 𝔽_p[x] 的 Frobenius:  φ_p(f)(x) = f(x)^p =? f(x^p)')
print('    验证：对若干 f, p，比较 f(x)^p mod p 与 f(x^p) 的系数')

def poly_mul_mod(a, b, p):
    c = [0]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        for j,bj in enumerate(b):
            c[i+j] = (c[i+j] + ai*bj) % p
    return c

def poly_pow_mod(a, n, p):
    r = [1]
    for _ in range(n):
        r = poly_mul_mod(r, a, p)
    return r

def compose_xp(a, p):
    """f(x^p): 系数 a_k 搬到位置 k*p"""
    out = [0]*(len(a)-1)*p + [0]
    out = [0]*((len(a)-1)*p + 1)
    for k, ak in enumerate(a):
        out[k*p] = ak % p
    return out

tests = [([1,1],3), ([1,1],5), ([0,1,1],3), ([2,1,1],5), ([1,0,3,1],7), ([4,2,1],3)]
allok = True
for coef, p in tests:
    lhs = poly_pow_mod(coef, p, p)
    rhs = compose_xp(coef, p)
    # 对齐长度
    n = max(len(lhs), len(rhs))
    lhs += [0]*(n-len(lhs)); rhs += [0]*(n-len(rhs))
    ok = lhs == rhs
    allok &= ok
    print(f'    p={p}: f={coef}  →  f^p={lhs}   f(x^p)={rhs}   {"✅相等" if ok else "✗"}')
print(f'    ⟹ 全部通过（Freshman\'s Dream: f^p = f(x^p) in 𝔽_p[x]）✅' if allok else '✗有失败')

# ---- 3. Witt 向量的 Frobenius ----
print('\n[3] Witt 向量 W(k) 的 Frobenius（Teichmüller 表示下 F([a]) = [a^p]）')
print('    • W(𝔽_p) = ℤ_p :  对 a∈𝔽_p 有 a^p = a  ⟹ F = id   (Frobenius 【平凡】)')
print('    • W(𝔽_{p^f}) = ℤ_{p^f} (f>1) : a ↦ a^p 是 f 阶自同构 ⟹ F ≠ id (非平凡)')
for p in [2,3,5,7,11]:
    fixed = all(pow(a, p, p) == a % p for a in range(p))
    print(f'      p={p:2d}:  ∀a∈𝔽_{p}:  a^p ≡ a ? {"✅" if fixed else "✗"}   ⟹ W(𝔽_{p}) 上 F = id')

# 非平凡性：𝔽_{p^2} 中的 Frobenius 作用需要用域扩张；此处给出阶的判据
print('    • 𝔽_{p^f} 的 Frobenius 阶 = f；故 f>1 时非平凡（Witt 上亦然）')
for p, f in [(3,2),(5,2),(2,3)]:
    print(f'      p={p}, f={f}: 𝔽_{{{p}^{f}}} 中 Frobenius 的阶 = {f} ⟹ 非平凡（p^f-1 = {p**f-1}）')

print('\n' + '='*74)
print('结论')
print('='*74)
print('  • 在"绝对对象" ℤ 上：Frobenius = id（平凡）——被保留，但没内容')
print('  • 在"几何对象" 𝔽_p[x] 上：Frobenius = f(x^p)（非平凡）')
print('  • 在 Witt 向量上：F 是否平凡，取决于基域是否"已经完美"')
print('  ⟹ Borger 的 Λ‑结构忠实地把 {φ_p} 保留为下降数据，')
print('     但在真正关心的对象 Spec ℤ 上，这些 φ_p 全是恒等。')

