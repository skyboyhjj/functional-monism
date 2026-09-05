"""波粒二象性演示：固定精度 vs 自适应精度。

两组实验对比：
  1. 固定高 γ：模拟物理刚性（F=ma 下的简谐运动类比）
  2. 动态 γ：模拟认知适应性（贝叶斯更新，精度随观测递增）

泛函形式：F(x) = ½γ·x²  —— 势能井 / 预测误差
"""

import jax.numpy as jnp
import matplotlib.pyplot as plt
from src.core.functional import FunctionalEngine


def quadratic_potential(gamma):
    """构造二次泛函 F(x) = ½γ·x²。

    Args:
        gamma: 精度参数（曲率），标量。

    Returns:
        callable: F(x) -> scalar
    """
    return lambda x: 0.5 * gamma * jnp.sum(x ** 2)


def run_fixed_precision(engine, x0, gamma, alpha, steps):
    """固定精度演化：γ 恒定不变。

    模拟物理刚性——自然规律不因观测而改变。梯度下降在固定曲率的
    势能井中匀速收敛，轨迹呈指数衰减。

    Args:
        engine: FunctionalEngine 实例。
        x0: 初始状态。
        gamma: 固定精度值。
        alpha: 步长。
        steps: 迭代步数。

    Returns:
        tuple: (状态轨迹, 精度轨迹)
    """
    F = quadratic_potential(gamma)
    x = x0
    xs = [float(x0[0])]
    gammas = [gamma]

    for _ in range(steps):
        x = engine.gradient_flow(F, x, alpha)
        xs.append(float(x[0]))
        gammas.append(gamma)

    return jnp.array(xs), jnp.array(gammas)


def run_adaptive_precision(engine, x0, gamma_0, gamma_rate, alpha, steps):
    """自适应精度演化：γ 随观测递增。

    模拟认知适应性——贝叶斯更新中，后验精度 = 先验精度 + 观测精度。
    每步获得新观测后，精度线性增长：γ_t = γ_0 + η·t。

    这导致早期大步探索（低精度 → 小梯度），后期精细收敛（高精度 → 大梯度）。

    Args:
        engine: FunctionalEngine 实例。
        x0: 初始状态。
        gamma_0: 初始精度。
        gamma_rate: 精度增长率 η。
        alpha: 步长。
        steps: 迭代步数。

    Returns:
        tuple: (状态轨迹, 精度轨迹)
    """
    x = x0
    xs = [float(x0[0])]
    gammas = [gamma_0]

    for t in range(steps):
        gamma_t = gamma_0 + gamma_rate * t
        F = quadratic_potential(gamma_t)
        x = engine.gradient_flow(F, x, alpha)
        xs.append(float(x[0]))
        gammas.append(gamma_t)

    return jnp.array(xs), jnp.array(gammas)


def plot_comparison(xs_fixed, gammas_fixed, xs_adaptive, gammas_adaptive, alpha):
    """绘制固定精度与自适应精度的对比图。

    上子图：状态轨迹 x(t)
    下子图：精度演化 γ(t)
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    steps = len(xs_fixed) - 1
    t = jnp.arange(steps + 1)

    # --- 上子图：状态轨迹 ---
    ax1.plot(t, xs_fixed, 'b-', linewidth=2, label='Fixed γ (Physical Rigidity)')
    ax1.plot(t, xs_adaptive, 'r--', linewidth=2, label='Adaptive γ (Bayesian Updating)')
    ax1.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
    ax1.set_ylabel('State $x$', fontsize=12)
    ax1.set_title('Functional Monism: Duality of Fixed vs Adaptive Precision', fontsize=13)
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)

    # --- 下子图：精度演化 ---
    ax2.plot(t, gammas_fixed, 'b-', linewidth=2, label=f'Fixed γ = {gammas_fixed[0]:.1f}')
    ax2.plot(t, gammas_adaptive, 'r--', linewidth=2,
             label=f'Adaptive γ (γ₀={gammas_adaptive[0]:.1f}, η={gammas_adaptive[-1] - gammas_adaptive[0]:.1f}/{steps})')
    ax2.set_xlabel('Step $t$', fontsize=12)
    ax2.set_ylabel('Precision $\\gamma$', fontsize=12)
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('duality_demo.png', dpi=150)
    plt.show()


def main():
    # --- 参数设置 ---
    x0 = jnp.array([3.0])       # 初始状态
    alpha = 0.08                 # 步长
    steps = 80                   # 迭代步数
    gamma_fixed = 5.0            # 固定精度（高刚性）
    gamma_0 = 0.5                # 自适应初始精度
    gamma_rate = 0.15            # 精度增长率

    engine = FunctionalEngine()

    print("=" * 60)
    print("Functional Monism — Duality Demo")
    print("=" * 60)
    print(f"  Functional:  F(x) = ½γ·x²")
    print(f"  Initial state: x₀ = {float(x0[0]):.2f}")
    print(f"  Step size: α = {alpha}")
    print(f"  Steps: {steps}")
    print()

    # --- 实验 1：固定精度 ---
    print("Experiment 1: Fixed High Precision (Physical Rigidity)")
    print(f"  γ = {gamma_fixed} (constant)")
    xs_fixed, gammas_fixed = run_fixed_precision(
        engine, x0, gamma_fixed, alpha, steps
    )
    print(f"  Final state: x = {float(xs_fixed[-1]):.6f}")
    print(f"  Precision at final: γ = {gamma_fixed}")
    print()

    # --- 实验 2：自适应精度 ---
    print("Experiment 2: Adaptive Precision (Bayesian Updating)")
    print(f"  γ₀ = {gamma_0}, η = {gamma_rate}")
    xs_adaptive, gammas_adaptive = run_adaptive_precision(
        engine, x0, gamma_0, gamma_rate, alpha, steps
    )
    print(f"  Final state: x = {float(xs_adaptive[-1]):.6f}")
    print(f"  Final precision: γ = {float(gammas_adaptive[-1]):.2f}")
    print()

    # --- 对比 ---
    print("Comparison:")
    print(f"  Fixed:    x({steps}) = {float(xs_fixed[-1]):.6f}")
    print(f"  Adaptive: x({steps}) = {float(xs_adaptive[-1]):.6f}")
    print()

    # --- 可视化 ---
    plot_comparison(xs_fixed, gammas_fixed, xs_adaptive, gammas_adaptive, alpha)


if __name__ == "__main__":
    main()