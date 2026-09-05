"""决策模型：基于泛函极值原理的决策框架。

将决策过程建模为效用泛函的最小化/最大化问题。
"""

import jax.numpy as jnp
from src.core.functional import FunctionalEngine


def decision_cost(choice):
    """决策代价泛函：包含风险与收益的权衡。

    Args:
        choice: 决策变量向量

    Returns:
        float: 决策代价
    """
    risk = jnp.sum(choice ** 2) * 0.5
    reward = -jnp.sum(jnp.log(jnp.abs(choice) + 1.0))
    return risk + reward


def optimal_decision(initial_guess, lr=0.1, steps=500):
    """寻找最优决策。

    Args:
        initial_guess: 初始决策猜测
        lr: 学习率
        steps: 迭代步数

    Returns:
        tuple: (最优决策, 最小代价, 搜索轨迹)
    """
    engine = FunctionalEngine()
    psi = initial_guess
    trajectory = [initial_guess]

    for _ in range(steps):
        psi = engine.gradient_flow(decision_cost, psi, alpha=lr)
        trajectory.append(psi)

    return psi, decision_cost(psi), jnp.stack(trajectory)


if __name__ == "__main__":
    guess = jnp.array([1.0, 1.0])
    best, cost, traj = optimal_decision(guess)
    print(f"最优决策: {best}")
    print(f"最小代价: {cost:.4f}")