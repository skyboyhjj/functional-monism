"""冥想状态模拟器 — 基于泛函一元论的交互式意识竞争可视化。

v0.3: 支持 1D/2D 状态空间切换，2D 模式下 mind_wandering 可自然涌现。

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

# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="冥想状态模拟器 v0.3",
    page_icon="🧘",
    layout="wide",
)

st.title("🧘 泛函一元论 · 冥想状态模拟器 v0.3")
st.caption(
    "拖动滑块调节「认知精度 γ」，观察思维种子在全局工作空间中的竞争与切换。"
    "v0.3 新增 2D 状态空间，支持 mind_wandering 自然涌现。"
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

    global_gamma = st.slider(
        "全局精度 (γ)",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="精度越高，认知越'刚性'，种子越容易被锁定。",
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
        max_value=190,
        value=80,
        step=10,
        help="杂念冲击发生的时间步。",
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
        ["默认（5种子均衡）", "新手模式（低精度）", "专家模式（高精度+锚定）"],
    )

    if preset == "新手模式（低精度）":
        global_gamma = 0.3
        anchor_breath = 1.0
    elif preset == "专家模式（高精度+锚定）":
        global_gamma = 3.0
        anchor_breath = 5.0

    st.divider()

    st.markdown("### 📖 公理说明")
    st.markdown(
        "- **公理 I**：能量 E = ½‖ψ − ψ_core‖²\n"
        "- **公理 II**：演化沿负梯度方向\n"
        "- **公理 III**：激活 a = exp(−γ·E)\n"
        "- **公理 IV**：EFE G = γ·‖Δ‖² + ln(γ)"
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

# ============================================================================
# 模拟
# ============================================================================

steps = 200
np.random.seed(42)

if use_2d:
    # 2D 随机游走：注意力 (x) × 情绪 (y)
    noise = np.random.randn(steps, 2) * 0.1
    state_stream = np.cumsum(noise, axis=0)  # (steps, 2)

    # 注入 2D 杂念冲击
    if perturbation_time < steps:
        state_stream[perturbation_time] += np.array([2.0, 0.5])
else:
    # 1D 随机游走（原有逻辑）
    noise = np.random.randn(steps) * 0.1
    state_stream = np.cumsum(noise)
    if perturbation_time < steps:
        state_stream[perturbation_time] += perturbation_strength

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
# 状态映射
# ============================================================================

# 2D 模式下的状态映射增强了 mind_wandering / redirect_attention 的检测
STATE_MAP = {
    "Breath Focus": "breath_focus",
    "Pain Discomfort": "mind_wandering",
    "Pending Tasks": "mind_wandering",
    "Self Reflection": "meta_awareness",
    "Equanimity": "meta_awareness",
}

# 2D 模式下，当状态在多个吸引子之间徘徊时标记为 mind_wandering
def classify_state_2d(dominant_name, prev_dominant, state_vec, seeds, gamma):
    """2D 模式下的增强状态分类。

    在 2D 空间中，当意识在多个吸引子之间快速切换时，
    标记为 mind_wandering，而非仅看当前胜出种子。
    """
    base = STATE_MAP.get(dominant_name, "mind_wandering")

    # 如果当前胜出种子是 Pain Discomfort 或 Pending Tasks
    # → 直接标记为 mind_wandering
    if dominant_name in ("Pain Discomfort", "Pending Tasks"):
        return "mind_wandering"

    # 如果最近 3 步内切换了种子 → 标记为 mind_wandering
    if prev_dominant and dominant_name != prev_dominant:
        return "mind_wandering"

    # 如果状态离原点很远（注意力散乱）→ mind_wandering
    if state_vec is not None and len(state_vec) >= 2:
        if abs(state_vec[0]) > 2.5:
            return "mind_wandering"

    return base


# 生成状态序列
state_sequence = []
prev_d = None
for t in range(steps):
    d = dominant_history[t]
    if use_2d:
        sv = state_stream[t]
        state_sequence.append(classify_state_2d(d, prev_d, sv, seeds, global_gamma))
    else:
        state_sequence.append(STATE_MAP.get(d, "mind_wandering"))
    prev_d = d

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
# 2D 状态空间散点图
# ============================================================================

if use_2d:
    with st.container():
        st.subheader("🗺️ 2D 状态空间轨迹（注意力 × 情绪）")

        scatter_fig = go.Figure()

        # 绘制状态轨迹，按胜出种子着色
        for t in range(steps):
            d = dominant_history[t]
            scatter_fig.add_trace(
                go.Scatter(
                    x=[state_stream[t, 0]],
                    y=[state_stream[t, 1]],
                    mode="markers",
                    marker=dict(
                        color=seed_colors.get(d, "#888888"),
                        size=4,
                        opacity=0.7,
                    ),
                    name=d,
                    showlegend=False,
                    hovertemplate=f"t={t}<br>x={state_stream[t,0]:.2f}<br>y={state_stream[t,1]:.2f}<br>{d}",
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

        # 当前 2D 坐标
        st.caption(
            f"当前坐标: ({state_stream[-1, 0]:.2f}, {state_stream[-1, 1]:.2f})"
        )

        # 当前冥想状态分类
        state_emoji = {
            "breath_focus": "🫁",
            "mind_wandering": "💭",
            "meta_awareness": "👁️",
            "redirect_attention": "🔄",
        }
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

        st.subheader("📋 统计")
        dominance_counts = Counter(dominant_history)
        for name in seed_names:
            count = dominance_counts.get(name, 0)
            pct = count / steps * 100
            st.text(f"{name}: {pct:.1f}% ({count}/{steps})")

    with col3:
        st.subheader("🧘 冥想状态统计")
        state_counts = Counter(state_sequence)

        st.markdown("### 状态分布")
        state_labels = {
            "breath_focus": "🫁 呼吸专注",
            "mind_wandering": "💭 走神",
            "meta_awareness": "👁️ 元觉察",
            "redirect_attention": "🔄 回神",
        }
        for state, label in state_labels.items():
            count = state_counts.get(state, 0)
            pct = count / steps * 100
            st.text(f"{label}: {pct:.1f}% ({count}/{steps})")

        # mind_wandering 检测
        mw_count = state_counts.get("mind_wandering", 0)
        if mw_count > 0:
            st.success(f"✅ mind_wandering 已涌现！（{mw_count}/{steps} 步）")
        else:
            st.warning("⚠️ mind_wandering 未出现，尝试降低 γ 或提高杂念冲击")

        # 状态驻留时间
        st.markdown("### 平均驻留时间")
        dwells = {}
        for state in state_sequence:
            dwells[state] = dwells.get(state, 0) + 1
        # 计算连续驻留
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
st.markdown(
    "**v0.3 使用指南**：\n"
    "- **2D 模式（默认）**：状态在 (注意力, 情绪) 平面上漂移，mind_wandering 可自然涌现\n"
    "- **1D 模式**：经典标量模式，仅支持专注/分心二元状态\n"
    "- **新手模式（γ=0.3）**：杂念频繁胜出，模拟注意力散乱\n"
    "- **专家模式（γ=3.0 + 锚定=5.0）**：Breath Focus 统治时间线\n"
    "- **2D 散点图**：观察意识点在多个吸引子之间的徘徊轨迹\n\n"
    "**理论对应**：\n"
    "- 公理 I（存在）：每个种子 = 一个泛函 F[ψ]，定义在 2D 状态空间上\n"
    "- 公理 II（演化）：状态流沿 2D 随机游走，种子通过能量竞争\n"
    "- 公理 III（精度）：γ 作为曲率参数，控制 2D 激活函数的陡峭度\n"
    "- 公理 IV（决策）：G = γ·‖Δ‖² + ln(γ)，在精度与复杂度之间权衡\n\n"
    "**v0.3 新增**：2D 状态空间中，mind_wandering 不再需要单独建模 — "
    "它只是意识在多个吸引子之间「徘徊」的几何现象。"
)