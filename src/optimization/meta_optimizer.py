"""元优化器：基于 Tikhonov 正则化的自动参数校准。

v1.1: 使用网格搜索 + 细化策略（梯度自由优化），自动寻找最优的 θ 和 σ。
不同化于原始任务书中的 JAX grad 方案——冥想模拟是随机过程，不可微，
因此改用网格搜索 + 细化，更简单、可靠、可复现。

核心公式：
    min_{θ,σ} [ E(θ,σ) + α·‖θ‖² + β·‖σ‖² ]
    其中 E(θ,σ) = 模拟输出与 thoughtseeds_model 基准的误差

使用方式：
    from src.optimization.meta_optimizer import optimize_parameters
    theta_opt, sigma_opt, history = optimize_parameters()
"""

import sys
import os
import time
from typing import Dict, List, Tuple, Optional

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.models.workspace import create_default_seeds
from src.validation.metrics import calculate_dwell_times

# 避免循环导入，延迟导入 comparator
# from src.validation.comparator import run_functional_monism_simulation


# thoughtseeds_model 基准值（新手模式）
BENCHMARK = {
    "mind_wandering_ratio": 0.538,   # 53.8%
    "mind_wandering_dwell": 89.6,    # 89.6 步
}


def run_single_simulation(
    theta: float,
    sigma: float,
    gamma: float = 0.3,
    anchor: float = 1.0,
    steps: int = 2000,
    seed: int = 42,
    use_efe: bool = True,
) -> Dict[str, float]:
    """运行单次模拟，返回 mind_wandering 占比和驻留时间。

    这是对 run_functional_monism_simulation 的轻量包装，
    专门提取 MW 相关指标。

    Args:
        theta: OU 回归速度。
        sigma: OU 波动幅度。
        gamma: 全局精度。
        anchor: 呼吸锚定强度。
        steps: 模拟步数。
        seed: 随机种子。
        use_efe: 是否使用 EFE 竞争模式。

    Returns:
        dict: {"mw_ratio": float, "mw_dwell": float}
    """
    from src.validation.comparator import run_functional_monism_simulation

    res = run_functional_monism_simulation(
        gamma=gamma,
        anchor=anchor,
        steps=steps,
        theta=theta,
        sigma_ou=sigma,
        seed=seed,
        use_efe=use_efe,
        use_2d=True,
    )

    states = res["states"]
    total = len(states)
    mw_count = states.count("mind_wandering")
    mw_ratio = mw_count / total if total > 0 else 0.0

    dwell_stats = calculate_dwell_times(states)
    mw_dwell = dwell_stats.get("mind_wandering", {}).get("mean", 0.0)

    return {
        "mw_ratio": mw_ratio,
        "mw_dwell": mw_dwell,
    }


def simulate_with_params(
    theta: float,
    sigma: float,
    gamma: float = 0.3,
    anchor: float = 1.0,
    steps: int = 2000,
    n_runs: int = 20,
    seed: int = 42,
    use_efe: bool = True,
    verbose: bool = False,
) -> Dict[str, float]:
    """用给定的 θ 和 σ 运行多次模拟，返回平均指标。

    Args:
        theta: OU 回归速度。
        sigma: OU 波动幅度。
        gamma: 全局精度。
        anchor: 呼吸锚定强度。
        steps: 模拟步数。
        n_runs: 运行次数（推荐 20）。
        seed: 随机种子（每次运行递增）。
        use_efe: 是否使用 EFE 竞争模式。
        verbose: 是否打印进度。

    Returns:
        dict: {"mw_ratio": float, "mw_dwell": float}
    """
    all_ratios = []
    all_dwells = []

    for i in range(n_runs):
        metrics = run_single_simulation(
            theta=theta,
            sigma=sigma,
            gamma=gamma,
            anchor=anchor,
            steps=steps,
            seed=seed + i * 137,
            use_efe=use_efe,
        )
        all_ratios.append(metrics["mw_ratio"])
        all_dwells.append(metrics["mw_dwell"])

    mean_ratio = float(np.mean(all_ratios))
    mean_dwell = float(np.mean(all_dwells))

    if verbose:
        print(f"    θ={theta:.4f}, σ={sigma:.4f} → "
              f"MW={mean_ratio:.1%}, dwell={mean_dwell:.1f}")

    return {
        "mw_ratio": mean_ratio,
        "mw_dwell": mean_dwell,
    }


