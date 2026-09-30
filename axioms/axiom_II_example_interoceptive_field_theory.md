# 公理 II 的实例：内感受场（场论版）

**——Axiom II · Interoceptive Field（实例节 · 场论版，不计入公理编号）**

> **定位**：承 [axiom_II_example_interoceptive_field.md](axiom_II_example_interoceptive_field.md)（轨迹版 $`\psi(t)`$），升级为 $`\psi(t,x)`$ 的**严格场论版**，并与 [axiom_II_example_dirac_field.md](axiom_II_example_dirac_field.md) 的 Dirac **密度**形式逐项对齐。
> **一句话**：同一个"矢势项"在场论里成为 $`A_\mu(\psi)\cdot\partial^\mu\psi`$；"不可写成势差"的判据从 $`\mathrm{curl}A`$ 升为**内部曲率** $`W_{ab}^{\ \mu}`$；而 **$`x`$-均匀极限严格归约回轨迹版**。

---

## 一、为什么要升级

| | 轨迹版 | 场论版 |
| :-- | :-- | :-- |
| 场 | $`\psi(t)`$（有限维） | $`\psi(t,x)`$（无限维） |
| 与 Dirac 同级？ | 否（Dirac 是场论） | **是** |
| 矢势 | 1-形式 $`A(\psi)`$ | 1-形式 $`A_\mu(\psi)`$ |
| 判据 | $`\mathrm{curl}A`$ | 内部曲率 $`W_{ab}^{\ \mu}`$ |

> 文章的场景本质是**场**：智能体在"世界 $`x`$ × 时间 $`t`$"里运动。所以严格的对齐对象是 Dirac 的**密度** $`\mathcal L_D`$，不是 Hamilton 量。

---

## 二、场构型：内感受场

内感受场取值于**内部状态空间**：

$$\psi:\ M\to\mathcal J,\qquad M=\mathbb R^{1+d},\quad \mathcal J=\mathbb R^n$$

- $`x\in\mathbb R^d`$ 读作"世界位置"，$`\psi(t,x)`$ = 智能体在 $`x`$ 处时刻 $`t`$ 的**内部状态**；
- $`n`$ 取 1 时是标量内感受场；本文算例取 $`n=2`$（与轨迹版对齐）。

---

## 三、代入：内感受拉氏密度

$$\mathcal L=\tfrac12\,\eta^{\mu\nu}\,\partial_\mu\psi\cdot\partial_\nu\psi-V(\psi)+A_\mu(\psi)\cdot\partial^\mu\psi$$

其中 $`\eta=\mathrm{diag}(+1,-1,\dots,-1)`$，$`\cdot`$ 是 $`\mathbb R^n`$ 内积，$`\partial^\mu=\eta^{\mu\nu}\partial_\nu`$。

### 3.1 与 Dirac 密度逐项对齐

Dirac：$`\mathcal L_D=\bar\psi\,(i\gamma^\mu\partial_\mu-m)\,\psi`$

| 项 | Dirac 密度 | 内感受拉氏密度 | 说明 |
| :-- | :-- | :-- | :-- |
| 场 | $`\psi:M\to\Delta`$（$`\mathbb C^4`$ 旋量） | $`\psi:M\to\mathcal J`$（$`\mathbb R^n`$） | 取值空间 |
| 一阶项 | $`i\bar\psi\gamma^\mu\partial_\mu\psi`$ | $`A_\mu(\psi)\cdot\partial^\mu\psi`$ | 含"内部结构" |
| 质量／势 | $`-m\,\bar\psi\psi`$ | $`-V(\psi)=-(D+U_{\text{ext}})`$ | 设定点（两本账） |
| 动能 | 无（Dirac 是一阶） | $`\tfrac12\eta^{\mu\nu}\partial_\mu\psi\cdot\partial_\nu\psi`$ | **差别所在** |
| 内部结构载体 | $`\gamma^\mu`$（Clifford，**常数**） | $`A_\mu(\psi)`$（**$`\psi`$-依赖**） | 见下 |
| 变分 $`\Rightarrow`$ | $`(i\gamma^\mu\partial_\mu-m)\psi=0`$ | $`\Box\psi=-\nabla V+W\,\partial\psi`$ | 场方程 |
| 精度 | $`\gamma\approx2\lVert D\rVert`$ | $`\gamma=\max_\mu\lVert W^\mu\rVert`$ | 二阶信息 |

