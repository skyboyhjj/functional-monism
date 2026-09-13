"""马尔可夫毯双通道：行动状态 a 与感知状态 ψ 的耦合（Phase 1）。

Phase 1 采用静态渗透性 κ，行动通道通过调制 OU 过程的均值实现"主动拉回"，
不破坏原有 OU 动力学（θ 与 σ 保持不变）。

核心方程：
    行动目标:   a_goal(ψ) = η_a · σ((‖ψ‖ − ρ) / τ) · (−ψ)
                其中 σ(x) = 1/(1+e^−x) 为 Sigmoid，提供软死区。
    行动更新:   a ← a − β·κ·(a − a_goal) + σ_a · dW
    均值耦合:   μ_eff = γ_a · a

参数语义：
    - κ（渗透性）：行动与内部状态的耦合强度（Phase 1 静态）。
    - β（行动步长）：行动状态向目标衰减的速率。
    - η_a（行动增益）：行动目标的最大幅度。
    - ρ（死区半径）：原点附近行动目标趋近 0（软死区，非硬死区）。
    - τ（过渡尺度）：Sigmoid 的平滑程度。
    - γ_a（均值耦合系数）：行动状态对 OU 有效均值 μ_eff 的影响。
"""

import numpy as np


class MarkovBlanket:
    """马尔可夫毯双通道：行动状态 a 与感知状态 psi 的耦合。

    Phase 1：静态渗透性 κ，行动通道调制 OU 均值。
    """

    def __init__(
        self,
        dim: int = 2,
        kappa: float = 0.15,
        beta: float = 0.1,
        sigma_a: float = 0.02,
        eta_a: float = 1.0,
        rho: float = 0.3,
        tau: float = 0.5,
        gamma_a: float = 0.1,
    ):
        """初始化马尔可夫毯。

        Args:
            dim: 状态空间维度（与 psi 相同）。
            kappa: 渗透性（耦合强度），Phase 1 静态。
            beta: 行动步长。
            sigma_a: 行动噪声。
            eta_a: 行动增益。
            rho: 死区半径。
            tau: 平滑过渡尺度。
            gamma_a: 行动对 OU 均值的影响系数。
        """
        self.dim = dim
        self.kappa = kappa
        self.beta = beta
        self.sigma_a = sigma_a
        self.eta_a = eta_a
        self.rho = rho
        self.tau = tau
        self.gamma_a = gamma_a
        self.a = np.zeros(dim)

    @staticmethod
    def _sigmoid(x):
        """数值稳定的 Sigmoid：1 / (1 + e^−x)。"""
        return 1.0 / (1.0 + np.exp(-x))

    def a_goal(self, psi) -> np.ndarray:
        """计算行动目标 a_goal(psi)。

        公式：a_goal = η_a · σ((‖ψ‖ − ρ) / τ) · (−ψ)

        软死区：仅当 ψ = (0,0) 时 a_goal 严格为 0；0 < ‖ψ‖ < ρ 时
        a_goal 非零但幅度较小。

        Returns:
            np.ndarray: 与 psi 同维的行动目标向量，指向原点（反向）。
        """
        psi = np.asarray(psi, dtype=float)
        norm = np.linalg.norm(psi)
        gain = self.eta_a * self._sigmoid((norm - self.rho) / self.tau)
        return -gain * psi

    def step(self, psi, dt: float = 1.0):
        """执行一步行动通道更新。

        公式：a ← a − β·κ·(a − a_goal) + σ_a·√dt·N(0,1)

        Returns:
            tuple: (更新后的行动状态 a, 调制后的 OU 均值 mu_eff)。
        """
        goal = self.a_goal(psi)
        noise = self.sigma_a * np.sqrt(dt) * np.random.randn(self.dim)
        self.a = self.a - self.beta * self.kappa * (self.a - goal) + noise
        return self.a.copy(), self.get_mu_eff()

    def get_mu_eff(self) -> np.ndarray:
        """返回当前调制的 OU 均值（供 OUNoise 使用）：μ_eff = γ_a · a。"""
        return self.gamma_a * self.a