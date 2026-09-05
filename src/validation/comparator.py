"""对比引擎：运行 functional-monism 模拟，与 thoughtseeds_model 数据对比。

通过在不同 (γ, anchor) 配置下运行 functional-monism 模拟器，
提取与 thoughtseeds_model 相同的指标，计算误差并评估复现程度。
"""

import sys
import os
from typing import Dict, List, Tuple, Optional

import numpy as np

# 确保可以导入项目模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.models.workspace import (
    MeditationSeed,
    GlobalWorkspace,
    create_default_seeds,
)
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
) -> Dict[str, object]:
    """运行 functional-monism 冥想模拟。

    将 functional-monism 的 5 个种子映射到 thoughtseeds_model 的对应概念：
        Breath Focus  → attend_breath
        Pain Discomfort → pain_discomfort
        Pending Tasks  → pending_tasks
        Self Reflection → aha_moment
        Equanimity     → equanimity

    将 dominant seed 映射到冥想状态：
        Breath Focus    → breath_focus
        Pain Discomfort → mind_wandering
        Pending Tasks   → mind_wandering
        Self Reflection → meta_awareness
        Equanimity      → meta_awareness

    Args:
        gamma: 全局精度。
        anchor: 呼吸锚定强度。
        steps: 模拟步数。
        perturbation_strength: 杂念冲击强度。
        perturbation_time: 杂念冲击时刻。
        seed: 随机种子。
        use_efe: 是否使用 EFE 竞争模式。

    Returns:
        dict: 包含状态序列、激活值历史、meta_awareness 等。
    """
    rng = np.random.RandomState(seed)

    # 种子映射：functional-monism → thoughtseeds_model
    NAME_MAP = {
        "Breath Focus": "attend_breath",
        "Pain Discomfort": "pain_discomfort",
        "Pending Tasks": "pending_tasks",
        "Self Reflection": "aha_moment",
        "Equanimity": "equanimity",
    }

    # 状态映射：dominant seed → meditation state
    STATE_MAP = {
        "Breath Focus": "breath_focus",
        "Pain Discomfort": "mind_wandering",
        "Pending Tasks": "mind_wandering",
        "Self Reflection": "meta_awareness",
        "Equanimity": "meta_awareness",
    }

    seeds = create_default_seeds()
    workspace = GlobalWorkspace(seeds)

    # 设置呼吸锚定
    for s in seeds:
        if s.name == "Breath Focus":
            s.precision_boost = anchor

    state = 0.0
    state_history = []
    activation_history = []
    meta_awareness_history = []
    dominant_history = []

    for t in range(steps):
        # 扰动
        if t == perturbation_time and perturbation_strength > 0:
            state += rng.normal(0, perturbation_strength)

        # 竞争
        activations, dominant = workspace.compete(
            state, global_gamma=gamma, use_efe=use_efe
        )

        # 记录
        state_history.append(STATE_MAP.get(dominant.name, "mind_wandering"))
        dominant_history.append(dominant.name)

        # 激活值（按 thoughtseeds_model 顺序）
        act_list = [
            activations.get("Breath Focus", 0.0),
            activations.get("Pain Discomfort", 0.0),
            activations.get("Pending Tasks", 0.0),
            activations.get("Self Reflection", 0.0),
            activations.get("Equanimity", 0.0),
        ]
        activation_history.append(act_list)

        # meta_awareness：meta_awareness 状态下激活值高 → 高水平
        if dominant.name in ("Self Reflection", "Equanimity"):
            ma = float(dominant.activation)
        elif dominant.name == "Breath Focus":
            # 呼吸焦点时，meta_awareness 与精度成正比
            ma = float(np.clip(gamma / 5.0, 0.0, 1.0))
        else:
            ma = float(np.clip(dominant.activation * 0.3, 0.0, 1.0))
        meta_awareness_history.append(ma)

        # 状态更新：随机游走 + 向吸引子靠近
        state += rng.normal(0, 0.1)
        # 向 dominant seed 的吸引子靠近
        attractor = float(dominant.core_attractor.ravel()[0])
        state += (attractor - state) * 0.05

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
        },
    }


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