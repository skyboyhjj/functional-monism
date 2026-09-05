"""指标提取模块：计算状态驻留时间、转移概率、平均激活值等关键指标。

与 thoughtseeds_model 论文图 3 的指标对齐：
- 状态驻留时间（dwell time）
- 状态转移概率（transition probability）
- Meta-awareness 平均水平
- Thoughtseed 激活差异
"""

from typing import Dict, List, Tuple, Optional

import numpy as np


def compute_dwell_time(
    states: List[str],
    target_state: Optional[str] = None,
) -> Dict[str, float]:
    """计算每个状态的平均连续驻留时间。

    Args:
        states: 状态序列（如 ["breath_focus", "breath_focus", "mind_wandering", ...]）。
        target_state: 如果指定，仅返回该状态的驻留时间；否则返回所有状态。

    Returns:
        dict: {state_name: mean_dwell_steps}。
    """
    if not states:
        return {}

    dwells: Dict[str, List[int]] = {}
    current_state = states[0]
    current_count = 1

    for s in states[1:]:
        if s == current_state:
            current_count += 1
        else:
            dwells.setdefault(current_state, []).append(current_count)
            current_state = s
            current_count = 1

    # 记录最后一段
    dwells.setdefault(current_state, []).append(current_count)

    result = {}
    for state, counts in dwells.items():
        if target_state is None or state == target_state:
            result[state] = float(np.mean(counts))

    return result


def compute_transition_probability(
    states: List[str],
) -> Dict[str, Dict[str, float]]:
    """计算状态转移概率矩阵。

    P(A → B) = count(A → B) / count(A → any)

    Args:
        states: 状态序列。

    Returns:
        dict: {from_state: {to_state: probability}}。
    """
    if len(states) < 2:
        return {}

    # 统计转移计数
    transitions: Dict[str, Dict[str, int]] = {}
    from_counts: Dict[str, int] = {}

    for i in range(len(states) - 1):
        src = states[i]
        dst = states[i + 1]
        transitions.setdefault(src, {}).setdefault(dst, 0)
        transitions[src][dst] += 1
        from_counts[src] = from_counts.get(src, 0) + 1

    # 转换为概率
    prob_matrix = {}
    for src, dst_counts in transitions.items():
        total = from_counts[src]
        prob_matrix[src] = {
            dst: count / total for dst, count in dst_counts.items()
        }

    return prob_matrix


def compute_mean_activation(
    activations: List[List[float]],
    ts_names: List[str],
) -> Dict[str, float]:
    """计算每个 thoughtseed 的平均激活值。

    Args:
        activations: 每个时间步的 5 个激活值列表。
        ts_names: thoughtseed 名称列表。

    Returns:
        dict: {ts_name: mean_activation}。
    """
    if not activations:
        return {}

    arr = np.array(activations)  # (T, N)
    mean_vals = np.mean(arr, axis=0)  # (N,)

    return {
        name: float(mean_vals[i])
        for i, name in enumerate(ts_names)
    }


def compute_mean_meta_awareness(
    meta_awareness: List[float],
) -> float:
    """计算平均 meta-awareness 水平。

    Args:
        meta_awareness: meta-awareness 序列。

    Returns:
        float: 平均 meta-awareness。
    """
    if not meta_awareness:
        return 0.0
    return float(np.mean(meta_awareness))


def compute_state_frequencies(
    states: List[str],
) -> Dict[str, float]:
    """计算每个状态的出现频率。

    Args:
        states: 状态序列。

    Returns:
        dict: {state_name: frequency}。
    """
    if not states:
        return {}

    unique, counts = np.unique(states, return_counts=True)
    total = len(states)
    return {
        str(state): float(count / total)
        for state, count in zip(unique, counts)
    }


def extract_all_metrics(
    states: List[str],
    activations: List[List[float]],
    meta_awareness: List[float],
    ts_names: List[str],
) -> Dict[str, object]:
    """提取所有关键指标。

    Args:
        states: 状态序列。
        activations: thoughtseed 激活值序列。
        meta_awareness: meta-awareness 序列。
        ts_names: thoughtseed 名称列表。

    Returns:
        dict: 包含驻留时间、转移概率、激活值、meta-awareness 等全部指标。
    """
    return {
        "dwell_time": compute_dwell_time(states),
        "transition_probability": compute_transition_probability(states),
        "state_frequencies": compute_state_frequencies(states),
        "mean_activation": compute_mean_activation(activations, ts_names),
        "mean_meta_awareness": compute_mean_meta_awareness(meta_awareness),
        "total_steps": len(states),
    }