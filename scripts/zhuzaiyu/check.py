import math
from math import sqrt, pi, log2

print("="*60)
print("① 勾股 / 律管长度（黄钟-蕤宾）")
print("="*60)
print("10*sqrt(2) =", 10*sqrt(2), " (文中 14.14213562373095)")
print("5*sqrt(2)  =", 5*sqrt(2), " (文中 7.071067811865475)")
print("回到黄正: 5sqrt2*sqrt2 =", 5*sqrt(2)*sqrt(2))
print("一致性:", abs(10*sqrt(2)-14.14213562373095) < 1e-12)

print()
print("="*60)
print("② 十二平均律比值 2^(n/12)（升）")
print("="*60)
for n in range(13):
    print(f"  n={n:2d}   2^(n/12) = {2**(n/12):.10f}")

print()
print("="*60)
print("③ 高精度 pi 近似（约率/密率）")
print("="*60)
print(f"  22/7    = {22/7:.10f}   误差 = {22/7 - pi:+.3e}")
print(f"  355/113 = {355/113:.10f}   误差 = {355/113 - pi:+.3e}")

print()
print("="*60)
print("④ 【找反例】黄金分割 phi 落在第'几律'？")
print("="*60)
phi = (1+sqrt(5))/2
print(f"  phi      = {phi:.10f} ;  1/phi = {1/phi:.10f}")
print(f"  log2(phi)   = {log2(phi):+.6f}  -> 律位(升,从黄钟) = {log2(phi)*12:+.3f}")
print(f"  log2(1/phi) = {log2(1/phi):+.6f}  -> 律位 = {abs(log2(1/phi))*12:.3f}")
print("  => phi 对应的律位约 8.33 / 3.67，【不是整数】——")
print("     所以 '姑洗=黄金分割点' 是【近似/巧合】，不是精确结构关系。")

print()
print("="*60)
print("⑤ 【找反例】纯五度 3/2 vs 平均律 2^(7/12)")
print("="*60)
print(f"  3/2      = {1.5:.10f}")
print(f"  2^(7/12) = {2**(7/12):.10f}")
print(f"  差(毕氏音差) = {1.5 - 2**(7/12):+.6f}  (~{((1.5/(2**(7/12))-1)*1200):.2f} 音分)")

print()
print("="*60)
print("⑥ 朱载堉大数：K 到底是谁?")
print("="*60)
Kt = 112246204830937298
print(f"  文中 K = {Kt}")
print(f"  2^(1/12)*1e17 = {2**(1/12)*1e17:.0f}   (半音比)")
print(f"  2^(1/6) *1e17 = {2**(1/6)*1e17:.0f}   (全音比)")
print(f"  => K 实为 2^(1/6) 放大 1e17（即'隔一律'的比），非 2^(1/12)。")

print()
print("="*60)
print("⑦ 【找反例】斐波那契相邻比 vs 十二律比")
print("="*60)
f=[1,1]
for _ in range(16): f.append(f[-1]+f[-2])
ratios=[f[i+1]/f[i] for i in range(1,14)]
print("  斐波那契相邻比:", [round(r,6) for r in ratios])
print("  十二律 2^(n/12):", [round(2**(n/12),6) for n in range(1,14)])
print("  => 两组比值【不相等】（一个趋向 phi=1.618，一个趋向 2），")
print("     '十二律耦合斐波那契' 只能是【同一黄金比背景下的并存】，非同一序列。")

print()
print("="*60)
print("⑧ 文章螺旋公式 P(n) 的笔误核查")
print("="*60)
print("  文中 P(n) = ((sqrt12*sqrt2)^n cos(n*pi/6), ..., n)")
print("  sqrt(12)*sqrt(2) =", sqrt(12)*sqrt(2), "  (太大，不像步长)")
print("  2^(1/12)         =", 2**(1/12), "  <- 与文中'半径按 2^(1/12) 增大'自洽")
print("  => '(sqrt12*sqrt2)^n' 应为 '2^(n/12)' 的笔误。")
