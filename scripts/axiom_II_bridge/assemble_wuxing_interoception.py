"""组装：五行(相位 S^1) + 内感受(幅度 R_ge0) → C 上的 Stuart-Landau（Hopf）

先算后说，四步：
1. 最小组装：Stuart-Landau z'=(μ+iω)z-|z|²z
   相位 θ'=ω（五行），幅度 r'=μr-r³（内感受）。
   —— 但两者【解耦】= 只是并置（C = 幅度×相位的平凡直积），不是真组装。
2. 耦合候选：Z_5-等变最低阶项 κ z̄⁴（保持五行 5 次对称的相位-幅度耦合）。
3a. 但 κ z̄⁴ 单独用会【发散】：四次项在 r 方程里是 +κr⁴cos5θ，无饱和 → r→∞。
    （复 GL 中 m 次共振项 z̄^{m-1} 破稳的经典性质，m=5）
3b. 加五次饱和 -δ|z|⁴z 后：既锁相（θ'→0，钉到 5 个离散相位）又有界。
    ⟹ 组装需要【共振项 + 饱和项】两项配合，不是一项搞定。
"""
import numpy as np

print("=" * 72)
print("1. 最小组装：Stuart-Landau（相位=五行，幅度=内感受）")
print("=" * 72)
def SL(mu, omega=1.0, z0=0.1 + 0j, dt=0.005, steps=8000):
    z = z0; rs = [abs(z0)]
    for _ in range(steps):
        z = z + dt * ((mu + 1j * omega) * z - abs(z) ** 2 * z)
        rs.append(abs(z))
    return np.array(rs)
for mu in (-0.5, 1.0):
    rs = SL(mu)
    print(f"  μ={mu:+.1f}: r {rs[0]:.2f}→{rs[-1]:.3f}（内感受/幅度），θ'=ω=1.00（五行/相位）")
print("  ⟹ 相位(五行)+幅度(内感受)装在 C 上；但两者解耦 = 只是【并置】。")

print()
print("=" * 72)
print("2. 耦合候选：Z_5-等变项 κ z̄⁴（五行 5 次对称的最低阶相位-幅度耦合）")
print("=" * 72)
w = np.exp(2j * np.pi / 5); z = 0.7 + 0.3j
fac = np.conj(w * z) ** 4 / (np.conj(z) ** 4)
print(f"  z̄⁴ 在 z→ωz 下的变换因子 = {np.round(fac, 3)}  (=ω ? {abs(fac - w) < 1e-9})")
print("  ⟹ κz̄⁴ 与 z 同变换，保持 Z_5 对称（合法的相位-幅度耦合，非随意加）。")

print()
print("=" * 72)
print("3. 组装：κz̄⁴ 单独发散，须配五次饱和 -δ|z|⁴z")
print("=" * 72)
def SL_coupled(kappa, delta, mu=1.0, omega=1.0, z0=1.0 + 0j, dt=0.001, steps=60000):
    z = z0; cum = 0.0; prev = np.angle(z0); rmax = abs(z0)
    for _ in range(steps):
        z = z + dt * ((mu + 1j * omega) * z - abs(z) ** 2 * z
                      - delta * abs(z) ** 4 * z + kappa * np.conj(z) ** 4)
        if not np.isfinite(abs(z)) or abs(z) > 1e6:
            return None, None, np.inf, None
        ang = np.angle(z); cum += (ang - prev + np.pi) % (2 * np.pi) - np.pi; prev = ang
        rmax = max(rmax, abs(z))
    return abs(z), cum / (steps * dt), rmax, np.angle(z)
for kappa, delta, tag in [(2.0, 0.0, "仅共振项"), (2.0, 1.0, "共振+饱和"),
                          (4.0, 1.0, "共振(强)+饱和")]:
    r_end, dth, rmax, th_end = SL_coupled(kappa, delta)
    if r_end is None:
        print(f"  κ={kappa}, δ={delta} ({tag}): ✗ 发散（r 爆掉）")
    else:
        ph = np.rad2deg(th_end) % 360
        off = min(abs((ph - 72 * k + 180) % 360 - 180) for k in range(5))
        print(f"  κ={kappa}, δ={delta} ({tag}): r→{r_end:.3f}, θ'≈{dth:+.3f} "
              f"({'锁相' if abs(dth) < 0.05 else '自由旋转'}), θ={ph:.1f}°(距72°倍数 {off:.1f}°)")
print("  ⟹ κz̄⁴ 单独用发散（四次项无饱和）；配 δ|z|⁴ 饱和后才既锁相又有界。")

print()
print("=" * 72)
print("结论")
print("=" * 72)
print("  五行(相位) + 内感受(幅度) → C 上的系统；")
print("  最小组装(SL)是解耦【并置】；真组装需 Z_5-等变耦合 κz̄⁴ + 五次饱和 -δ|z|⁴z。")
print("  效果：内感受(幅度)把五行(相位)钉到 5 个离散相位（锁相）。")
print("  诚实：① 单靠 κz̄⁴ 会发散（须配饱和）；② 钉住点有偏移（五行节律 vs 锁定张力）。")
