"""Thoughtseed：基于预期自由能（EFE）的认知种子竞争模型。

将每个认知假设建模为一个"思想种子"，种子之间通过 EFE 近似计算
进行赢家通吃（Winner-Take-All）竞争。被激活的种子驱动当前认知状态
向核心吸引子收敛。
"""

import jax.numpy as jnp


class Thoughtseed:
    """认知种子：泛函场上的局部吸引子。

    每个 Thoughtseed 代表一个潜在的认知假设，其核心吸引子 ψ_core
    定义了该假设的"理想状态"。精度 γ 度量该假设的置信度。

    Attributes:
        core_attractor: 核心吸引子状态 ψ_core ∈ ℝⁿ，jnp.ndarray。
        precision: 当前精度 γ > 0，标量。
        name: 可选的种子标识符。
    """

    def __init__(self, core_attractor, precision=1.0, name=None):
        """
        Args:
            core_attractor: 核心吸引子状态向量。
            precision: 初始精度 γ₀（默认 1.0）。
            name: 可选的种子名称。
        """
        self.core_attractor = jnp.asarray(core_attractor, dtype=jnp.float32)
        self.precision = float(precision)
        self.name = name or f"seed_{id(self):x}"
        self._active = False

    # ------------------------------------------------------------------
    # 预期自由能（Expected Free Energy, EFE）
    # ------------------------------------------------------------------

    def expected_free_energy(self, current_state=None):
        """计算当前种子的预期自由能 G。

        EFE 的近似形式：
            G = −γ · A + C

        其中：
            A = −‖ψ − ψ_core‖²    —— 准确性（负平方误差，越大越好）
            C = ln(γ)              —— 复杂度代价（精度越高，模型越复杂）

        因此：
            G = −γ · ‖ψ − ψ_core‖² + ln(γ)

        当 current_state 为 None 时，以 core_attractor 自身作为参考，
        此时 G = ln(γ)（纯复杂度代价，无误差）。

        Args:
            current_state: 当前全局状态 ψ，若为 None 则使用自身 attractor。

        Returns:
            float: 预期自由能 G。
        """
        if current_state is None:
            psi = self.core_attractor
        else:
            psi = jnp.asarray(current_state, dtype=jnp.float32)

        # 准确性：负平方误差（值越大 → 越接近 attractor）
        squared_error = jnp.sum((psi - self.core_attractor) ** 2)
        accuracy = -squared_error

        # 复杂度代价：精度越高，模型越复杂
        complexity = jnp.log(self.precision + 1e-12)

        # EFE = −γ · A + C（注意 A 已为负值，所以 −γ·A = γ·‖Δ‖²）
        G = -self.precision * accuracy + complexity

        return float(G)

    # ------------------------------------------------------------------
    # 赢家通吃竞争
    # ------------------------------------------------------------------

    def compete(self, neighbors, current_state=None):
        """基于 EFE 的赢家通吃竞争。

        计算自身与所有邻居种子的 EFE，EFE 最小者被激活，其余抑制。

        竞争规则：
            seed*.active = True   ⇔  G(seed*) = min{G(self), G(neighbor₁), ...}
            其他种子 .active = False

        Args:
            neighbors: 邻居 Thoughtseed 实例的列表。
            current_state: 当前全局状态 ψ（可选），用于计算 EFE 的准确性项。

        Returns:
            bool: 自身是否被激活（True = 激活，False = 抑制）。
        """
        # 收集所有竞争者（自身 + 邻居）
        all_seeds = [self] + list(neighbors)

        # 计算每个种子的 EFE
        energies = [seed.expected_free_energy(current_state) for seed in all_seeds]

        # 找到最低 EFE 的种子
        winner_idx = int(jnp.argmin(jnp.array(energies)))
        winner = all_seeds[winner_idx]

        # 赢家通吃：激活胜者，抑制其余
        for seed in all_seeds:
            seed._active = (seed is winner)

        return self._active

    # ------------------------------------------------------------------
    # 属性访问
    # ------------------------------------------------------------------

    @property
    def is_active(self):
        """当前种子是否处于激活状态。"""
        return self._active

    def __repr__(self):
        status = "ACTIVE" if self._active else "suppressed"
        return (f"Thoughtseed({self.name}, γ={self.precision:.3f}, "
                f"‖ψ_core‖={float(jnp.linalg.norm(self.core_attractor)):.2f}, "
                f"{status})")


# ------------------------------------------------------------------
# 辅助函数：批量竞争
# ------------------------------------------------------------------

def winner_take_all(seeds, current_state=None):
    """在种子集合中执行全局赢家通吃竞争。

    所有种子中 EFE 最低者被激活，其余全部抑制。

    Args:
        seeds: Thoughtseed 实例列表。
        current_state: 当前全局状态（可选）。

    Returns:
        Thoughtseed: 获胜的种子。
    """
    if not seeds:
        raise ValueError("seeds 列表不能为空")

    energies = [s.expected_free_energy(current_state) for s in seeds]
    winner_idx = int(jnp.argmin(jnp.array(energies)))
    winner = seeds[winner_idx]

    for s in seeds:
        s._active = (s is winner)

    return winner


def update_precision(seed, current_state, learning_rate=0.1):
    """基于当前状态更新种子的精度（贝叶斯学习）。

    精度更新规则：
        γ ← γ + η · ‖ψ − ψ_core‖²

    即：观测误差越大，精度增长越快（后验精度 = 先验精度 + 数据精度）。

    Args:
        seed: 要更新的 Thoughtseed。
        current_state: 当前全局状态 ψ。
        learning_rate: 学习率 η。

    Returns:
        float: 更新后的精度。
    """
    psi = jnp.asarray(current_state, dtype=jnp.float32)
    squared_error = jnp.sum((psi - seed.core_attractor) ** 2)
    seed.precision = seed.precision + learning_rate * float(squared_error)
    return seed.precision