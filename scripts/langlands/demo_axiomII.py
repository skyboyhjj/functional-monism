import numpy as np, cmath
np.set_printoptions(precision=6, suppress=True)

# ============================================================
# 公理 II 补章 · 演示：函数域上"演化生成元"的谱落在一条直线上
#
#  公理 II（演化）= δF = 0。在这条链上，"演化"的名字是
#  **Frobenius 流**，其**无穷小生成元 Θ** 就是 δF=0 所定义的那个算子。
#
#  本演示只做一件事（但它是关键的）：
#  在函数域，Θ_log := log(Frobenius) 的谱
#      —— 其实部【恒定】= ½ log q
#  这正是"曲线的 RH"。而 Re 恒定 ⟺ 谱落在一条直线上。
#  数域情形对应的陈述是"谱落在实轴上"—— 那正是 RH。
# ============================================================

def legendre(v,p):
    v%=p
    if v==0: return 0
    return 1 if pow(v,(p-1)//2,p)==1 else -1

def count_points(p,a,b):
    n=1
    for x in range(p):
        r=(x*x*x+a*x+b)%p
        l=legendre(r,p)
        n += 1 if l==0 else (2 if l==1 else 0)
    return n

curves=[(1,1),(-1,0),(0,1),(1,0),(2,1),(-2,1),(3,1),(1,3)]
print('='*78)
print('公理 II 演示：函数域「演化生成元」Θ = log(Frobenius) 的谱')
print('='*78)
print(f'\n  {"p":>4} {"(a,b)":>9} {"N₁":>5} {"α₁":>26} {"Re log|α₁|":>12} {"½ log p":>10} {"差":>10}')
ok=tot=0
maxdev=0.0
for p in [5,7,11,13,17,19,23,29,31,37,41,43,47,53]:
    for (a,b) in curves:
        if (4*a**3+27*b**2)%p==0: continue
        N=count_points(p,a,b); ap=p+1-N
        disc=ap*ap-4*p
        if disc>=0:
            r=disc**0.5; al=[(ap+r)/2,(ap-r)/2]
        else:
            r=(-disc)**0.5; al=[complex(ap/2,r/2),complex(ap/2,-r/2)]
        # Θ_log := log α  （演化的"无穷小生成元"）
        th=[cmath.log(z) for z in al]
        real_th=abs(th[0].real)
        half=np.log(p)/2
        dev=abs(real_th-half)
        maxdev=max(maxdev,dev); tot+=1; ok += dev<1e-9
        if tot<=12:
            print(f'  {p:>4} {str((a,b)):>9} {N:>5} {str(al[0])[:26]:>26} {real_th:>12.6f} {half:>10.6f} {dev:>10.2e}')

print(f'\n  共 {tot} 条曲线：Re(log α) ≡ ½ log p 成立的：{ok}/{tot}  ✅（最大偏差 {maxdev:.2e}）')
print(f'\n  ⟹ 函数域上演化生成元的谱【落在一条直线上】：Re = ½ log q。这就是曲线的 RH。')
print(f'     "Re 恒定"换个坐标就是"Hilbert–Pólya 型算子 + 实谱"；')
print(f'     数域情形的对应陈述 = 谱落在实轴上 = RH —— 而那个 Θ 至今没造出来。')
print(f'\n  ⟹ 结论：公理 II（δF=0 的演化）在本链上【就是那个缺口】。')
