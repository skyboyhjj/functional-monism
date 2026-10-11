"""公理 III（精度）侦察线：先算后说

主命题候选：精度 = 一族"精度商" Π_ε : X → X_ε（粗粒化 / 连续→有限）。

验证三个触点（两个已知 + 一个自检）：
1. p 进精度：Z_p → Z/p^n（n=精度），精度↑ 分辨↑。
2. κ 相位精度：S^1 → 5 相位（κ=精度强度），κ↑ 势阱↑。
3. 精度 = 信息量：H(Π_N) = log2 N；粗粒化免费、细化不免费（同型缺口）。
"""
import numpy as np

print("=" * 72)
print("1. p 进精度：Z_p → Z/p^n，精度↑ 分辨↑")
print("=" * 72)
for p, n in [(5, 1), (5, 2), (5, 3), (2, 3)]:
    res = p ** n
    print(f"  p={p}, n={n}: 分辨 mod {res}, 信息 {np.log2(res):.2f} bits, "
          f"最小可辨距离 p^-n={p ** -n:.2e}")

print()
print("=" * 72)
print("2. κ 相位精度：S^1 → 5 相位（κ = 精度强度）")
print("=" * 72)
for kappa in (0.0, 1.0, 3.0):
    tag = "无 5 结构（连续）" if kappa == 0 else ("锁相（离散 5 相位）" if kappa > 1 else "临界")
    print(f"  κ={kappa}: 势阱深度 ∝ κ = {kappa:.1f}, {tag}")
print("  ⟹ 精度商 S^1 → Z_5 的强度 = κ（承接「公理II续5」）。")

print()
print("=" * 72)
print("3. 精度 = 信息量；粗粒化免费、细化不免费")
print("=" * 72)
def Pi(x, N):
    return np.floor(x * N) / N            # 粗粒化到 N 格
for N in (2, 8, 64):
    print(f"  N={N}: 粗粒化后熵 H = log2 N = {np.log2(N):.1f} bits")
coarse = Pi(0.37, 2)                       # = 0.0
cands = sorted({Pi(x, 4) for x in np.linspace(0, 1, 9) if Pi(x, 2) == coarse})
print(f"  粗块 {coarse} 可来自细块（N=4）: {cands}  共 {len(cands)} 个（>1 ⟹ 细化不唯一）")
print("  ⟹ 粗粒化（X→X_ε）确定、免费；细化（X_ε→X）多对一、不免费。")

print()
print("=" * 72)
print("结论")
print("=" * 72)
print("  精度 = 一族精度商 Π_ε: X→X_ε（连续→有限），由精度参数 ε 控制。")
print("  p 进（ε=p^-n）与 κ（ε↔1/κ）都是它的实例 ⟹ 公理 III 的候选统一形式。")
print("  精度↑ = 信息↑ = 分辨↑；粗粒化免费、细化不免费（又一同型缺口）。")
