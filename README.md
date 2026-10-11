# functional-monism

> 基于泛函一元论 (Functional Monism) 公理的计算框架

## 🧘 v1.0 已发布

功能性认知模拟框架 functional-monism 已完成与 [thoughtseeds_model](https://github.com/prakash-kavi/thoughtseeds_model) 的定量验证。

| 指标 | 结果 |
|:---|:---|
| 定性复现 | **7/7** ✅ |
| 核心定量误差 | **< 30%** ✅ |
| 专家模式 breath_focus 驻留 | **106.7 步**（基准 93.7） |
| 新手模式 mind_wandering 占比 | **47.5%**（基准 53.8%） |
| 新手模式 mind_wandering 驻留 | **69.5 步**（基准 89.6） |

> 口径：20 次 × 2000 步、可复现随机种子；以「核心误差 < 30%」为发布区间。
> 📊 [查看完整验证报告](results/v1.0_release_summary.md)

## 概述

泛函一元论提出：一切存在态均可表示为统一泛函场上的变换，且场的演化遵循最小作用量原理。本项目将这一哲学公理体系转化为可计算、可验证的数值框架。

## 一元 · 两本账

泛函一元论把一切存在收拢为**一个母泛函** $`F[\psi]`$，它记着**两本账**：

- **显账**——**母泛函 $F$ 能生成的那一层**：可形式化、可计算、可验证（公理 I 存在、公理 II 演化、公理 III 精度）。
- **暗账**——**母泛函生成不了的那一层**：意义与理解——"它究竟关于什么、为何如此"。

> **显账可以外包给机器，暗账不能**。
> 从"算得出"到"真懂了"，中间那座桥，只能自己走。

## 核心公理

| 公理 | 名称 | 内容 |
|------|------|------|
| 公理 I | 存在公理 | 实体 $`\mathcal{E}`$ 等价于泛函 $`F[\psi]`$ |
| 公理 II | 演化公理 | 路径积分满足 $`\delta\int F[\psi]\,dt = 0`$ |
| 公理 III | 精度公理 | 认知置信度 $`\gamma = \left\lVert \dfrac{\delta^2 F}{\delta\psi^2} \right\rVert_{\mathcal{S}_1}`$（Schatten-1 / 迹范数） |

> 另有<strong>公理 IV（泛函对应原理）</strong>处理连续极限与重整化。全部公理详见 [axioms/](axioms/) 目录。

## 项目结构

```
functional-monism/
├── axioms/          # 核心公理与定理（形式化证明）
├── src/             # 源代码
│   ├── core/        # 核心引擎（泛函求极值、精度计算）
│   ├── models/      # 预置模型（全局工作空间、OU 噪声、马尔可夫毯）
│   ├── validation/  # 验证模块（指标、对比器、报告生成）
│   ├── optimization/ # 元优化器（θ/σ 自动校准）
│   └── examples/    # 示例与教程
├── apps/            # 交互式应用（冥想状态模拟仪表盘）
├── examples/        # 验证与实验入口脚本
├── results/         # 验证报告与优化结果
├── community/       # 社区贡献指南
├── LICENSE          # MIT 开源协议
└── README.md
```

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 公理可编程性验证
python src/examples/demo_basic.py

# 精度对偶性演示（固定 vs 自适应）
python src/examples/duality_demo.py

# 冥想状态模拟仪表盘
streamlit run apps/meditation_dashboard.py

# 运行验证（与 thoughtseeds_model 对比）
python examples/run_validation.py

# 决策模型示例
python src/examples/decision_model.py
```

## 核心依赖

- numpy — 数值计算基础
- jax / jaxlib — 自动微分与泛函求导
- matplotlib — 可视化
- streamlit / plotly — 交互式仪表盘与绘图

完整依赖见 [requirements.txt](requirements.txt)。

## 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](community/CONTRIBUTING.md)。

## 许可证

本项目采用 [MIT License](LICENSE)。