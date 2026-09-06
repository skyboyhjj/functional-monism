"""冥想状态模拟器 — 基于泛函一元论的交互式意识竞争可视化。

v0.4: Ornstein-Uhlenbeck 噪声驱动，mind_wandering 逼近 thoughtseeds_model 基准值，
      引入 redirect_attention 检测与 OU 参数调节。

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

# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="冥想状态模拟器 v0.4",
    page_icon="🧘",
    layout="wide",
)

st.title("🧘 泛函一元论 · 冥想状态模拟器 v0.4")
st.caption(
    "v0.4 升级：Ornstein-Uhlenbeck 噪声驱动，带均值回归的状态动力学。"
    "意识不再是"无头苍蝇"，而是"系着弹性绳的漫步者"。"
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

    st.markdown("### 🌊 OU 噪声参数（v0.4 新增）")
    st.caption("Ornstein-Uhlenbeck: dx = θ(μ − x)dt + σ · dW")

    theta = st.slider(
        "回归速度 (θ)",
        min_value=0.02,
        max_value=0.50,
        value=0.15,
        step=0.01,
        help="θ 越大 → 状态越快回归原点（breath_focus）。专家模式建议 0.20~0.30，新手模式建议 0.05~0.10。",
    )

    sigma_ou = st.slider(
        "波动幅度 (σ)",
        min_value=0.05,
        max_value=0.50,
        value=0.20,
        step=0.01,
        help="σ 越大 → 走神越剧烈。新手模式建议 0.25~0.35，专家模式建议 0.10~0.20。",
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
        theta = 0.08
        sigma_ou = 0.30
    elif "专家" in preset:
        global_gamma = 3.0
        anchor_breath = 5.0
        theta = 0.25
        sigma_ou = 0.15

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

steps = 200
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
# v0.4 增强状态分类：基于吸引子距离 + 连续驻留 + 回归检测
# ============================================================================

def classify_state_v4(
    state_vec: np.ndarray,
    dominant_name: str,
    attractors: dict,
    prev_state_vec: np.ndarray = None,
    threshold_near: float = 1.5,
    threshold_far: float = 2.0,
) -> str:
    """基于吸引子距离和回归检测的 4 状态分类。

    1. 杂念种子附近 → mind_wandering
    2. 远离原点后快速回拉 → redirect_attention
    3. 元认知种子附近 → meta_awareness
    4. 默认 → breath_focus

    Args:
        state_vec: 当前 2D 状态坐标。
        dominant_name: 当前胜出种子名。
        attractors: {name: np.ndarray} 吸引子坐标。
        prev_state_vec: 上一步状态坐标（用于回归检测）。
        threshold_near: 被视为"在吸引子附近"的距离阈值。
        threshold_far: 被视为"远离原点"的距离阈值。

    Returns:
        str: 冥想状态 (breath_focus | mind_wandering | meta_awareness | redirect_attention)。
    """
    dist_to_origin = np.linalg.norm(state_vec)

    # 1. 杂念种子吸引子附近 → mind_wandering
    dist_to_pain = np.linalg.norm(state_vec - attractors["Pain Discomfort"])
    dist_to_tasks = np.linalg.norm(state_vec - attractors["Pending Tasks"])
    if dist_to_pain < threshold_near or dist_to_tasks < threshold_near:
        return "mind_wandering"

    # 2. 远离原点后快速回拉 → redirect_attention
    if prev_state_vec is not None:
        prev_dist = np.linalg.norm(prev_state_vec)
        if (
            prev_dist > threshold_far
            and dist_to_origin < threshold_near
            and dist_to_origin < prev_dist * 0.6
        ):
            return "redirect_attention"

    # 3. 元认知种子附近 → meta_awareness
    dist_to_reflection = np.linalg.norm(state_vec - attractors["Self Reflection"])
    dist_to_equanimity = np.linalg.norm(state_vec - attractors["Equanimity"])
    if dist_to_reflection < threshold_near or dist_to_equanimity < threshold_near:
        return "meta_awareness"

    # 4. 默认 → breath_focus
    return "breath_focus"


# 生成状态序列
state_sequence = []
if use_2d:
    for t in range(steps):
        prev_sv = state_stream[t - 1] if t > 0 else None
        sv = state_stream[t]
        d = dominant_history[t]
        med_state = classify_state_v4(
            sv, d, attractor_positions, prev_state_vec=prev_sv
        )
        state_sequence.append(med_state)
else:
    STATE_MAP = {
        "Breath Focus": "breath_focus",
        "Pain Discomfort": "mind_wandering",
        "Pending Tasks": "mind_wandering",
        "Self Reflection": "meta_awareness",
        "Equanimity": "meta_awareness",
    }
    for d in dominant_history:
        state_sequence.append(STATE_MAP.get(d, "mind_wandering"))

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
st.markdown(
    "**v0.4 使用指南**：\n"
    "- **OU 噪声**：状态遵循 Ornstein-Uhlenbeck 过程，具有向原点回归的内置倾向\n"
    "- **θ（回归速度）**：越高 → 回神越快 → 专家模式；越低 → 容易走神 → 新手模式\n"
    "- **σ（波动幅度）**：越高 → 走神越剧烈 → 新手模式；越低 → 状态越稳定\n"
    "- **2D 散点图**：按冥想状态着色（绿=专注, 橙=走神, 紫=元觉察, 蓝=回神）\n"
    "- **原点 μ**：OU 均值回归目标，标记为黑色十字 ✚\n\n"
    "**理论对应**：\n"
    "- 公理 I（存在）：每个种子 = 一个泛函 F[ψ]，定义在 2D 状态空间上\n"
    "- 公理 II（演化）：dx = θ(μ − x)dt + σ · dW — 均值回归 + 扩散\n"
    "- 公理 III（精度）：γ 作为曲率参数，控制激活函数的陡峭度\n"
    "- 公理 IV（决策）：G = γ·‖Δ‖² + ln(γ)，在精度与复杂度之间权衡\n\n"
    "**v0.4 新增**：OU 噪声驱动 → 状态自带"弹性绳" → mind_wandering 比例"
    "逼近 thoughtseeds_model 基准值（新手 40-55%，专家 20-30%），"
    "redirect_attention 从状态回归中自然涌现。"
)