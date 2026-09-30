# 公理 II 的实例：内感受场

**——Axiom II · Interoceptive Instance（实例节，不计入公理编号）**

> **定位**：照 `axioms/axiom_II_example_dirac_field.md` 的样板，把内感受 AI 的内部状态场写成公理 II 的**显式实例**。
> **它回答**：《读解：把「缺口卡在公理 II」再压一层》留下的那句 —— "`F` 里缺一个**不可写成势差**的动力学项"—— **补上之后 `F` 长什么样**。
> **一句话**：那一项是矢势项 $`A(\psi)\cdot\dot\psi`$；它"不可写成势差"的判据是 $`\mathrm{curl}A\neq0`$；而文章原型的 $`\mathrm{curl}A`$ 恒为零。

---

## 一、公理 II 回顾

公理 II（演化公理）：场构型 $`\psi`$ 的演化满足变分原理

$$\delta\int F[\psi]\,dt=0$$

其一般形式（拉氏量）为

$$F[\psi]=\int\mathcal L[\psi,\partial_t\psi]\,dt$$

（其中 $`\mathcal L`$ 为拉氏密度；本文取 $`\psi=\psi(t)`$，即"内部状态轨迹"，故这里是**有限维拉氏量**而非场密度。这与 Dirac 实例的场论写法只差 $`\psi`$ 的变元个数。）

---

## 二、场构型：内感受场

Dirac 实例取 $`\psi:M\to\Delta`$（旋量场）。本文取内感受 AI 的**内部状态**作场。

文章把状态因子化 $`S=S^E\times S^b\times S^I`$。本文取

$$\psi(t)=s^I(t)\in\mathcal I,\qquad \mathcal I=\mathbb R^n$$

即**内部状态轨迹**；$`s^E`$、$`s^b`$（外部与身体）作为背景参数，进入势项。

**与旋量实例的对应**（分层纪律照抄 `axiom_II_spinor_interface.md`）：

| 层 | 旋量实例 | 本文实例 |
| :-- | :-- | :-- |
| 场 $`\psi`$ | 旋量场 | 内部状态轨迹 |
| 硬包含 | 变分 $`\Rightarrow`$ Dirac 方程 | 变分 $`\Rightarrow`$ 内感受方程 |
| 半硬 | 旋量 = 最小自洽取法 | 内部状态 = 最简取法（$`n`$ 维） |
| 主题呼应 | — | "内感受 = 生命的内稳态" |

★ **纪律**：第三、四行是**主题呼应**，**不得**写成等价。

---

## 三、代入：内感受拉氏量

$$\mathcal L=\tfrac12 m\lVert\dot\psi\rVert^2-V(\psi)+A(\psi)\cdot\dot\psi$$

三项（势项内含"两本账"）：

1. **惯性项** $`\tfrac12 m\lVert\dot\psi\rVert^2`$ —— 动能；
2. **势项** $`V(\psi)=D(\psi)+U_{\text{ext}}(\psi)`$ —— $`D`$ 是内感受（到设定点的距离，文章账 B），$`U_{\text{ext}}`$ 是外感受（账 A 的相位）；
3. **内生驱动项** $`A(\psi)\cdot\dot\psi`$ —— $`A`$ 是内部状态空间上的一个矢量势。**这一项就是"不能写成势差"的那一项。**

对照 Dirac 拉氏量 $`\mathcal L_D=\bar\psi(i\gamma^\mu\partial_\mu-m)\psi`$：后者是**双线性**，前者含**一阶项** $`A\cdot\dot\psi`$。

> 两者的"一阶性"是同一件事 —— 正因如此，它们的精度 $`\gamma`$ 都只能从**混合变分**提取（见 §六）。

---

## 四、变分 → 内感受方程

Euler–Lagrange 方程

$$\frac{d}{dt}\Big(\frac{\partial\mathcal L}{\partial\dot\psi}\Big)-\frac{\partial\mathcal L}{\partial\psi}=0$$

代入 $`\mathcal L`$，得（二维；$`\mathrm{curl}A=\partial_xA_y-\partial_yA_x`$）

$$m\ddot\psi=-\nabla V(\psi)+(\mathrm{curl}A)\,\mathcal J\,\dot\psi,\qquad \mathcal J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$$

两项分明：

- **势型项** $`-\nabla V`$：趋近设定点（文章做的正是这一半）；
- **洛伦兹型项** $`(\mathrm{curl}A)\,\mathcal J\,\dot\psi`$：**缺的就是它** —— 速度依赖、与速度垂直的驱动。

> 文章的取法给出 $`\mathrm{curl}A=0`$（见 §五），后项消失，方程退化为**纯梯度流**。这正是"仅改奖励项不改变最优策略"（Ng et al. 1999）的**连续版**。

