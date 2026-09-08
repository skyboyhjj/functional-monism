#!/usr/bin/env python
"""运行元优化：自动寻找最优的 θ 和 σ。

v1.1: 基于 Tikhonov 正则化的两级网格搜索，替代手工调参。

用法：
    python examples/run_meta_optimization.py
    python examples/run_meta_optimization.py --quick  # 快速模式（10×10粗搜）
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.optimization.meta_optimizer import optimize_parameters, BENCHMARK


def main():
    parser = argparse.ArgumentParser(
        description="v1.1 元优化器：自动校准 θ 和 σ"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="快速模式：10×10 粗搜索 + 5×5 细化（约 2 分钟）",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.5,
        help="θ 正则化强度（默认 0.5）",
    )
    parser.add_argument(
        "--beta",
        type=float,
        default=0.3,
        help="σ 正则化强度（默认 0.3）",
    )
    args = parser.parse_args()

    n_coarse = 10 if args.quick else 20
    n_refine = 5 if args.quick else 10

    theta_opt, sigma_opt, history = optimize_parameters(
        theta_init=0.05,
        sigma_init=0.28,
        alpha=args.alpha,
        beta=args.beta,
        n_coarse=n_coarse,
        n_refine=n_refine,
        verbose=True,
    )

    # 打印 top 5
    print("\nTop 5 参数组合:")
    print("-" * 60)
    print(f"{'θ':>8}  {'σ':>8}  {'loss':>10}  {'MW%':>8}  {'dwell':>8}  "
          f"{'Δ%':>8}  {'Δdwell':>8}")
    print("-" * 60)
    for r in history[:5]:
        print(f"{r['theta']:8.4f}  {r['sigma']:8.4f}  {r['loss']:10.4f}  "
              f"{r['mw_ratio']:7.1%}  {r['mw_dwell']:7.1f}  "
              f"{r['ratio_error']:7.1%}  {r['dwell_error']:7.1f}")

    # 对比 v0.9
    v09_ratio_error = abs(0.452 - BENCHMARK["mind_wandering_ratio"])
    v09_dwell_error = abs(61.3 - BENCHMARK["mind_wandering_dwell"])
    best = history[0]

    print(f"\n  占比误差: v0.9 = {v09_ratio_error:.1%} → v1.1 = {best['ratio_error']:.1%}")
    print(f"  驻留误差: v0.9 = {v09_dwell_error:.1f} 步 → v1.1 = {best['dwell_error']:.1f} 步")


if __name__ == "__main__":
    main()