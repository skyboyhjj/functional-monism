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


def calculate_dwell_times(state_sequence: List[str]) -> Dict[str, Dict[str, float]]:
    """v0.5: 计算每个状态的连续驻留时间分布统计。

    与 compute_dwell_time 不同，此函数返回完整的分布统计：
    均值、中位数、最大值、标准差、驻留段数。

    Args:
        state_sequence: 状态序列（如 ["breath_focus", "breath_focus", "mind_wandering", ...]）。

    Returns:
        dict: {state: {"mean": float, "median": float, "max": float, "std": float, "count": int}}。
    """
    if not state_sequence:
        return {}

    dwells: Dict[str, List[int]] = {}
    current_state = state_sequence[0]
    current_count = 1

    for s in state_sequence[1:]:
        if s == current_state:
            current_count += 1
        else:
            dwells.setdefault(current_state, []).append(current_count)
            current_state = s
            current_count = 1
    dwells.setdefault(current_state, []).append(current_count)

    result = {}
    for state, counts in dwells.items():
        arr = np.array(counts, dtype=float)
        result[state] = {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "max": float(np.max(arr)),
            "std": float(np.std(arr)),
            "count": len(counts),
        }
    return result


def compute_buffer_size(
    gamma: float = 0.5,
    sigma: float = 0.35,
    min_size: int = 3,
    max_size: int = 12,
) -> int:
    """v0.8: 根据精度 γ 和波动幅度 σ 动态计算缓冲大小。

    公式：buffer_size = round(9 / (γ + 1) + σ * 1.5)
    - γ 越高 → 缓冲越短（专家需要灵敏切换）
    - σ 越大 → 缓冲越长（噪声大时需要更多证据）

    参数范围：
        gamma: 0.1 ~ 5.0
        sigma: 0.05 ~ 0.50
    返回: 3 ~ 12 之间的整数

    Examples:
        >>> compute_buffer_size(3.0, 0.15)  # 专家模式：快速响应
        3
        >>> compute_buffer_size(0.3, 0.35)  # 新手模式：稳定判别
        7
    """
    raw = 9.0 / (gamma + 1.0) + sigma * 1.5
    return int(round(max(min_size, min(max_size, raw))))