★ **结构性观察**（非等价）：Dirac 的 $`\gamma^\mu`$ **不依赖** $`\psi`$，故场方程**线性**（自由场）；内感受的 $`A_\mu`$ **依赖** $`\psi`$，故可以有 $`W\neq0`$，场方程**非线性**（自作用）。这条差别正是"机制"所在。

---

## 四、场论变分 → 场方程

多分量场的 Euler–Lagrange：

$$\partial_\mu\Big(\frac{\partial\mathcal L}{\partial(\partial_\mu\psi^a)}\Big)-\frac{\partial\mathcal L}{\partial\psi^a}=0$$

代入 $`\mathcal L`$，得（记 $`\Box=\partial^\mu\partial_\mu`$）

$$\Box\psi_a=-\partial_aV+W_{ab}^{\ \mu}\,\partial_\mu\psi^b,\qquad W_{ab}^{\ \mu}=\partial_aA^{\mu}_{b}-\partial_bA^{\mu}_{a}$$

- $`-\partial_aV`$：**势型**（趋近设定点）；
- $`W_{ab}^{\ \mu}\partial_\mu\psi^b`$：**内生驱动** —— 就是"不能写成势差"的那一项，其载体是**内部曲率** $`W`$（关于 $`a,b`$ 反对称）。

> 对照轨迹版：那里是 $`M_{ab}=\partial_aA_b-\partial_bA_a`$（2 指标）；这里每个时空方向 $`\mu`$ 各带一个 $`W^{\mu}`$。**轨迹版是场论版只留 $`\mu=t`$ 的特例**（见 §六）。

---

## 五、那一项为什么"不可写成势差"（场论判据）

**(a) 全散度（严格）。** 若矢势在内部指标上是纯梯度

$$A^{\mu}_{a}=\partial_a\Lambda^{\mu}\quad\Rightarrow\quad A^{\mu}_{a}\partial_\mu\psi^a=\partial_\mu(\Lambda^{\mu}\circ\psi)$$

右边是**全散度**，在作用量里是边界项 ⟹ 不影响场方程。故 $`A\cdot\partial\psi`$ 项**被吸收**当且仅当它是内部梯度；真正的驱动只有**不可积部分** $`W\neq0`$。

**(b) 内部规范不变（严格）。** 作变换 $`A^{\mu}_{a}\to A^{\mu}_{a}+\partial_a\chi^{\mu}`$（$`\chi^{\mu}`$ 是 $`\psi`$ 的标量函数），则

$$W_{ab}^{\ \mu}\ \longmapsto\ W_{ab}^{\ \mu}+\partial_a\partial_b\chi^{\mu}-\partial_b\partial_a\chi^{\mu}=W_{ab}^{\ \mu}$$

即 $`W`$ **不变**。于是：$`A`$ 能写成势差（内部梯度）**当且仅当** $`W=0`$。

> ★ 结论与轨迹版同构，且更强：**"不可写成势差" = "内部曲率为零"的否定**。文章的 $`r_t=D(s_t)-D(s_{t+1})`$ 对应 $`A_t^a=\partial_a(-D)`$（每点内部梯度，仅 $`\mu=t`$ 分量非零）⟹ $`W\equiv0`$。

---

## 六、均匀极限：严格归约回轨迹版

若场在 $`x`$ 上均匀（$`\partial_x\psi\equiv0`$），则 $`\Box\psi=\partial_t^2\psi`$，且 $`\partial_\mu\psi`$ 只剩 $`\mu=t`$ 一项，场方程退化为

$$\partial_t^2\psi_a=-\partial_aV+W_{ab}^{\ t}\,\partial_t\psi^b$$

这正是轨迹版 $`m\ddot\psi=-\nabla V+(\mathrm{curl}A)\,\mathcal J\,\dot\psi`$（取 $`m=1`$、$`M_{ab}=W_{ab}^{\ t}`$）。

