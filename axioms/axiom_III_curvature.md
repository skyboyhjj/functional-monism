# 公理 III：精度公理 (Axiom of Curvature / Precision)

## 形式化陈述

$$
\boxed{\;\gamma = \left\| \frac{\delta^2 F}{\delta \psi^2} \right\|\;}
$$

**认知置信度 $\gamma$ 等于泛函 $F$ 对场构型 $\psi$ 的二阶泛函导数的范数。**

## 严格定义

设 $F[\psi]$ 为存在公理中的泛函表示，$\frac{\delta^2 F}{\delta \psi^2}$ 为泛函的二阶泛函导数（泛函 Hessian 算子）。定义认知置信度 $\gamma$：

$$
\gamma \equiv \left\| \frac{\delta^2 F}{\delta \psi^2} \right\|_{\mathcal{H}}
$$

其中 $\|\cdot\|_{\mathcal{H}}$ 为泛函 Hilbert 空间 $\mathcal{H}$ 上的算子范数：

$$
\|A\|_{\mathcal{H}} \equiv \sup_{\|\eta\|=1} \|A\eta\|_{\mathcal{H}}
$$

## 二阶泛函导数的坐标表示

在离散化表象下，将 $\psi$ 展开为基函数 $\{\phi_i\}$ 的线性组合 $\psi = \sum_i c_i \phi_i$，则：

$$
\left(\frac{\delta^2 F}{\delta \psi^2}\right)_{ij} = \frac{\partial^2 F}{\partial c_i \partial c_j}
$$

即泛函 Hessian 矩阵，其正定性度量了 $F$ 在 $\psi$ 处的局部曲率。

## 精度公理的几何意义

$F[\psi]$ 在泛函空间中构成一个"泛函曲面"。$\frac{\delta^2 F}{\delta \psi^2}$ 是该曲面在 $\psi$ 处的**曲率张量**：

- **高曲率** ($\gamma \gg 1$)：泛函曲面尖锐，$F$ 对 $\psi$ 的变化敏感 → 高置信度
- **低曲率** ($\gamma \ll 1$)：泛函曲面平坦，$F$ 对 $\psi$ 的变化不敏感 → 低置信度
- **零曲率** ($\gamma = 0$)：泛函曲面退化，$F$ 无法区分不同的 $\psi$ → 零置信度（无知状态）

## 认知置信度的统计解释

若将 $F[\psi]$ 解释为负对数似然 (Negative Log-Likelihood)，即 $F[\psi] = -\log p(\psi)$，则：

$$
\frac{\delta^2 F}{\delta \psi^2} = -\frac{\delta^2}{\delta \psi^2} \log p(\psi) = \mathcal{I}(\psi)
$$

其中 $\mathcal{I}(\psi)$ 为 **Fisher 信息矩阵**。因此：

$$
\gamma = \|\mathcal{I}(\psi)\|
$$

即认知置信度等价于 Fisher 信息的范数——信息量越大，认知越精确。

## 与 Cramér-Rao 界的关系

由精度公理可导出泛函版本的 Cramér-Rao 不等式：

$$
\text{Cov}(\hat{\psi}) \succeq \left(\frac{\delta^2 F}{\delta \psi^2}\right)^{-1}
$$

即：对 $\psi$ 的任何无偏估计 $\hat{\psi}$，其协方差矩阵的下界由泛函 Hessian 的逆给出。曲率越大，估计越精确。

## 直观解释

精度公理将**认知的确定性**与**泛函的几何曲率**联系起来。一个泛函表示的"尖锐程度"直接决定了我们对它所描述实体的认知置信度。这为认识论提供了一个几何化的、可计算的数学基础。

## 直接推论

| 序号 | 推论 | 数学表达 |
|------|------|----------|
| 1 | 曲率-不确定性关系 | $\Delta \psi \cdot \gamma \geq \frac{1}{2}$（泛函版本的 Heisenberg 不确定性） |
| 2 | 信息单调性 | 在泛函变换 $\mathcal{T}$ 下，$\gamma(\mathcal{T}[F]) \leq \gamma(F)$（数据处理不等式） |
| 3 | 收敛判据 | 演化过程中 $\frac{d\gamma}{dt} \geq 0$：认知置信度单调不减（学习不可逆） |
| 4 | 精度谱分解 | $\gamma = \sum_i \lambda_i$，其中 $\lambda_i$ 为 Hessian 的特征值，对应不同认知维度 |

## 数值计算

在实际计算中，泛函 Hessian 的迹给出精度：

$$
\gamma \approx \text{Tr}\left(\frac{\delta^2 F}{\delta \psi^2}\right) = \sum_i \frac{\partial^2 F}{\partial c_i^2}
$$

可使用 JAX 的 `jax.hessian` 自动计算，详见 [src/core/precision.py](../src/core/precision.py)。