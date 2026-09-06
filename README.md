# functional-monism

> 基于泛函一元论 (Functional Monism) 公理的计算框架

## 🧘 v1.0 已发布

功能性认知模拟框架 functional-monism 已完成与 [thoughtseeds_model](https://github.com/prakash-kavi/thoughtseeds_model) 的定量验证。

| 指标 | 结果 |
|:---|:---|
| 定性复现 | **7/7** ✅ |
| 核心定量误差 | **< 35%** |
| 专家模式 breath_focus 驻留 | **97.0 步**（基准 93.7） |
| 新手模式 mind_wandering 占比 | **45.2%**（基准 53.8%） |
| 新手模式 mind_wandering 驻留 | **61.3 步**（基准 89.6） |

📊 [查看完整验证报告](results/v0.8_release_summary.md)

## 概述

泛函一元论提出：一切存在态均可表示为统一泛函场上的变换，且场的演化遵循最小作用量原理。本项目将这一哲学公理体系转化为可计算、可验证的数值框架。

## 核心公理

| 公理 | 名称 | 内容 |
|------|------|------|
| 公理 I | 存在公理 | 实体 $\mathcal{E}$ 等价于泛函 $F[\psi]$ |
| 公理 II | 演化公理 | 路径积分满足 $\delta\int F[\psi]dt = 0$ |
| 公理 III | 精度公理 | 认知置信度 $\gamma = \|\delta^2 F/\delta\psi^2\|$ |

详见 [axioms/](axioms/) 目录。

## 项目结构

```
functional-monism/
├── axioms/          # 核心公理与定理（形式化证明）
├── src/             # 源代码
│   ├── core/        # 核心引擎（泛函求极值、精度计算）
│   ├── models/      # 预置模型（PDE求解器、贝叶斯滤波器）
│   └── examples/    # 示例与教程
├── papers/          # 理论论文与白皮书
├── experiments/     # 实验与仿真脚本
├── docs/            # 完整文档与API参考
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

# 冥想状态模拟仪表盘（v0.9）
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

## 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](community/CONTRIBUTING.md)。

## 许可证

本项目采用 [MIT License](LICENSE)。