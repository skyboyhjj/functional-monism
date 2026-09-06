"""对比引擎：运行 functional-monism 模拟，与 thoughtseeds_model 数据对比。

v0.4: 集成 Ornstein-Uhlenbeck 噪声，支持 theta/sigma 参数扫描。
"""

import sys
import os
from typing import Dict, List, Tuple, Optional

import numpy as np
import jax.numpy as jnp

# 确保可以导入项目模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.models.workspace import (
    MeditationSeed,
    GlobalWorkspace,
    create_default_seeds,
)
from src.models.ou_noise import OUNoise
from .data_loader import THOUGHTSEED_NAMES, MEDITATION_STATES
from .metrics import extract_all_metrics


def run_functional_monism_simulation(
    gamma: float = 1.0,
    anchor: float = 1.0,
    steps: int = 200,
    perturbation_strength: float = 0.0,
    perturbation_time: int = 160,
    seed: int = 42,
    use_efe: bool = False,
    use_2d: bool = False,
    dim: int = 2,
    theta: float = 0.15,
    sigma_ou: float = 0.20,
) -> Dict[str, object]:
    """运行 functional-monism 冥想模拟。

    v0.4: 使用 Ornstein-Uhlenbeck 噪声驱动状态，支持 theta/sigma 参数调节。

    状态映射（1D 和 2D 通用）：
        Breath Focus    → breath_focus
        Pain Discomfort → mind_wandering
        Pending Tasks   → mind_wandering
        Self Reflection → meta_awareness
        Equanimity      → meta_awareness

    v0.4 增强分类（2D 模式）：
        基于吸引子距离 + 连续驻留 + 回归检测，自动识别 redirect_attention。

    Args:
        gamma: 全局精度。
        anchor: 呼吸锚定强度。
        steps: 模拟步数。
        perturbation_strength: 杂念冲击强度。
        perturbation_time: 杂念冲击时刻。
        seed: 随机种子。
        use_efe: 是否使用 EFE 竞争模式。
        use_2d: 是否使用 2D 状态空间。
        dim: 状态空间维度。
        theta: OU 回归速度（v0.4 新增）。
        sigma_ou: OU 波动幅度（v0.4 新增）。

    Returns:
        dict: 包含状态序列、激活值历史、meta_awareness 等。
    """
    rng = np.random.RandomState(seed)

    seeds = create_default_seeds(dim=dim if use_2d else 1)
    workspace = GlobalWorkspace(seeds)

    for s in seeds:
        if s.name == "Breath Focus":
            s.precision_boost = anchor

    # 种子吸引子坐标
    attractors = {
        s.name: np.array(s.core_attractor).ravel() for s in seeds
    }

    # OU 噪声生成轨迹
    if use_2d:
        ou = OUNoise(dim=2, theta=theta, sigma=sigma_ou)
        perturbations = []
        if perturbation_time < steps and perturbation_strength > 0:
            perturbations.append((perturbation_time, np.array([2.0, 0.5])))
        state_stream = ou.generate_trajectory(steps, perturbations=perturbations)
    else:
        ou = OUNoise(dim=1, theta=theta, sigma=sigma_ou)
        perturbations = []
        if perturbation_time < steps and perturbation_strength > 0:
            perturbations.append((perturbation_time, np.array([perturbation_strength])))
        state_stream = ou.generate_trajectory(steps, perturbations=perturbations).ravel()

    state_history = []
    activation_history = []
    meta_awareness_history = []
    dominant_history = []

    for t in range(steps):
        if use_2d:
            state_jnp = jnp.asarray(state_stream[t], dtype=jnp.float32)
        else:
            state_jnp = float(state_stream[t])

        activations, dominant = workspace.compete(
            state_jnp, global_gamma=gamma, use_efe=use_efe
        )

        dominant_history.append(dominant.name)

        # v0.4 增强状态分类
        if use_2d:
            prev_sv = state_stream[t - 1] if t > 0 else None
            sv = state_stream[t]
            med_state = _classify_state_v4(sv, dominant.name, attractors, prev_sv)
        else:
            STATE_MAP = {
                "Breath Focus": "breath_focus",
                "Pain Discomfort": "mind_wandering",
                "Pending Tasks": "mind_wandering",
                "Self Reflection": "meta_awareness",
                "Equanimity": "meta_awareness",
            }
            med_state = STATE_MAP.get(dominant.name, "mind_wandering")
        state_history.append(med_state)

        # 激活值
        act_list = [
            activations.get("Breath Focus", 0.0),
            activations.get("Pain Discomfort", 0.0),
            activations.get("Pending Tasks", 0.0),
            activations.get("Self Reflection", 0.0),
            activations.get("Equanimity", 0.0),
        ]
        activation_history.append(act_list)

        # meta_awareness
        if dominant.name in ("Self Reflection", "Equanimity"):
            ma = float(dominant.activation)
        elif dominant.name == "Breath Focus":
            ma = float(np.clip(gamma / 5.0, 0.0, 1.0))
        else:
            ma = float(np.clip(dominant.activation * 0.3, 0.0, 1.0))
        meta_awareness_history.append(ma)

    return {
        "states": state_history,
        "activations": activation_history,
        "meta_awareness": meta_awareness_history,
        "dominant_history": dominant_history,
        "config": {
            "gamma": gamma,
            "anchor": anchor,
            "steps": steps,
            "perturbation_strength": perturbation_strength,
            "perturbation_time": perturbation_time,
            "use_efe": use_efe,
            "use_2d": use_2d,
            "theta": theta,
            "sigma_ou": sigma_ou,
        },
    }


