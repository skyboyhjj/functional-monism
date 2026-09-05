"""全局工作空间：冥想状态模拟器的多种子竞争引擎。

基于"泛函一元论"公理体系，将意识建模为多个思维种子在全局工作空间中
的竞争过程。激活值最高的种子胜出，占据当前意识的"聚光灯"。

使用方式:
    from src.models.workspace import MeditationSeed, GlobalWorkspace

    seeds = [
        MeditationSeed("Breath Focus", [0.0]),
        MeditationSeed("Pain Discomfort", [2.0]),
    ]
    workspace = GlobalWorkspace(seeds)
    activations, dominant = workspace.compete(current_state, gamma=1.0)
"""

import jax.numpy as jnp
from src.core.functional import FunctionalEngine


class MeditationSeed:
    """冥想场景中的思维种子。

    每个种子代表一个潜在的认知内容（呼吸、杂念、身体感受等），
    通过核心吸引子 ψ_core 定义其"理想状态"。

    公理 I（存在公理）：种子能量定义为
        E(ψ) = ½ ‖ψ − ψ_core‖²

    公理 III（精度公理）：激活值受全局精度 γ 调制
        a = exp(−γ · E)

    Attributes:
        name: 种子名称（如 "Breath Focus"）。
        core_attractor: 核心吸引子状态，jnp.ndarray。
        activation: 当前激活值 a ∈ [0, 1]，越高越接近意识中心。
        precision_boost: 注意力锚定增强因子（>= 1.0），用于模拟刻意专注。
    """

    def __init__(self, name, core_attractor, initial_activation=0.0):
        self.name = name
        self.core_attractor = jnp.asarray(core_attractor, dtype=jnp.float32)
        self.activation = float(initial_activation)
        self.precision_boost = 1.0
        self.engine = FunctionalEngine()

    def compute_energy(self, current_state):
        """计算种子在当前状态下的泛函能量。

        公理 I：E(ψ) = ½ ‖ψ − ψ_core‖²
        离核心吸引子越远，能量越高 → 激活越低。

        Args:
            current_state: 当前全局状态 ψ，标量或 jnp.ndarray。

        Returns:
            float: 泛函能量值。
        """
        psi = jnp.asarray(current_state, dtype=jnp.float32)
        delta = psi - self.core_attractor
        return 0.5 * float(jnp.sum(delta ** 2))

    def update_activation(self, current_state, global_gamma):
        """基于全局精度更新激活值。

        公理 III：激活值 a = exp(−γ_eff · E)
        其中 γ_eff = global_gamma × precision_boost（注意力锚定放大）。

        Args:
            current_state: 当前全局状态。
            global_gamma: 全局精度 γ > 0。

        Returns:
            float: 更新后的激活值 a ∈ [0, 1]。
        """
        energy = self.compute_energy(current_state)
        effective_gamma = global_gamma * self.precision_boost
        self.activation = float(jnp.exp(-effective_gamma * energy))
        return self.activation

    def __repr__(self):
        return (f"MeditationSeed({self.name}, "
                f"ψ_core={float(self.core_attractor.ravel()[0]):.1f}, "
                f"a={self.activation:.3f})")


class GlobalWorkspace:
    """全局工作空间：管理多个冥想种子的竞争。

    模拟意识中多思维内容的并行竞争过程。每一时间步，
    所有种子更新激活值，最高者胜出成为"当前意识内容"。

    Attributes:
        seeds: MeditationSeed 实例列表。
        dominant_seed: 当前胜出种子（MeditationSeed 或 None）。
    """

    def __init__(self, seeds):
        self.seeds = list(seeds)
        self.dominant_seed = None

    def compete(self, current_state, global_gamma):
        """执行一轮种子竞争。

        1. 每个种子基于当前状态和全局精度更新激活值。
        2. 赢家通吃：激活值最高者胜出。

        Args:
            current_state: 当前全局状态 ψ。
            global_gamma: 全局精度 γ > 0。

        Returns:
            tuple: (activations_dict, dominant_seed)
                - activations_dict: {seed_name: activation_value}
                - dominant_seed: 胜出的 MeditationSeed 实例
        """
        activations = {}
        for seed in self.seeds:
            activations[seed.name] = seed.update_activation(
                current_state, global_gamma
            )

        # 赢家通吃
        winner_name = max(activations, key=activations.get)
        self.dominant_seed = next(
            s for s in self.seeds if s.name == winner_name
        )
        return activations, self.dominant_seed

    def get_activation_array(self):
        """返回所有种子激活值的 numpy 数组，便于可视化。

        Returns:
            list[float]: 按 seeds 顺序排列的激活值列表。
        """
        return [s.activation for s in self.seeds]

    def __repr__(self):
        if self.dominant_seed:
            return (f"GlobalWorkspace(seeds={len(self.seeds)}, "
                    f"dominant={self.dominant_seed.name})")
        return f"GlobalWorkspace(seeds={len(self.seeds)}, dominant=None)"


# ------------------------------------------------------------------
# 预设种子配置
# ------------------------------------------------------------------

def create_default_seeds():
    """创建冥想模拟器的默认 5 种子配置。

    Returns:
        list[MeditationSeed]: 预设种子列表。
    """
    return [
        MeditationSeed("Breath Focus", [0.0]),
        MeditationSeed("Pain Discomfort", [2.0]),
        MeditationSeed("Pending Tasks", [3.5]),
        MeditationSeed("Self Reflection", [5.0]),
        MeditationSeed("Equanimity", [-1.0]),
    ]