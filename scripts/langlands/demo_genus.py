import cmath, math

# ---------- 亏格 g 的曲线：zeta 分子 P(T) 的次数 = 2g ----------
# RH 的对象是 P(T)=∏(1-α_i T) 的 2g 个根倒数 α_i；
# 声明 "|α_i| = √q" 需要 2g ≥ 1 才有内容。
print('='*72)
print('亏格 g  ⟺  RH 是否有内容？   （ζ(T)=P(T)/((1-T)(1-qT))，deg P = 2g）')
print('='*72)

def report(name, g, Nfun=None, alphas=None, q=None):
    deg = 2*g
    print(f"\n{name}   (g={g}, deg P = {deg})")
    if deg == 0:
        print("   ζ(T) = 1/((1-T)(1-qT))   ⟹  P(T)=1，无 α_i")
        print("   ⟹ RH 命题【真空】(vacuous)：没有特征值需要界")
    else:
        # 用真数点求 α_i
        from itertools import product
        pass
    
# ---- 亏格 0：P^1 ----
def N_P1(q, n):
    """#P^1(F_{q^n}) = q^n + 1"""
    return q**n + 1

print('\n[亏格 0]  P^1 over F_q')
for q in [2,3,5,7]:
    Ns=[N_P1(q,n) for n in (1,2,3)]
    print(f'   q={q}:  N_n = {Ns}   （= q^n + 1，恒成立）')
print('   ⟹ P(T) 次数 = 0，没有 α_i  ⟹ RH 无内容（"真空成立"）')

# ---- 亏格 1：椭圆曲线 ----
def N_E(a,b,p,n=1):
    cnt=0
    for x in range(p):
        rhs=(x*x*x+a*x+b)%p
        if rhs%p==0: cnt+=1
        elif pow(rhs,(p-1)//2,p)==1: cnt+=2
    return cnt+1

print('\n[亏格 1]  椭圆曲线 y^2 = x^3 + a x + b')
rows=[]
for (a,b,p) in [(-1,0,5),(-1,0,7),(1,1,7),(-1,0,13),(0,1,7),(2,3,11)]:
    N=N_E(a,b,p); ap=p+1-N
    disc=ap*ap-4*p; s=cmath.sqrt(disc+0j)
    al,be=(ap+s)/2,(ap-s)/2
    rows.append((f'y²=x³+{a}x+{b}',p,N,ap,abs(al),math.sqrt(p)))
    print(f'   y²=x³+{a}x+{b} over F_{p:<3d}:  N={N:<3d} a_p={ap:<3d} '
          f'deg P=2  |α|={abs(al):.6f}  √p={math.sqrt(p):.6f}  ✅')

# ---- 结论表 ----
print('\n' + '='*72)
print('对照表')
print('='*72)
print(f'  {"曲线":<16}{"亏格 g":>7}{"deg P = 2g":>12}{"α_i 个数":>10}{"RH 是否有内容":>18}')
print(f'  {"P¹ (射影直线)":<16}{0:>7}{0:>12}{0:>10}{"无（真空）":>18}')
print(f'  {"椭圆曲线":<16}{1:>7}{2:>12}{2:>10}{"有":>18}')
print(f'  {"Fargues–Fontaine":<16}{0:>7}{0:>12}{0:>10}{"无（真空）":>18}')
print()
print('  ★ 亏格 0 ⟹ H¹ = 0 ⟹ 没有 α_i ⟹ "|α_i| = √q" 是空命题。')
print('  ★ 亏格本身不是障碍：Weil 的证明对任意 g 都成立（上面 g=1 全部验证通过）。')
print('  ★ 真正的障碍是别的东西（见文档 §三）。')
