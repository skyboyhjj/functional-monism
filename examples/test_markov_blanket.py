"""验证马尔可夫毯双通道（Phase 1）的基本行为。

运行方式:
    python examples/test_markov_blanket.py

覆盖:
    1. a_goal 在原点处严格为 0
    2. 软死区：0 < ||psi|| < rho 时 a_goal 非零但幅度较小
    3. a_goal 在远处指向原点
    4. 行动状态 a 向 a_goal 指数衰减
    5. 均值耦合 mu_eff = gamma_a * a
    6. OU 向后兼容：逐步 step 与 generate_trajectory 随机数序列一致（mu_eff=0）
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from src.models.markov_blanket import MarkovBlanket
from src.models.ou_noise import OUNoise


def test_a_goal_origin():
    """验证 a_goal 在原点处严格为 0。"""
    blanket = MarkovBlanket(dim=2)
    a = blanket.a_goal(np.array([0.0, 0.0]))
    assert np.allclose(a, 0.0, atol=1e-12), f"原点处 a_goal 应为 0，实际 {a}"


def test_a_goal_soft_dead_zone():
    """验证软死区：0 < ||psi|| < rho 时 a_goal 非零但幅度较小。"""
    blanket = MarkovBlanket(dim=2, eta_a=1.0, rho=0.3, tau=0.5)
    near = blanket.a_goal(np.array([0.1, 0.0]))   # ||psi|| = 0.1 < rho = 0.3
    far = blanket.a_goal(np.array([1.0, 0.0]))    # ||psi|| = 1.0 > rho = 0.3
    assert np.linalg.norm(near) > 0, "软死区下 a_goal 不应严格为 0"
    assert np.linalg.norm(near) < np.linalg.norm(far), "近原点幅度应小于远点"


def test_a_goal_points_to_origin():
    """验证远处 a_goal 指向原点（与 psi 方向相反）。"""
    blanket = MarkovBlanket(dim=2)
    psi = np.array([2.0, 1.0])
    a = blanket.a_goal(psi)
    assert np.dot(a, psi) < 0, f"远处 a_goal 应指向原点（点积 < 0），实际 {a}"


def test_step_decay_toward_goal():
    """验证 a 向 a_goal 指数衰减（关闭噪声观察确定性方向）。"""
    blanket = MarkovBlanket(dim=2, kappa=0.15, beta=0.1, sigma_a=0.0)
    blanket.a = np.array([0.0, 0.0])
    psi = np.array([3.0, 0.0])
    goal = blanket.a_goal(psi)
    a1, _ = blanket.step(psi)
    assert np.dot(a1, goal) > 0, f"a 应朝 a_goal 移动，实际 a1={a1}, goal={goal}"


def test_get_mu_eff():
    """验证均值耦合 mu_eff = gamma_a * a。"""
    blanket = MarkovBlanket(dim=2, gamma_a=0.1)
    blanket.a = np.array([1.0, -2.0])
    mu_eff = blanket.get_mu_eff()
    assert np.allclose(mu_eff, np.array([0.1, -0.2])), f"mu_eff 计算错误: {mu_eff}"


def test_ou_backward_compat():
    """验证逐步 step 与 generate_trajectory 随机数序列完全一致（mu_eff=0）。"""
    steps = 100
    theta, sigma = 0.0139, 0.29

    np.random.seed(42)
    ref_ou = OUNoise(dim=2, theta=theta, sigma=sigma)
    ref = ref_ou.generate_trajectory(steps)

    np.random.seed(42)
    step_ou = OUNoise(dim=2, theta=theta, sigma=sigma)
    traj = np.zeros((steps, 2))
    for t in range(steps):
        traj[t] = step_ou.step()

    assert np.allclose(ref, traj), "逐步 step 与 generate_trajectory 不一致"


if __name__ == "__main__":
    tests = [
        test_a_goal_origin,
        test_a_goal_soft_dead_zone,
        test_a_goal_points_to_origin,
        test_step_decay_toward_goal,
        test_get_mu_eff,
        test_ou_backward_compat,
    ]
    for fn in tests:
        fn()
        print(f"✓ {fn.__name__} 通过")
    print("\n全部测试通过 ✅")