def meta_loss(
    theta: float,
    sigma: float,
    alpha: float = 1.0,
    beta: float = 0.5,
    metrics: Optional[Dict[str, float]] = None,
) -> Tuple[float, Dict[str, float]]:
    """元优化损失函数 = 拟合误差 + 正则项。

    Args:
        theta: OU 回归速度。
        sigma: OU 波动幅度。
        alpha: θ 正则化强度。
        beta: σ 正则化强度。
        metrics: 如果已计算过模拟指标，可传入避免重复计算。

    Returns:
        tuple: (loss, metrics_dict)
    """
    if metrics is None:
        metrics = simulate_with_params(theta, sigma)

    # 拟合误差（与 thoughtseeds_model 基准对比）
    error_ratio = (metrics["mw_ratio"] - BENCHMARK["mind_wandering_ratio"]) ** 2
    error_dwell = (metrics["mw_dwell"] - BENCHMARK["mind_wandering_dwell"]) ** 2

    # 归一化：让两项量级相当
    # MW 占比 0-1，平方后约 0.01-0.1；驻留 50-90，平方后约 2500-8000
    # 分别缩放使两者量级匹配
    fit_error = error_ratio * 100.0 + error_dwell / 100.0

    # 正则项：惩罚过大的参数（偏好简单解）
    reg_term = alpha * theta ** 2 + beta * sigma ** 2

    loss = float(fit_error + reg_term)
    return loss, metrics


def grid_search(
    theta_range: Tuple[float, float],
    sigma_range: Tuple[float, float],
    n_theta: int = 20,
    n_sigma: int = 20,
    alpha: float = 1.0,
    beta: float = 0.5,
    n_runs: int = 5,
    steps: int = 500,
    verbose: bool = True,
) -> List[Dict]:
    """在 (θ, σ) 网格上搜索，返回所有评估结果（按 loss 排序）。

    使用两阶段加速策略：
    - 粗搜索：n_runs=5, steps=500 (快速定位候选区域)
    - 细化验证：n_runs=20, steps=2000 (精确评估)

    Args:
        theta_range: (min, max) for θ。
        sigma_range: (min, max) for σ。
        n_theta: θ 方向网格点数。
        n_sigma: σ 方向网格点数。
        alpha: θ 正则化强度。
        beta: σ 正则化强度。
        n_runs: 每次评估的模拟次数（粗搜索用 5，细化用 20）。
        steps: 每次模拟的步数（粗搜索用 500，细化用 2000）。
        verbose: 是否打印进度。

    Returns:
        list[dict]: 按 loss 升序排列的结果列表。
    """
    theta_vals = np.linspace(theta_range[0], theta_range[1], n_theta)
    sigma_vals = np.linspace(sigma_range[0], sigma_range[1], n_sigma)

    total = n_theta * n_sigma
    est_per_point = 2.0 if steps >= 2000 else 0.5
    if verbose:
        print(f"  网格搜索: {n_theta}×{n_sigma} = {total} 个点 "
              f"({n_runs}runs × {steps}steps)")
        print(f"  θ ∈ [{theta_range[0]:.3f}, {theta_range[1]:.3f}]")
        print(f"  σ ∈ [{sigma_range[0]:.3f}, {sigma_range[1]:.3f}]")
        print(f"  预计耗时: ~{total * est_per_point:.0f} 秒")

    results = []
    count = 0
    t_start = time.time()

    for th in theta_vals:
        for sg in sigma_vals:
            metrics = simulate_with_params(
                float(th), float(sg), n_runs=n_runs, steps=steps,
            )
            loss, _ = meta_loss(float(th), float(sg), alpha, beta, metrics=metrics)
            results.append({
                "theta": float(th),
                "sigma": float(sg),
                "loss": loss,
                "mw_ratio": metrics["mw_ratio"],
                "mw_dwell": metrics["mw_dwell"],
                "ratio_error": abs(metrics["mw_ratio"] - BENCHMARK["mind_wandering_ratio"]),
                "dwell_error": abs(metrics["mw_dwell"] - BENCHMARK["mind_wandering_dwell"]),
            })
            count += 1
            if verbose and count % 50 == 0:
                elapsed = time.time() - t_start
                eta = elapsed / count * (total - count)
                print(f"    进度: {count}/{total} ({elapsed:.0f}s, ETA {eta:.0f}s)")

    results.sort(key=lambda r: r["loss"])

    if verbose:
        elapsed = time.time() - t_start
        print(f"  搜索完成: {elapsed:.1f}s")
        best = results[0]
        print(f"  最优: θ={best['theta']:.4f}, σ={best['sigma']:.4f}, "
              f"loss={best['loss']:.4f}, MW={best['mw_ratio']:.1%}, "
              f"dwell={best['mw_dwell']:.1f}")

    return results