def _classify_state_v4(
    state_vec: np.ndarray,
    dominant_name: str,
    attractors: dict,
    prev_state_vec: np.ndarray = None,
    threshold_near: float = 2.5,
    threshold_far: float = 1.0,
) -> str:
    """v0.4 增强状态分类：基于吸引子距离 + 种子胜出 + 回归检测。

    1. 杂念种子胜出 → mind_wandering
    2. 杂念种子吸引子附近 → mind_wandering
    3. 远离原点后快速回归（回归系数 ≥ 40%） → redirect_attention
    4. 元认知种子附近 → meta_awareness
    5. 默认 → breath_focus
    """
    dist_to_origin = np.linalg.norm(state_vec)

    # 1. 杂念种子胜出 → mind_wandering（无论距离）
    if dominant_name in ("Pain Discomfort", "Pending Tasks"):
        return "mind_wandering"

    dist_to_pain = np.linalg.norm(state_vec - attractors["Pain Discomfort"])
    dist_to_tasks = np.linalg.norm(state_vec - attractors["Pending Tasks"])
    if dist_to_pain < threshold_near or dist_to_tasks < threshold_near:
        return "mind_wandering"

    # 3. 远离原点后快速回归 → redirect_attention
    if prev_state_vec is not None:
        prev_dist = np.linalg.norm(prev_state_vec)
        threshold_return = threshold_near * 0.5
        if prev_dist > threshold_far and dist_to_origin < threshold_return:
            regression_ratio = (prev_dist - dist_to_origin) / max(prev_dist, 1e-6)
            if regression_ratio >= 0.40:
                return "redirect_attention"

    dist_to_reflection = np.linalg.norm(state_vec - attractors["Self Reflection"])
    dist_to_equanimity = np.linalg.norm(state_vec - attractors["Equanimity"])
    if dist_to_reflection < threshold_near or dist_to_equanimity < threshold_near:
        return "meta_awareness"

    return "breath_focus"


def compute_relative_error(
    reference: float,
    predicted: float,
) -> float:
    """计算相对误差（带除零保护）。

    Args:
        reference: 参考值。
        predicted: 预测值。

    Returns:
        float: 相对误差 = |predicted - reference| / (|reference| + 1e-12)。
    """
    return float(abs(predicted - reference) / (abs(reference) + 1e-12))