> ⟹ **轨迹版被场论版严格包含**（$`\mathrm{curl}\,A`$ 就是 $`W^t`$）。数值见算据 1、4：把轨迹解嵌入 $`x`$-均匀场，$`1{+}1`$ 维场方程残差随步长收敛（$`x`$-均匀下 $`1{+}1`$ 场方程与 $`0{+}1`$ 轨迹方程**逐点同一**，故残差相同）；独立的归约验证见算据 4 的 $`k=0`$ 模态对比。

---

## 七、精度 γ（形式观察）

$`\mathcal L`$ 含一阶项 $`A_\mu\cdot\partial^\mu\psi`$；**这一项**对纯二阶变分（$`\partial^2/\partial\psi^2`$ 与 $`\partial^2/\partial(\partial\psi)^2`$）贡献为零，其全部二阶贡献落在**混合**变分

$$\frac{\partial^2\mathcal L}{\partial\psi^a\,\partial(\partial_\mu\psi^b)}=\partial_aA^{\mu}_{b}=J^{\mu}_{ab}$$

运动方程只用到 $`J^\mu`$ 的**全**反对称差，取它的范数：

$$\gamma=\max_\mu\big\lVert J^{\mu}-(J^{\mu})^{\mathsf T}\big\rVert=\max_\mu\lVert W^{\mu}\rVert$$

> **口径注（反对称块 = 全差）**：$`W^\mu=J^\mu-(J^\mu)^{\mathsf T}`$ 是 $`J^\mu`$ 的**全**反对称差（非 $`\tfrac12(J-(J)^{\mathsf T})`$），与轨迹版 $`\mathrm{curl}A`$ 同源——运动方程用到的正是这个全差。

> **与 Dirac 同构（一处不同）**：那边 $`\psi`$ 与 $`\bar\psi`$ 配对、对单一 $`\psi`$ 线性故纯二阶变分本身为零，Hessian 取反对角块得 $`\approx2\lVert D\rVert`$（见 `axiom_II_example_dirac_field.md` §六口径补注）；这边 $`\psi`$ 与 $`\partial_\mu\psi`$ 配对、取反对称块得 $`\max_\mu\lVert W^\mu\rVert`$。不同在于本拉氏密度还有动能 $`\eta^{\mu\nu}`$ 与势 $`-\partial_a\partial_bV`$ 的**对称**纯二阶块——它们不进反对称（曲率）部分，故 $`\gamma`$ 仍只由 $`J^\mu-(J^\mu)^{\mathsf T}`$ 决定。

**精度桥**：$`\pi=\sigma^{-2}`$（逐信道）的全局合成，其形式对应即 $`\max_\mu\lVert W^\mu\rVert`$。★ 仅形式对应，非定理。

---

## 八、$`1{+}1`$ 维算例（$`n=2`$）

取 $`V=\tfrac12k\lVert\psi\rVert^2`$、$`A_t=\tfrac{w}{2}(-\psi_2,\psi_1)`$、$`A_x=0`$。此时 $`W_{12}^{\ t}=w`$，场方程是**线性**的：

$$\Box\psi_1=-k\psi_1+w\,\partial_t\psi_2,\qquad \Box\psi_2=-k\psi_2-w\,\partial_t\psi_1$$

用 FFT 谱法（每模态 $`\text{RK4}`$）解之，初值 $`\psi_1`$ 为高斯包、$`\psi_2=0`$：

| $`w`$ | $`\max\lvert\psi_1\rvert`$ | $`\max\lvert\psi_2\rvert`$ | $`k=0`$ 模态 vs 轨迹版 |
| :-- | :-- | :-- | :-- |
| 0 | 1.0000 | 0.000e+00 | 差 = 0 |
| 1.2 | 1.0000 | 8.97e−01 | 差 = 0 |

> ⟹ $`w=0`$（$`W=0`$，纯势差）时 $`\psi_2`$ **严格为零**（无偏振、无耦合）；$`w\neq0`$ 时 $`\psi_2`$ 被激发 —— 这是"内生耦合"的可观测后果。而 $`k=0`$ 模态（$`x`$-均匀）**逐点等于**轨迹版。

