# 公理 III：精度公理 (Axiom of Curvature / Precision)

## 形式化陈述

$$\boxed{\gamma = \left\| \frac{\delta^2 F}{\delta \psi^2} \right\|_{\mathcal{S}_1}}$$

**认知置信度 $`\gamma`$ 等于泛函 $`F`$ 对场构型 $`\psi`$ 的二阶泛函导数的 Schatten-1 范数（核范数 / 迹范数）。**

## 严格定义

设 $`F[\psi]`$ 为存在公理中的泛函表示，$`\frac{\delta^2 F}{\delta \psi^2}`$ 为泛函的二阶泛函导数（泛函 Hessian 算子，记为 $`H`$）。定义认知置信度 $`\gamma`$：

$$\gamma \equiv \left\| \frac{\delta^2 F}{\delta \psi^2} \right\|_{\mathcal{S}_1} \equiv \mathrm{Tr}\left(\frac{\delta^2 F}{\delta \psi^2}\right)$$

其中 $`\|\cdot\|_{\mathcal{S}_1}`$ 为 **Schatten-1 范数**（迹范数 / 核范数）。对正定 Hessian 而言，其 Schatten-1 范数等于全部特征值之和：

$$\|H\|_{\mathcal{S}_1} = \sum_i \lambda_i = \mathrm{Tr}(H)$$

语义上，$`\gamma`$ 度量的是"总认知信息量"——所有认知维度曲率的总和，而非单一最敏感方向的曲率。

## 二阶泛函导数的坐标表示

在离散化表象下，将 $`\psi`$ 展开为基函数 $`\{\phi_i\}`$ 的线性组合 $`\psi = \sum_i c_i \phi_i`$，则：

$$\left(\frac{\delta^2 F}{\delta \psi^2}\right)_{ij} = \frac{\partial^2 F}{\partial c_i \partial c_j}$$

即泛函 Hessian 矩阵，其正定性度量了 $`F`$ 在 $`\psi`$ 处的局部曲率。

## 精度公理的几何意义

$`F[\psi]`$ 在泛函空间中构成一个"泛函曲面"。$`\frac{\delta^2 F}{\delta \psi^2}`$ 是该曲面在 $`\psi`$ 处的**曲率张量**：

- **高曲率** ($`\gamma \gg 1`$)：泛函曲面总曲率大，$`F`$ 对 $`\psi`$ 的变化敏感 → 高置信度
- **低曲率** ($`\gamma \ll 1`$)：泛函曲面总曲率小，$`F`$ 对 $`\psi`$ 的变化不敏感 → 低置信度
- **零曲率** ($`\gamma = 0`$)：泛函曲面退化，$`F`$ 无法区分不同的 $`\psi`$ → 零置信度（无知状态）

## 认知置信度的统计解释

若将 $`F[\psi]`$ 解释为负对数似然 (Negative Log-Likelihood)，即 $`F[\psi] = -\log p(\psi)`$，则：

$$\frac{\delta^2 F}{\delta \psi^2} = -\frac{\delta^2}{\delta \psi^2} \log p(\psi) = \mathcal{I}(\psi)$$

其中 $`\mathcal{I}(\psi)`$ 为 **Fisher 信息矩阵**。因此：

$$\gamma = \mathrm{Tr}\left(\mathcal{I}(\psi)\right) = \sum_i \mathcal{I}_{ii}(\psi)$$

即认知置信度等价于 Fisher 信息的迹——总信息量越大，认知越精确。

## 与 Cramér-Rao 界的关系

由精度公理可导出泛函版本的 Cramér-Rao 不等式：

$$\text{Cov}(\hat{\psi}) \succeq \left(\frac{\delta^2 F}{\delta \psi^2}\right)^{-1}$$

即：对 $`\psi`$ 的任何无偏估计 $`\hat{\psi}`$，其协方差矩阵的下界由泛函 Hessian 的逆给出。曲率越大，估计越精确。

## 直观解释

精度公理将**认知的确定性**与**泛函的几何曲率**联系起来。一个泛函表示的"尖锐程度"直接决定了我们对它所描述实体的认知置信度。这为认识论提供了一个几何化的、可计算的数学基础。

## 直接推论

