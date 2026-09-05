"""数据加载模块：加载 thoughtseeds_model 的 JSON 数据。

thoughtseeds_model 数据格式（实际）：
- 文件名：training_results_{expert|novice}_seed{N}.json
- 12000 步：8000 训练 + 4000 冻结评估
- 状态：breath_focus, mind_wandering, meta_awareness, redirect_attention
- 5 个 thoughtseed：attend_breath, pain_discomfort, pending_tasks, aha_moment, equanimity
"""

import json
import os
import glob
from typing import Dict, List, Tuple, Optional, Any

import numpy as np

# thoughtseeds_model 的 5 个种子名称
THOUGHTSEED_NAMES = [
    "attend_breath",
    "pain_discomfort",
    "pending_tasks",
    "aha_moment",
    "equanimity",
]

# 4 个冥想状态
MEDITATION_STATES = [
    "breath_focus",
    "mind_wandering",
    "meta_awareness",
    "redirect_attention",
]


def load_seed_data(json_path: str) -> Dict[str, Any]:
    """加载单个 JSON 文件，提取关键时间序列。

    Args:
        json_path: JSON 文件路径。

    Returns:
        dict: 包含状态序列、激活值、元意识、自由能、预测误差等。
    """
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return {
        "states": raw["state_history"],
        "activations": raw["thoughtseed_activations_history"],
        "prior_activations": raw.get("thoughtseed_prior_activations_history", []),
        "meta_awareness": raw.get("meta_awareness_history", []),
        "free_energy": raw.get("free_energy_history", []),
        "prediction_error": raw.get("forward_error_history", []),
        "network_activations": raw.get("network_activations_history", []),
        "transitions": raw.get("transitions", []),
        "phase_history": raw.get("phase_history", []),
        "experience_level": raw.get("experience_level", "unknown"),
        "seed": raw.get("seed", -1),
        "timesteps": raw.get("timesteps", 0),
        "training_steps": raw.get("training_steps", 8000),
        "evaluation_steps": raw.get("evaluation_steps", 4000),
    }


def load_expert_data(data_dir: str) -> List[Dict[str, Any]]:
    """加载所有专家数据（JSON 文件）。

    Args:
        data_dir: data/ 目录路径。

    Returns:
        list[dict]: 每个文件的数据字典列表。
    """
    pattern = os.path.join(data_dir, "training_results_expert_seed*.json")
    json_files = sorted(glob.glob(pattern))
    return [load_seed_data(f) for f in json_files]


def load_novice_data(data_dir: str) -> List[Dict[str, Any]]:
    """加载所有新手数据（JSON 文件）。

    Args:
        data_dir: data/ 目录路径。

    Returns:
        list[dict]: 每个文件的数据字典列表。
    """
    pattern = os.path.join(data_dir, "training_results_novice_seed*.json")
    json_files = sorted(glob.glob(pattern))
    return [load_seed_data(f) for f in json_files]


def aggregate_data(
    data_list: List[Dict[str, Any]],
    eval_only: bool = True,
) -> Dict[str, Any]:
    """聚合多个模拟数据，提取评估窗口的统计。

    Args:
        data_list: load_seed_data 返回的字典列表。
        eval_only: 是否仅使用评估窗口（后 2000 步）。

    Returns:
        dict: 聚合统计结果。
    """
    if not data_list:
        return {}

    n = len(data_list)

    # 确定评估窗口：每个文件使用相同的评估窗口
    if eval_only:
        first = data_list[0]
        eval_start = first["training_steps"]
        # 使用最后 2000 步（与 thoughtseeds_model 论文一致）
        eval_start = eval_start + (first["evaluation_steps"] - 2000)
    else:
        eval_start = 0

    # 聚合状态序列
    all_states = []
    for d in data_list:
        all_states.extend(d["states"][eval_start:])

    # 聚合 meta_awareness
    all_ma = []
    for d in data_list:
        all_ma.extend(d["meta_awareness"][eval_start:])

    # 聚合 thoughtseed 激活值
    all_activations = []
    for d in data_list:
        all_activations.extend(d["activations"][eval_start:])

    # 计算平均激活值
    ts_arrays = {name: [] for name in THOUGHTSEED_NAMES}
    for d in data_list:
        for step_acts in d["activations"][eval_start:]:
            for i, name in enumerate(THOUGHTSEED_NAMES):
                ts_arrays[name].append(step_acts[i])

    mean_activations = {
        name: float(np.mean(ts_arrays[name])) for name in THOUGHTSEED_NAMES
    }

    return {
        "n_seeds": n,
        "total_steps": len(all_states),
        "states": all_states,
        "meta_awareness": all_ma,
        "mean_meta_awareness": float(np.mean(all_ma)),
        "ts_activations": ts_arrays,
        "mean_activations": mean_activations,
        "experience_level": data_list[0].get("experience_level", "unknown"),
    }