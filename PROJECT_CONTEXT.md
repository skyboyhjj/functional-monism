# PROJECT\_CONTEXT.md — 泛函一元论 (Functional Monism)

> 本文件是 AI 辅助开发的项目上下文共享模板。放置于项目根目录，在新对话中引用即可让 AI（如 Trae/Claude）快速理解项目全貌并遵循公理约束。

***

## 项目概述

**Functional Monism (泛函一元论)** — 基于"存在即泛函极值"公理，构建统一物理与认知的可计算、可推演、可编程的数学框架。

核心模块/产品：

| 模块                                      |   状态  | 说明                                          |
| --------------------------------------- | :---: | ------------------------------------------- |
| 核心引擎 (`src/core/`)                      | ✅ 已上线 | 实现泛函求梯度、曲率（精度）计算，以及梯度流演化。                   |
| 对偶演示 (`src/examples/duality_demo.py`)   | ✅ 已上线 | 生成"固定精度(物理态) vs 自适应精度(认知态)"对比图，验证公理 I & II。 |
| 思维种子建模 (`src/models/thoughtseed.py`)    | ✅ 已上线 | 预期自由能（EFE）赢家通吃竞争机制。                         |
| 冥想模拟 (`src/examples/meditation_sim.py`) | ✅ 已上线 | 基于精度动态，模拟泛函场向稳态收敛。                          |
| 决策模型 (`src/examples/decision_model.py`) | ✅ 已上线 | 效用泛函极值优化的决策框架。                              |
| 公理验证 (`src/examples/demo_basic.py`)     | ✅ 已上线 | 三大公理可编程性验证（JAX 自动微分）。                       |

<!-- 状态可选: ✅ 已上线 / 🔜 开发中 / 🟡 预览版 / 🟢 稳定版 -->

## 🧬 项目哲学（元指令 / 第一性原理）

**AI 编码时必须遵循的三大公理约束：**

1. **公理 I（存在公理）**：所有实体 ( \mathcal{S} ) 必须定义为状态空间 ( \Omega ) 上的实值泛函 ( \mathcal{F}\[\psi] )。
2. **公理 II（演化公理）**：状态 ( \psi(t) ) 的动力学必须源于对总作用量 ( \mathcal{A} = \int \mathcal{F} dt ) 的变分（( \delta \mathcal{A} = 0 )）。
3. **公理 III（观测公理）**：认知置信度（精度 ( \gamma )）必须定义为泛函 ( \mathcal{F} ) 对状态 ( \psi ) 的二阶变分（曲率）。

> **编程铁律（硬约束）**：
>
> - 不允许硬编码"物理规律"或"认知规则"，只能编码"代价函数"和"变分更新规则"。
>
> - 不允许将"物理"和"认知"视为两个独立的模块，必须共享同一个底层 `FunctionalEngine`（见下方架构）。
>
> - 精度（( \gamma )）不是静态超参数，必须有随误差动态演化的机制。

***

## 🤖 AI 辅助开发约定（Trae 专属工作流）

为了最高效地推进开发，AI 助手需遵循以下命令与上下文操作：

| 指令/概念                               | 用途说明                                                                         |
| :---------------------------------- | :--------------------------------------------------------------------------- |
| **`/tests`** **\[文件名]**             | 生成对应的单元测试代码（基于 JAX 自动微分测试梯度与 Hessian 的数值稳定性）。                                |
| **`@workspace`** **+ 描述**           | 用于跨文件全局重构（例如："`@workspace` 将 `precision` 变量从静态配置改为由 `MetaCognition` 类动态生成"）。 |
| **"基于 Functional Monism 的公理系统..."** | 复杂任务启动前缀，用于锚定 AI 思维（例如："基于公理系统，实现一个基于泛函极值的 HJB 方程求解器"）。                      |

**提交前强制检查**：

- [ ] 新代码是否违反"三大公理"？（是否引入了非变分的经验规则？）

- [ ] 核心参数（如学习率、精度）是否以显式公式定义，而非魔数？

***

