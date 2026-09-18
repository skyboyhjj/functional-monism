import mpmath as mp
mp.mp.dps = 30

def Lambda(n):
    N=n; d=2; facs=[]
    while d*d<=N:
        if N%d==0:
            facs.append(d)
            while N%d==0: N//=d
        d+=1
    if N>1: facs.append(N)
    if facs and len(set(facs))==1: return mp.log(facs[0])
    return mp.mpf(0)

def psi_arith(x):
    return sum((Lambda(n) for n in range(2,int(x)+1)), mp.mpf(0))

def psi_spec(x, zeros):
    x=mp.mpf(x)
    base = x - mp.log(2*mp.pi) - mp.log(1-x**-2)/2
    tot=mp.mpf(0)
    for g in zeros:
        rho = mp.mpf('0.5')+1j*g
        tot += 2*mp.re(mp.power(x,rho)/rho)
    return base-tot

print('取前 100 个零点 …')
zeros=[mp.im(mp.zetazero(k)) for k in range(1,101)]
print('  γ_100 =', mp.nstr(zeros[-1],8))
print()
print(' x   算术侧 ΣΛ(n)        谱侧(100 零点)      相对误差')
for X in [10, 20, 30, 50]:
    e=psi_arith(X); v=psi_spec(X,zeros)
    rel=abs(v-e)/e
    print(f'{X:3d}   {mp.nstr(e,12):>16}   {mp.nstr(v,12):>16}   {mp.nstr(rel,4)}')