### 4.1 与文章那条账的核对

文章的机制句是

$$r_t=D(s_t^I)-D(s_{t+1}^I)$$

连续极限即 $`r=-\dot D=-\nabla D\cdot\dot s`$ —— 等价于取 $`A=-\nabla D`$（文献常写 $`A=\nabla(-D)`$）。于是

$$\mathrm{curl}A=\mathrm{curl}(\nabla(-D))=0$$

即：**文章那个 $`F`$ 的曲率恒为零**。这一条是它"机制未落地"的**一个数**。

---

## 五、那一项为什么"不可写成势差"

两种说法，等价：

**(a) 规范不变性（严格）。** 作变换 $`A\to A+\nabla\chi`$，方程不变 —— 因为运动方程只用到 $`J_A^{\mathsf T}-J_A`$ 的反对称部分。而 $`\mathrm{Hess}\chi`$ 是对称的，贡献为零。故 $`A`$ 可自由加减梯度，只有**规范不变量** $`\mathrm{curl}A`$ 有物理意义。

> 于是：能写成势差，当且仅当 $`\mathrm{curl}A=0`$（纯规范）。这正是"势差型整形被值函数吸收"的**几何版**。

**(b) 非保守（严格）。** 沿闭合回路的功

$$\oint A\cdot d\psi=\int(\mathrm{curl}A)\,dS$$

当 $`\mathrm{curl}A\neq0`$ 时它不为零 ⟹ 不存在任何势函数生成该力 ⟹ 字面意义上的"不可写成势差"。

### 5.1 两个缺口的**同一个零点**

| 缺口 | 数学表达 | 文章原型取值 |
| :-- | :-- | :-- |
| 机制（公理 II） | 内生项 $`(\mathrm{curl}A)\,\mathcal J\,\dot\psi`$ 非零 | $`=0`$ ⟹ 缺 |
| 精度（公理 III） | $`\gamma=\lVert\mathrm{curl}A\rVert`$ 非零 | $`=0`$ ⟹ 缺 |

> ⟹ **"框架齐、机制未落地"可以写成一个数：曲率。**

---

## 六、精度 γ（形式观察）

公理 III：$`\gamma=\lVert\delta^2F/\delta\psi^2\rVert`$。合成本拉氏量的二阶变分：动能项 $`\tfrac12 m\lVert\dot\psi\rVert^2`$ 给**对称**块 $`m\,\mathbf I`$，势项给 $`-\nabla^2 V`$；而一阶项 $`A\cdot\dot\psi`$ **对纯二阶变分（$`\partial^2/\partial\psi^2`$ 与 $`\partial^2/\partial\dot\psi^2`$）贡献为零**，其全部二阶贡献落在**混合**变分

$$\frac{\partial^2\mathcal L}{\partial\psi\,\partial\dot\psi}=\frac{\partial A}{\partial\psi}=J_A$$

运动方程只用到反对称组合 $`J_A^{\mathsf T}-J_A=2\,\mathrm{antisym}\,J_A`$，取它的范数：

$$\gamma=\big\lVert J_A^{\mathsf T}-J_A\big\rVert=\lVert\mathrm{curl}A\rVert=2\,\big\lVert\mathrm{antisym}\,J_A\big\rVert$$

> **口径补注（因子 2）**：与 Dirac 那处 $`\gamma\approx2\|D\|`$ 同型——$`\mathrm{curl}A`$ 是 $`J_A`$ 反对称程度的**全量**，$`\mathrm{antisym}J_A`$ 只是它的一半。脚本 E 组实跑：$`w=1.2\Rightarrow\lVert\mathrm{antisym}J_A\rVert=0.6,\ \lVert\mathrm{curl}A\rVert=1.2`$。

> **与 Dirac 那处同构（一处不同）**：那边 $`\psi`$ 与 $`\bar\psi`$ 配对、对单一 $`\psi`$ 线性故纯二阶变分本身为零，Hessian 取反对角块得 $`\lVert D\rVert`$；这边 $`\psi`$ 与 $`\dot\psi`$ 配对、取反对称块得 $`\lVert\mathrm{curl}A\rVert`$。不同在于本拉氏量还有 $`m\,\mathbf I`$ 与 $`-\nabla^2V`$ 的**对称**纯二阶块——它们不进反对称（曲率）部分，故 $`\gamma`$ 仍只由 $`J_A^{\mathsf T}-J_A`$ 决定。

**精度桥（回应公理 III"未打通"）**：逐信道精度 $`\pi=\sigma^{-2}`$ 的全局合成，其形式对应就是 $`\lVert\mathrm{curl}A\rVert`$（$`J_A`$ 在某方向上的特征值 ↔ 逐信道精度）。

