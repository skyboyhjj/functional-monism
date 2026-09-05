# 公理 II：演化公理 (Axiom of Evolution)

## 形式化陈述

$$
\boxed{\;\delta \int F[\psi]\,dt = 0\;}
$$

**泛函 $F[\psi]$ 的演化路径积分满足变分原理（最小作用量原理）。**

## 严格定义

设泛函 $F[\psi(t)]$ 为时间 $t \in [t_0, t_1] \subset \mathbb{R}$ 的参数化泛函族。定义作用量泛函 (Action Functional)：

$$
S[F] \equiv \int_{t_0}^{t_1} F[\psi(t)]\,dt
$$

演化公理要求：

$$
\delta S[F] = \delta \int_{t_0}^{t_1} F[\psi(t)]\,dt = 0
$$

其中 $\delta$ 为泛函变分算子 (Functional Variation Operator)，定义为：

$$
\delta S[F] \equiv \lim_{\varepsilon \to 0} \frac{S[F + \varepsilon\eta] - S[F]}{\varepsilon} = \int_{t_0}^{t_1} \frac{\delta F}{\delta \psi} \cdot \eta(t)\,dt
$$

其中 $\eta(t)$ 为任意变分函数，满足 $\eta(t_0) = \eta(t_1) = 0$，$\frac{\delta F}{\delta \psi}$ 为泛函导数。

## 泛函 Euler-Lagrange 方程

由 $\delta S = 0$ 对任意 $\eta$ 成立，可得：

$$
\frac{\delta F}{\delta \psi(t)} = 0,\quad \forall t \in [t_0, t_1]
$$

即：泛函场在演化路径上的每一点处，其泛函导数为零——这是泛函版本的"稳态条件"。

## 演化方程的一般形式

引入泛函 Lagrangian 密度 $\mathcal{L}[\psi, \partial_t\psi, \partial_x\psi]$：

$$
F[\psi] = \int \mathcal{L}[\psi, \partial_t\psi, \partial_x\psi]\,dx
$$

则泛函 Euler-Lagrange 方程展开为：

$$
\frac{\partial\mathcal{L}}{\partial\psi} - \partial_t \frac{\partial\mathcal{L}}{\partial(\partial_t\psi)} - \partial_x \frac{\partial\mathcal{L}}{\partial(\partial_x\psi)} = 0
$$

## 直观解释

演化公理断言：泛函场的演化不是任意的，而是遵循**变分原理**——泛函 $F[\psi]$ 在时间演化中总是沿着使作用量积分取极值（通常是极小值）的路径行进。这赋予了泛函一元论以动力学内容。

## 直接推论

| 序号 | 推论 | 数学表达 |
|------|------|----------|
| 1 | 演化确定性 | 给定初始 $F[\psi(t_0)]$，演化路径唯一确定 |
| 2 | Noether 定理推广 | 泛函场的每个连续对称性对应一个守恒量：$\frac{d}{dt}Q = 0$ |
| 3 | Hamilton 形式 | 可定义泛函 Hamilton 量 $H = \int \pi \cdot \partial_t\psi\,dx - F$，满足 $\frac{dH}{dt} = 0$ |
| 4 | 路径积分等价形式 | $\int \mathcal{D}\psi\,e^{iS[\psi]/\hbar}$ 给出量子版本的泛函传播子 |

## 边界条件

变分原理的边界项：

$$
\delta S = \int_{t_0}^{t_1} \frac{\delta F}{\delta \psi} \cdot \eta\,dt + \left[\frac{\partial\mathcal{L}}{\partial(\partial_t\psi)} \cdot \eta\right]_{t_0}^{t_1}
$$

边界项 $\left[\frac{\partial\mathcal{L}}{\partial(\partial_t\psi)} \cdot \eta\right]_{t_0}^{t_1} = 0$ 由 $\eta(t_0) = \eta(t_1) = 0$ 保证，这意味着演化公理在固定端点条件下成立。