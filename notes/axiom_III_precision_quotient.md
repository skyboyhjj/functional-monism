# 公理 III · 提法之三：精度商（信息面）

**——把"认知置信度"读成"分辨结构 / 精度商"**

> **定位**：`notes/` 级长文 · **公理 III 提法之三（信息面）**；与 [公理 III 曲率版](../axioms/axiom_III_curvature.md)（提法一）、[γ 正则化与 η](axiom_III_IV_gamma_regularity_and_eta.md)（提法二）并列。
>
> **版本**：v1.0　**时间**：2026-09-27
>
> **来源**：2026-09-27「公理 III 侦察线」精度商版。

---

## 0. 一句话

**存在域配有一个"精度结构"——一族精度商（粗粒化满射）$`\Pi_\epsilon:X\twoheadrightarrow X_\epsilon`$；而 $`\gamma`$ 就是分辨谱的"逆平方和" $`\sum_i\epsilon_i^{-2}`$。** 这与曲率版 $`\gamma=\sum_i\lambda_i`$ 在 $`\lambda_i=\epsilon_i^{-2}`$ 下**逐项相同**。

## 1. 形式化陈述

**定义（精度结构）**：设 $`X`$ 为存在域（公理 I 的对象空间）。$`X`$ 上的**精度结构**是一族满射（精度商 / 粗粒化）

$$\Pi_\epsilon: X \twoheadrightarrow X_\epsilon,\qquad \epsilon\in(0,\epsilon_0],$$

满足三条：

- **(精化序)** $`0<\epsilon_1<\epsilon_2\ \Rightarrow\ \Pi_{\epsilon_1}`$ 精化 $`\Pi_{\epsilon_2}`$（$`\Pi_{\epsilon_2}`$ 因子化过 $`\Pi_{\epsilon_1}`$）；
- **(相容)** $`\Pi_{\epsilon_2}=\rho_{\epsilon_2\epsilon_1}\circ\Pi_{\epsilon_1}`$（$`\epsilon_1<\epsilon_2`$）——即一个**投影系统**；
- **(极限重建)** $`X\cong\varprojlim_{\epsilon\to0}X_\epsilon`$。

**公理 III（信息面）**：

> **存在域 $`X`$ 配有一个精度结构 $`\{\Pi_\epsilon\}`$；$`\epsilon`$ 度量分辨的粗细，$`\log(\text{分辨数})=-\log\epsilon`$ 度量信息量。**

**群 / 对称性面**（精度商天然带对称性**收缩**）：$`\Pi_\epsilon`$ 把连续对称群 $`G`$ 约化为子群——如 $`U(1)\to\mathbb Z_5`$。故**精度 = 对称性的离散化 / 收缩**。

## 2. 与曲率版"同体"（关键·定量）

由公理 III 推论 1（Cramér–Rao）：$`\mathrm{Cov}\succeq H^{-1}`$，有效估计下取等，于是**分辨（标准差）** 与 **Hessian 特征值** 满足

$$\lambda_i=\epsilon_i^{-2}\qquad\Longrightarrow\qquad\gamma=\mathrm{Tr}(H)=\sum_i\lambda_i=\sum_i\epsilon_i^{-2}.$$

⟹ **曲率谱 = 分辨谱的逆平方**：两版是**同一对象的两种读法**（几何 ↔ 信息），**逐项对应**。

## 3. 关系的严格版（"三面"须厘清）

**先分清**：本套装是"**三提法**"（一 = 曲率·有限维；二 = 重整化·连续极限；三 = 信息·精度商，即本版），**不是"三面"**。就"面"而言只有**两个**（几何、信息）——"几何"因有限维 / 连续极限而分成两提法。

| 边 | 状态 | 依据 |
| :-- | :-- | :-- |
| 三（信息）↔ 一（几何·有限维） | ✓ **闭合（定量）** | $`\lambda_i=\epsilon_i^{-2}`$（Cramér–Rao） |
| 一（有限维）↔ 二（连续极限） | ✓ **闭合** | 重整化（$`\mathrm{Tr}H\to\zeta_{D^2}(-1/2)`$，同一 $`\gamma`$） |
| 二（重整化）↔ 三（信息） | ✗ 未闭合 | 仅"机制类比"（减发散取有限 ⟺ 有限→无限不免费） |
| 信息 → 拓扑 | ✓ **闭合（派生）** | 一致结构 / 极限拓扑（见 `06`） |
| 拓扑 ↔ 几何 | ✓ **闭合（派生）** | $`H^1`$ 障碍（de Rham） |

⟹ **三角已闭合**（三条边各有依据，见 `06-第三角_拓扑面_派生面.md`）；**拓扑面是派生面（非独立提法）**；唯 二（重整化）↔ 三（信息）仍只到机制类比。

## 4. 与其它公理的接口

| 公理 | 接口 |
| :-- | :-- |
| I（存在） | 精度结构 = 存在域的"有限分辨影子" |
| II（演化） | $`\kappa`$ = 精度商 $`S^1\twoheadrightarrow\mathbb Z_5`$ 的强度（演化被精度**截断**） |
| IV（对应） | 精度结构的"**有 / 无**"：p 进 / $`\kappa`$ **有** → 免费；算术**缺** → 正性不免费 |

## 5. 实例

| 实例 | 精度商 | 精度参数 |
| :-- | :-- | :-- |
| p 进 | $`\mathbb Z_p\twoheadrightarrow\mathbb Z/p^n`$ | $`\epsilon=p^{-n}`$ |
| $`\kappa`$（相位） | $`S^1\twoheadrightarrow\mathbb Z_5`$ | $`\kappa`$（$`\leftrightarrow\epsilon`$） |
| 有限维 Hessian | 特征值截断 | $`\epsilon_i=\lambda_i^{-1/2}`$ |

## 6. 诚实边界

- 三提法间已**三角闭合**（几何↔信息、有限维↔连续极限、信息→拓扑→几何）；**"拓扑面"是派生面**（非独立提法，见 `06`）；唯 **二↔三**仍只到机制类比；
- "精度商族 + 极限重建"是**最宽泛**的候选，**未证唯一**；
- 与公理 IV 的"有 / 无"是**结构性描述**，不是定理；
- "群的收缩"（$`U(1)\to\mathbb Z_5`$）是**实例层面**（来自 $`\kappa`$），**不是**公理层面的普遍断言。

## 附：一句话

**公理 III 的信息面 = "精度结构"（一族精度商 $`\Pi_\epsilon:X\twoheadrightarrow X_\epsilon`$，带精化序、相容、极限重建）；$`\gamma=\sum_i\epsilon_i^{-2}`$。它与曲率版 $`\gamma=\sum_i\lambda_i`$ 逐项同体（$`\lambda_i=\epsilon_i^{-2}`$，由 Cramér–Rao）。上接 I（有限分辨影子）、左接 II（$`\kappa`$ = 精度截断）、右接 IV（精度结构的"有/无" = 正性的免费/不免费）。**

---

*文档版本：v1.0*
*时间：2026-09-27*
*定位：`notes/` · 公理 III 提法之三（信息面）*
*上游：`notes/axiom_II_bridge_phase_amplitude.md` §6（κ 的落点）*
*配套：公理 III 侦察线脚本（[explore_gongli3_precision.py](../scripts/axiom_III/explore_gongli3_precision.py) 等）*
