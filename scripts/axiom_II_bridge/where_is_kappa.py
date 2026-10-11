"""κ 从哪来？—— 耦合项的结构来源

核心线索：κ z̄⁴ 把 U(1)（连续相位）破缺到 Z_5（离散相位）。
⟹ κ = 离散性进入连续演化的强度。而离散性 = 公理 III（精度）。
   κ=0 五行 5 相位消失（纯连续）；κ>0 离散性打开（5 相位出现）。

三步：
1. U(1) 等变性检验：κ=0 对【任意】α 等变（连续对称）；
   κ≠0 只对 α=2πk/5 等变（破缺到 Z_5，离散对称）。
2. κ 控制 5 个势阱的深度（五行 5 相位的开关）。
3. 结论：κ 是离散性的开关，形式（5 次）来自五行有 5 个元素，
   其不能在公理 II 内部推出 ⟹ 来自公理 III（精度）。
"""
import numpy as np

print("=" * 72)
print("1. U(1) 等变性：κ z̄⁴ 把 U(1) 破缺到 Z_5")
print("=" * 72)
def f(z, mu=1.0, omega=1.0, kappa=0.0):
    return (mu + 1j * omega) * z - abs(z) ** 2 * z + kappa * np.conj(z) ** 4
z0 = 0.7 + 0.3j
def equivariant(alpha, kappa):
    z = z0
    return abs(f(np.exp(1j * alpha) * z, kappa=kappa)
               - np.exp(1j * alpha) * f(z, kappa=kappa)) < 1e-9
for kappa in (0.0, 1.0):
    gen = equivariant(0.9, kappa)            # 一般角度（非 2πk/5）
    z5 = equivariant(2 * np.pi / 5, kappa)   # 72°
    print(f"  κ={kappa}: 一般 α=0.9rad 等变? {gen}   α=2π/5 等变? {z5}")
print("  ⟹ κ=0 全 U(1) 等变（连续）；κ≠0 只剩 Z_5 等变（离散）。")

print()
print("=" * 72)
print("2. κ 控制 5 个势阱深度（五行 5 相位的开关）")
print("=" * 72)
omega = 1.0
for kappa in (0.0, 1.0, 3.0):
    depth = kappa * 1.0 ** 3                  # 势阱深度 ∝ κ r³
    tag = "锁相（5 相位出现）" if depth > omega else "不锁相（无 5 结构）"
    print(f"  κ={kappa}: 势阱深度 ∝ κr³ = {depth:.1f}, 阈值 ω={omega} ⟹ {tag}")
print("  ⟹ κ=0 五行 5 相位「消失」（纯连续旋转）；κ>0 出现 5 势阱，κ 大则深。")

print()
print("=" * 72)
print("3. 三层来源（嵌套，不是竞争）")
print("=" * 72)
print("  表层：κ = 相位(五行)与幅度(内感受)的耦合强度。")
print("  中层：κ z̄⁴ 的【形式】(Z_5，5 次) 来自「五行有 5 个元素」（最低阶等变项）。")
print("  深层：κ z̄⁴ 把 U(1) 破缺到 Z_5 ⟹ κ 是【离散性】的作用强度。")
print("        离散性 = 公理 III（精度）⟹ κ 不能在公理 II 内部推出。")

print()
print("=" * 72)
print("结论")
print("=" * 72)
print("  κ 不是「从哪来」能自洽推出的——它恰恰是【离散性（公理 III）】")
print("  进入【连续演化（公理 II）】的接口：κ=0 纯连续（五行消失），")
print("  κ>0 离散性打开（五行 5 相位出现）。")
print("  ⟹ 「公理 II 的桥」要搭起来，必须借「公理 III」——而公理 III 长期空白。")
