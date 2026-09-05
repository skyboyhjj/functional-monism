"""冥想状态模拟：泛函场的稳态演化。

将冥想状态建模为泛函场向低能稳态的收敛过程。
"""

import jax.numpy as jnp
from src.core.functional import FunctionalEngine


def meditation_energy(state):
    """冥想能量泛函：低能态对应平静状态。

    Args:
        state: 意识状态向量

    Returns:
        float: 能量值
    """
    return jnp.sum(state ** 2) + 0.1 * jnp.sum(jnp.sin(state * 5))


def simulate_meditation(initial_state, lr=0.05, steps=200):
    """模拟冥想过程：从初始状态向稳态收敛。

    Args:
        initial_state: 初始意识状态
        lr: 收敛速率
        steps: 冥想步数

    Returns:
        tuple: (最终稳态, 最终能量, 演化轨迹)
    """
    engine = FunctionalEngine()
    psi = initial_state
    trajectory = [initial_state]

    for _ in range(steps):
        psi = engine.gradient_flow(meditation_energy, psi, alpha=lr)
        trajectory.append(psi)

    return psi, meditation_energy(psi), jnp.stack(trajectory)


if __name__ == "__main__":
    state0 = jnp.array([3.0, -2.0, 1.0])
    final, energy, traj = simulate_meditation(state0)
    print(f"初始状态: {state0}")
    print(f"稳态: {final}")
    print(f"能量: {energy:.4f}")