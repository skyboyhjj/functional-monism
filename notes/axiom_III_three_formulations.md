# 公理 III 的三提法与两面

**——曲率 / 重整化 / 精度商，与几何·信息·派生拓扑**

> **定位**：`notes/` 级 · **公理 III 总览（索引）**；把三提法与两面收在一处，并给 [公理 III 提法之三（精度商）](axiom_III_precision_quotient.md) 与 [派生拓扑面](axiom_III_topological_face.md) 一个共同入口。
>
> **版本**：v1.0　**时间**：2026-09-27
>
> **来源**：2026-09-27「公理 III 侦察线」（配合 `notes/axiom_II_bridge_phase_amplitude.md` §6 的 κ 落点）。

---

## 0. 一句话

**公理 III（曲率 / 精度）有"三提法"与"两面"，外加一个派生拓扑面。** 三提法间**三角闭合**（三条边各有依据）；唯"重整化 ↔ 信息"这条外接边**仅到机制类比**。

## 1. 三提法

| # | 提法 | 面 | 核心 | 文档 |
| :-- | :-- | :-- | :-- | :-- |
| **一** | 曲率版（有限维） | 几何 | $`\gamma=\lVert\delta^2F/\delta\psi^2\rVert_{S_1}=\mathrm{Tr}\,H`$ | [axiom_III_curvature](../axioms/axiom_III_curvature.md) |
| **二** | 重整化版（连续极限） | 几何 | $`\gamma_{\text{ren}}=\zeta_{D^2}(-1/2)`$ | [axiom_IV_note_gamma_renormalization](axiom_IV_note_gamma_renormalization.md)、[axiom_III_IV_gamma_regularity_and_eta](axiom_III_IV_gamma_regularity_and_eta.md) |
| **三** | 精度商版 | 信息 | 精度结构 $`\{\Pi_\epsilon\}`$，$`\gamma=\sum_i\epsilon_i^{-2}`$ | [axiom_III_precision_quotient](axiom_III_precision_quotient.md) |

## 2. 两面与派生拓扑面

- **两面**：**几何**（曲率谱 $`\lambda_i`$）与**信息**（分辨谱 $`\epsilon_i`$）——由 $`\lambda_i=\epsilon_i^{-2}`$（Cramér–Rao）**定量接通**。
- **派生拓扑面**（$`H^*`$、一致结构）：见 [axiom_III_topological_face](axiom_III_topological_face.md)。它是**派生面**（从信息面导出），**不是第四提法**。

## 3. 接通图

| 边 | 状态 | 依据 |
| :-- | :-- | :-- |
| 几何 ↔ 信息 | ✓ 闭合（定量） | $`\lambda_i=\epsilon_i^{-2}`$（Cramér–Rao） |
| 几何有限维 ↔ 连续极限 | ✓ 闭合 | 重整化（同一 $`\gamma`$） |
| 信息 → 拓扑 | ✓ 闭合（定义性） | 一致结构 / 极限拓扑 |
| 拓扑 ↔ 几何 | ✓ 闭合 | $`H^1`$ 障碍（de Rham） |
| **二（重整化）↔ 三（信息）** | ✗ **未闭合** | 仅机制类比（减发散取有限 ⟺ 有限→无限不免费） |

⟹ **三角闭合；一条外接边未闭合。**

## 4. 与其它公理的接口

| 公理 | 接口 |
| :-- | :-- |
| I（存在） | 精度结构 = 存在域的"有限分辨影子" |
| II（演化） | $`\kappa`$ = 精度商 $`S^1\to\mathbb Z_5`$ 的强度（演化被精度**截断**）——见 [bridge note](axiom_II_bridge_phase_amplitude.md) §6 |
| IV（对应） | 精度结构的"有 / 无"：p 进 / $`\kappa`$ **有** → 免费；算术**缺** → 正性不免费 |

## 5. 命名更正（重要）

"三面"是**误称**——**面只有两个**（几何、信息）；"三"指**提法**（几何因有限维 / 连续极限而分两提法）。故准确名称是 **"三提法 · 两面（+派生拓扑面）"**。

## 6. 诚实边界

- 三提法间三角闭合，但**拓扑面是派生面**（非独立提法）；
- 唯 **"重整化 ↔ 信息"** 仍只到机制类比（未定量闭合）；
- 与公理 IV 的"有 / 无"是**结构性描述**，不是定理。

---

*文档版本：v1.0*
*时间：2026-09-27*
*定位：`notes/` · 公理 III 总览（索引）*
*上游：axioms/axiom_III_curvature.md、notes/axiom_III_IV_gamma_regularity_and_eta.md*
*配套：axiom_III_precision_quotient.md、axiom_III_topological_face.md*
