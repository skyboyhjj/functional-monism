"""Ornstein-Uhlenbeck 噪声过程 —— 带均值回归的随机游走。

v0.4: 将状态驱动从"高斯随机游走"升级为 OU 过程。

核心方程：
    dx = θ(μ - x)dt + σ · dW

    其中 θ 是回归速度，μ 是长期均值（通常为 0，即 breath_focus 原点），
    σ 是波动幅度。

参数语义：
    - theta ↑ → 回归力强 → 专家模式（注意力稳定）
    - theta ↓ → 回归力弱 → 新手模式（容易走神）
    - sigma ↑ → 波动大 → 走神剧烈
    - sigma ↓ → 波动小 → 走神温和
"""

import numpy as np
from typing import Optional, List


class OUNoise:
    """Ornstein-Uhlenbeck 噪声过程。

    产生带均值回归的连续随机轨迹。

    Attributes:
        dim: 状态空间维度。
        theta: 回归速度（越大 → 越快拉回均值）。
        mu: 长期均值（通常为 0，即 breath_focus 原点）。
        sigma: 波动幅度（扩散强度）。
        dt: 时间步长。
        state: 当前状态。
    """

    def __init__(
        self,
        dim: int = 2,
        theta: float = 0.15,
        mu: float = 0.0,
        sigma: float = 0.2,
        dt: float = 1.0,
    ):
        self.dim = dim
        self.theta = theta
        self.mu = mu
        self.sigma = sigma
        self.dt = dt
        self.state = np.zeros(dim)

    def reset(self, initial_state: Optional[np.ndarray] = None) -> np.ndarray:
        """重置状态。

        Args:
            initial_state: 初始状态，默认为原点。

        Returns:
            np.ndarray: 重置后的状态。
        """
        self.state = (
            initial_state.copy()
            if initial_state is not None
            else np.zeros(self.dim)
        )
        return self.state.copy()

    def step(self) -> np.ndarray:
        """执行一步 OU 更新。

        dx = θ(μ - x)dt + σ · dW

        Returns:
            np.ndarray: 更新后的状态。
        """
        dW = np.random.randn(self.dim) * np.sqrt(self.dt)
        dx = self.theta * (self.mu - self.state) * self.dt + self.sigma * dW
        self.state += dx
        return self.state.copy()

    def generate_trajectory(
        self,
        steps: int,
        initial_state: Optional[np.ndarray] = None,
        perturbations: Optional[List[tuple]] = None,
    ) -> np.ndarray:
        """生成完整轨迹。

        Args:
            steps: 轨迹步数。
            initial_state: 初始状态，默认为原点。
            perturbations: 扰动列表，每项为 (time, vector)，在指定时刻注入扰动。

        Returns:
            np.ndarray: 形状 (steps, dim) 的轨迹。
        """
        self.reset(initial_state)
        trajectory = np.zeros((steps, self.dim))

        # 构建扰动字典
        pert_dict = {}
        if perturbations:
            for t, vec in perturbations:
                pert_dict[t] = np.asarray(vec)

        for t in range(steps):
            if t in pert_dict:
                self.state += pert_dict[t]
            trajectory[t] = self.step()

        return trajectory

    @staticmethod
    def expert_params() -> dict:
        """专家模式推荐参数：高回归速度 + 低波动。"""
        return {"theta": 0.25, "sigma": 0.15}

    @staticmethod
    def novice_params() -> dict:
        """新手模式推荐参数：低回归速度 + 高波动。"""
        return {"theta": 0.08, "sigma": 0.30}

    @staticmethod
    def default_params() -> dict:
        """默认参数：中等回归 + 中等波动。"""
        return {"theta": 0.15, "sigma": 0.20}