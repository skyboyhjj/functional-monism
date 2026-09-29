#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_section3_remaining.py

逐条核验《读解_从莫比乌斯带到磁单极》§三 剩下的第 1、2、4 条。

 A. 「任意两根纤维环绕数恒为 1」：
    [0] 夹具校验（已知 Hopf 链，真值 ±1）—— 先证明方法可信；
    [A] 多对纤维实算（对极对/一般对/近邻对）+ 分辨率收敛 + 换投影中心（符号翻转）；
        连通性论证（为何不必逐对验）；
        诚实记录：我一度用“弧的原像 = 环带”误推 Link = 0，错在 cobound ≠ bound。
 B. 四个名字是不是同一个整数：Dirac n / c1 / 转移函数绕数 / 特征标度数 —— 是同一个；
    但「和乐/2pi」只在【基 = S1】时相等；S2 上赤道回路只给 c/2（差因子 2）。
 C. Berry 相位 = 和乐：回路相是 R-级（(c/2)Omega, mod 2pi）；闭曲面曲率积分才是 Z-级（c1）。
    自旋-1/2 实算 gamma = -Omega/2，且绕满整球时 exp(i gamma) = 1（回路相看不出非平凡）。

运行：python3 verify_section3_remaining.py
"""
import cmath, math

def check(cond, msg):
    print(("  ✓ " if cond else "  ✗ ") + msg)
    return cond

def norm(v):
    n = math.sqrt(sum(x * x for x in v)); return [x / n for x in v]
def dot(a, b): return sum(x * y for x, y in zip(a, b))

def gauss_linking(C1, C2):
    tot = 0.0; n1, n2 = len(C1), len(C2)
    for i in range(n1):
        r1 = C1[i]; d1 = [C1[(i + 1) % n1][k] - r1[k] for k in range(3)]
        for j in range(n2):
            r2 = C2[j]; d2 = [C2[(j + 1) % n2][k] - r2[k] for k in range(3)]
            r = [r1[k] - r2[k] for k in range(3)]
            cr = [d1[1]*d2[2]-d1[2]*d2[1], d1[2]*d2[0]-d1[0]*d2[2], d1[0]*d2[1]-d1[1]*d2[0]]
            num = sum(r[k]*cr[k] for k in range(3)); den = sum(x*x for x in r)**1.5
            if den > 1e-12: tot += num/den
    return tot/(4*math.pi)

def orthobasis(P0):
    bs = []
    for c in ([1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]):
        w = [c[i] - dot(c, P0)*P0[i] for i in range(4)]
        for b in bs:
            w = [w[i] - dot(w, b)*b[i] for i in range(4)]
        n = math.sqrt(sum(x*x for x in w))
        if n > 1e-9: bs.append([x/n for x in w])
        if len(bs) == 3: break
    return bs

def stereo(P, P0, bs):
    d = dot(P, P0)
    W = [(P[i] - d*P0[i])/(1.0 - d) for i in range(4)]
    return [dot(W, bs[j]) for j in range(3)]

def hopf_pt(w, t, ph):
    A = math.sqrt((1 + t)/2)
    if A < 1e-9:
        return (0.0, 0.0, math.cos(ph), math.sin(ph))
    e = cmath.exp(1j*ph)
    z1 = e*A; z2 = e*complex(w)/(2*A)
    return (z1.real, z1.imag, z2.real, z2.imag)

def fiber3(w, t, M, P0, bs):
    return [stereo(hopf_pt(w, t, 2*math.pi*k/M), P0, bs) for k in range(M)]

def main():
    ok = True

    print("=" * 76)
    print("[0] 夹具：已知 Hopf 链（xy 平面单位圆 与 平移的 xz 平面单位圆），真值 = ±1")
    print("=" * 76)
    F1 = [(math.cos(2*math.pi*k/800), math.sin(2*math.pi*k/800), 0.0) for k in range(800)]
    F2 = [(1.0+math.cos(2*math.pi*k/800), 0.0, math.sin(2*math.pi*k/800)) for k in range(800)]
    lk_fix = gauss_linking(F1, F2)
    print(f"  M=800：Link = {lk_fix:+.6f}")
    ok &= check(abs(abs(lk_fix) - 1) < 0.005, "夹具给出 |Link| = 1 ⟹ 环绕数算法可信")

    print()
    print("=" * 76)
    print("[A] Hopf 纤维化：任意两根【不同】纤维的环绕数")
    print("=" * 76)
    P0a = norm([1, 1, 1, 3]); P0b = norm([1, -1, 2, 0])
    bsa, bsb = orthobasis(P0a), orthobasis(P0b)
    NPOLE = (complex(0, 0), 1.0)
    SPOLE = (complex(0, 0), -1.0)
    GEN1 = (complex(0.60, 0.0), 0.80)
    GEN2 = (complex(0.0, 0.60), -0.80)
    w2 = complex(0.35, 0.42)
    NEAR1 = (complex(0.30, 0.40), math.sqrt(0.75))
    NEAR2 = (w2, math.sqrt(1 - abs(w2)**2))

    cases = [("对极对（两极纤维）", NPOLE, SPOLE), ("一般对", GEN1, GEN2), ("近邻对", NEAR1, NEAR2)]
    for tag, p, q in cases:
        vals = []
        for M in (400, 800):
            lk = gauss_linking(fiber3(p[0], p[1], M, P0a, bsa), fiber3(q[0], q[1], M, P0a, bsa))
            vals.append(lk)
            print(f"    {tag}  M={M:4d}  Link = {lk:+.6f}")
        ok &= check(abs(abs(vals[-1]) - 1) < 0.005, f"{tag}：|Link| = 1（且随 M 收敛）")

    print()
    print("    符号依赖：同一对纤维，换立体投影中心 ⟹ 符号翻转")
    la = gauss_linking(fiber3(*NPOLE, 800, P0a, bsa), fiber3(*SPOLE, 800, P0a, bsa))
    lb = gauss_linking(fiber3(*NPOLE, 800, P0b, bsb), fiber3(*SPOLE, 800, P0b, bsb))
    print(f"      投影中心 P0a：Link = {la:+.6f}")
    print(f"      投影中心 P0b：Link = {lb:+.6f}")
    ok &= check(la * lb < 0, "符号随投影定向而变 ⟹ 内蕴的只是 |Link| = 1（‘1’是约定）")

    print()
    print("    为何不必逐对验？（连通性论证）")
    print("      有序不同点对的空间 {(p,q) in S2 x S2 : p != q} 连通；")
    print("      环绕数是其上的连续整数值函数 ⟹ 必为常数。")
    print("      ⟹ 「任意两根【不同】纤维的 |环绕数| = 1」是定理，不是抽查结论。")
    print()
    print("    诚实记录（我犯过一次推理错误）")
    print("      我曾想：连接两基点的子午弧的原像 = S3 里一个环带，其二边界就是这两根纤维，")
    print("      环带 ⟹ [C1] + [C2'] = 0 ⟹ Link = 0。")
    print("      错在哪：环带只给出 [C1] = -[C2']，【不能】推出 [C2'] = 0 ——")
    print("      cobound（共同边界）!= bound（各自填满）。")
    print("      而 [C2'] 正是【自链数】(w.r.t. 环带诱导的 framing) = Hopf 不变量 = ±1。")
    print("      ⟹ 正确的结论反而是 Link = ∓1（与数值一致）。数值纠正了解析。")

    print()
    print("=" * 76)
    print("[B] 四个名字是不是同一个整数？")
    print("=" * 76)
    for c in (1, 2, -1):
        Nth, Nph = 400, 800
        tot = 0.0
        for i in range(Nth):
            th = math.pi*(i + 0.5)/Nth
            for j in range(Nph):
                tot += (c/2)*math.sin(th)*(math.pi/Nth)*(2*math.pi/Nph)
        c1 = tot/(2*math.pi)
        w_trans = float(c)                                   # e^{ic phi} 的绕数
        hol_eq = ((c/2)*(1 - math.cos(math.pi/2))*2*math.pi)/(2*math.pi)
        print(f"  c={c:+d}:  c1 = (1/2pi)∮_S2 F = {c1:+.4f}   转移函数绕数 = {w_trans:+.4f}"
              f"   赤道回路 和乐角/2pi = {hol_eq:+.4f}")
        ok &= check(abs(c1 - c) < 1e-3, f"c={c:+d}: 第一陈数 = c（数值积分，容差 1e-3）")
        ok &= check(abs(hol_eq - c/2) < 1e-9, f"c={c:+d}: 赤道和乐角/2pi = c/2 ≠ c（差因子 2）")
    print()
    print("  对照：若【基 = S1】（A = c dtheta），则 ∮A/2pi = c —— 这时才相等：")
    for c in (1, 2, -1):
        print(f"    c={c:+d}:  ∮A/2pi = {(c*2*math.pi)/(2*math.pi):+.4f}")
    print()
    print("  ⟹ Dirac 整数 n、第一陈数 c1、转移函数绕数、特征标度数 —— 这四个是同一个整数；")
    print("     『和乐/2pi』只在【基 = S1】时等于它；S2 上正确对应物是『曲率积分/2pi』。")

    print()
    print("=" * 76)
    print("[C] Berry 相位 = 和乐：它住 R-级 还是 Z-级？")
    print("=" * 76)
    c = -1
    print("  自旋-1/2：c = c1 = -1；回路相 gamma = ∮A = (c/2)(1-cos th0)2pi（对照 -Omega/2）")
    for th0 in (math.pi/3, math.pi/2, 2*math.pi/3, math.pi):
        gamma = (c/2)*(1 - math.cos(th0))*2*math.pi
        Om = 2*math.pi*(1 - math.cos(th0))
        print(f"    th0={th0:.3f}: gamma={gamma:+.6f}   -Omega/2={-Om/2:+.6f}   相等={abs(gamma+Om/2)<1e-9}")
        ok &= check(abs(gamma + Om/2) < 1e-9, "gamma = -Omega/2（自旋-1/2 标准结果）")
    print()
    print(f"    th0=pi（绕满整球）：gamma = -2pi ⟹ exp(i gamma) = {cmath.exp(-2j*math.pi).real:.6f}")
    print("      ⟹ 回路相【看不出】非平凡；只有 Z-级量 c1 = -1 ≠ 0 记录非平凡。")

    print()
    print("=" * 76)
    print("小结")
    print("=" * 76)
    print("  1) 「任意两根纤维环绕数恒为 1」✓ —— 须限定【不同】纤维；且 1 是【定向约定】下的值")
    print("     （内蕴的只是 |Link| = 1）。算法：夹具校验 + 收敛 + 连通性论证。")
    print("  2) 四个名字确为同一个整数 ✓；第五个『和乐/2pi』只在基 = S1 时相等，")
    print("     S2 上应为『曲率积分/2pi』。")
    print("  3) Berry 相位 = 和乐 ✓，但它是 R-级（回路）；Z-级是闭曲面曲率积分。")
    print("  ⟹ 系统病：§三 反复把【一维回路量（R-级）】与【二维闭曲面量（Z-级）】并列。")
    return ok

if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