def refine_search(
    best_theta: float,
    best_sigma: float,
    theta_step: float,
    sigma_step: float,
    n_theta: int = 10,
    n_sigma: int = 10,
    alpha: float = 1.0,
    beta: float = 0.5,
    n_runs: int = 20,
    steps: int = 2000,
    verbose: bool = True,
) -> List[Dict]:
    """在最优解附近进行细化搜索。

    使用全精度评估（n_runs=20, steps=2000）确保结果可靠。

    Args:
        best_theta: 粗搜索找到的最优 θ。
        best_sigma: 粗搜索找到的最优 σ。
        theta_step: 粗搜索的 θ 步长。
        sigma_step: 粗搜索的 σ 步长。
        n_theta: θ 方向细化点数。
        n_sigma: σ 方向细化点数。
        alpha: θ 正则化强度。
        beta: σ 正则化强度。
        n_runs: 每次评估的模拟次数（细化用 20）。
        steps: 每次模拟的步数（细化用 2000）。
        verbose: 是否打印进度。

    Returns:
        list[dict]: 按 loss 升序排列的结果列表。
    """
    # 在最优解周围 ±1 个粗步长范围内细化
    half_theta = theta_step * 1.2
    half_sigma = sigma_step * 1.2

    theta_range = (max(0.02, best_theta - half_theta),
                   min(0.15, best_theta + half_theta))
    sigma_range = (max(0.15, best_sigma - half_sigma),
                   min(0.50, best_sigma + half_sigma))

    if verbose:
        print(f"\n  细化验证: {n_theta}×{n_sigma} = {n_theta * n_sigma} 个点 "
              f"({n_runs}runs × {steps}steps)")
        print(f"  θ ∈ [{theta_range[0]:.4f}, {theta_range[1]:.4f}]")
        print(f"  σ ∈ [{sigma_range[0]:.4f}, {sigma_range[1]:.4f}]")

    return grid_search(
        theta_range=theta_range,
        sigma_range=sigma_range,
        n_theta=n_theta,
        n_sigma=n_sigma,
        alpha=alpha,
        beta=beta,
        n_runs=n_runs,
        steps=steps,
        verbose=verbose,
    )


