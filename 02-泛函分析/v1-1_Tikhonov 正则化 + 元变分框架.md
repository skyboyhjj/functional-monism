好的！让我们将 **Tikhonov 正则化 + 元变分框架** 的理论，正式落地到 `functional-monism` 项目中。

这将是 **v1.1 的核心功能**：**让优化器自动寻找最优的 \( \theta \) 和 \( \sigma \)，取代手工调参。**

---

## 🧘 任务目标：实现“参数自动校准”模块

### 一、核心思路

将你 v0.9 手工找到的 \((θ=0.05, σ=0.28)\) 作为**起点**，而不是终点。我们构建一个**元优化器**：

\[
\min_{\theta, \sigma} \Big[ \underbrace{\mathcal{E}(\theta, \sigma)}_{\text{模拟与 thoughtseeds 基准的误差}} + \underbrace{\alpha \|\theta\|^2 + \beta \|\sigma\|^2}_{\text{参数复杂度惩罚}} \Big]
\]

然后让 JAX 的自动微分 + 梯度下降自动找到最优的 \((\theta, \sigma)\)。

### 二、技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                  元优化器 (Meta-Optimizer)                   │
│  目标：最小化 拟合误差 + 正则项                              │
│  变量：θ (回归速度), σ (波动幅度)                           │
│  优化器：JAX + Adam                                        │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               模拟引擎 (Simulation Engine)                   │
│  输入：θ, σ, γ, anchor, steps, n_runs                      │
│  输出：mind_wandering 占比、驻留时间等指标                   │
│  复用：OUNoise + GlobalWorkspace + 状态分类                 │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│             误差计算器 (Error Calculator)                    │
│  将模拟输出与 thoughtseeds_model 基准对比                    │
│  基准：MW 占比 53.8%, MW 驻留 89.6 步                      │
└─────────────────────────────────────────────────────────────┘
```


## 📋 三、具体任务清单（供 Trae 执行）

### 任务 1：创建 `src/optimization/meta_optimizer.py`

```python
"""元优化器：自动校准认知动力学参数 θ 和 σ。"""

import jax
import jax.numpy as jnp
from src.models.ou_noise import OUNoise
from src.models.workspace import GlobalWorkspace, create_default_seeds
from src.validation.metrics import classify_state_with_buffer, compute_buffer_size
from src.validation.comparator import run_single_simulation

# thoughtseeds_model 基准值（新手模式）
BENCHMARK = {
    'mind_wandering_ratio': 0.538,   # 53.8%
    'mind_wandering_dwell': 89.6,    # 89.6 步
}


def simulate_with_params(theta, sigma, gamma=0.3, anchor=1.0, steps=2000, n_runs=20, seed=42):
    """用给定的 θ 和 σ 运行模拟，返回关键指标。"""
    # 运行 n_runs 次模拟，取平均
    all_ratios = []
    all_dwells = []
    for i in range(n_runs):
        # 调用现有的模拟函数
        result = run_single_simulation(
            gamma=gamma,
            anchor=anchor,
            theta=theta,
            sigma=sigma,
            steps=steps,
            seed=seed + i,
            use_efe=True,
        )
        all_ratios.append(result['mind_wandering_ratio'])
        all_dwells.append(result['mind_wandering_dwell'])
    
    return {
        'mw_ratio': jnp.mean(jnp.array(all_ratios)),
        'mw_dwell': jnp.mean(jnp.array(all_dwells)),
    }


def meta_loss(theta, sigma, alpha=1.0, beta=0.5):
    """元优化损失函数 = 拟合误差 + 正则项。"""
    # 1. 运行模拟
    metrics = simulate_with_params(theta, sigma)
    
    # 2. 拟合误差（与 thoughtseeds_model 基准对比）
    error_ratio = (metrics['mw_ratio'] - BENCHMARK['mind_wandering_ratio']) ** 2
    error_dwell = (metrics['mw_dwell'] - BENCHMARK['mind_wandering_dwell']) ** 2
    
    # 归一化：让两项量级相当
    fit_error = error_ratio * 100 + error_dwell / 100
    
    # 3. 正则项
    reg_term = alpha * theta ** 2 + beta * sigma ** 2
    
    return fit_error + reg_term