## 关键文件与代码坐标

| 文件                              | 用途                                                                                      |
| :------------------------------ | :-------------------------------------------------------------------------------------- |
| `src/core/functional.py`        | **核心引擎**：`FunctionalEngine` 类，含 `compute_gradient`、`compute_precision`、`gradient_flow`。 |
| `src/core/precision.py`         | 精度计算：相对误差估计与收敛阶分析。                                                                      |
| `src/examples/demo_basic.py`    | **公理可编程性验证**：JAX 自动微分验证三大公理。                                                            |
| `src/examples/duality_demo.py`  | **第一性原理可视化**：固定 vs 自适应精度对比图。                                                            |
| `src/models/thoughtseed.py`     | 思维种子竞争逻辑（EFE 赢家通吃）。                                                                     |
| `src/models/pde_solver.py`      | 泛函变分 PDE 求解器。                                                                           |
| `src/models/bayesian_filter.py` | 泛函贝叶斯滤波器。                                                                               |
| `src/models/workspace.py`       | 冥想种子引擎：`MeditationSeed` + `GlobalWorkspace` 赢家通吃竞争。                                     |
| `apps/meditation_dashboard.py`  | **交互式仪表盘**：Streamlit + Plotly 可视化，γ 滑块、呼吸锚定、杂念冲击时间点可调。                                  |
| `axioms/` 目录                    | 三大公理与定理的 LaTeX 数学形式化。                                                                   |

***

## 架构

```
┌─────────────────────────────────────────────┐
│           公理层 (Axioms Layer)              │ ← 定义 F[ψ] 与变分规则
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│        核心计算引擎 (FunctionalEngine)       │ ← 自动微分 + 梯度流 (JAX)
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│     模型层 (Models: Thoughtseed/PDE Solver)  │ ← 具体应用（物理场 / 思维种子）
└──────────────────┬──────────────────────────┘
                   ▼
┌─────────────────────────────────────────────┐
│         示例层 (Examples / Demos)            │ ← 数值实验与可视化
└─────────────────────────────────────────────┘
```

***

## 部署与运行命令

```bash
# 安装依赖（需 Python 3.9+）
pip install -r requirements.txt

# 公理可编程性验证
python src/examples/demo_basic.py

# 运行物理-认知对偶演示
python src/examples/duality_demo.py

# 运行单元测试（如已生成）
pytest tests/
```

***

## 待办事项（Next Steps）

- [x] **已完成**：生成"固定精度 vs 自适应精度"对比图（`duality_demo.py`）。

- [x] **已完成**：实现 Thoughtseed 的 EFE 赢家通吃竞争（`thoughtseed.py`）。

- [x] **已完成**：公理可编程性验证（`demo_basic.py`）。

- [ ] **优化方向 1（动态精度更新）**：将自适应精度从线性增长（`gamma_0 + eta * t`）改为由\*\*当前预测误差（梯度大小）\*\*驱动的闭环更新。探索动量式或贝叶斯式的更新规则。

- [ ] **优化方向 2（探索-利用权衡）**：在 `thoughtseed.py` 中引入更复杂的**预期自由能 (EFE)** 计算，让思维种子在"高精度利用（锁定目标）"和"低精度探索（收集信息）"之间做出权衡。

- [ ] **优化方向 4（状态空间升维）**：将 `meditation_dashboard.py` 的状态流从 1D 标量扩展为 R² 或 R³ 多维空间。需配套设计多维可视化方案（2D 热力图/相图，3D 轨迹图），`workspace.py` 模型层已支持多维 `core_attractor`，主要改动在仪表盘前端。可结合"情绪-注意力"双轴或"效价-唤醒度"平面进行概念建模。

- [ ] **文档**：撰写 `papers/duality_experiment_report.md`，记录 `duality_demo.py` 的实验结论。

***

## 分支管理 SOP

本项目采用双分支模型，区分"稳定发布"与"活跃开发"两条线。

