"""公理 II 的桥：离散演化(阴阳五行) 与 连续演化(内感受) 之间缺的到底是什么

先算后说，分四步：
1. 阴阳五行生克 R = 圆上 72° 旋转 = 连续流 φ_t(θ)=θ+72°t 的时间-1 映射
   ⟹ 离散↔连续的桥 = 时间-1 映射（成熟、通用）。
2. 圆旋转 θ'=ω 不是梯度流（无全局势）⟹ 它是『保守/等距』演化。
3. 内感受自由能梯度流 s'=-∇F 是『耗散』演化（F 单调降）。
4. 保守↔耗散的桥 = 阻尼 γ（谐振子演示：γ=0 保守，γ>0 耗散）。

结论：公理 II 真正的缺口不是『离散↔连续』（时间-1 映射成熟），而是『保守↔耗散』。
"""
import numpy as np

print("=" * 72)
print("1. 阴阳五行生克 R = 圆上 72° 旋转 = 连续流的时间-1 映射")
print("=" * 72)
R = lambda i: (i + 1) % 5                       # 相生：木0火1土2金3水4
def phi(t, theta):
    return (theta + np.deg2rad(72) * t) % (2 * np.pi)   # 连续旋转流
ok = all(abs(np.rad2deg(phi(1, np.deg2rad(72 * i))) % 360 - 72 * R(i)) < 1e-6
         for i in range(5))
print(f"  φ_1(θ_i) = θ_(R(i))  ?  {ok}")
print("  ⟹ 离散生克 R 嵌入连续旋转流；桥(离散↔连续) = 时间-1 映射 f = φ_1，机制成熟通用。")

print()
print("=" * 72)
print("2. 圆旋转 θ'=ω 不是梯度流（无全局势）⟹ 保守演化")
print("=" * 72)
omega = 1.0
F = lambda th: -omega * th            # 若 θ'=-F'=ω，则 F=-ωθ+C
print(f"  F(2π)-F(0) = {F(2*np.pi)-F(0):.3f} ≠ 0  ⟹ F 在圆上不单值")
print("  ⟹ 圆旋转无全局势，不是梯度流；是『保守/等距』演化（可逆、无耗散）。")

print()
print("=" * 72)
print("3. 内感受自由能梯度流 s'=-∇F 是『耗散』演化")
print("=" * 72)
def grad_flow(s0, dt=0.05, steps=80):
    s, Fs, ss = s0, [s0 * s0 / 2], [s0]
    for _ in range(steps):
        s = s - dt * s          # s' = -s（F=s²/2 的梯度流）
        ss.append(s); Fs.append(s * s / 2)
    return np.array(ss), np.array(Fs)
ss, Fs = grad_flow(3.0)
print(f"  s: {ss[0]:+.2f} -> {ss[-1]:+.4f}（趋向内稳态 0）")
print(f"  F: {Fs[0]:+.2f} -> {Fs[-1]:+.6f}（单调下降 = 耗散、不可逆）")

print()
print("=" * 72)
print("4. 保守 ↔ 耗散的桥 = 阻尼 γ（谐振子：x'' = -x - γx'）")
print("=" * 72)
def osc(gamma, x0=1.0, v0=0.0, dt=0.02, steps=1500):
    x, v, E = x0, v0, []
    for _ in range(steps):
        v = v + dt * (-x - gamma * v)   # 辛欧拉：先 v（用旧 x），保能量
        x = x + dt * v                  # 后 x（用新 v）
        E.append(0.5 * (v * v + x * x))
    return np.array(E)
for gamma in (0.0, 0.1):
    E = osc(gamma)
    print(f"  γ={gamma}: 能量 E 首尾 {E[0]:.4f} -> {E[-1]:.4f}  "
          f"({'守恒(振荡)' if E[-1] > 0.5 * E[0] else '耗散(衰减)'})")
print("  ⟹ γ=0 保守(等距可逆)，γ>0 耗散(吸引子不可逆)；桥 = 阻尼 γ。")

print()
print("=" * 72)
print("结论")
print("=" * 72)
print("  离散↔连续 : 时间-1 映射（φ_1=R）——成熟、通用、两边都成立。")
print("  保守↔耗散 : 圆旋转(无势、可逆) vs 梯度流(有势、不可逆)——不是同一种演化。")
print("  ⟹ 公理 II 真正的缺口不是『离散↔连续』，而是『保守↔耗散』。")
