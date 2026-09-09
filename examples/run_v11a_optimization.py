#!/usr/bin/env python
"""v1.1a 优化：CRN + 扩展 θ 范围。

用法：
    # 完整模式（约 90 分钟）
    python examples/run_v11a_optimization.py

    # 快速模式（约 3 分钟，粗搜 8×8 × 3 runs × 200 steps）
    python examples/run_v11a_optimization.py --quick

输出：
    - 控制台：完整优化结果
    - results/v1.1a_optimization_result.json：机器可读结果
"""
import sys, os, json, time, argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.optimization.meta_optimizer import optimize_parameters, BENCHMARK

parser = argparse.ArgumentParser(description="v1.1a 元优化器")
parser.add_argument("--quick", action="store_true", help="快速模式（8×8 × 3r×200s）")
args = parser.parse_args()

if args.quick:
    n_coarse, n_refine = 8, 5
    coarse_runs, coarse_steps = 3, 200
    refine_runs, refine_steps = 10, 1000
else:
    n_coarse, n_refine = 10, 5
    coarse_runs, coarse_steps = 10, 500
    refine_runs, refine_steps = 20, 2000

t0 = time.time()

# 使用 grid_search 和 refine_search 直接调用，以控制 runs/steps
from src.optimization.meta_optimizer import grid_search, refine_search

theta_min, theta_max = 0.005, 0.15
sigma_min, sigma_max = 0.15, 0.50

print("=" * 60)
print("v1.1a 元优化器：Tikhonov 正则化 + CRN 自动校准")
print("=" * 60)
print(f"  模式: {'快速' if args.quick else '完整'}")
print(f"  基准: MW 占比 {BENCHMARK['mind_wandering_ratio']:.1%}, "
      f"MW 驻留 {BENCHMARK['mind_wandering_dwell']:.1f} 步")
print(f"  v0.9 手工调参: θ=0.05, σ=0.28")
print(f"  CRN: 开启")
print(f"  θ 范围: [{theta_min}, {theta_max}]")
print()

# 阶段 1: 粗搜索
print(f"阶段 1: 粗搜索（{coarse_runs} runs × {coarse_steps} steps, CRN）")
coarse_results = grid_search(
    theta_range=(theta_min, theta_max),
    sigma_range=(sigma_min, sigma_max),
    n_theta=n_coarse, n_sigma=n_coarse,
    alpha=0.5, beta=0.3,
    n_runs=coarse_runs, steps=coarse_steps,
    verbose=True, use_crn=True,
)
best_coarse = coarse_results[0]

theta_step = (theta_max - theta_min) / (n_coarse - 1)
sigma_step = (sigma_max - sigma_min) / (n_coarse - 1)

# 阶段 2: 细化
print(f"\n阶段 2: 细化验证（{refine_runs} runs × {refine_steps} steps, CRN）"
      f" — 围绕 θ={best_coarse['theta']:.4f}, σ={best_coarse['sigma']:.4f}")
refine_results = refine_search(
    best_theta=best_coarse["theta"],
    best_sigma=best_coarse["sigma"],
    theta_step=theta_step, sigma_step=sigma_step,
    n_theta=n_refine, n_sigma=n_refine,
    alpha=0.5, beta=0.3,
    n_runs=refine_runs, steps=refine_steps,
    verbose=True, use_crn=True,
    theta_min=theta_min, theta_max=theta_max,
)
best_refine = refine_results[0]

elapsed = time.time() - t0
all_results = coarse_results + refine_results
all_results.sort(key=lambda r: r["loss"])
best = all_results[0]

# 对比
v09_ratio_err = abs(0.452 - BENCHMARK["mind_wandering_ratio"])
v09_dwell_err = abs(61.3 - BENCHMARK["mind_wandering_dwell"])

print(f"\n{'='*60}")
print(f"v1.1a 优化结果总结")
print(f"{'='*60}")
print(f"  v0.9 手工调参:   θ=0.05, σ=0.28, 误差 {v09_ratio_err:.1%}/{v09_dwell_err:.1f}步")
print(f"  v1.1 粗搜(旧):  θ=0.02, σ=0.3056, 误差 1.0%/3.1步")
print(f"  v1.1a 粗搜(CRN): θ={best_coarse['theta']:.4f}, σ={best_coarse['sigma']:.4f}, "
      f"MW={best_coarse['mw_ratio']:.1%}, dwell={best_coarse['mw_dwell']:.1f}")
print(f"  v1.1a 细化(CRN): θ={best_refine['theta']:.4f}, σ={best_refine['sigma']:.4f}")
print(f"  MW 占比: {best['mw_ratio']:.1%} (基准 {BENCHMARK['mind_wandering_ratio']:.1%})")
print(f"  MW 驻留: {best['mw_dwell']:.1f} (基准 {BENCHMARK['mind_wandering_dwell']:.1f})")
print(f"  占比误差: {best['ratio_error']:.1%}")
print(f"  驻留误差: {best['dwell_error']:.1f}步")
print(f"  总耗时: {elapsed:.0f}s")

# 保存结果
result = {
    "mode": "quick" if args.quick else "full",
    "theta_opt": best["theta"],
    "sigma_opt": best["sigma"],
    "mw_ratio": best["mw_ratio"],
    "mw_dwell": best["mw_dwell"],
    "ratio_error": best["ratio_error"],
    "dwell_error": best["dwell_error"],
    "elapsed_s": elapsed,
    "coarse_best": {
        "theta": best_coarse["theta"],
        "sigma": best_coarse["sigma"],
        "mw_ratio": best_coarse["mw_ratio"],
        "mw_dwell": best_coarse["mw_dwell"],
    },
    "refine_best": {
        "theta": best_refine["theta"],
        "sigma": best_refine["sigma"],
        "mw_ratio": best_refine["mw_ratio"],
        "mw_dwell": best_refine["mw_dwell"],
    },
    "top5": [dict(r) for r in all_results[:5]],
}
out_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "results", "v1.1a_optimization_result.json",
)
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)
print(f"\n结果已保存: {out_path}")
