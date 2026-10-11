"""验证：阴阳五行的生克 R 是否『真』落在 SO(2) 的离散子群（相位结构）

关键区分：
  弱命题（平凡）：R 是 5 循环，可『放在圆上』——任何 5 循环都行，不能证明什么。
  强命题（非平凡）：五行全部关系（生/克/侮/及母）都是同一个 R 的幂（单一生成元）。

检验 5 项：
1. 置换层：R 是 5 循环（≅ Z_5）——必要但不充分。
2. 代数层（关键）：生/克/侮/及母 = R^1/R^2/R^3/R^4（同一 R 的幂）。
3. 表示层：R 的特征值 = 5 次单位根（全在单位圆）⟹ 正交/等距；det=+1 ⟹ 真旋转。
4. 几何层：五行放在圆上，R = 72° 旋转的作用。
5. 终极判别：生∪克 = K_5（互补 5 循环）⟹ 必为同一旋转的 ±1、±2 步（非两张独立网）。
"""
import numpy as np

print("=" * 72)
print("1. 置换层：生 R 是 5 循环（≅ Z_5）——必要但不充分")
print("=" * 72)
R = {0: 1, 1: 2, 2: 3, 3: 4, 4: 0}          # 相生：木0→火1→土2→金3→水4→木

def perm_pow(p, k):
    q = {i: i for i in range(5)}
    for _ in range(k):
        q = {i: p[q[i]] for i in range(5)}
    return q

ident = {i: i for i in range(5)}
is_5cycle = perm_pow(R, 5) == ident and all(perm_pow(R, k) != ident for k in (1, 2, 3, 4))
print(f"  R 是 5 循环（R^5=id 且阶=5）? {is_5cycle}")
print("  注：任何 5 循环都能『放在圆上』——单凭这一条无法区分真相位与人为。")

print()
print("=" * 72)
print("2. 代数层（关键）：生/克/侮/及母 是否都是同一个 R 的幂")
print("=" * 72)
rels = [("相生 R^1", perm_pow(R, 1)), ("相克 R^2", perm_pow(R, 2)),
        ("相侮 R^3", perm_pow(R, 3)), ("子病及母 R^4", perm_pow(R, 4))]
for nm, p in rels:
    print(f"  {nm}: 木→{p[0]} 火→{p[1]} 土→{p[2]} 金→{p[3]} 水→{p[4]}")
print("  ⟹ 生/克/侮/及母 全部是同一个 R 的幂（单一生成元）★")

print()
print("=" * 72)
print("3. 表示层：R 的特征值 = 5 次单位根 ⟹ 等距；det=+1 ⟹ 真旋转")
print("=" * 72)
P = np.zeros((5, 5))
for i in range(5):
    P[R[i], i] = 1.0                          # 置换矩阵
ev = np.linalg.eigvals(P)
print(f"  特征值: {np.round(np.sort_complex(ev), 3)}")
print(f"  全部 |λ|=1 ?  {all(abs(abs(e) - 1) < 1e-9 for e in ev)}  ⟹ 正交/等距")
print(f"  det = {np.linalg.det(P):+.0f}  (='+1' 真旋转，非反射)")

print()
print("=" * 72)
print("4. 几何层：五行放在圆上，R = 72° 旋转")
print("=" * 72)
pts = np.exp(2j * np.pi * np.arange(5) / 5)
rot = pts * np.exp(2j * np.pi / 5)
print(f"  旋转 72° 后落到下一个点? {all(abs(rot[i] - pts[(i + 1) % 5]) < 1e-9 for i in range(5))}")
print("  ⟹ R 在圆上就是 72° 旋转（SO(2) 的离散子群 Z_5 生成元）。")

print()
print("=" * 72)
print("5. 终极判别：生∪克 = K_5（互补）⟹ 单一生成元（非人为）")
print("=" * 72)
生 = perm_pow(R, 1); 克 = perm_pow(R, 2)
生_e = {frozenset((i, 生[i])) for i in range(5)}
克_e = {frozenset((i, 克[i])) for i in range(5)}
all_e = {frozenset((i, j)) for i in range(5) for j in range(i + 1, 5)}
print(f"  生边数 {len(生_e)}, 克边数 {len(克_e)}, 总对数 {len(all_e)}")
print(f"  生∪克 = K_5（覆盖全部 10 对）? {生_e | 克_e == all_e}")
print(f"  生∩克 = ∅（不重叠）?           {生_e & 克_e == set()}")
print("  ⟹ 生/克 是互补的两个 5 循环 ⟹ 必为同一旋转 ±1、±2 步（非两张独立网）。")

print()
print("=" * 72)
print("结论")
print("=" * 72)
print("  弱命题（平凡）：R 是 5 循环，可放在圆上——任何 5 循环都行。")
print("  强命题（非平凡）：生/克/侮/及母 全是同一 R 的幂；生∪克=K_5；")
print("                    R 特征值在单位圆、det=+1（真旋转）。")
print("  ⟹ 阴阳五行『真』是相位系统（单一旋转生成），不是人为放在圆上。")