def classify_state_with_buffer(
    state_stream: List[np.ndarray],
    attractors: Dict[str, np.ndarray],
    dominant_history: List[str] = None,
    buffer_size: int = None,
    gamma: float = 0.5,
    sigma: float = 0.35,
    breath_zone_radius: float = 0.5,
    mw_zone_radius: float = 1.8,
    meta_zone_radius: float = 1.5,
) -> List[str]:
    """v0.8: 基于连续驻留缓冲的状态分类，支持自适应缓冲大小。

    核心原则：状态不是空间中的一个点，而是一条轨迹片段的涌现属性。
    只有连续 N 步满足条件，才触发状态切换。

    使用迭代而非递归，支持 2000+ 步序列。

    v0.7 升级：buffer_size 可从 gamma/sigma 动态计算（自适应缓冲），
    也可以显式指定（向下兼容 v0.6）。

    Args:
        state_stream: 原始状态向量序列 [(x, y), ...]。
        attractors: {name: np.ndarray} 吸引子坐标。
        dominant_history: 每步的胜出种子名（可选，作为辅助信号）。
        buffer_size: 连续驻留窗口大小（None 则从 gamma/sigma 动态计算）。
        gamma: 全局精度 γ（v0.7 自适应缓冲参数）。
        sigma: OU 波动幅度 σ（v0.7 自适应缓冲参数）。
        breath_zone_radius: 呼吸区半径（默认 0.5）。
        mw_zone_radius: 杂念区半径（默认 1.5）。
        meta_zone_radius: 元认知区半径（默认 1.5）。

    Returns:
        list[str]: 与 state_stream 等长的状态标签序列。
    """
    # v0.7: 自适应缓冲大小
    if buffer_size is None:
        buffer_size = compute_buffer_size(gamma, sigma)
    n_steps = len(state_stream)
    if n_steps == 0:
        return []

    pain_attr = attractors.get("Pain Discomfort")
    tasks_attr = attractors.get("Pending Tasks")
    refl_attr = attractors.get("Self Reflection")
    equa_attr = attractors.get("Equanimity")

    # 预计算每步到各吸引子的距离
    dist_to_origin = np.array([np.linalg.norm(s) for s in state_stream])
    dist_to_pain = np.array([np.linalg.norm(s - pain_attr) for s in state_stream]) if pain_attr is not None else None
    dist_to_tasks = np.array([np.linalg.norm(s - tasks_attr) for s in state_stream]) if tasks_attr is not None else None
    dist_to_refl = np.array([np.linalg.norm(s - refl_attr) for s in state_stream]) if refl_attr is not None else None
    dist_to_equa = np.array([np.linalg.norm(s - equa_attr) for s in state_stream]) if equa_attr is not None else None

    labels = []
    prev_label = "breath_focus"  # 初始默认

    def in_breath_zone(idx: int) -> bool:
        return dist_to_origin[idx] < breath_zone_radius

    def in_mw_zone(idx: int) -> bool:
        if dist_to_pain is not None and dist_to_pain[idx] < mw_zone_radius:
            return True
        if dist_to_tasks is not None and dist_to_tasks[idx] < mw_zone_radius:
            return True
        return False

    def in_meta_zone(idx: int) -> bool:
        if dist_to_refl is not None and dist_to_refl[idx] < meta_zone_radius:
            return True
        if dist_to_equa is not None and dist_to_equa[idx] < meta_zone_radius:
            return True
        return False

    def is_regressing_window(start: int, end: int) -> bool:
        """检查窗口内状态是否整体向原点回归。"""
        if start >= end or end >= n_steps:
            return False
        first_dist = dist_to_origin[start]
        last_dist = dist_to_origin[end]
        # 要求：起点远离原点，终点靠近原点，整体缩小 ≥ 30%
        if first_dist < 2.0 or last_dist > 1.0:
            return False
        return (first_dist - last_dist) / max(first_dist, 1e-6) >= 0.30

    for t in range(n_steps):
        # 缓冲期：前面几步默认 breath_focus
        if t < buffer_size - 1:
            labels.append("breath_focus")
            continue

        # 窗口 [t - buffer_size + 1, t]
        w_start = t - buffer_size + 1
        w_end = t

        # 1. 辅助信号：杂念种子胜出 + 在杂念区 → 直接 mind_wandering
        if dominant_history is not None and t < len(dominant_history):
            if dominant_history[t] in ("Pain Discomfort", "Pending Tasks") and in_mw_zone(t):
                labels.append("mind_wandering")
                prev_label = "mind_wandering"
                continue

        # 2. 连续 N 步在呼吸区 → breath_focus
        if all(in_breath_zone(i) for i in range(w_start, w_end + 1)):
            labels.append("breath_focus")
            prev_label = "breath_focus"
            continue

        # 3. 连续 N 步在杂念区 → mind_wandering
        if all(in_mw_zone(i) for i in range(w_start, w_end + 1)):
            labels.append("mind_wandering")
            prev_label = "mind_wandering"
            continue

        # 4. 连续 N 步在元认知区 → meta_awareness
        if all(in_meta_zone(i) for i in range(w_start, w_end + 1)):
            labels.append("meta_awareness")
            prev_label = "meta_awareness"
            continue

        # 5. 回归检测：窗口内整体向原点回归
        if is_regressing_window(w_start, w_end):
            labels.append("redirect_attention")
            prev_label = "redirect_attention"
            continue

        # 6. 默认：保持前一个状态（惰性传递）
        labels.append(prev_label)

    return labels


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