def compare_metrics(
    thoughtseeds_metrics: Dict[str, object],
    fm_metrics: Dict[str, object],
    reference_metrics: Optional[Dict[str, Dict[str, float]]] = None,
) -> Dict[str, object]:
    """对比两个模型的关键指标。

    Args:
        thoughtseeds_metrics: thoughtseeds_model 的指标。
        fm_metrics: functional-monism 的指标。
        reference_metrics: 可选，论文中的参考值（如 task document 中的基准表）。

    Returns:
        dict: 包含各项对比误差。
    """
    errors = {}

    # 1. 驻留时间对比
    ts_dwell = thoughtseeds_metrics.get("dwell_time", {})
    fm_dwell = fm_metrics.get("dwell_time", {})
    dwell_comparison = {}
    for state in set(list(ts_dwell.keys()) + list(fm_dwell.keys())):
        ts_val = ts_dwell.get(state, 0.0)
        fm_val = fm_dwell.get(state, 0.0)
        dwell_comparison[state] = {
            "thoughtseeds": ts_val,
            "functional_monism": fm_val,
            "absolute_error": abs(ts_val - fm_val),
            "relative_error": compute_relative_error(ts_val, fm_val),
        }
    errors["dwell_time"] = dwell_comparison

    # 2. 转移概率对比
    ts_trans = thoughtseeds_metrics.get("transition_probability", {})
    fm_trans = fm_metrics.get("transition_probability", {})
    trans_comparison = {}
    for src in set(list(ts_trans.keys()) + list(fm_trans.keys())):
        ts_dst = ts_trans.get(src, {})
        fm_dst = fm_trans.get(src, {})
        for dst in set(list(ts_dst.keys()) + list(fm_dst.keys())):
            ts_val = ts_dst.get(dst, 0.0)
            fm_val = fm_dst.get(dst, 0.0)
            key = f"{src} → {dst}"
            trans_comparison[key] = {
                "thoughtseeds": ts_val,
                "functional_monism": fm_val,
                "absolute_error": abs(ts_val - fm_val),
                "relative_error": compute_relative_error(ts_val, fm_val),
            }
    errors["transition_probability"] = trans_comparison

    # 3. Meta-awareness 对比
    ts_ma = thoughtseeds_metrics.get("mean_meta_awareness", 0.0)
    fm_ma = fm_metrics.get("mean_meta_awareness", 0.0)
    errors["meta_awareness"] = {
        "thoughtseeds": ts_ma,
        "functional_monism": fm_ma,
        "absolute_error": abs(ts_ma - fm_ma),
        "relative_error": compute_relative_error(ts_ma, fm_ma),
    }

    # 4. 激活值对比
    ts_act = thoughtseeds_metrics.get("mean_activation", {})
    fm_act = fm_metrics.get("mean_activation", {})
    act_comparison = {}
    for name in THOUGHTSEED_NAMES:
        ts_val = ts_act.get(name, 0.0)
        fm_val = fm_act.get(name, 0.0)
        act_comparison[name] = {
            "thoughtseeds": ts_val,
            "functional_monism": fm_val,
            "absolute_error": abs(ts_val - fm_val),
            "relative_error": compute_relative_error(ts_val, fm_val),
        }
    errors["mean_activation"] = act_comparison

    # 5. 与参考基准对比（如果有）
    if reference_metrics:
        ref_comparison = {}
        for key, ref_val in reference_metrics.items():
            fm_key = key.replace("breath_control", "breath_focus")
            fm_val = None
            # 尝试从驻留时间中查找
            if "驻留" in key or "dwell" in key.lower():
                for state, vals in dwell_comparison.items():
                    if fm_key.replace(" ", "_").startswith(state):
                        fm_val = vals["functional_monism"]
                        break
            if fm_val is not None:
                ref_comparison[key] = {
                    "reference": ref_val,
                    "functional_monism": fm_val,
                    "absolute_error": abs(ref_val - fm_val),
                    "relative_error": compute_relative_error(ref_val, fm_val),
                }
        errors["reference_benchmark"] = ref_comparison

    # 6. 综合得分
    all_rel_errors = []
    for category in ["dwell_time", "transition_probability", "mean_activation"]:
        for item in errors.get(category, {}).values():
            if isinstance(item, dict) and "relative_error" in item:
                all_rel_errors.append(item["relative_error"])
    if "meta_awareness" in errors:
        all_rel_errors.append(errors["meta_awareness"]["relative_error"])

    errors["summary"] = {
        "mean_relative_error": float(np.mean(all_rel_errors)) if all_rel_errors else 0.0,
        "median_relative_error": float(np.median(all_rel_errors)) if all_rel_errors else 0.0,
        "n_metrics_compared": len(all_rel_errors),
    }

    return errors


def scan_ou_parameters(
    theta_values: List[float],
    sigma_values: List[float],
    gamma: float = 1.0,
    anchor: float = 1.0,
    steps: int = 200,
    use_efe: bool = False,
    seed: int = 42,
) -> List[Dict[str, object]]:
    """v0.4: 在 (theta, sigma) 网格上扫描 OU 参数。

    Args:
        theta_values: θ 值列表。
        sigma_values: σ 值列表。
        gamma: 全局精度。
        anchor: 呼吸锚定强度。
        steps: 模拟步数。
        use_efe: 是否使用 EFE 模式。
        seed: 随机种子。

    Returns:
        list[dict]: 每组的配置 + 状态分布统计。
    """
    results = []
    for th in theta_values:
        for sg in sigma_values:
            res = run_functional_monism_simulation(
                gamma=gamma,
                anchor=anchor,
                steps=steps,
                use_2d=True,
                theta=th,
                sigma_ou=sg,
                use_efe=use_efe,
                seed=seed,
            )
            states = res["states"]
            counts = {}
            for s in states:
                counts[s] = counts.get(s, 0) + 1
            total = len(states)
            results.append({
                "theta": th,
                "sigma": sg,
                "breath_focus_pct": counts.get("breath_focus", 0) / total * 100,
                "mind_wandering_pct": counts.get("mind_wandering", 0) / total * 100,
                "meta_awareness_pct": counts.get("meta_awareness", 0) / total * 100,
                "redirect_attention_pct": counts.get("redirect_attention", 0) / total * 100,
            })
    return results