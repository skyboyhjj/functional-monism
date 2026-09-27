# 公理 III · 三提法两面 — 配套脚本

本目录脚本对应 [公理 III 三提法两面](../../notes/axiom_III_three_formulations.md) 的数值验证。均为「先算后说」——运行即打印数值结论，仅依赖 numpy，无第三方库。

## 脚本清单

| 脚本 | 对应文档 | 验证内容 |
| :-- | :-- | :-- |
| `explore_gongli3_precision.py` | 提法三·精度商（[precision_quotient](../../notes/axiom_III_precision_quotient.md)） | 精度商三触点：p 进精度、κ 相位精度（$`S^1\to\mathbb Z_5`$）、精度 = 信息量 |
| `demo_topological_face.py` | 派生拓扑面（[topological_face](../../notes/axiom_III_topological_face.md)） | 信息→拓扑（一致结构）、拓扑↔几何（$`H^1`$ 障碍） |
| `explore_gongli3_s4_positivity.py` | 侦察线 S4（对应 [γ 正则化与 η](../../notes/axiom_III_IV_gamma_regularity_and_eta.md)） | 否证「正性 = 精度极限」 |

## 诚实边界

- `explore_gongli3_s4_positivity.py` 是**否证**：候选「正性 = 精度极限」不成立——正性对极限封闭（若存在极限，正性本已免费），但 semilocal 测度随 places 增加发散（$`\mu_S(0)=\prod_{p\le P}(1-p^{-1/2})^{-2}\to\infty`$），故不存在「精度极限」。结论是公理 III 的精度结构在算术情形仍**缺失**，而非正面构造。
- 前两个脚本是**存在性 / 示意**验证（一个可行实例），不是定理证明。

## 复现

```bash
python scripts/axiom_III/explore_gongli3_precision.py
python scripts/axiom_III/demo_topological_face.py
python scripts/axiom_III/explore_gongli3_s4_positivity.py
```