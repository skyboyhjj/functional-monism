# 公理 II 的桥 · 验证脚本

> 配套长文：[公理 II 的桥：相位↔幅度的桥](../../notes/axiom_II_bridge_phase_amplitude.md)

仅依赖 numpy。逐个运行：

```bash
python demo_gongli2_bridge.py
python demo_circle_dissipation.py
python verify_wuxing_phase.py
python assemble_wuxing_interoception.py
python where_is_kappa.py
```

| 脚本 | 内容 | 关键校验点 |
| :-- | :-- | :-- |
| `demo_gongli2_bridge.py` | 时间-1 映射；阻尼 γ（保守↔耗散） | φ₁(θᵢ)=θ_{R(i)}；自由能 F 单调降；γ=0 守恒、γ>0 耗散 |
| `demo_circle_dissipation.py` | 拓扑障碍 H¹(S¹)=ℝ；Kuramoto / Stuart-Landau | Kuramoto 锁相约 30° |
| `verify_wuxing_phase.py` | 五行相位检验 | 生/克/侮/及母=R¹..R⁴；生∪克=K₅；特征值单位圆、det=+1 |
| `assemble_wuxing_interoception.py` | 组装 κz̄⁴ + 五次饱和 | 仅 κ 项发散；配饱和后锁相，距 72° 倍数随 κ 而定（κ=2 约 1.4°、κ=4 约 0.1°） |
| `where_is_kappa.py` | κ 把 U(1) 破缺到 Z₅ | κ=0 全 U(1) 等变；κ≠0 只 Z₅ 等变 |

## 诚实边界

- 「五行 = 相位」通过，但判别力只来自「生/克互补」；「互补是发现的还是定义的」未定。
- 组装是存在性（一个可行组装），非唯一/必然；耦合是选的，不是推的。
- 「离散性 = 公理 III」是分类判断，不是定理。