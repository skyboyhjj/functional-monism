"""基于泛函变分原理的 PDE 求解器。

将偏微分方程转化为泛函极值问题，利用 JAX 自动微分求解。
"""

import jax
import jax.numpy as jnp


class PDESolver:
    """泛函变分 PDE 求解器。

    将 PDE 转化为能量泛函的极小化问题。
    """

    def __init__(self, energy_functional):
        """
        Args:
            energy_functional: 能量泛函 E[u]，接受场函数 u 返回标量
        """
        self.energy = energy_functional
        self.grad_energy = jax.grad(energy_functional)

    def solve(self, u0, lr=0.01, steps=5000):
        """通过梯度下降求解 PDE。

        Args:
            u0: 初始场配置
            lr: 学习率
            steps: 迭代步数

        Returns:
            tuple: (解, 能量值, 求解轨迹)
        """
        u = u0
        trajectory = [u0]
        energies = [self.energy(u0)]

        for _ in range(steps):
            u = u - lr * self.grad_energy(u)
            trajectory.append(u)
            energies.append(self.energy(u))

        return u, energies[-1], jnp.stack(trajectory), jnp.array(energies)