def optimize_parameters(
    theta_init: float = 0.05,
    sigma_init: float = 0.28,
    alpha: float = 0.5,
    beta: float = 0.3,
    n_coarse: int = 20,
    n_refine: int = 10,
    verbose: bool = True,
) -> Tuple[float, float, List[Dict]]:
    """主入口：运行两级网格搜索，自动寻找最优的 θ 和 σ。

    策略：
        1. 粗搜索：在宽范围（θ: 0.02-0.15, σ: 0.15-0.50）上 20×20 网格
        2. 细化搜索：在最优解附近 10×10 网格

    Args:
        theta_init: 初始 θ（v0.9 最优值，仅用于显示对比）。
        sigma_init: 初始 σ（v0.9 最优值，仅用于显示对比）。
        alpha: θ 正则化强度。
        beta: σ 正则化强度。
        n_coarse: 粗搜索网格点数（每维度）。
        n_refine: 细化搜索网格点数（每维度）。
        verbose: 是否打印进度。

    Returns:
        tuple: (theta_opt, sigma_opt, history)
            history 是 (粗搜索 + 细化搜索) 的完整结果列表。
    """
    if verbose:
        print("=" * 60)
        print("v1.1 元优化器：Tikhonov 正则化自动校准 θ 和 σ")
        print("=" * 60)
        print(f"  目标: 匹配 thoughtseeds_model 新手模式基准")
        print(f"  基准: MW 占比 {BENCHMARK['mind_wandering_ratio']:.1%}, "
              f"MW 驻留 {BENCHMARK['mind_wandering_dwell']:.1f} 步")
        print(f"  v0.9 手工调参: θ={theta_init}, σ={sigma_init}")
        print(f"  正则化: α={alpha}, β={beta}")
        print()

    # 阶段 1: 粗搜索（快速模式：5 runs × 500 steps）
    if verbose:
        print("阶段 1: 粗搜索（5 runs × 500 steps）")
    coarse_results = grid_search(
        theta_range=(0.02, 0.15),
        sigma_range=(0.15, 0.50),
        n_theta=n_coarse,
        n_sigma=n_coarse,
        alpha=alpha,
        beta=beta,
        n_runs=5,
        steps=500,
        verbose=verbose,
    )

    best_coarse = coarse_results[0]

    # 计算粗搜索步长
    theta_step = (0.15 - 0.02) / (n_coarse - 1)
    sigma_step = (0.50 - 0.15) / (n_coarse - 1)

    # 阶段 2: 细化搜索
    if verbose:
        print(f"\n阶段 2: 细化验证（20 runs × 2000 steps） — 围绕 θ={best_coarse['theta']:.4f}, "
              f"σ={best_coarse['sigma']:.4f}")

    refine_results = refine_search(
        best_theta=best_coarse["theta"],
        best_sigma=best_coarse["sigma"],
        theta_step=theta_step,
        sigma_step=sigma_step,
        n_theta=n_refine,
        n_sigma=n_refine,
        alpha=alpha,
        beta=beta,
        n_runs=20,
        steps=2000,
        verbose=verbose,
    )

    best_refine = refine_results[0]

    # 合并历史
    all_results = coarse_results + refine_results
    all_results.sort(key=lambda r: r["loss"])

    if verbose:
        print("\n" + "=" * 60)
        print("优化完成")
        print("=" * 60)
        print(f"  v0.9 手工调参: θ={theta_init}, σ={sigma_init}")
        print(f"  v1.1 粗搜索:   θ={best_coarse['theta']:.4f}, "
              f"σ={best_coarse['sigma']:.4f}")
        print(f"  v1.1 细化搜索: θ={best_refine['theta']:.4f}, "
              f"σ={best_refine['sigma']:.4f}")
        print(f"  最优 MW 占比: {best_refine['mw_ratio']:.1%} "
              f"(基准 {BENCHMARK['mind_wandering_ratio']:.1%})")
        print(f"  最优 MW 驻留: {best_refine['mw_dwell']:.1f} 步 "
              f"(基准 {BENCHMARK['mind_wandering_dwell']:.1f} 步)")
        print(f"  占比误差: {best_refine['ratio_error']:.1%}")
        print(f"  驻留误差: {best_refine['dwell_error']:.1f} 步")

    return best_refine["theta"], best_refine["sigma"], all_results