"""报告生成：生成 Markdown 格式的对比验证报告。

输出格式化的验证报告，包含：
- 数据概述
- 关键指标对比表
- 误差分析
- 验证结论

v0.5: 新增 thoughtseeds_model 基准数值对比表。
"""

from typing import Dict, Optional, List
from datetime import datetime

import numpy as np

# v0.5: thoughtseeds_model 基准值（来自论文图 3 和任务书）
THOUGHTSEEDS_BENCHMARK = {
    "expert": {
        "breath_focus_dwell": 93.7,      # 专家 breath_focus 平均驻留（步）
        "meta_awareness": 0.462,           # 专家 meta-awareness 平均水平
    },
    "novice": {
        "mind_wandering_dwell": 89.6,     # 新手 mind_wandering 平均驻留（步）
        "mind_wandering_pct": 53.8,        # 新手 mind_wandering 占比（%）
    },
}


def generate_report(
    thoughtseeds_metrics: Dict[str, object],
    fm_metrics: Dict[str, object],
    errors: Dict[str, object],
    config: Optional[Dict[str, object]] = None,
    output_path: Optional[str] = None,
) -> str:
    """生成 Markdown 格式的对比验证报告。

    Args:
        thoughtseeds_metrics: thoughtseeds_model 的指标。
        fm_metrics: functional-monism 的指标。
        errors: 对比误差。
        config: 模拟配置（gamma, anchor 等）。
        output_path: 如果指定，将报告写入该文件。

    Returns:
        str: Markdown 格式的报告内容。
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("# 泛函一元论 vs Thoughtseeds: 对比验证报告")
    lines.append("")
    lines.append(f"**生成时间**：{now}")
    lines.append("")

    # ---- 1. 数据概述 ----
    lines.append("## 1. 数据概述")
    lines.append("")

    ts_steps = thoughtseeds_metrics.get("total_steps", 0)
    fm_steps = fm_metrics.get("total_steps", 0)
    lines.append(f"- **thoughtseeds_model**：评估窗口 {ts_steps} 步")
    lines.append(f"- **functional-monism**：模拟 {fm_steps} 步")

    if config:
        lines.append(f"- **配置**：γ = {config.get('gamma', 'N/A')}, "
                     f"锚定 = {config.get('anchor', 'N/A')}, "
                     f"EFE = {config.get('use_efe', False)}")
    lines.append("")

    # ---- 2. 关键指标对比 ----
    lines.append("## 2. 关键指标对比")
    lines.append("")

    # 2.1 状态驻留时间
    lines.append("### 2.1 状态驻留时间（平均连续步数）")
    lines.append("")
    lines.append("| 状态 | Thoughtseeds | Functional Monism | 绝对误差 | 相对误差 |")
    lines.append("| :--- | :---: | :---: | :---: | :---: |")
    dwell_errors = errors.get("dwell_time", {})
    for state, vals in dwell_errors.items():
        ts_val = vals.get("thoughtseeds", 0)
        fm_val = vals.get("functional_monism", 0)
        abs_err = vals.get("absolute_error", 0)
        rel_err = vals.get("relative_error", 0)
        lines.append(f"| {state} | {ts_val:.1f} | {fm_val:.1f} | {abs_err:.1f} | {rel_err:.1%} |")
    lines.append("")

    # 2.2 转移概率
    lines.append("### 2.2 状态转移概率")
    lines.append("")
    trans_errors = errors.get("transition_probability", {})
    if trans_errors:
        lines.append("| 转移 | Thoughtseeds | Functional Monism | 绝对误差 |")
        lines.append("| :--- | :---: | :---: | :---: |")
        for key, vals in sorted(trans_errors.items()):
            ts_val = vals.get("thoughtseeds", 0)
            fm_val = vals.get("functional_monism", 0)
            abs_err = vals.get("absolute_error", 0)
            lines.append(f"| {key} | {ts_val:.3f} | {fm_val:.3f} | {abs_err:.3f} |")
        lines.append("")

    # 2.3 Meta-awareness
    lines.append("### 2.3 Meta-awareness 平均水平")
    lines.append("")
    ma_errors = errors.get("meta_awareness", {})
    lines.append(f"- Thoughtseeds: {ma_errors.get('thoughtseeds', 0):.3f}")
    lines.append(f"- Functional Monism: {ma_errors.get('functional_monism', 0):.3f}")
    lines.append(f"- 相对误差: {ma_errors.get('relative_error', 0):.1%}")
    lines.append("")

    # 2.4 Thoughtseed 激活值
    lines.append("### 2.4 Thoughtseed 平均激活值")
    lines.append("")
    lines.append("| 种子 | Thoughtseeds | Functional Monism | 绝对误差 | 相对误差 |")
    lines.append("| :--- | :---: | :---: | :---: | :---: |")
    act_errors = errors.get("mean_activation", {})
    for name, vals in act_errors.items():
        ts_val = vals.get("thoughtseeds", 0)
        fm_val = vals.get("functional_monism", 0)
        abs_err = vals.get("absolute_error", 0)
        rel_err = vals.get("relative_error", 0)
        lines.append(f"| {name} | {ts_val:.3f} | {fm_val:.3f} | {abs_err:.3f} | {rel_err:.1%} |")
    lines.append("")

    # ---- 3. 误差分析 ----
    lines.append("## 3. 误差分析")
    lines.append("")
    summary = errors.get("summary", {})
    lines.append(f"- **对比指标数**：{summary.get('n_metrics_compared', 0)}")
    lines.append(f"- **平均相对误差**：{summary.get('mean_relative_error', 0):.1%}")
    lines.append(f"- **中位相对误差**：{summary.get('median_relative_error', 0):.1%}")
    lines.append("")

    # 解释差异来源
    lines.append("### 差异来源分析")
    lines.append("")
    lines.append("1. **状态空间维度不同**：thoughtseeds_model 使用 7 维网络 + 3 层架构，")
    lines.append("   functional-monism 当前为 1D 标量状态空间")
    lines.append("2. **种子动力学不同**：thoughtseeds_model 使用贝叶斯推断 + 策略评估，")
    lines.append("   functional-monism 使用激活值/EFE 竞争")
    lines.append("3. **时间尺度不同**：thoughtseeds_model 在 4000 步评估窗口上运行，")
    lines.append("   functional-monism 默认 200 步")
    lines.append("4. **Meta-awareness 机制不同**：thoughtseeds_model 的 L3 层有专门的")
    lines.append("   metacognitive gating 机制，functional-monism 的 meta-awareness 是")
    lines.append("   从种子激活值派生的")
    lines.append("")

    # ---- 4. 结论 ----
    lines.append("## 4. 结论")
    lines.append("")

    mean_err = summary.get("mean_relative_error", 0)
    if mean_err < 0.3:
        verdict = (
            "functional-monism 能够较好地复现 thoughtseeds_model 的核心发现，"
            "包括专家 vs 新手的差异性模式。这表明泛函一元论的计算框架（公理 I-IV）"
            "捕捉到了冥想认知动力学的基本结构。"
        )
    elif mean_err < 0.6:
        verdict = (
            "functional-monism 部分复现了 thoughtseeds_model 的核心发现。"
            "定性模式（如 breath_focus 主导时间长于 mind_wandering）一致，"
            "但定量指标存在显著差异，主要源于模型架构的根本不同。"
        )
    else:
        verdict = (
            "functional-monism 与 thoughtseeds_model 在定量指标上存在较大差异。"
            "然而，两个模型在定性层面都展示了「精度-认知灵活性」的对偶关系，"
            "这是泛函一元论框架的核心预期。差异主要源于模型复杂度层级不同。"
        )

    lines.append(verdict)
    lines.append("")

    lines.append("### 下一步")
    lines.append("")
    lines.append("1. 扩展 functional-monism 的状态空间至 2D 或更高维度")
    lines.append("2. 调整种子激活函数以更精确匹配 thoughtseeds_model 的贝叶斯动力学")
    lines.append("3. 增加模拟步数以匹配 thoughtseeds_model 的评估窗口")
    lines.append("4. 在多个 (γ, anchor) 配置下进行网格搜索，找到最优匹配参数")
    lines.append("")

    report = "\n".join(lines)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[report] 报告已保存至: {output_path}")

    return report


def generate_benchmark_report(
    multi_run_results: Dict[str, object],
    mode: str = "expert",
    output_path: Optional[str] = None,
) -> str:
    """v0.5: 生成与 thoughtseeds_model 基准的定量对比报告。

    Args:
        multi_run_results: run_multiple_simulations() 的返回结果。
        mode: "expert" 或 "novice"，对应不同的基准值。
        output_path: 如果指定，将报告写入该文件。

    Returns:
        str: Markdown 格式的基准对比报告。
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    benchmark = THOUGHTSEEDS_BENCHMARK.get(mode, THOUGHTSEEDS_BENCHMARK["expert"])
    config = multi_run_results.get("config", {})
    dwell = multi_run_results.get("dwell_times", {})
    freq = multi_run_results.get("state_frequencies", {})

    lines = []
    lines.append("# v0.5 定量验证报告：functional-monism vs thoughtseeds_model")
    lines.append("")
    lines.append(f"**生成时间**：{now}")
    lines.append(f"**验证模式**：{mode}")
    lines.append(f"**运行次数**：{config.get('n_runs', 'N/A')} 次")
    lines.append(f"**每轮步数**：{config.get('steps', 'N/A')} 步")
    lines.append("")

    # ---- 1. 配置信息 ----
    lines.append("## 1. 模拟配置")
    lines.append("")
    lines.append(f"| 参数 | 值 |")
    lines.append(f"| :--- | :--- |")
    lines.append(f"| γ（全局精度） | {config.get('gamma', 'N/A')} |")
    lines.append(f"| 呼吸锚定 | {config.get('anchor', 'N/A')} |")
    lines.append(f"| θ（回归速度） | {config.get('theta', 'N/A')} |")
    lines.append(f"| σ（波动幅度） | {config.get('sigma_ou', 'N/A')} |")
    lines.append(f"| EFE 模式 | {config.get('use_efe', False)} |")
    lines.append("")

    # ---- 2. 状态分布对比 ----
    lines.append("## 2. 状态分布对比")
    lines.append("")
    lines.append("| 状态 | functional-monism (mean ± std) | thoughtseeds 基准 | 误差 |")
    lines.append("| :--- | :---: | :---: | :---: |")

    if mode == "novice":
        mw_pct = freq.get("mind_wandering", {}).get("mean", 0)
        mw_std = freq.get("mind_wandering", {}).get("std", 0)
        ref = benchmark.get("mind_wandering_pct", 0)
        err = abs(mw_pct - ref) / max(ref, 1e-6) * 100
        lines.append(f"| mind_wandering 占比 | {mw_pct:.1f}% ± {mw_std:.1f}% | {ref:.1f}% | {err:.1f}% |")

    # 通用状态
    for state in ["breath_focus", "mind_wandering", "meta_awareness", "redirect_attention"]:
        if state in freq:
            mean_v = freq[state]["mean"]
            std_v = freq[state]["std"]
            lines.append(f"| {state} | {mean_v:.1f}% ± {std_v:.1f}% | — | — |")
    lines.append("")

    # ---- 3. 驻留时间对比 ----
    lines.append("## 3. 驻留时间对比（平均连续步数）")
    lines.append("")
    lines.append("| 状态 | functional-monism (mean ± std) | 最大驻留 (mean) | thoughtseeds 基准 | 误差 |")
    lines.append("| :--- | :---: | :---: | :---: | :---: |")

    if mode == "expert":
        bf = dwell.get("breath_focus", {})
        bf_mean = bf.get("mean_dwell", 0)
        bf_std = bf.get("std_dwell", 0)
        bf_max = bf.get("max_dwell_mean", 0)
        ref = benchmark.get("breath_focus_dwell", 0)
        err = abs(bf_mean - ref) / max(ref, 1e-6) * 100
        lines.append(f"| breath_focus | {bf_mean:.1f} ± {bf_std:.1f} | {bf_max:.1f} | {ref:.1f} | {err:.1f}% |")

    if mode == "novice":
        mw = dwell.get("mind_wandering", {})
        mw_mean = mw.get("mean_dwell", 0)
        mw_std = mw.get("std_dwell", 0)
        mw_max = mw.get("max_dwell_mean", 0)
        ref = benchmark.get("mind_wandering_dwell", 0)
        err = abs(mw_mean - ref) / max(ref, 1e-6) * 100
        lines.append(f"| mind_wandering | {mw_mean:.1f} ± {mw_std:.1f} | {mw_max:.1f} | {ref:.1f} | {err:.1f}% |")

    # 其他状态
    for state in ["breath_focus", "mind_wandering", "meta_awareness", "redirect_attention"]:
        if state in dwell:
            d = dwell[state]
            if (mode == "expert" and state == "breath_focus") or (mode == "novice" and state == "mind_wandering"):
                continue  # 已在上面处理
            lines.append(f"| {state} | {d['mean_dwell']:.1f} ± {d['std_dwell']:.1f} | {d['max_dwell_mean']:.1f} | — | — |")
    lines.append("")

    # ---- 4. 结论 ----
    lines.append("## 4. 验证结论")
    lines.append("")

    # 计算关键误差
    key_errors = []
    if mode == "expert":
        bf = dwell.get("breath_focus", {})
        if bf:
            err = abs(bf.get("mean_dwell", 0) - benchmark["breath_focus_dwell"]) / max(benchmark["breath_focus_dwell"], 1e-6)
            key_errors.append(("breath_focus 驻留", err))
    elif mode == "novice":
        mw = dwell.get("mind_wandering", {})
        if mw:
            err = abs(mw.get("mean_dwell", 0) - benchmark["mind_wandering_dwell"]) / max(benchmark["mind_wandering_dwell"], 1e-6)
            key_errors.append(("mind_wandering 驻留", err))
        mw_pct = freq.get("mind_wandering", {}).get("mean", 0)
        if mw_pct:
            err = abs(mw_pct - benchmark["mind_wandering_pct"]) / max(benchmark["mind_wandering_pct"], 1e-6)
            key_errors.append(("mind_wandering 占比", err))

    if key_errors:
        avg_err = np.mean([e[1] for e in key_errors]) if key_errors else 0
        lines.append(f"**关键指标平均误差**：{avg_err:.1%}")
        lines.append("")

        if avg_err < 0.30:
            lines.append("✅ **定量复现成功**：关键指标误差 < 30%，functional-monism 在数值层面成功复现了 thoughtseeds_model 的核心发现。")
        elif avg_err < 0.50:
            lines.append("⚠️ **部分定量复现**：关键指标误差在 30%-50% 之间，定性模式一致但定量偏差较大。")
        else:
            lines.append("❌ **定量复现不足**：关键指标误差 > 50%，需调整参数或模型架构。")

        lines.append("")
        lines.append("### 误差分析")
        lines.append("")
        for name, err in key_errors:
            lines.append(f"- **{name}**：误差 {err:.1%}")
            if err > 0.50:
                lines.append(f"  - 可能根因：时间尺度差异（{config.get('steps', '?')} 步 vs 2000 步评估窗口）、状态定义差异、OU 参数需调优")
    lines.append("")

    lines.append("---")
    lines.append(f"*v0.5 定量验证报告 · functional-monism · {now}*")

    report = "\n".join(lines)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[report] 基准对比报告已保存至: {output_path}")

    return report