| 分支       | 定位               | 受众                 | 同步方向                 |
| -------- | ---------------- | ------------------ | -------------------- |
| `main`   | **稳定发布分支**（默认分支） | 一般用户下载、pip 安装、论文复现 | 仅从 `master` 合并，不直接推送 |
| `master` | **活跃开发分支**       | 开发者日常提交、功能集成       | 所有开发直接推送（或通过 PR 合并）  |

**分支策略**：

- **当前阶段**（v0.1.x，单开发者）：

  - 日常开发在 `master` 上直接提交，保持原子性（一个提交 = 一个完整功能点）。

  - 当 `master` 达到一个稳定里程碑（如公理体系定型、首个可运行 demo 通过），将 `master` 合并到 `main` 并打 tag：

    ```
    git checkout main
    git merge master
    git tag v0.1.0
    git push origin main --tags
    ```

- **协作阶段**（v0.2+，引入贡献者）：

  ```
  main            ← 稳定发布（默认分支），仅通过 master 合并，打 tag 后对外发布
  master          ← 集成分支，仅通过 PR 合并
  feature/xxx     ← 功能分支，从 master 分出，完成后 PR 合并回 master
  fix/xxx         ← 紧急修复分支
  hotfix/xxx      ← 线上紧急修复，从 main 分出，修复后同时合并回 main 和 master
  ```

**设定** **`main`** **为 GitHub 默认分支**：

在 GitHub 仓库 Settings → Branches → Default branch 中，将默认分支从 `master` 切换为 `main`。这样：

- 访问仓库首页展示的是 `main` 分支的稳定代码

- `git clone` 默认检出 `main`，用户直接获得可运行版本

- README 中的徽章、链接均指向 `main` 的稳定状态

**Tag 规范**：

- 版本号格式：`v<MAJOR>.<MINOR>.<PATCH>`（语义化版本）

- 仅在 `main` 分支上打 tag，确保每个 tag 对应一个经过验证的稳定版本

- 里程碑节点（如公理体系定型、首个论文发布）必须打 tag

- 示例：`v0.1.0`（初始框架）、`v0.2.0`（首个模型验证）、`v1.0.0`（论文发表）

## 同步方式

**多会话同步**（同一开发者跨 Trae 会话）：

1. 每次新会话启动时，引用 `PROJECT_CONTEXT.md` 作为上下文锚点：

   > "参考 PROJECT\_CONTEXT.md，继续开发 functional-monism 项目"

2. 会话结束后，将本次会话的进展更新到 `PROJECT_CONTEXT.md` 的 **已完成** / **待办** 列表。

**多开发者同步**：

1. 所有开发者以 `master` 分支为唯一上游。
2. 提交前执行 `git pull --rebase origin master` 确保线性历史。
3. 修改 `PROJECT_CONTEXT.md` 时，优先更新自己负责的模块状态，避免冲突。
4. 重大架构变更（如新增公理、修改 FunctionalEngine 接口）需在 PR 描述中引用 `PROJECT_CONTEXT.md` 的相关章节。

## 版本控制约定

每次提交代码前：

1. 读取 `PROJECT_CONTEXT.md`，与本地实际状态比较
2. 如有冲突（文件不存在、接口变更、架构调整等），先更新 `PROJECT_CONTEXT.md` 再提交
3. 提交信息格式：`<type>: <简短描述>`

   - 类型：`feat`（新功能）、`fix`（修复）、`refactor`（重构）、`docs`（文档）、`axiom`（公理更新）

   - 示例：`feat: add Thoughtseed EFE competition`、`axiom: formalize Axiom III curvature`
4. **数据隐私检查（强制）**：提交前扫描确保未泄露：

   - API 密钥、Token、密码

   - 个人邮箱、手机号

   - 数据库连接字符串

   - 第三方服务 Access Key / Secret Key

***

## 新对话快速启动

在新对话（如新的 Trae 会话）中引用此文件即可无缝继续：

> *"参考 PROJECT\_CONTEXT.md，继续开发 functional-monism 项目。当前待办中最优先的是【优化方向 1】动态精度更新，或【优化方向 3】多维非凸泛函扩展。"*

