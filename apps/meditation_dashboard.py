"""冥想状态模拟器 — 基于泛函一元论的交互式意识竞争可视化。

v0.9: 微调 OU 参数，延长新手 mind_wandering 驻留时间。

启动方式:
    streamlit run apps/meditation_dashboard.py

依赖:
    pip install streamlit plotly jax jaxlib numpy
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import numpy as np
import jax.numpy as jnp
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter

from src.models.workspace import MeditationSeed, GlobalWorkspace, create_default_seeds
from src.models.ou_noise import OUNoise
from src.validation.comparator import run_multiple_simulations
from src.validation.metrics import classify_state_with_buffer, compute_buffer_size
from src.validation.report import generate_benchmark_report, THOUGHTSEEDS_BENCHMARK

# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="冥想状态模拟器 v0.9",
    page_icon="🧘",
    layout="wide",
)

st.title("🧘 泛函一元论 · 冥想状态模拟器 v0.9")
st.caption(
    "v0.9 微调：降低新手模式 σ（0.35→0.28）和 θ（0.06→0.05），"
    "延长 mind_wandering 连续驻留，减少碎片化。"
)

# ============================================================================
# 侧边栏：控制旋钮
# ============================================================================

with st.sidebar:
    st.header("⚙️ 控制旋钮")

    # 模式选择
    use_2d = st.checkbox(
        "2D 状态空间（注意力 × 情绪）",
        value=True,
        help="启用 2D 模式后，状态在 (注意力, 情绪) 平面上漂移，"
             "mind_wandering 可自然涌现。关闭则回退到 1D 标量模式。",
    )

    st.divider()

    st.markdown("### ⏱️ 模拟步数（v0.5 新增）")
    steps = st.slider(
        "模拟步数",
        min_value=100,
        max_value=5000,
        value=2000,
        step=100,
        help="v0.5 默认 2000 步，与 thoughtseeds_model 评估窗口对齐。步数越多，驻留时间统计越准确。",
    )

    st.divider()

    global_gamma = st.slider(
        "全局精度 (γ)",
        min_value=0.1,
        max_value=5.0,
        value=0.5,
        step=0.1,
        help="精度越高，认知越'刚性'，种子越容易被锁定。v0.4 默认 0.5 以促进走神。",
    )

    anchor_breath = st.slider(
        "呼吸锚定强度",
        min_value=1.0,
        max_value=10.0,
        value=1.0,
        step=0.5,
        help="增强 Breath Focus 种子的有效精度。",
    )

    perturbation_strength = st.slider(
        "杂念冲击强度",
        min_value=0.0,
        max_value=5.0,
        value=2.0,
        step=0.5,
        help="外部杂念的干扰强度。",
    )

    perturbation_time = st.slider(
        "杂念冲击时刻",
        min_value=0,
        max_value=steps - 10,
        value=min(80, steps - 10),
        step=10,
        help="杂念冲击发生的时间步。",
    )

    st.divider()

    st.markdown("### 🌊 OU 噪声参数（v0.4 新增）")
    st.caption("Ornstein-Uhlenbeck: dx = θ(μ − x)dt + σ · dW")

    theta = st.slider(
        "回归速度 (θ)",
        min_value=0.02,
        max_value=0.50,
        value=0.10,
        step=0.01,
        help="θ 越大 → 状态越快回归原点（breath_focus）。v0.4 默认 0.10 平衡走神与回神。专家建议 0.20~0.30，新手建议 0.05~0.10。",
    )

    sigma_ou = st.slider(
        "波动幅度 (σ)",
        min_value=0.05,
        max_value=0.50,
        value=0.35,
        step=0.01,
        help="σ 越大 → 走神越剧烈。新手模式建议 0.25~0.35，专家模式建议 0.10~0.20。",
    )

    st.divider()

    st.markdown("### 🎯 状态分类阈值（v0.4 新增）")
    st.caption("调整阈值以控制状态分类的敏感度")

    threshold_near = st.slider(
        "吸引子附近阈值",
        min_value=0.5,
        max_value=4.0,
        value=2.5,
        step=0.1,
        help="状态距离吸引子多远算'在附近'。值越大 → 越容易触发 mind_wandering。v0.4 默认 2.5。",
    )

    threshold_far = st.slider(
        "远离原点阈值",
        min_value=0.5,
        max_value=3.0,
        value=1.0,
        step=0.1,
        help="状态距离原点多远算'远离'，用于触发 redirect_attention。值越小 → 越容易检测回神。v0.4 默认 1.0。",
    )

    st.divider()

    st.markdown("### ⏳ 时域滤波（v0.8 自适应）")
    st.caption("buffer_size = round(9/(γ+1) + σ×1.5)，范围 [2, 12]")

    # v0.7: 自适应缓冲大小，从 γ 和 σ 动态计算
    buffer_size = compute_buffer_size(global_gamma, sigma_ou)
    st.metric(
        label="当前自适应缓冲大小",
        value=f"{buffer_size} 步",
        delta=f"γ={global_gamma:.1f}, σ={sigma_ou:.2f}",
    )
    st.caption(
        "buffer_size 由 γ 和 σ 自动决定，无需手动调整。"
        "γ 越高 → 缓冲越短（灵敏切换）；σ 越大 → 缓冲越长（稳定判别）。"
    )

    breath_zone_radius = st.slider(
        "呼吸区半径",
        min_value=0.2,
        max_value=2.0,
        value=0.5,
        step=0.1,
        help="原点周围多大范围算'呼吸专注区'。专家模式建议 0.3~0.5，新手模式建议 0.5~1.0。",
    )

    st.divider()

    use_efe = st.checkbox(
        "EFE 竞争模式（预期自由能最小化）",
        value=False,
        help="启用后，竞争机制从'激活值最高者胜出'切换为'预期自由能最低者胜出'。",
    )

    st.divider()

    st.markdown("### 🧠 场景预设")
    preset = st.selectbox(
        "选择预设场景",
        [
            "默认（5种子均衡）",
            "新手模式（低精度 + 弱回归 + 高波动）",
            "专家模式（高精度 + 锚定 + 强回归）",
        ],
    )

    if "新手" in preset:
        global_gamma = 0.3
        anchor_breath = 1.0
        theta = 0.05
        sigma_ou = 0.28
    elif "专家" in preset:
        global_gamma = 3.0
        anchor_breath = 5.0
        theta = 0.25
        sigma_ou = 0.15

    st.divider()

    st.markdown("### 🔬 验证模式（v0.5 新增）")
    validate_mode = st.checkbox(
        "启用定量验证",
        value=False,
        help="启用后自动运行 20 次 × 2000 步模拟，"
             "与 thoughtseeds_model 基准进行数值对比。",
    )

    if validate_mode:
        validate_mode_type = st.selectbox(
            "验证场景",
            ["专家模式", "新手模式"],
            help="选择与哪个 thoughtseeds_model 基准对比。",
        )

    st.divider()

    st.markdown("### 📖 公理说明")
    st.markdown(
        "- **公理 I**：能量 E = ½‖ψ − ψ_core‖²\n"
        "- **公理 II**：演化沿负梯度方向\n"
        "- **公理 III**：激活 a = exp(−γ·E)\n"
        "- **公理 IV**：EFE G = γ·‖Δ‖² + ln(γ)\n\n"
        "**v0.4 OU 动力学**：\n"
        "- dx = θ(μ − x)dt + σ · dW\n"
        "- 高 θ = 强回归 → 专家稳定\n"
        "- 低 θ = 弱回归 → 新手走神"
    )

# ============================================================================
# 初始化种子与工作空间
# ============================================================================

dim = 2 if use_2d else 1
seeds = create_default_seeds(dim=dim)
seed_names = [s.name for s in seeds]
seed_colors = {
    "Breath Focus": "#4CAF50",
    "Pain Discomfort": "#FF5722",
    "Pending Tasks": "#FF9800",
    "Self Reflection": "#9C27B0",
    "Equanimity": "#2196F3",
}

workspace = GlobalWorkspace(seeds)

# 种子吸引子坐标（用于距离计算）
attractor_positions = {
    s.name: np.array(s.core_attractor).ravel() for s in seeds
}

# ============================================================================
# 模拟：OU 噪声驱动
# ============================================================================

np.random.seed(42)

if use_2d:
    # OU 过程生成 2D 轨迹
    ou = OUNoise(dim=2, theta=theta, sigma=sigma_ou)
    perturbations = []
    if perturbation_time < steps:
        perturbations.append((perturbation_time, np.array([2.0, 0.5])))
    state_stream = ou.generate_trajectory(steps, perturbations=perturbations)
else:
    # 1D OU 过程
    ou = OUNoise(dim=1, theta=theta, sigma=sigma_ou)
    perturbations = []
    if perturbation_time < steps:
        perturbations.append((perturbation_time, np.array([perturbation_strength])))
    state_stream = ou.generate_trajectory(steps, perturbations=perturbations).ravel()

# 存储每步的激活值
activation_history = {name: np.zeros(steps) for name in seed_names}
dominant_history = [""] * steps

for t in range(steps):
    if use_2d:
        state = jnp.asarray(state_stream[t], dtype=jnp.float32)
    else:
        state = float(state_stream[t])

    workspace.seeds[0].precision_boost = anchor_breath
    activations, dominant = workspace.compete(state, global_gamma, use_efe=use_efe)

    for seed in workspace.seeds:
        activation_history[seed.name][t] = seed.activation
    dominant_history[t] = dominant.name

# ============================================================================
# v0.7 时域滤波分类：使用 classify_state_with_buffer（自适应缓冲）
# ============================================================================

# 生成状态序列（v0.7：自适应缓冲，buffer_size 从 gamma/sigma 动态计算）
state_sequence = []
if use_2d:
    state_sequence = classify_state_with_buffer(
        state_stream=list(state_stream),
        attractors=attractor_positions,
        dominant_history=dominant_history,
        gamma=global_gamma,
        sigma=sigma_ou,
        buffer_size=buffer_size,
        breath_zone_radius=breath_zone_radius,
    )
else:
    STATE_MAP = {
        "Breath Focus": "breath_focus",
        "Pain Discomfort": "mind_wandering",
        "Pending Tasks": "mind_wandering",
        "Self Reflection": "meta_awareness",
        "Equanimity": "meta_awareness",
    }
    state_sequence = [STATE_MAP.get(d, "mind_wandering") for d in dominant_history]

# ============================================================================
# 主区域：图表
# ============================================================================

if use_2d:
    col1, col2, col3 = st.columns([2, 1, 1])
else:
    col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📈 思维种子激活轨迹")

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.75, 0.25],
        vertical_spacing=0.08,
        subplot_titles=("激活值 (0~1)", "当前主宰种子"),
    )

    for name in seed_names:
        fig.add_trace(
            go.Scatter(
                y=activation_history[name],
                mode="lines",
                name=name,
                line=dict(color=seed_colors.get(name, "#888888"), width=2),
                hovertemplate=f"{name}: %{{y:.3f}}",
            ),
            row=1, col=1,
        )

    if perturbation_time < steps:
        fig.add_vline(
            x=perturbation_time, line_dash="dash", line_color="red",
            annotation_text="杂念冲击", annotation_position="top",
            row=1, col=1,
        )

    unique_dominants = sorted(set(dominant_history))
    name_to_y = {name: i for i, name in enumerate(unique_dominants)}
    y_vals = [name_to_y[d] for d in dominant_history]
    color_vals = [seed_colors.get(d, "#888888") for d in dominant_history]

    fig.add_trace(
        go.Scatter(
            y=y_vals,
            mode="markers",
            marker=dict(color=color_vals, size=3, symbol="square"),
            showlegend=False,
            hovertemplate="%{text}",
            text=dominant_history,
        ),
        row=2, col=1,
    )

    fig.update_yaxes(
        tickvals=list(name_to_y.values()),
        ticktext=list(name_to_y.keys()),
        row=2, col=1,
    )
    fig.update_xaxes(title_text="时间步", row=2, col=1)
    fig.update_layout(
        height=550,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )

    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# 2D 状态空间散点图（v0.4：按冥想状态着色）
# ============================================================================

if use_2d:
    with st.container():
        st.subheader("🗺️ 2D 状态空间轨迹 — 按冥想状态着色（v0.4）")

        scatter_fig = go.Figure()

        state_colors = {
            "breath_focus": "#4CAF50",
            "mind_wandering": "#FF5722",
            "meta_awareness": "#9C27B0",
            "redirect_attention": "#2196F3",
        }

        # 绘制状态轨迹，按冥想状态着色
        for t in range(steps):
            med_s = state_sequence[t]
            scatter_fig.add_trace(
                go.Scatter(
                    x=[state_stream[t, 0]],
                    y=[state_stream[t, 1]],
                    mode="markers",
                    marker=dict(
                        color=state_colors.get(med_s, "#888888"),
                        size=4,
                        opacity=0.7,
                    ),
                    name=med_s,
                    showlegend=False,
                    hovertemplate=f"t={t}<br>x={state_stream[t,0]:.2f}<br>y={state_stream[t,1]:.2f}<br>状态: {med_s}<br>种子: {dominant_history[t]}",
                )
            )

        # 标记种子吸引子位置
        for s in seeds:
            core = s.core_attractor
            scatter_fig.add_trace(
                go.Scatter(
                    x=[float(core[0])],
                    y=[float(core[1])],
                    mode="markers+text",
                    marker=dict(
                        color=seed_colors.get(s.name, "#888888"),
                        size=14,
                        symbol="star",
                        line=dict(width=2, color="white"),
                    ),
                    text=[s.name],
                    textposition="top center",
                    textfont=dict(size=10),
                    name=f"吸引子: {s.name}",
                    showlegend=True,
                    hovertemplate=f"吸引子: {s.name}<br>({float(core[0]):.1f}, {float(core[1]):.1f})",
                )
            )

        # 标记原点（OU 均值回归目标）
        scatter_fig.add_trace(
            go.Scatter(
                x=[0],
                y=[0],
                mode="markers+text",
                marker=dict(color="black", size=16, symbol="cross", line=dict(width=2)),
                text=["原点 μ"],
                textposition="bottom right",
                textfont=dict(size=10, color="black"),
                name="OU 均值 μ",
                showlegend=True,
                hovertemplate="OU 均值 μ (0, 0)<br>回归目标",
            )
        )

        # 标记起始点
        scatter_fig.add_trace(
            go.Scatter(
                x=[state_stream[0, 0]],
                y=[state_stream[0, 1]],
                mode="markers",
                marker=dict(color="black", size=10, symbol="circle-open"),
                name="起点",
                showlegend=True,
            )
        )

        # 标记终点
        scatter_fig.add_trace(
            go.Scatter(
                x=[state_stream[-1, 0]],
                y=[state_stream[-1, 1]],
                mode="markers",
                marker=dict(color="black", size=10, symbol="x"),
                name="终点",
                showlegend=True,
            )
        )

        # v0.6: 呼吸区叠加（浅绿色半透明圆）
        theta_circle = np.linspace(0, 2 * np.pi, 100)
        cx = breath_zone_radius * np.cos(theta_circle)
        cy = breath_zone_radius * np.sin(theta_circle)
        scatter_fig.add_trace(
            go.Scatter(
                x=cx.tolist(),
                y=cy.tolist(),
                mode="lines",
                fill="toself",
                fillcolor="rgba(76, 175, 80, 0.12)",
                line=dict(color="rgba(76, 175, 80, 0.4)", width=1, dash="dot"),
                name=f"呼吸区 r={breath_zone_radius}",
                showlegend=True,
                hovertemplate=f"呼吸区 r={breath_zone_radius}",
            )
        )

        scatter_fig.update_layout(
            height=500,
            xaxis_title="注意力 (专注 ← → 散乱)",
            yaxis_title="情绪 (平和 ← → 紧张)",
            xaxis=dict(range=[-6, 6], zeroline=True, zerolinecolor="#ddd"),
            yaxis=dict(range=[-6, 6], zeroline=True, zerolinecolor="#ddd"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )

        st.plotly_chart(scatter_fig, use_container_width=True)

# ============================================================================
# 右侧：当前状态与统计
# ============================================================================

state_emoji = {
    "breath_focus": "🫁",
    "mind_wandering": "💭",
    "meta_awareness": "👁️",
    "redirect_attention": "🔄",
}
state_labels = {
    "breath_focus": "🫁 呼吸专注",
    "mind_wandering": "💭 走神",
    "meta_awareness": "👁️ 元觉察",
    "redirect_attention": "🔄 回神",
}

if use_2d:
    with col2:
        st.subheader("🎯 当前状态")
        current_dominant = dominant_history[-1]
        current_meditation_state = state_sequence[-1]
        st.metric(
            label="聚光灯种子",
            value=current_dominant,
            delta=f"γ={global_gamma:.1f}",
        )
        st.caption(
            f"当前坐标: ({state_stream[-1, 0]:.2f}, {state_stream[-1, 1]:.2f})"
        )
        st.metric(
            label="冥想状态",
            value=f"{state_emoji.get(current_meditation_state, '❓')} {current_meditation_state}",
        )

        st.subheader("📊 最终激活值")
        final_acts = {name: activation_history[name][-1] for name in seed_names}
        bar_fig = go.Figure(
            go.Bar(
                x=list(final_acts.values()),
                y=list(final_acts.keys()),
                orientation="h",
                marker_color=[seed_colors.get(n, "#888888") for n in final_acts.keys()],
                text=[f"{v:.3f}" for v in final_acts.values()],
                textposition="outside",
            )
        )
        bar_fig.update_layout(
            height=250,
            margin=dict(l=0, r=40, t=0, b=0),
            xaxis=dict(range=[0, 1.05], title="激活值"),
        )
        st.plotly_chart(bar_fig, use_container_width=True)

        if use_efe:
            st.subheader("⚡ 预期自由能 (EFE)")
            current_state = jnp.asarray(state_stream[-1], dtype=jnp.float32)
            efe_values = workspace.get_efe_values(current_state, global_gamma)
            for name in seed_names:
                efe = efe_values.get(name, 0.0)
                st.text(f"{name}: {efe:.3f}")
            st.caption("EFE 越低 = 该种子越有优势")

        st.subheader("📋 种子统计")
        dominance_counts = Counter(dominant_history)
        for name in seed_names:
            count = dominance_counts.get(name, 0)
            pct = count / steps * 100
            st.text(f"{name}: {pct:.1f}% ({count}/{steps})")

    with col3:
        st.subheader("🧘 冥想状态统计")
        state_counts = Counter(state_sequence)

        st.markdown("### 状态分布")
        for state, label in state_labels.items():
            count = state_counts.get(state, 0)
            pct = count / steps * 100
            st.text(f"{label}: {pct:.1f}% ({count}/{steps})")

        # mind_wandering 比例检测
        mw_count = state_counts.get("mind_wandering", 0)
        mw_pct = mw_count / steps * 100
        if mw_pct >= 40:
            st.success(f"✅ mind_wandering {mw_pct:.1f}%（接近 ts 新手基准 53.8%）")
        elif mw_pct >= 20:
            st.info(f"✅ mind_wandering {mw_pct:.1f}%（接近 ts 专家基准 24.1%）")
        elif mw_pct > 0:
            st.warning(f"⚠️ mind_wandering {mw_pct:.1f}%（偏低，尝试降低 θ 或提高 σ）")
        else:
            st.warning("⚠️ mind_wandering 未出现")

        # redirect_attention 检测
        ra_count = state_counts.get("redirect_attention", 0)
        ra_pct = ra_count / steps * 100
        if ra_pct > 0:
            st.success(f"✅ redirect_attention {ra_pct:.1f}% 已涌现！")
        else:
            st.info("ℹ️ redirect_attention 未出现，尝试提高 θ 以增强回归力")

        # 状态驻留时间
        st.markdown("### 平均驻留时间")
        consec_dwells = {}
        current_s = state_sequence[0] if state_sequence else ""
        current_count = 1
        for s in state_sequence[1:]:
            if s == current_s:
                current_count += 1
            else:
                consec_dwells.setdefault(current_s, []).append(current_count)
                current_s = s
                current_count = 1
        consec_dwells.setdefault(current_s, []).append(current_count)

        for state in ["breath_focus", "mind_wandering", "meta_awareness", "redirect_attention"]:
            if state in consec_dwells:
                avg = np.mean(consec_dwells[state])
                st.text(f"{state_labels.get(state, state)}: {avg:.1f} 步")

        # OU 参数信息
        st.markdown("### 🌊 OU 参数")
        st.caption(f"θ = {theta:.2f}（回归速度）")
        st.caption(f"σ = {sigma_ou:.2f}（波动幅度）")
        st.caption(f"目标均值 μ = 0（原点）")

else:
    with col2:
        st.subheader("🎯 当前状态")
        current_dominant = dominant_history[-1]
        st.metric(
            label="聚光灯种子",
            value=current_dominant,
            delta=f"γ={global_gamma:.1f}",
        )

        bar_title = "最终激活值（EFE 模式下的胜出者）" if use_efe else "最终激活值"
        st.subheader(f"📊 {bar_title}")
        final_acts = {name: activation_history[name][-1] for name in seed_names}
        bar_fig = go.Figure(
            go.Bar(
                x=list(final_acts.values()),
                y=list(final_acts.keys()),
                orientation="h",
                marker_color=[seed_colors.get(n, "#888888") for n in final_acts.keys()],
                text=[f"{v:.3f}" for v in final_acts.values()],
                textposition="outside",
            )
        )
        bar_fig.update_layout(
            height=250,
            margin=dict(l=0, r=40, t=0, b=0),
            xaxis=dict(range=[0, 1.05], title="激活值"),
        )
        st.plotly_chart(bar_fig, use_container_width=True)

        if use_efe:
            st.subheader("⚡ 预期自由能 (EFE)")
            current_state = float(state_stream[-1])
            efe_values = workspace.get_efe_values(current_state, global_gamma)
            for name in seed_names:
                efe = efe_values.get(name, 0.0)
                st.text(f"{name}: {efe:.3f}")
            st.caption("EFE 越低 = 该种子越有优势")

        st.subheader("📋 统计")
        dominance_counts = Counter(dominant_history)
        for name in seed_names:
            count = dominance_counts.get(name, 0)
            pct = count / steps * 100
            st.text(f"{name}: {pct:.1f}% ({count}/{steps})")

# ============================================================================
# 底部说明
# ============================================================================

st.divider()

# ============================================================================
# v0.5 验证模式：定量对比
# ============================================================================

if validate_mode:
    st.header("🔬 v0.5 定量验证报告")

    # 根据验证场景选择参数
    if "专家" in validate_mode_type:
        v_gamma = 3.0
        v_anchor = 3.0
        v_theta = 0.25
        v_sigma = 0.15
        v_efe = False
        mode_key = "expert"
    else:
        v_gamma = 0.3
        v_anchor = 1.0
        v_theta = 0.06
        v_sigma = 0.35
        v_efe = True
        mode_key = "novice"

    with st.spinner(f"正在运行 20 次 × 2000 步模拟（{validate_mode_type}）..."):
        multi_results = run_multiple_simulations(
            n_runs=20,
            steps=2000,
            gamma=v_gamma,
            anchor=v_anchor,
            theta=v_theta,
            sigma_ou=v_sigma,
            use_efe=v_efe,
            threshold_near=threshold_near,
            threshold_far=threshold_far,
        )

    benchmark = THOUGHTSEEDS_BENCHMARK.get(mode_key, {})

    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.subheader("📊 状态分布 (mean ± std)")
        freq = multi_results.get("state_frequencies", {})
        for state in ["breath_focus", "mind_wandering", "meta_awareness", "redirect_attention"]:
            if state in freq:
                f = freq[state]
                st.metric(
                    label=state_labels.get(state, state),
                    value=f"{f['mean']:.1f}%",
                    delta=f"±{f['std']:.1f}%",
                )

    with col_v2:
        st.subheader("⏱️ 平均驻留时间 (mean ± std)")
        dwell = multi_results.get("dwell_times", {})
        for state in ["breath_focus", "mind_wandering", "meta_awareness", "redirect_attention"]:
            if state in dwell:
                d = dwell[state]
                st.metric(
                    label=state_labels.get(state, state),
                    value=f"{d['mean_dwell']:.1f} 步",
                    delta=f"±{d['std_dwell']:.1f} 步",
                )

    st.divider()

    # 基准对比表
    st.subheader("🎯 thoughtseeds_model 基准对比")
    report = generate_benchmark_report(multi_results, mode=mode_key)
    st.markdown(report)

    # 误差条图
    st.subheader("📉 驻留时间误差条图")
    error_fig = go.Figure()

    dwell_states = []
    dwell_means = []
    dwell_stds = []
    for state in ["breath_focus", "mind_wandering", "meta_awareness", "redirect_attention"]:
        if state in dwell:
            dwell_states.append(state_labels.get(state, state))
            dwell_means.append(dwell[state]["mean_dwell"])
            dwell_stds.append(dwell[state]["std_dwell"])

    if dwell_states:
        error_fig.add_trace(
            go.Bar(
                x=dwell_states,
                y=dwell_means,
                error_y=dict(type="data", array=dwell_stds, visible=True),
                marker_color=["#4CAF50", "#FF5722", "#9C27B0", "#2196F3"][:len(dwell_states)],
                name="functional-monism",
            )
        )

        # 添加基准线
        if mode_key == "expert" and "breath_focus_dwell" in benchmark:
            error_fig.add_hline(
                y=benchmark["breath_focus_dwell"],
                line_dash="dash",
                line_color="green",
                annotation_text=f"ts 基准: {benchmark['breath_focus_dwell']} 步",
            )
        elif mode_key == "novice" and "mind_wandering_dwell" in benchmark:
            error_fig.add_hline(
                y=benchmark["mind_wandering_dwell"],
                line_dash="dash",
                line_color="orange",
                annotation_text=f"ts 基准: {benchmark['mind_wandering_dwell']} 步",
            )

        error_fig.update_layout(
            height=400,
            yaxis_title="平均驻留时间（步）",
            showlegend=False,
        )
        st.plotly_chart(error_fig, use_container_width=True)

st.divider()
st.markdown(
    "**v0.7 使用指南**：\n"
    "- **自适应缓冲**：buffer_size = round(10/(γ+1) + σ×2)，高精度→短缓冲（灵敏切换），低精度→长缓冲（稳定驻留）\n"
    "- **时代滤波**：状态必须连续 N 步满足条件才触发切换，消除瞬时几何分类的碎片化\n"
    "- **呼吸区**：2D 散点图中浅绿色半透明圆，半径 = 呼吸区半径，状态在此区域内连续驻留 → breath_focus\n"
    "- **OU 噪声**：状态遵循 Ornstein-Uhlenbeck 过程，具有向原点回归的内置倾向\n"
    "- **θ（回归速度）**：越高 → 回神越快 → 专家模式；越低 → 容易走神 → 新手模式\n"
    "- **模拟步数**：默认 2000 步，与 thoughtseeds_model 评估窗口对齐\n"
    "- **验证模式**：启用后自动运行 20 次 × 2000 步，输出 mean ± std 和基准对比\n\n"
    "**v0.9 默认参数**：γ=0.5, θ=0.10, σ=0.35, buffer=自适应, breath_zone=0.5, mw_zone=1.8\n"
    "**v0.9 新手模式**：γ=0.3, θ=0.05, σ=0.28, EFE=开  (驻留目标 55-65 步)\n"
    "**理论对应**：\n"
    "- 公理 I（存在）：每个种子 = 一个泛函 F[ψ]，定义在 2D 状态空间上\n"
    "- 公理 II（演化）：dx = θ(μ − x)dt + σ · dW — 均值回归 + 扩散\n"
    "- 公理 III（精度）：γ 作为曲率参数，控制激活函数的陡峭度 和 缓冲时间窗口\n"
    "- 公理 IV（决策）：G = γ·‖Δ‖² + ln(γ)，在精度与复杂度之间权衡\n\n"
    "**v0.9 微调**：降低 σ（0.35→0.28）减少高频振荡，降低 θ（0.06→0.05）减弱回归力。"
    "让状态在杂念吸引域内更平滑地停留，延长 mind_wandering 连续驻留。"
)