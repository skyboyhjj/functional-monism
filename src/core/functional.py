"""泛函核心引擎。

基于 JAX 自动微分实现泛函变分、精度计算与梯度流演化。
"""

import jax
import jax.numpy as jnp


class FunctionalEngine:
    """泛函一元论核心计算引擎。

    利用 JAX 的自动微分能力，实现泛函 F[ψ] 的梯度、Hessian 计算，
    以及基于梯度流的演化步进。

    Attributes:
        _grad: JAX 编译后的梯度算子。
        _hessian: JAX 编译后的 Hessian 算子。
    """

    def __init__(self):
        pass

    def compute_gradient(self, F, psi):
        """计算泛函 F 对状态 ψ 的一阶变分导数（梯度）。

        根据公理 II（演化公理），δF/δψ 决定了泛函场的演化方向。

        Args:
            F: 泛函函数，签名为 F(psi) -> scalar，接受 jnp.ndarray 返回标量。
            psi: 状态向量或张量，jnp.ndarray。

        Returns:
            jnp.ndarray: 梯度 ∇F(ψ)，与 psi 同形状。

        Example:
            >>> engine = FunctionalEngine()
            >>> F = lambda psi: jnp.sum(psi ** 2)
            >>> psi = jnp.array([1.0, 2.0, 3.0])
            >>> engine.compute_gradient(F, psi)
            Array([2., 4., 6.], dtype=float32)
        """
        return jax.grad(F)(psi)

    def compute_precision(self, F, psi):
        """计算二阶变分导数——Hessian 矩阵的 Frobenius 范数，作为精度 γ。

        根据公理 III（精度公理），γ = ‖δ²F/δψ²‖ 度量了泛函在 ψ 处的
        局部曲率，即认知置信度。

        计算方式：
            1. 使用 jax.hessian 计算 Hessian 矩阵 H。
            2. 取 H 的 Frobenius 范数 ‖H‖_F = sqrt(∑_ij H_ij²)。

        Args:
            F: 泛函函数，签名为 F(psi) -> scalar。
            psi: 状态向量（1D）或张量，jnp.ndarray。

        Returns:
            float: 精度 γ = ‖H‖_F（Frobenius 范数）。

        Note:
            对于高维张量输入，Hessian 会先展平为矩阵再计算范数。

        Example:
            >>> engine = FunctionalEngine()
            >>> F = lambda psi: jnp.sum(psi ** 2)
            >>> psi = jnp.array([1.0, 2.0])
            >>> engine.compute_precision(F, psi)
            # H = diag(2, 2), ‖H‖_F = sqrt(4+4) ≈ 2.828
        """
        H = jax.hessian(F)(psi)

        # 将 Hessian 展平为 2D 矩阵再计算 Frobenius 范数
        H_flat = H.reshape(psi.size, psi.size)
        gamma = jnp.linalg.norm(H_flat, ord='fro')
        return float(gamma)

    def gradient_flow(self, F, psi, alpha):
        """执行梯度下降步进：ψ_{t+1} = ψ_t − α·∇F(ψ_t)。

        根据公理 II，泛函场沿负梯度方向演化为极小化作用量。

        Args:
            F: 泛函函数，签名为 F(psi) -> scalar。
            psi: 当前状态 ψ_t，jnp.ndarray。
            alpha: 步长（学习率），正标量。

        Returns:
            jnp.ndarray: 更新后的状态 ψ_{t+1}，与 psi 同形状。

        Example:
            >>> engine = FunctionalEngine()
            >>> F = lambda psi: jnp.sum(psi ** 2)
            >>> psi = jnp.array([1.0, 2.0])
            >>> engine.gradient_flow(F, psi, alpha=0.1)
            Array([0.8, 1.6], dtype=float32)
        """
        grad = jax.grad(F)(psi)
        return psi - alpha * grad