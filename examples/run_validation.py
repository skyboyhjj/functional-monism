#!/usr/bin/env python
"""运行验证：functional-monism vs thoughtseeds_model 对比。

用法：
    python examples/run_validation.py [--gamma 3.0] [--anchor 5.0] [--efe]

输出：
    - 控制台：关键指标对比摘要
    - results/validation_report.md：完整验证报告
"""

import sys
import os
import argparse

# 确保可以导入项目模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.validation.data_loader import (
    load_seed_data,
    load_expert_data,
    THOUGHTSEED_NAMES,
)
from src.validation.metrics import extract_all_metrics
from src.validation.comparator import (
    run_functional_monism_simulation,
    compare_metrics,
)
from src.validation.report import generate_report


# 任务文档中的参考基准
REFERENCE_BENCHMARK = {
    "breath_focus_驻留时间": 18.7,
    "mind_wandering_驻留时间": 8.5,
    "breath_focus → mind_wandering": 0.30,
    "mind_wandering → meta_awareness": 0.35,
    "平均 meta_awareness": 0.82,
}


def main():
    parser = argparse.ArgumentParser(
        description="functional-monism vs thoughtseeds_model 对比验证"
    )
    parser.add_argument(
        "--gamma", type=float, default=3.0,
        help="全局精度 γ（默认 3.0，模拟专家模式）"
    )
    parser.add_argument(
        "--anchor", type=float, default=5.0,
        help="呼吸锚定强度（默认 5.0）"
    )
    parser.add_argument(
        "--steps", type=int, default=200,
        help="模拟步数（默认 200）"
    )
    parser.add_argument(
        "--efe", action="store_true",
        help="启用 EFE 竞争模式"
    )
    parser.add_argument(
        "--data-dir", type=str,
        default="thoughtseeds_model/data",
        help="thoughtseeds_model 数据目录"
    )
    parser.add_argument(
        "--output", type=str,
        default="results/validation_report.md",
        help="报告输出路径"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  泛函一元论 vs Thoughtseeds: 对比验证")
    print("=" * 60)
    print()

    # ---- 加载 thoughtseeds_model 数据 ----
    print("[1/4] 加载 thoughtseeds_model 数据...")
    expert_data = load_expert_data(args.data_dir)
    if not expert_data:
        print(f"  错误: 在 {args.data_dir} 中未找到专家数据")
        print("  请确保已克隆 thoughtseeds_model 仓库")
        sys.exit(1)

    print(f"  加载了 {len(expert_data)} 个专家种子数据")

    # 使用 seed104（论文主要种子）的评估窗口
    data = expert_data[0]  # 使用第一个可用数据
    eval_start = data["training_steps"] + (data["evaluation_steps"] - 2000)
    states_eval = data["states"][eval_start:]
    acts_eval = data["activations"][eval_start:]
    ma_eval = data["meta_awareness"][eval_start:]

    print(f"  评估窗口: {len(states_eval)} 步")
    print(f"  经验水平: {data['experience_level']}")

    ts_metrics = extract_all_metrics(
        states_eval, acts_eval, ma_eval, THOUGHTSEED_NAMES
    )

    print(f"  breath_focus 驻留: {ts_metrics['dwell_time'].get('breath_focus', 0):.1f} 步")
    print(f"  mind_wandering 驻留: {ts_metrics['dwell_time'].get('mind_wandering', 0):.1f} 步")
    print(f"  平均 meta_awareness: {ts_metrics['mean_meta_awareness']:.3f}")
    print()

    # ---- 运行 functional-monism 模拟 ----
    print(f"[2/4] 运行 functional-monism 模拟 (γ={args.gamma}, anchor={args.anchor}, EFE={args.efe})...")
    fm_result = run_functional_monism_simulation(
        gamma=args.gamma,
        anchor=args.anchor,
        steps=args.steps,
        use_efe=args.efe,
    )

    fm_metrics = extract_all_metrics(
        fm_result["states"],
        fm_result["activations"],
        fm_result["meta_awareness"],
        THOUGHTSEED_NAMES,
    )

    print(f"  breath_focus 驻留: {fm_metrics['dwell_time'].get('breath_focus', 0):.1f} 步")
    print(f"  mind_wandering 驻留: {fm_metrics['dwell_time'].get('mind_wandering', 0):.1f} 步")
    print(f"  平均 meta_awareness: {fm_metrics['mean_meta_awareness']:.3f}")
    print()

    # ---- 对比 ----
    print("[3/4] 计算对比指标...")
    errors = compare_metrics(
        ts_metrics,
        fm_metrics,
        reference_metrics=REFERENCE_BENCHMARK,
    )

    summary = errors["summary"]
    print(f"  平均相对误差: {summary['mean_relative_error']:.1%}")
    print(f"  中位相对误差: {summary['median_relative_error']:.1%}")
    print(f"  对比指标数: {summary['n_metrics_compared']}")
    print()

    # ---- 生成报告 ----
    print("[4/4] 生成验证报告...")
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    report = generate_report(
        ts_metrics,
        fm_metrics,
        errors,
        config={
            "gamma": args.gamma,
            "anchor": args.anchor,
            "use_efe": args.efe,
            "steps": args.steps,
        },
        output_path=args.output,
    )

    print(f"  报告已保存至: {args.output}")
    print()
    print("=" * 60)
    print("  验证完成")
    print("=" * 60)

    return report


if __name__ == "__main__":
    main()