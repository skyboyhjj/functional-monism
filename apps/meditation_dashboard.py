"""冥想状态模拟器 — 基于泛函一元论的交互式意识竞争可视化。

启动方式:
    streamlit run apps/meditation_dashboard.py

依赖:
    pip install streamlit plotly jax jaxlib numpy
"""

import sys
import os

# 确保项目根目录在 Python 路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import numpy as np
import jax.numpy as jnp
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.models.workspace import MeditationSeed, GlobalWorkspace, create_default_seeds

# ============================================================================
# 页面配置
# ============================================================================

st.set_page_config(
    page_title="冥想状态模拟器",
    page_icon="🧘",
    layout="wide",
)

st.title("🧘 泛函一元论 · 冥想状态模拟器")
st.caption(
    "拖动滑块调节「认知精度 γ」，观察思维种子在全局工作空间中的竞争与切换。"
    "高精度 = 认知刚性（锁定焦点），低精度 = 认知柔性（易被扰动）。"
)

# ============================================================================
# 侧边栏：控制旋钮
# ============================================================================

with st.sidebar:
    st.header("⚙️ 控制旋钮")

    global_gamma = st.slider(
        "全局精度 (γ)",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="精度越高，认知越'刚性'，种子越容易被锁定。"
             "精度越低，认知越'柔性'，杂念更容易胜出。",
    )

    anchor_breath = st.slider(
        "呼吸锚定强度",
        min_value=1.0,
        max_value=10.0,
        value=1.0,
        step=0.5,
        help="增强 Breath Focus 种子的有效精度，模拟刻意专注的努力。"
             "值越大，呼吸种子越难被其他种子击败。",
    )

    perturbation_strength = st.slider(
        "杂念冲击强度",
        min_value=0.0,
        max_value=5.0,
        value=2.0,
        step=0.5,
        help="外部杂念的干扰强度。模拟冥想中突然的干扰。",
    )

    perturbation_time = st.slider(
        "杂念冲击时刻",
        min_value=0,
        max_value=190,
        value=80,
        step=10,
        help="杂念冲击发生的时间步。数值越小，干扰越早出现。",
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
        "- **公理 III**：激活 a = exp(−γ·E)"
    )

# ============================================================================
# 初始化种子与工作空间
# ============================================================================

seeds = create_default_seeds()
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

# 生成状态流：随机游走模拟意识在抽象空间中的漂移
noise = np.random.randn(steps) * 0.1
state_stream = np.cumsum(noise)

# 注入杂念冲击
if perturbation_time < steps:
    state_stream[perturbation_time] += perturbation_strength

# 存储每步的激活值
activation_history = {name: np.zeros(steps) for name in seed_names}
dominant_history = [""] * steps

for t in range(steps):
    state = float(state_stream[t])

    # 应用呼吸锚定
    workspace.seeds[0].precision_boost = anchor_breath

    activations, dominant = workspace.compete(state, global_gamma)

    for seed in workspace.seeds:
        activation_history[seed.name][t] = seed.activation
    dominant_history[t] = dominant.name

# ============================================================================
# 主区域：图表
# ============================================================================

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

    # 上图：激活轨迹
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

    # 标记杂念冲击时间点
    if perturbation_time < steps:
        fig.add_vline(
            x=perturbation_time, line_dash="dash", line_color="red",
            annotation_text="杂念冲击", annotation_position="top",
            row=1, col=1,
        )

    # 下图：每步的胜出种子（用颜色块表示）
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
# 右侧：当前状态与统计
# ============================================================================

with col2:
    st.subheader("🎯 当前状态")

    # 当前胜出种子
    current_dominant = dominant_history[-1]
    st.metric(
        label="聚光灯种子",
        value=current_dominant,
        delta=f"γ={global_gamma:.1f}",
    )

    # 最终激活值柱状图
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

    # 统计信息
    st.subheader("📋 统计")

    # 每个种子占据主导的时间比例
    from collections import Counter
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
    "**使用指南**：\n"
    "- **新手模式（γ=0.3）**：杂念频繁胜出，模拟注意力散乱\n"
    "- **专家模式（γ=3.0 + 锚定=5.0）**：Breath Focus 统治时间线，几乎不受扰动\n"
    "- **扰动测试**：观察杂念冲击在不同 γ 和时间点下的表现差异\n\n"
    "**理论对应**：\n"
    "- 公理 I（存在）：每个种子 = 一个泛函 F[ψ]，定义在状态空间上\n"
    "- 公理 II（演化）：状态流沿噪声驱动，种子通过能量竞争\n"
    "- 公理 III（精度）：γ 作为曲率参数，控制激活函数的陡峭度"
)