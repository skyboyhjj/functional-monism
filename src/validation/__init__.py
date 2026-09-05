# 泛函一元论 · 验证模块
# 与 thoughtseeds_model 的对比验证，建立实证锚点

from .data_loader import (
    load_seed_data,
    load_expert_data,
    load_novice_data,
    aggregate_data,
    THOUGHTSEED_NAMES,
    MEDITATION_STATES,
)
from .metrics import (
    compute_dwell_time,
    compute_transition_probability,
    compute_mean_activation,
    compute_mean_meta_awareness,
    extract_all_metrics,
)
from .comparator import (
    run_functional_monism_simulation,
    compare_metrics,
    compute_relative_error,
)
from .report import generate_report

__all__ = [
    "load_seed_data",
    "load_expert_data",
    "load_novice_data",
    "aggregate_data",
    "THOUGHTSEED_NAMES",
    "MEDITATION_STATES",
    "compute_dwell_time",
    "compute_transition_probability",
    "compute_mean_activation",
    "compute_mean_meta_awareness",
    "extract_all_metrics",
    "run_functional_monism_simulation",
    "compare_metrics",
    "compute_relative_error",
    "generate_report",
]