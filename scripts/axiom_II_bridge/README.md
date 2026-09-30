# 公理 II 的桥 · 验证脚本

> 配套长文：[公理 II 的桥：相位↔幅度的桥](../../notes/axiom_II_bridge_phase_amplitude.md)

第一轮（下 5 个）仅依赖 numpy；第二轮（桥·组装，下 3 个）另需 scipy、mpmath。逐个运行：

```bash
python demo_gongli2_bridge.py
python demo_circle_dissipation.py
python verify_wuxing_phase.py
python assemble_wuxing_interoception.py
python where_is_kappa.py
```

| 脚本 | 内容 | 关键校验点 |
| :-- | :-- | :-- |
| `demo_gongli2_bridge.py` | 时间-1 映射；阻尼 δ（保守↔耗散） | φ₁(θᵢ)=θ_{R(i)}；自由能 F 单调降；δ=0 守恒、δ>0 耗散 |
| `demo_circle_dissipation.py` | 拓扑障碍 H¹(S¹)=ℝ；Kuramoto / Stuart-Landau | Kuramoto 锁相约 30° |
| `verify_wuxing_phase.py` | 五行相位检验 | 生/克/侮/及母=R¹..R⁴；生∪克=K₅；特征值单位圆、det=+1 |
| `assemble_wuxing_interoception.py` | 组装 κz̄⁴ + 五次饱和 | 仅 κ 项发散；配饱和后锁相，距 72° 倍数随 κ 而定（κ=2 约 1.4°、κ=4 约 0.1°） |
| `where_is_kappa.py` | κ 把 U(1) 破缺到 Z₅ | κ=0 全 U(1) 等变；κ≠0 只 Z₅ 等变 |

## 第二轮：桥 · 组装（2026-09-30）

配套三篇新笔记（“缺口 = W → 组装成 C → 朗兰兹接桥”）：

| 脚本 | 配套文档 | 核验内容 | 依赖 |
| :-- | :-- | :-- | :-- |
| `verify_three_instances_gap.py` | [统一性检验（缺口是不是 W）](../../notes/axiom_II_bridge_gap_W.md) | 五行（相生=矢势型、无耗散）；朗兰兹（显式公式=等式、局部积发散） | numpy + mpmath |
| `assemble_bridge_C.py` | [组装（内感受幅度×五行相位）](../../notes/axiom_II_bridge_assembly_C.md) | 2×2 分解定理 / 生成元 / 三态 / 不免费 / Z₅ 钉相 | numpy + scipy |
| `langlands_into_the_bridge.py` | [朗兰兹接桥](../../notes/axiom_II_bridge_langlands.md) | 极限环 / 零点相位谱 / 显式公式 / 局部积发散 | numpy + mpmath |

```bash
python verify_three_instances_gap.py
python assemble_bridge_C.py
python langlands_into_the_bridge.py
```

## 诚实边界

- 「五行 = 相位」通过，但判别力只来自「生/克互补」；「互补是发现的还是定义的」未定。
- 组装是存在性（一个可行组装），非唯一/必然；耦合是选的，不是推的。
- 「离散性 = 公理 III」是分类判断，不是定理。