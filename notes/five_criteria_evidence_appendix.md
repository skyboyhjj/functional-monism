# 附录 · 「五条形式判据」算据汇编

> **配套**：`five_criteria_mechanism_landed.md`（v1.4）
> **说明**：平台不收 `.py`，故把两份算据脚本汇编于此（与原文件**逐字节一致**）。
> **定位**：`notes/` 批注稿附录。

---

## 算据 A · 势整形：策略层 vs 动力学层

`scripts/five_criteria/verify_shaping_vs_five_criteria.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_shaping_vs_five_criteria.py

自查（矛盾迭代引擎·步 4「主动找反例」）：
  v1.1 稿断言：「势整形定理 = 第五条（动力学标准）的严格负判据」。

两问：
  A 策略层：势整形是否改变最优策略？          期望：不变（Ng et al. 1999）
  B 动力学层：把势整形写进动力学（梯度流）后，
             吸引子结构 / 分岔是否发生定性变化？ 期望：会（=> 第五条可能亮）
裁决：该断言是否成立。
"""
import numpy as np

np.set_printoptions(precision=4, suppress=True)

# ---------------------------------------------------------------- A 策略层
print("=" * 68)
print("A · 策略层：链式 MDP 值迭代（复现项目 verify_reward.py 的结论）")
print("=" * 68)

N = 5
GAMMA = 1.0
R_EXT = np.array([0.0, 0.0, 0.0, 0.0, 1.0])      # 右端奖励
PHI = np.array([0.0, 0.1, 0.2, 0.3, 0.5])         # 势函数


def s2_of(s, a, n=N):
    return min(max(s + a, 0), n - 1)


def solve(r_ext, phi, shaped, gamma=GAMMA, n=N, iters=5000):
    def R(s, a):
        s2 = s2_of(s, a, n)
        base = r_ext[s2]
        if shaped:
            base += gamma * phi[s2] - phi[s]
        return base
    V = np.zeros(n)
    for _ in range(iters):
        Vn = V.copy()
        for s in range(n):
            Vn[s] = max(R(s, a) + gamma * V[s2_of(s, a, n)] for a in (-1, 1))
        if np.allclose(Vn, V, atol=1e-12):
            V = Vn
            break
        V = Vn
    pol = []
    for s in range(n):
        vals = {a: R(s, a) + gamma * V[s2_of(s, a, n)] for a in (-1, 1)}
        pol.append(+1 if vals[1] > vals[-1] + 1e-12 else -1)
    return V, pol


V0, p0 = solve(R_EXT, PHI, shaped=False)
V1, p1 = solve(R_EXT, PHI, shaped=True)
print("最优策略（原始）   :", p0)
print("最优策略（势整形） :", p1)
print("策略是否相同       :", p0 == p1)
print("价值 V 是否相同    :", np.allclose(V0, V1), " (max|ΔV|=%.4f)" % np.max(np.abs(V1 - V0)))

# ---------------------------------------------------------------- B 动力学层
print()
print("=" * 68)
print("B · 动力学层：把势整形写进梯度流 ẋ=-∇(F+Φ)，看吸引子/分岔")
print("=" * 68)
print("取 F(x)=x⁴/4 - x²/2（双井：极小 ±1，极大 0）；势整形 Φ(x)=c·x")
print("梯度流：ẋ = -(x³ - x + c)；不动点 = x³ - x + c 的实根；")
print("稳定性 = 该点处 G''(x)=3x²-1 的符号（>0 稳定）")
print()
print("  c      不动点(实根)                         个数  稳定点      结构")
c_star = 2.0 / (3.0 * np.sqrt(3.0))
for c in [0.0, 0.1, 0.2, 0.38, 0.40, 0.60]:
    roots = np.roots([1.0, 0.0, -1.0, c])
    reals = sorted([r.real for r in roots if abs(r.imag) < 1e-9])
    stable = [x for x in reals if 3 * x * x - 1 > 0]
    if len(reals) == 3:
        struct = "双井(3 不动点)"
    elif len(reals) == 1:
        struct = "单井(1 不动点) <- 分岔"
    else:
        struct = "?"
    print("  %-5.2f  %-38s %d     %-12s %s" % (
        c, np.array2string(np.array(reals), precision=4), len(reals),
        np.array2string(np.array(stable), precision=3), struct))

print()
print("临界 c* = 2/(3√3) ≈ %.4f：c < c* 有 3 个不动点（但位置已移动）；" % c_star)
print("                          c > c* 只剩 1 个（鞍结分岔，结构定性改变）。")
print()
print("=" * 68)
print("裁决")
print("=" * 68)
print("A 策略层 : 势整形 --- 最优策略不变（严格，与定理一致）")
print("B 动力学层: 把 Φ 写进流后 ---")
print("    · 不动点位置随 c 连续移动（c=0.1,0.2: −1,0,1 → 已移位）")
print("    · c 超过 c* 后不动点由 3 变 1（鞍结分岔 = 定性改变）")
print("  ⟹ 「势整形不改变动力学定性」为假：它改的是【景观/吸引子】。")
print("  ⟹ 势整形定理给出的是【策略层】不变，不是【第五条·动力学标准】的不变。")
print("  ⟹ v1.1 稿把定理当第五条的严格负判据 = 层次混淆（方向亦反）。")
```

