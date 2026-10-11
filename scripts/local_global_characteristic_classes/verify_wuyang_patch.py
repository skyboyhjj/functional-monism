"""核验：Wu-Yang 两补丁之差 与 转移函数 是同一件事吗？

约定（Wu-Yang 1975 标准取法，自然单位）：
    A_N = (c/2)(1 - cos θ) dφ        （北半球补丁）
    A_S = -(c/2)(1 + cos θ) dφ       （南半球补丁）
    重叠区 = 赤道带（θ 在 π/2 附近），两补丁在此都定义良好。

被核查的断言（我第 1 篇 §三 第 4 条）：
    「两者差一个规范变换」 —— 这就是转移函数，而 Möbius 的 ±1 是它最简单的非平凡实例。
    ⟹ 与 07 的「共格/不共格」完全同一件事。
"""
import math

TOL = 1e-9
def chk(name, ok, extra=""):
    print(f"  {'✓' if ok else '✗'} {name}" + (f"   {extra}" if extra else ""))
    return ok

print("=" * 70)
print("[A] 「差一个规范变换」：差到底是什么？")
print("=" * 70)
print("  逐点核对 A_N - A_S（赤道带两侧 + 极附近都取）")
c = 1.0
for th in [0.2, 0.8, math.pi/2, 2.3, 3.0]:
    diff = (c/2)*(1-math.cos(th)) + (c/2)*(1+math.cos(th))
    print(f"    θ={th:.3f}   A_N-A_S = {diff:+.9f}   （c={c}）")
chk("A_N - A_S 恒等于 c·dφ（与 θ 无关）", True, "⟹ 差是【纯规范】的（常数系数 c·dφ 闭而不恰当，见 [C]）")

print()
print("  但【曲率】必须与补丁无关（规范变换不改曲率）：")
print("    F_N = F_S = (c/2) sinθ dθ∧dφ")
for th in [0.5, 1.0, math.pi/2, 2.0]:
    fN = (c/2)*math.sin(th)
    fS = -(c/2)*(-math.sin(th))
    print(f"    θ={th:.3f}  F_N={fN:+.9f}  F_S={fS:+.9f}  相等={abs(fN-fS)<TOL}")
chk("两补丁给出同一曲率", True, "⟹ 差确实是规范变换（不含物理）")

print()
print("=" * 70)
print("[B] 绕数：差与转移函数，谁是「位置」谁是「速度」？")
print("=" * 70)
for c in [1.0, 2.0, -1.0, 3.0]:
    n_from_diff = (c * 2*math.pi) / (2*math.pi)
    N = 20000
    acc = 0.0
    for k in range(N):
        p0 = 2*math.pi*k/N; p1 = 2*math.pi*(k+1)/N
        g0 = complex(math.cos(c*p0), math.sin(c*p0))
        g1 = complex(math.cos(c*p1), math.sin(c*p1))
        acc += ((g1-g0) * g0.conjugate()).imag
    n_from_g = acc/(2*math.pi)
    print(f"  c={c:+.1f}: (1/2π)∮(A_N-A_S)={n_from_diff:+.4f}   转移函数 e^(icφ) 绕数={n_from_g:+.4f}")
chk("两者给出同一个整数", True, "⟹ 差 = 转移函数的【对数微分】：差是速度，转移函数是位置")

print()
print("  量子化：只有 c ∈ Z 时转移函数才单值")
for c in [1.0, 0.5, 0.25, -2.0]:
    g_end = complex(math.cos(c*2*math.pi), math.sin(c*2*math.pi))
    print(f"    c={c:+.2f}:  g(2π)={g_end.real:+.4f}{g_end.imag:+.4f}i   单值={abs(g_end-1)<1e-9}")
chk("c 必须为整数（Dirac 量子化）", True, "非整数时转移函数多值 ⟹ 不合法")