def optimize_parameters(
    theta_init=0.06,
    sigma_init=0.35,
    alpha=1.0,
    beta=0.5,
    lr=0.01,
    n_iterations=100,
):
    """使用梯度下降优化 θ 和 σ。"""
    # 用 JAX 自动微分
    grad_loss = jax.grad(meta_loss, argnums=(0, 1))
    
    theta = theta_init
    sigma = sigma_init
    history = []
    
    for i in range(n_iterations):
        g_theta, g_sigma = grad_loss(theta, sigma, alpha, beta)
        theta = theta - lr * g_theta
        sigma = sigma - lr * g_sigma
        # 边界约束：保持正数
        theta = jnp.maximum(theta, 0.01)
        sigma = jnp.maximum(sigma, 0.05)
        
        if i % 10 == 0:
            loss = meta_loss(theta, sigma, alpha, beta)
            history.append({
                'iter': i,
                'theta': float(theta),
                'sigma': float(sigma),
                'loss': float(loss),
            })
            print(f"Iter {i}: θ={theta:.4f}, σ={sigma:.4f}, loss={loss:.4f}")
    
    return float(theta), float(sigma), history
```

### 任务 2：创建 `examples/run_meta_optimization.py`

```python
"""运行元优化，寻找最优的 θ 和 σ。"""

from src.optimization.meta_optimizer import optimize_parameters

if __name__ == "__main__":
    print("🔬 启动元优化：自动校准 θ 和 σ")
    print("目标：匹配 thoughtseeds_model 新手模式基准")
    print("基准：MW 占比 53.8%, MW 驻留 89.6 步")
    print("-" * 50)
    
    theta_opt, sigma_opt, history = optimize_parameters(
        theta_init=0.06,
        sigma_init=0.35,
        alpha=0.5,      # 正则强度（可调）
        beta=0.3,
        lr=0.005,
        n_iterations=200,
    )
    
    print("-" * 50)
    print(f"✅ 优化完成！")
    print(f"最优 θ: {theta_opt:.4f}")
    print(f"最优 σ: {sigma_opt:.4f}")
    print(f"v0.9 手工调参: θ=0.05, σ=0.28")
```

### 任务 3：Dashboard 集成（可选）

在 `meditation_dashboard.py` 侧边栏增加一个按钮：
> **“🔬 自动校准参数”**
> 点击后，运行元优化，自动搜索最优的 θ 和 σ，并将结果填入滑块。

### 任务 4：更新 `PROJECT_CONTEXT.md`

在“待办事项”中标记：
```markdown
- [x] v1.0 发布
- [ ] v1.1 元优化器（Tikhonov 正则化自动校准 θ 和 σ）
```

---

## 🔬 四、预期结果

| 指标 | v0.9 手工调参 | v1.1 自动优化（预期） |
| :--- | :---: | :---: |
| θ | 0.05 | ≈ 0.04–0.06 |
| σ | 0.28 | ≈ 0.25–0.32 |
| MW 占比误差 | 16.0% | **< 10%** |
| MW 驻留误差 | 31.6% | **< 20%** |
| 调参时间 | 数小时 | **几分钟** |

---

## 🧘 五、底层逻辑回顾

你之前手工调参时，是在 **“经验空间”** 里搜索——凭感觉判断“走神占比高了还是低了”。

元优化器将这个搜索过程**数学化**：
- **拟合误差** 告诉你“离目标多远”
- **正则项** 告诉你“参数多复杂”
- **梯度下降** 告诉你“往哪个方向走能同时降低两者”

这正是泛函分析中 **“变分正则化”** 的工程化实现——将调参问题本身，转化为一个严格的优化问题。

---

## 📥 执行指令（供 Trae）

```
参考 PROJECT_CONTEXT.md，启动 v1.1 元优化器开发。

核心任务：实现基于 Tikhonov 正则化的自动参数校准模块。

请依次完成：

1. 创建 src/optimization/meta_optimizer.py：
   - 定义 BENCHMARK 常量（MW 占比 53.8%，驻留 89.6 步）
   - 实现 simulate_with_params(theta, sigma) 函数
   - 实现 meta_loss(theta, sigma, alpha, beta) 函数
   - 实现 optimize_parameters() 函数，使用 JAX 自动微分

2. 创建 examples/run_meta_optimization.py：
   - 运行优化，打印结果

3. 验证：
   - 运行后，θ 应收敛到 0.04–0.06，σ 到 0.25–0.32
   - 误差应低于 v0.9 手工调参结果

完成后，生成 v1.1 更新摘要。
```

---

当你准备好时，直接将这些指令发送给 Trae，它会把 Tikhonov 正则化理论编译成可运行的代码。🧘