| 序号 | 推论 | 数学表达 |
|------|------|----------|
| 1 | 曲率-不确定性关系 | $`\Delta\psi^2\cdot\gamma \ge n^2`$，即 $`\mathrm{Tr}(H^{-1})\mathrm{Tr}(H)\ge n^2`$（Schatten-1 口径；见注 1） |
| 2 | 信息单调性 | 对确定性马尔可夫核 $`\mathcal{T}`$，$`\gamma(\mathcal{T}[F]) \le \gamma(F)`$（数据处理不等式；见注 2） |
| 3 | 收敛 / 学习不可逆 | 沿梯度流 $`\frac{dF}{dt} = -\|\nabla F\|^2 \le 0`$（自由能单调不增；见注 3） |
| 4 | 精度谱分解 | $`\gamma = \sum_i \lambda_i`$，其中 $`\lambda_i`$ 为 Hessian 的特征值，对应不同认知维度 |

> **注 1（推论 1 的推导，Schatten-1 口径）**
> 记 $`H=\frac{\delta^2 F}{\delta \psi^2}`$，$`\Delta\psi^2:=\mathrm{Tr}(H^{-1})`$ 定义为总方差的**可达下界**（Laplace / Cramér–Rao 给出 $`\mathrm{Cov}\succeq H^{-1}`$，有效估计下取等，即 $`\Delta\psi^2=\mathrm{Tr}(\mathrm{Cov})`$），$`n=\dim\psi`$。由 Cauchy–Schwarz，
> $$\mathrm{Tr}(H^{-1})\mathrm{Tr}(H) = \Big(\sum_i \tfrac{1}{\lambda_i}\Big)\Big(\sum_i \lambda_i\Big) \geq n^2,$$
> 即 $`\Delta\psi^2\cdot\gamma \geq n^2`$。等号成立当且仅当 $`H \propto I`$（各向同性曲率）且估计有效。$`n=1`$ 时退化为 $`\mathrm{Var}\cdot I \geq 1`$（一维 Cramér–Rao）。
>
> **边界说明（无限维退化）**：在无限维情形下，若 $`H`$ 为迹类算子（$`\mathrm{Tr}(H)<\infty`$），则 $`\lambda_i\to0`$，$`\mathrm{Tr}(H^{-1})=\sum_i 1/\lambda_i=\infty`$，不等式退化为平凡。因此推论 1 的非平凡下界**仅在有限维（或有限截断）下有效**。
>
> **边界说明（理论下限）**：$`n^2`$ 是**理论下限**（等号仅在各向同性曲率 $`H\propto I`$ 下成立）。实际认知系统中 Hessian 通常各向异性，$`\Delta\psi^2\cdot\gamma`$ 严格大于 $`n^2`$——这反映曲率谱展宽对"总不确定度 × 总曲率"的贡献。
>
> **注 2（推论 2 的条件）**：数据处理不等式 $`\gamma(\mathcal{T}[F])\le\gamma(F)`$ 仅当 $`\mathcal{T}`$ 为**确定性马尔可夫核**（或等价地，条件期望）时成立；对任意泛函变换不成立。严格地，Fisher 信息满足矩阵偏序 $`\mathcal{I}(\mathcal{T}[\psi])\preceq\mathcal{I}(\psi)`$，取迹得 γ 版本。
>
> **注 3（推论 3 的条件）**：$`d\gamma/dt\ge0`$（曲率单调）**不具一般性**。沿梯度流 $`d\psi/dt=-\nabla F`$，
> $$\frac{d\gamma}{dt}=\mathrm{Tr}\big(\nabla^3 F\cdot(-\nabla F)\big),$$
> 其符号依赖三阶导数，无法保证非负。反例：$`F(\psi)=\psi^4`$，梯度流下 $`F(t)\to0`$（自由能下降）但 $`\gamma=12\psi^2\to0`$（曲率减小）。故"学习不可逆 / 收敛"的正确数学表述是 $`\frac{dF}{dt}=-\|\nabla F\|^2\le0`$，而非 $`d\gamma/dt\ge0`$。

## 数值计算

在实际计算中，泛函 Hessian 的迹给出精度：

$$\gamma = \text{Tr}\left(\frac{\delta^2 F}{\delta \psi^2}\right) = \sum_i \frac{\partial^2 F}{\partial c_i^2}$$

可使用 JAX 的 `jax.hessian` 自动计算 Hessian 后取迹，详见 [src/core/functional.py](../src/core/functional.py) 中的 `compute_precision`。