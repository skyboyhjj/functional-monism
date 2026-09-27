"""圆上的耗散化：为什么纯圆无法耗散，如何补上

先算后说，四步：
1. 拓扑障碍：圆旋转 φ_t(θ)=θ+ωt，绕一圈势净增 2πω ≠ 0 ⟹ 无单值势
   （上同调：H^1(S^1)=R≠0，存在"闭但非恰当"的旋转 1-形式 dθ）。
2. 圆上引入梯度项 → Kuramoto 锁相 θ'=ω-γsinθ：γ>ω 时圆上出现吸引子。
3. Stuart-Landau：z'=(μ+iω)z-|z|²z，z=re^{iθ}
   → 相位 θ'=ω（守恒/圆旋转）+ 幅度 r'=μr-r³（耗散/实线梯度流）
   ⟹ 圆上的耗散化 = 补径向维度：C = R_{≥0} × S^1（幅度×相位）。
4. 对比 R(H^1=0，全有势，耗散免费) vs S^1(H^1=R，有纯旋转，耗散不免费)。

结论：圆上耗散化的障碍是拓扑的（H^1(S^1)=R）；解法是补径向维度（Hopf/Stuart-Landau）。
      保守↔耗散的桥 = 相位↔幅度的桥（角向↔径向）。
"""
import numpy as np

print("=" * 72)
print("1. 拓扑障碍：圆旋转无单值势（H^1(S^1) = R ≠ 0）")
print("=" * 72)
omega = 1.0
net = -omega * 2 * np.pi                    # ∮(-F')dθ = -2πω
print(f"  绕圆一周势变化 ∮(-F')dθ = -2πω = {net:.4f} ≠ 0")
print("  ⟹ 圆上不存在单值势 ⟹ 纯旋转不是梯度流 ⟹ 纯圆不可耗散。")

print()
print("=" * 72)
print("2. 圆上引入梯度项 → Kuramoto 锁相 θ' = ω - γ sinθ")
print("=" * 72)
for gamma in (0.5, 2.0):
    locked = gamma > omega
    th_star = np.arcsin(omega / gamma) if locked else None
    th, dt = -2.0, 0.01
    for _ in range(20000):
        th = th + dt * (omega - gamma * np.sin(th))
    tag = f"θ*={np.rad2deg(th_star):.1f}°(吸引子)" if locked else "不收敛(自由旋转)"
    print(f"  γ={gamma}: {'锁相' if locked else '自由旋转'}  "
          f"θ→{np.rad2deg(th) % 360:.1f}°，{tag}")
print("  ⟹ 加梯度项(-γsinθ)后，γ>ω 时圆上出现吸引子（耗散）；桥 = 外加强度 γ。")

print()
print("=" * 72)
print("3. Stuart-Landau：圆上的耗散化 = 补径向维度 C = R_{≥0} × S^1")
print("=" * 72)
def stuart_landau(mu, omega=1.0, z0=0.1 + 0j, dt=0.01, steps=5000):
    z, rs, ths, th = z0, [abs(z0)], [0.0], 0.0
    for _ in range(steps):
        z = z + dt * ((mu + 1j * omega) * z - abs(z) ** 2 * z)
        th += dt * omega                        # θ' = ω（解析，避免角绕卷）
        rs.append(abs(z)); ths.append(th)
    return np.array(rs), np.array(ths)
for mu in (-0.5, 1.0):
    rs, ths = stuart_landau(mu)
    dth = (ths[-1] - ths[0]) / ((len(ths) - 1) * 0.01)
    tag = "衰减到0(耗散，相位随之消没)" if mu < 0 else f"→√μ={np.sqrt(mu):.2f}极限环"
    print(f"  μ={mu:+.1f}: |z| {rs[0]:.3f}→{rs[-1]:.3f} ({tag})，θ'=ω={dth:.2f}")
print("  ⟹ 相位方向守恒(θ'=ω)、径向方向耗散(r'=μr-r³)。")
print("  ⟹ 圆上的耗散化 = 给圆补上径向(幅度)维度：C = R_{≥0} × S^1。")

print()
print("=" * 72)
print("4. 对比：R(全有势) vs S^1(有纯旋转)")
print("=" * 72)
print("  实线 R : H^1=0，一切向量场都是梯度(有势) ⟹ 耗散『免费』(阻尼 = 更多势)。")
print("  圆  S^1: H^1=R≠0，存在纯旋转(无势) ⟹ 耗散『不免费』(须破坏拓扑性)。")
print()
print("结论：圆上耗散化的障碍是拓扑的(H^1(S^1)=R)；")
print("      解法是补径向维度(C=R_{≥0}×S^1)，即 Hopf/Stuart-Landau：")
print("      相位旋转(保守) + 幅度梯度流(耗散)。")
print("      ⟹ 保守↔耗散的桥 = 相位↔幅度的桥（角向↔径向）。")
