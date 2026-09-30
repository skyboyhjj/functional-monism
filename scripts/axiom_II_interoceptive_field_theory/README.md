# 公理 II 内感受场（场论版）· 验证脚本

> 配套文档：[公理 II 的实例：内感受场（场论版）](../../axioms/axiom_II_example_interoceptive_field_theory.md)

仅依赖 numpy。运行：

```bash
python verify_interoceptive_field_F.py
```

| 脚本 | 内容 | 关键校验点 |
| :-- | :-- | :-- |
| `verify_interoceptive_field_F.py` | 场论拉氏密度 L = ½η∂ψ∂ψ − V + A_μ·∂^μψ 的六组核验 | E–L 场方程；全散度判据；内部规范不变；x-均匀归约；γ = max_μ‖W^μ‖ |

## 诚实边界

- 各组均为**数值**（有限差分 / FFT 谱法 + RK4），非解析证明。
- 组 1 的"1+1 ≡ 0+1"是 x-均匀极限下的**恒等**（连续层同式），真正的独立归约验证在组 4 的 k=0 模态对比。
- "精度 γ = max_μ‖W^μ‖" 的**精度桥**是**形式对应**，不是定理。
- 脚本无 assert，`exit 0` 仅表示未崩溃；结论靠表中数值逐一对照。