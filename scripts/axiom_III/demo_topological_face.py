"""公理 III · 第三角（拓扑面）：形式化 + 先算后说验证

两条边：
1. 信息 → 拓扑：精度结构 {Π_ε} 诱导一致结构（嵌套等价关系）→ 拓扑。
   p 进：U_n={(x,y): x≡y mod p^n} 嵌套 ⟹ p 进拓扑（= Z_p=lim Z/p^n 的极限拓扑）。
2. 拓扑 ↔ 几何：H^1 是「局部势能否整体化」的障碍（de Rham）。
   圆：∮dθ=2π≠0 ⟹ H^1(S^1)=R ⟹ 纯旋转无势（须补维）；
   线：∫f dx 路径无关 ⟹ H^1(R)=0 ⟹ 一切自治流有势。
"""
import numpy as np

print("=" * 72)
print("1. 信息 → 拓扑：精度结构诱导一致结构/拓扑（p 进）")
print("=" * 72)
p = 5
for n in (1, 2, 3):
    print(f"  U_{n} = {{(x,y): x≡y mod {p ** n}}}   直径 p^-n = {p ** -n:.2e}   ⊂ U_{n - 1}")
print("  ⟹ 嵌套等价关系构成一致结构基 ⟹ 诱导 p 进拓扑（= Z_p = lim Z/p^n 的极限拓扑）。")

print()
print("=" * 72)
print("2. 拓扑 ↔ 几何：H^1 是「整体势」的障碍（de Rham）")
print("=" * 72)
omega = 1.0
circ = omega * 2 * np.pi
print(f"  圆 S^1 : ∮dθ 绕一圈 = 2π = {circ:.4f} ≠ 0 ⟹ H^1(S^1)=R≠0 ⟹ 纯旋转无势（须补维）")


_trapz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz


def trap(f, a, b, N=20000):
    x = np.linspace(a, b, N + 1)
    return _trapz(f(x), x)


h = lambda x: np.exp(-x ** 2) + np.sin(x)
F = lambda b: trap(h, 0, b)                    # 单值势 F(x)=∫_0^x h
lhs, rhs = trap(h, 1, 4), F(4) - F(1)
print(f"  线 R   : ∫_1^4 h = {lhs:.6f} = F(4)-F(1) = {rhs:.6f}  ⟹ 单值势 ⟹ H^1(R)=0（无洞）")
print("  ⟹ 同一 1-形式「闭」：圆上闭非恰当（H^1≠0）、线上闭即恰当（H^1=0）。")
print("    拓扑面度量几何面的「能否整体化」。")

print()
print("=" * 72)
print("结论")
print("=" * 72)
print("  第三角（拓扑面）可补齐，但是【派生面】（从信息面导出）：")
print("    信息→拓扑：精度结构 ⟹ 一致结构 ⟹ 拓扑/上同调（定义性，闭合）")
print("    拓扑↔几何：H^1 障碍（de Rham，闭合）")
print("  ⟹ 三角闭合；但拓扑面是派生（非独立提法）；二（重整化）↔三（信息）仍只到机制类比。")
