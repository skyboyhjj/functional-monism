"""公理 III 侦察线 · S4：检验候选「正性 = 精度极限」

两个事实：
(A) 正性（PSD）对极限【封闭】：有限 PSD → 极限 PSD。
    ⟹ 若存在「精度极限」，正性必免费——缺口不可能出在「极限处的正性」。
(B) semilocal 测度在加 places 时【发散】：μ_S(0)=∏_{p≤P}(1-p^{-1/2})^{-2} → ∞。
    ⟹ 【不存在「精度极限」】——semilocal 不是 global 的「有限精度影子」。

结论：候选「正性 = 精度极限」【不成立】（被证伪）。
      真缺口 = 「无整体对象」⟹ 公理 III（精度结构）在算术情形【缺失】。
"""
import numpy as np

print("=" * 72)
print("(A) 正性对极限封闭：一列 PSD → 极限 PSD")
print("=" * 72)
for n in (2, 5, 100):
    a = 1 - 1 / n
    ev = np.linalg.eigvalsh(np.array([[1, a], [a, 1]]))
    print(f"  n={n}: 特征值 {np.round(ev, 4)}  PSD? {bool((ev >= -1e-12).all())}")
print("  ⟹ x'A_n x >= 0 → x'A_∞ x >= 0。PSD 对极限封闭（所以若有极限，正性免费）。")

print()
print("=" * 72)
print("(B) semilocal 测度加 places 时发散：不存在「精度极限」")
print("=" * 72)
def primes_upto(N):
    s = np.ones(N + 1, bool); s[:2] = False
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]
for P in (10, 100, 1000, 10000, 100000, 1000000):
    ps = primes_upto(P)
    logmu = -2 * np.sum(np.log(1 - 1 / np.sqrt(ps)))
    print(f"  P={P:>8}: μ_S(0) = ∏(1-p^-1/2)^-2 = {np.exp(logmu):.3e}  "
          f"(log10 = {logmu / np.log(10):.1f})")
print("  ⟹ μ_S(0) 随 P 发散 ⟹ 无极限测度 ⟹ 无「精度极限」（semilocal 不是 global 的截断）。")

print()
print("=" * 72)
print("结论")
print("=" * 72)
print("  (A) 正性对极限封闭  ⟹ 缺口不可能出在「极限处的正性」。")
print("  (B) semilocal 测度发散 ⟹ 根本【没有「精度极限」】。")
print("  ⟹ 候选「正性 = 精度极限」不成立（证伪）。")
print("  真缺口 = 「无整体对象」：semilocal 不是 global 的精度截断")
print("         ⟹ 公理 III（精度结构）在算术情形【缺失】。")