---

## 九、边界：哪些严格、哪些形式

| 条目 | 状态 |
| :-- | :-- |
| 场论变分 $`\Rightarrow`$ 场方程（含 $`W`$ 项） | **严格**（标准 E–L） |
| $`A_\mu^a=\partial_a\Lambda_\mu\Rightarrow`$ 全散度 $`\Rightarrow`$ 场方程不变 | **严格** |
| 内部规范 $`A\to A+\partial_\psi\chi`$ 保 $`W`$ 不变 | **严格** |
| $`x`$-均匀 $`\Rightarrow`$ 归约到轨迹版 | **严格**（＋数值） |
| 线性算例的偏振耦合（$`w\neq0`$ 激发 $`\psi_2`$） | **半严格（数值）** |
| $`\gamma=\max_\mu\lVert W^\mu\rVert`$；文章原型 $`\gamma\equiv0`$ | **严格**（定义 ＋ 数值） |
| "$`A_\mu`$ = 内部丛上的联络，$`W`$ = 曲率" | **结构性**（非可证等价） |
| "$`\gamma^\mu`$（常数）↔ 自由场；$`A_\mu(\psi)`$（依赖）↔ 自作用" | **结构性** |
| "内感受 = 生命的内稳态"（生物学） | **主题呼应**（不在本文范围） |

★ **不得**把"曲率非零"写成"证明了内感受的自主性"。

---

## 十、算据

脚本 `scripts/axiom_II_interoceptive_field_theory/verify_interoceptive_field_F.py`（exit 0）：

| 组 | 检验 | 结果 |
| :-- | :-- | :-- |
| 1 | 归约（$`x`$-均匀）：$`1{+}1`$ 场方程残差随 $`h`$ 收敛 | 9.1e−8 ／ 2.3e−8 ／ 6.4e−9 |
| 2 | 全散度：$`\max\lVert W(\partial\Lambda)\rVert`$ | 4.2e−11 |
| 3 | 内部规范：$`\lVert W(A)-W(A+\partial\chi)\rVert`$ | 5.6e−11 |
| 4 | $`1{+}1`$ 谱解 $`w=0`$ | $`\max\lvert\psi_2\rvert=0`$ |
| 4 | $`1{+}1`$ 谱解 $`w=1.2`$ | $`\max\lvert\psi_2\rvert=0.897`$ |
| 4 | $`k=0`$ 模态 vs 轨迹版（独立积分器对比） | 差 **0.0** |
| 5 | 文章原型 $`\max_\mu\lVert W^\mu\rVert`$ | 4.2e−11 ⟹ $`\gamma=0`$ |

---

## 十一、小结

- **一句话**：内感受场的拉氏密度

$$\mathcal L=\tfrac12\,\eta^{\mu\nu}\partial_\mu\psi\cdot\partial_\nu\psi-V(\psi)+A_\mu(\psi)\cdot\partial^\mu\psi$$

变分给出 $`\Box\psi=-\nabla V+W\,\partial\psi`$；"那一项"的判据是**内部曲率** $`W_{ab}^{\ \mu}\neq0`$。

- **升级买到了什么**：与 Dirac **同级的场论对象**；轨迹版被**严格包含**（$`x`$-均匀极限）；$`\gamma`$ 与 Dirac 的 $`\approx2\lVert D\rVert`$ 严格同构。
- **不变的是什么**：机制（公理 II）与精度（公理 III）**仍共用同一个零点** —— 文章原型 $`W\equiv0`$。
- **边界**：变分／全散度／规范不变／归约４处**严格**；偏振耦合**半严格（数值）**；"联络／曲率"与"$`\gamma^\mu`$ 对齐"**结构性**。

---

*文档版本：v1.1　时间：2026-09-30*
*定位：`axioms/` · 公理 II 实例节（场论版，不计入公理编号）*
*配套：`scripts/axiom_II_interoceptive_field_theory/verify_interoceptive_field_F.py`；[axiom_II_example_interoceptive_field.md](axiom_II_example_interoceptive_field.md)（轨迹版）；[axiom_II_example_dirac_field.md](axiom_II_example_dirac_field.md)*