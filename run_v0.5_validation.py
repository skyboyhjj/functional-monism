"""v0.5 完整定量验证：专家模式 + 新手模式，各 20 次 × 2000 步"""
import sys
import time
sys.path.insert(0, "e:/00-FunctionalMonism")

from src.validation.comparator import run_multiple_simulations
from src.validation.report import generate_benchmark_report

print("=" * 60)
print("v0.5 定量验证：functional-monism vs thoughtseeds_model")
print("=" * 60)

configs = [
    ("expert", "专家模式", 3.0, 3.0, 0.25, 0.15, False),
    ("novice", "新手模式", 0.3, 1.0, 0.06, 0.35, True),
]

for mode_key, mode_label, gamma, anchor, theta, sigma, use_efe in configs:
    print(f"\n{'='*60}")
    print(f"正在运行 {mode_label}：20 次 × 2000 步...")
    print(f"参数: gamma={gamma}, anchor={anchor}, theta={theta}, sigma={sigma}, EFE={use_efe}")
    t0 = time.time()

    results = run_multiple_simulations(
        n_runs=20,
        steps=2000,
        gamma=gamma,
        anchor=anchor,
        theta=theta,
        sigma_ou=sigma,
        use_efe=use_efe,
    )

    elapsed = time.time() - t0
    print(f"完成，耗时 {elapsed:.1f}s")

    print(f"\n--- {mode_label} 状态分布 (mean ± std) ---")
    freq = results["state_frequencies"]
    for state in ["breath_focus", "mind_wandering", "meta_awareness", "redirect_attention"]:
        if state in freq:
            f = freq[state]
            print(f"  {state:20s}: {f['mean']:6.1f}% ± {f['std']:5.1f}%")

    print(f"\n--- {mode_label} 驻留时间 (mean ± std, 步) ---")
    dwell = results["dwell_times"]
    for state in ["breath_focus", "mind_wandering", "meta_awareness", "redirect_attention"]:
        if state in dwell:
            d = dwell[state]
            print(f"  {state:20s}: mean={d['mean_dwell']:6.1f} ± {d['std_dwell']:5.1f}, max={d['max_dwell_mean']:6.1f}")

    # 生成报告
    report = generate_benchmark_report(results, mode=mode_key)
    report_path = f"results/v0.5_benchmark_{mode_key}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n报告已保存: {report_path}")

print("\n" + "=" * 60)
print("v0.5 定量验证完成！")
print("=" * 60)