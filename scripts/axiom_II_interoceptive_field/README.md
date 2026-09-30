# 公理 II 内感受场实例 · 验证脚本

> 配套文档：[公理 II 的实例：内感受场](../../axioms/axiom_II_example_interoceptive_field.md)

仅依赖 numpy。运行：

```bash
python verify_interoceptive_F.py
```

| 脚本 | 内容 | 关键校验点 |
| :-- | :-- | :-- |
| `verify_interoceptive_F.py` | 内感受拉氏量 L = ½m‖ψ̇‖² − V + A·ψ̇ 的五组核验 | E–L 残差随 h 收敛；∮A·ds = curl·Area；γ = ‖curl A‖ = 2‖antisym J_A‖ |

## 诚实的边界

- 五组核验均为**数值**（RK4 + 步长细扫），非解析证明。
- "精度 γ = ‖curl A‖" 的**精度桥**是**形式对应**，不是定理。
- 脚本无 assert，`exit 0` 仅表示未崩溃；结论靠表中数值逐一对照。