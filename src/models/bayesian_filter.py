"""贝叶斯滤波器：基于泛函观点的状态估计。

将贝叶斯滤波解释为泛函场上的信息更新过程。
"""

import jax.numpy as jnp


class BayesianFilter:
    """泛函贝叶斯滤波器。

    状态估计视为泛函场上的概率密度演化。
    """

    def __init__(self, state_dim, observation_dim):
        """
        Args:
            state_dim: 状态空间维度
            observation_dim: 观测空间维度
        """
        self.state_dim = state_dim
        self.obs_dim = observation_dim
        self.belief = None

    def initialize(self, initial_belief):
        """初始化信念分布。

        Args:
            initial_belief: 初始概率密度函数
        """
        self.belief = initial_belief

    def predict(self, transition_model):
        """预测步：应用状态转移模型。

        Args:
            transition_model: 状态转移函数 f(x_t-1) -> x_t
        """
        self.belief = transition_model(self.belief)
        return self.belief

    def update(self, observation, likelihood):
        """更新步：融合观测信息。

        Args:
            observation: 观测值
            likelihood: 似然函数 p(z|x)

        Returns:
            更新后的信念分布
        """
        self.belief = self.belief * likelihood(observation, self.belief)
        self.belief = self.belief / jnp.sum(self.belief)
        return self.belief