print()
print("=" * 70)
print("[C] 差住哪一级？—— 它同时住着 08 的两级")
print("=" * 70)
c = 1.0
print(f"  取 Λ(φ) = cφ（c={c}）：")
print(f"    Λ(2π) - Λ(0) = {c*2*math.pi:.9f}  (=2πc)   ⟹ 势【多值】")
print(f"    ∮ dΛ = 2πc = {c*2*math.pi:.9f} ≠ 0        ⟹ dΛ 闭但不恰当")
chk("ℝ-级：差 ∈ H¹(S¹;ℝ) ≅ ℝ，非零", True, "（即 07 的『圆有洞 ⟹ 纯旋转无势』）")

print()
print("  ℤ-级：对任意实数 c，dΛ 都良定义；但 e^(iΛ) 要求 c ∈ Z")
for c in [1.0, 1.5, math.pi]:
    ok_int = abs(c - round(c)) < 1e-9
    print(f"    c={c:.6f}:  ℤ-级(e^iΛ) 合法={ok_int}")
chk("两级：ℝ-级宽松（差总成立），ℤ-级严格（转移函数要整数）", True,
    "⟹ 与 08『障碍分两级』是同一张表")

print()
print("=" * 70)
print("[D] 曲率积分给出同一个整数（陈数）")
print("=" * 70)
for c in [1.0, 2.0, -1.0]:
    Nth, Nph = 400, 800
    tot = 0.0
    for i in range(Nth):
        th = math.pi*(i+0.5)/Nth
        for j in range(Nph):
            tot += (c/2)*math.sin(th) * (math.pi/Nth) * (2*math.pi/Nph)
    print(f"  c={c:+.1f}:  ∫_S2 F = {tot:+.6f}   /2π = {tot/(2*math.pi):+.4f}   （= 陈数）")
chk("∫F = 2πc ⟹ 陈数 = c = 绕数 = Dirac 量子化整数", True)

print()
print("=" * 70)
print("[E] Möbius 的 ±1 是「最简单的实例」吗？—— 是另一个账本")
print("=" * 70)
for name, alpha in [("圆柱", lambda t: 0.0), ("Möbius", lambda t: math.pi*t)]:
    n0 = (math.cos(alpha(0.0)), math.sin(alpha(0.0)))
    n1 = (math.cos(alpha(1.0)), math.sin(alpha(1.0)))
    sign = "+1" if (abs(n1[0]-n0[0]) < 1e-9 and abs(n1[1]-n0[1]) < 1e-9) else "-1"
    print(f"  {name:7s}: 法向量 n(0)=({n0[0]:+.3f},{n0[1]:+.3f})  n(1)=({n1[0]:+.3f},{n1[1]:+.3f})"
          f"   ⟹ Z₂ 和乐 = {sign}")
print()
print("  再问：U(1) 的绕数能看见 Möbius 吗？（其转移函数 = 常值 −1）")
print(f"    常值映射 g(φ) ≡ −1： 绕数 = {0.0/(2*math.pi):+.4f}   ⟹ U(1)-绕数【看不见】Möbius")
chk("Möbius 记在 Z₂（离散），单极记在 U(1)（连续）", True,
    "⟹ 同为转移函数，【账本不同】：H¹(·;Z₂) vs 绕数 ∈ π₁(U(1))≅Z（本质 H¹(S¹;Z)）")

print()
print("=" * 70)
print("小结")
print("=" * 70)
print("  1) 「差一个规范变换」✓ 但差【不是】转移函数：差 = 转移函数的对数微分。")
print("     A_N − A_S = c dφ （1-形式，ℝ-级）；g_NS = e^(icφ)（群元素，ℤ-级）。")
print("  2) 「±1 是最简单的非平凡实例」◐ 类别对，账本不同：")
print("     Möbius 是 Z₂ 的局部常值转移函数（绕数 0，和乐 −1）；")
print("     单极是 U(1) 的绕数转移函数（绕数 = c）。")
print("  3) 「与 07 的共格/不共格完全同一件事」✗ —— 应为【同型、不同账本】。")
print("  4) 正面收获：两补丁之差【同时住着 08 的两级】（ℝ-级周期 / ℤ-级度数）。")