> ★ 此处**仅给形式对应**，**不是**定理。

---

## 七、边界：哪些严格、哪些形式

| 条目 | 状态 |
| :-- | :-- |
| 变分 $`\Rightarrow`$ 内感受方程（含洛伦兹项） | **严格**（标准 E–L 结果） |
| $`A\to A+\nabla\chi`$ 不改方程（规范不变） | **严格** |
| 环积分 $`\oint A\cdot d\psi=\mathrm{curl}A\cdot\mathrm{Area}`$ | **严格** |
| $`\mathrm{curl}A=0`$ 当且仅当 $`A`$ 可写成势差 | **严格** |
| 轨迹定性改变（$`\mathrm{curl}A=0`$ 是一维；$`\neq0`$ 进入二维环流） | **半严格（数值）** |
| $`\gamma=\lVert\mathrm{curl}A\rVert`$；文章原型 $`\gamma\equiv0`$ | **严格**（定义 ＋ 数值） |
| "内感受 = 内部状态空间上的联络，$`\mathrm{curl}A`$ = 曲率" | **结构性**（非可证等价） |
| "内感受 = 生命的内稳态"（生物学） | **主题呼应**（不在本文范围） |

★ **不得**把"曲率非零"写成"证明了内感受的自主性"。

---

## 八、算据

脚本 `scripts/axiom_II_interoceptive_field/verify_interoceptive_F.py`（Numerical RK4，步长细扫 $`h=10^{-3}/5\times10^{-4}/2.5\times10^{-4}`$，exit 0）：

| 组 | 检验 | 结果 |
| :-- | :-- | :-- |
| A | E–L 残差随 $`h`$ 收敛 | 9.3e−8 ／ 2.3e−8 ／ 6.7e−9 |
| A | 作用量驻定（两端归零扰动） | $`\Delta S`$ 比值 4.0、4.0 ⟹ O(eps²) |
| B | 规范不变：力场差 | 2.9e−11 |
| B | 规范不变：轨迹差 | 5.0e−12 |
| C | 势型 $`(w=0)`$ | $`\max\lvert y\rvert=0`$，面积 = 0 |
| C | 非势差 $`(w=1.2)`$ | $`\max\lvert y\rvert=0.999`$，面积 = 7.11 |
| D | 环积分 $`(r_0=1)`$ | 3.769911，与 $`\mathrm{curl}\cdot\mathrm{Area}`$ 差 −1.6e−10 |
| D | 环积分 ＋ $`\nabla\chi`$ 后不变 | 差 −3.1e−15 |
| E | 文章原型 $`\max\lvert\mathrm{curl}A\rvert`$ | 1.1e−10 ⟹ $`\gamma=0`$ |

> 说明：C 组用**有向面积**（$`\tfrac12\oint(x\,dy-y\,dx)`$）作判据 —— $`w=0`$ 时轨迹锁在一维直线、面积恒零；$`w\neq0`$ 时进入二维环流、面积非零。这是"动力学定性改变"的数值证据。

---

## 九、小结

- **一句话**：内感受 AI 的 $`F`$ 可写成

$$\mathcal L=\tfrac12 m\lVert\dot\psi\rVert^2-V(\psi)+A(\psi)\cdot\dot\psi$$

"那一项"是矢势项；"不可写成势差"的判据是 $`\mathrm{curl}A\neq0`$。

- **意义**：把"缺口卡在公理 II"从一句判断，变成一个**可写、可算的 $`F`$**，并给出**可复制模板**。
- **最有价值的一个数**：$`\mathrm{curl}A`$ —— 机制（公理 II）与精度（公理 III）**共用同一个零点**。
- **边界**：变分／规范／环积分三处**严格**；"轨迹定性改变"**半严格（数值）**；"联络／曲率"与"生物学"分别为**结构性**与**主题呼应**。

**可复制模板（照 Dirac 样板补 $`F`$）**：

1. 写出 $`F`$ ＝ 动能 − 势 ＋ 矢势项；
2. 变分，得方程；
3. 查矢势项的 $`\mathrm{curl}A`$：$`=0`$ ⟹ 仍停在"奖励整形"；$`\neq0`$ ⟹ 机制落地。

---

*文档版本：v1.1　时间：2026-09-30*
*定位：`axioms/` · 公理 II 实例节（不计入公理编号）*
*配套：`scripts/axiom_II_interoceptive_field/verify_interoceptive_F.py`；`axioms/axiom_II_example_dirac_field.md`；《读解：把「缺口卡在公理 II」再压一层》*