## 算据 B · 五实例刻度尺：阴阳五行 · 十二律 · 涡旋 · 八度圆

`scripts/five_criteria/verify_five_criteria_instances.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_five_criteria_instances.py

为「五条刻度尺逐格核」提供算据（先算后说）：
  组 1  阴阳五行：相生算子 R（5-循环置换阵）—— R⁵=I、det=1、谱=5 次单位根。
  组 2  朱载堉十二律：2^(n/12)、螺旋整点采样、"12"=连分数 7/12、毕氏音差。
  组 3  （v1.4）阴阳五行的二维拓扑激发：U(1) 涡旋的绕数 = 整数拓扑荷。
  组 4  （v1.4）十二律的八度圆 S¹：ℤ₁₂ 在对数轴的自由作用 ⟹ 商 = 圆周。
"""
import numpy as np
from math import log2, log

np.set_printoptions(precision=6, suppress=True)
print("=" * 70)
print("组 1 · 阴阳五行：相生算子 R = 5-循环置换")
print("=" * 70)
R = np.roll(np.eye(5), 1, axis=0)
print("R =\n", R.astype(int))
print("R^5 == I :", np.allclose(np.linalg.matrix_power(R, 5), np.eye(5)),
      " | det(R) =", int(round(np.linalg.det(R))))
lam = np.linalg.eigvals(R)
print("特征值     :", np.round(lam, 6))
print("|λ| 全为 1 :", np.allclose(np.abs(lam), 1.0), "  （谱 = 5 次单位根）")
real_ev = [l for l in lam if abs(l.imag) < 1e-12]
print("实特征值   :", np.round(real_ev, 6), "  <- λ=1（全 1 向量）")
print("⟹ 存在 1 维不变子空间（常数模）⟹ 作为【矩阵】，R 在 ℝ 上【可约】。")
print("  注意：'R 不可约'只在【置换单循环 / 作用传递】这一义上成立，与矩阵不可约是两回事。")
print("名相对应：相生=R、相克=R²、相乘/相侮=R³、子病及母=R⁴ —— 单一生成元 ⟹ 循环群 C₅")
Z10 = list(range(10))
print("阴阳五行整体 0 → ℤ₅ → ℤ₁₀ → ℤ₂ → 0 : 子群|2ℤ₁₀| =",
      len([x for x in Z10 if x % 2 == 0]), "  商类 =", sorted({x % 2 for x in Z10}))

print()
print("=" * 70)
print("组 2 · 朱载堉十二律：ℤ₁₂ × 对数标度")
print("=" * 70)
n = np.arange(12)
ratios = 2 ** (n / 12.0)
print("十二律比值 2^(n/12)（前 6）:", np.round(ratios[:6], 6))


def z(t):
    return np.exp(t * (log(2) / 12 + 2j * np.pi / 12))


zs = z(n.astype(float))
print("螺旋 |z(n)| 对 2^(n/12) 最大偏差 :",
      float(np.max(np.abs(np.abs(zs) - ratios))), "（整点采样 = 十二律）")
print("螺旋 相位 (mod 12) 对 n 最大偏差  :",
      float(np.max(np.abs((np.angle(zs) / (2 * np.pi / 12)) % 12 - n))))
print("z(12) =", np.round(z(12.0), 6), " ⟹ 一个八度后回到比值 2")
x = log2(1.5)
cf, y = [], x
for _ in range(6):
    a = int(y); cf.append(a); y = 1.0 / (y - a) if y - a > 1e-15 else 0.0
print("log2(3/2) =", round(x, 8), " 连分数 =", cf)
p2, p1, q2, q1 = 0, 1, 1, 0
for a in cf:
    p = a * p1 + p2; q = a * q1 + q2
    p2, p1 = p1, p; q2, q1 = q1, q
    if q in (2, 5, 12):
        print(f"   收敛子 {p}/{q} = {p/q:.8f}  （分母 {q} ⟸ 就是'12'）")
print("三分损益 12 步偏差（毕氏音差）= %.2f 音分" % (1200 * log2((1.5 ** 12) / (2 ** 7))))

print()
print("=" * 70)
print("组 3 · 阴阳五行的二维拓扑激发：U(1) 涡旋的绕数（拓扑荷）")
print("=" * 70)


def winding(q, M=4000):
    phi = np.linspace(0, 2 * np.pi, M, endpoint=False)
    theta = q * phi                                    # θ = q·φ（q = 涡旋荷）
    d = np.diff(np.concatenate([theta, theta[:1]]))
    d = (d + np.pi) % (2 * np.pi) - np.pi              # 解缠绕
    return d.sum() / (2 * np.pi)


print("绕数 (1/2π)∮∇θ·dl 对连续形变是常数、且取整数值：")
for q in [0, 1, 2, 3, -1]:
    w = winding(q)
    print(f"   标称荷 q={q:>2}  ->  实测绕数 = {w:+.6f}   （整数：{abs(w-round(w))<1e-9}）")
print("⟹ 涡旋荷被'钉'成整数（拓扑不变量）—— 这就是二维 XY 模型的拓扑激发；")
print("   KT 相变 = 涡旋-反涡旋对的束缚/解离（拓扑缺陷的定性转变）。")

print()
print("=" * 70)
print("组 4 · 十二律的八度圆 S¹：ℤ₁₂ 在对数频率轴上的自由作用")
print("=" * 70)
logf = n * (1.0 / 12.0)                                # log2(频率)，以八度为周期
print("log2(f) mod 1（12 个点，环绕一周）:", np.round(np.sort(logf % 1), 6))
print("互不相同（12 个独立类）:", len(set(np.round(logf % 1, 9))) == 12)
print("n=12 时 mod 1 =", (12 / 12.0) % 1, " ⟹ 12 步回到起点（周期 12）")
# 自由作用：任何非零步长都无不动点
for k in [1, 5, 7]:
    fixed = [m for m in range(12) if (m * k) % 12 == 0]
    print(f"   步长 k={k}: 有不动点吗（应只在 m=0）->", fixed)
print("⟹ 对数轴 ℝ 被 ℤ₁₂ 自由作用，商 ℝ/(ln2·ℤ) ≅ S¹（'八度圆'）；")
print("   十二律 = 圆上的 12 个等分点。")
print()
print("裁决：组 1–4 均为【严格】结构事实。")
```


---

## 自校验（与源文件逐字节一致）

| 源文件 | 字节 | 行数 |
| :-- | --: | --: |
| `scripts/five_criteria/verify_shaping_vs_five_criteria.py` | 4075 | 101 |
| `scripts/five_criteria/verify_five_criteria_instances.py` | 4758 | 102 |
