# 公理 II 的旋量实例：Dirac 场

**——Axiom II · Spinor Instance（实例节，不计入公理编号）**

> **定位**：本文档把 Dirac 旋量场作为公理 II（演化公理）的**显式实例**写清。**不计入公理编号**，作为"实例节"补入。

---

## 一、公理 II 回顾

公理 II（演化公理）：场构型 ψ 的演化满足变分原理

$$\delta\int F[\psi]\,dt=0$$

其相关推论：

- 推论 3（拉氏密度形式）：F[ψ] = ∫L(ψ, ∂ψ) dx；
- 推论 4（路径积分）：$\int\mathcal D\psi\,e^{iS[\psi]/\hbar}$。

---

## 二、场构型：旋量场

取 ψ 为 **Dirac 旋量场**，即取值于自旋群 Spin(1,3) 表示空间的场：

$$\psi:\ M\to\Delta,\qquad \Delta=\mathbb C^4\ (\text{Weyl}_L\oplus\text{Weyl}_R)$$

（自旋群的双覆盖结构，见 [spinor_notes.md](../notes/spinor_notes.md)。）

---

## 三、代入：Dirac 拉氏量

Dirac 拉氏密度、泛函、作用量：

$$\mathcal L_D=\bar\psi\,(i\gamma^\mu\partial_\mu-m)\,\psi,\qquad F[\psi]=\int\mathcal L_D\,dx,\qquad S=\int F\,dt=\int d^4x\,\mathcal L_D$$

其中 γ 矩阵满足 Clifford 代数 $\{\gamma^\mu,\gamma^\nu\}=2\eta^{\mu\nu}I$。

---

## 四、变分 → Dirac 方程

对 ψ̄ 变分，令 δS = 0：

$$\frac{\delta S}{\delta\bar\psi}=(i\gamma^\mu\partial_\mu-m)\,\psi=0$$

即 **Dirac 方程**（对 ψ 变分给出共轭方程）。故：

> **Dirac 旋量场满足公理 II。**（此步**严格**，是标准变分结果。）

---

## 五、路径积分形式（公理 II 推论 4 的旋量版）

$$\int\mathcal D\psi\,\mathcal D\bar\psi\;e^{\,iS[\psi]/\hbar}$$

对旋量而言，ψ、ψ̄ 是 **Grassmann 变量**，$\mathcal D\psi$ 是 **Berezin 积分**——这正是"费米子为何用反对易数"的路径积分解释。

---

## 六、精度 γ（形式化观察）

公理 III：$\gamma=\big\|\delta^2F/\delta\psi^2\big\|_{S1}$。因 Dirac 作用量是 ψ 与 ψ̄ 的**双线性型**（对单一 ψ 线性）：

$$\frac{\delta^2F}{\delta\bar\psi\,\delta\psi}=i\gamma^\mu\partial_\mu-m\quad(\text{Dirac operator})$$

即：**自旋场的精度 γ = Dirac 算子的范数**（形式上）。

> **口径补注。** 公理 III 的 γ 用**纯二阶变分** $\delta^2F/\delta\psi^2$；而 Dirac 作用量对单一 ψ 线性，纯二阶变分为零，非零的只有**混合变分** $\delta^2F/(\delta\bar\psi\,\delta\psi)=D$。严格化需把 $(\psi,\bar\psi)$ 合并为联立场，Hessian 取反对角块，此时 $\gamma\approx 2\|D\|$（而非 $\|D\|$），且 Dirac 算子 $D$ 在连续谱下非迹类、迹范数发散——与公理 IV"总曲率 γ 迹发散"自洽。故此处为**形式观察**，待超代数框架严格化。

---

## 七、边界：哪些严格、哪些形式

| 条目 | 状态 |
| :--- | :--- |
| 变分 → Dirac 方程 | **严格**（标准结果） |
| 路径积分 = Berezin 积分 | **严格**（费米子路径积分标准做法） |
| γ = Dirac 算子范数 | **形式**（Grassmann 的"二阶变分"需超代数框架才严格） |
| 旋量 = ψ 的最小自洽取法 | **半硬**（有对称性根据，"最小"需在表示论意义下界定） |

---

## 八、小结

- **一句话**：Dirac 场是公理 II 的**显式实例**——ψ = 旋量场，F = Dirac 拉氏量，变分给出 Dirac 方程。
- **意义**：它给"公理 II 不只是哲学口号"提供了一个**可验证的物理落点**，也把"旋量"正式接进 `functional-monism`。
- **边界**：变分与路径积分两处**严格**；γ 那处**形式**，待超代数化。

---

*文档版本：v1.0*
*时间：2026-09-14*
*配套：axiom_II_evolution.md、axiom_II_spinor_interface.md、notes/spinor_notes.md*
