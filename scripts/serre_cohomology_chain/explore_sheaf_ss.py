#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""explore_sheaf_ss.py

核验「层上同调 / 谱序列」到底怎样把【局部】拼成【整体】——为《层上同调 <-> 构造层缺口》提供算据。

三验（全部只用整数秩，纯 Python，无依赖）：
  A. Leray 谱序列：Hopf 纤维化  S^1 -> S^3 -> S^2
     由「底 S^2 的上同调 + 纤维 S^1 的上同调 + 一个 d_2 微分」拼出 H*(S^3) = (1,0,0,1)。
     —— 这就是『先搭平台、逐级升高、层层逼近整体』的精确内容。
  B. 对照：平凡积 S^1 x S^2 的谱序列在 E_2 退化（无微分），H* = H*(S^2) (x) H*(S^1) = (1,1,1,1)。
     —— 有没有那一个微分，决定整体上同调是不是「底与纤维的张量积」。
  C. Serre / Poincare 对偶的「两本账」：Betti 数回文  h^i = h^{n-i}。
     例：P^2、亏格 2 曲线、P^1 x P^1、K3 曲面。

运行：python3 explore_sheaf_ss.py
"""
from itertools import product


def show(name, betti):
    print(f"  {name}: " + ",".join(str(b) for b in betti))


def check(cond, msg):
    print(("  ✓ " if cond else "  ✗ ") + msg)
    return cond


# ---------------------------------------------------------------- 谱序列引擎
class LeraySS:
    """E_2^{p,q} = H^p(base; H^q(fiber))；只记自由秩。"""

    def __init__(self, base_betti, fiber_betti, name):
        self.base = base_betti                      # H^p(base)
        self.fiber = fiber_betti                    # H^q(fiber)
        self.name = name
        # E2[p][q] = 秩
        self.E = {}
        for p, bp in enumerate(base_betti):
            for q, fq in enumerate(fiber_betti):
                if bp and fq:
                    self.E[(p, q)] = bp * fq

    def e2_table(self):
        ps = range(len(self.base))
        qs = range(len(self.fiber))
        return {p: {q: self.E.get((p, q), 0) for q in qs} for p in ps}

    def apply_d2_iso(self, p, q):
        """d_2: E_2^{p,q} -> E_2^{p+2,q-1} 是同构（Hopf 情形的欧拉类为生成元）。"""
        src, dst = (p, q), (p + 2, q - 1)
        r = self.E.get(src, 0)
        assert r == self.E.get(dst, 0) == 1, "本演示只处理秩 1 的同构微分"
        self.E.pop(src)                             # ker(d_2)=0
        self.E.pop(dst)                             # coker(d_2)=0
        return r

    def totals(self, nmax):
        """E_inf 的对角线和 -> 整体上同调的自由秩。"""
        return [sum(v for (p, q), v in self.E.items() if p + q == k) for k in range(nmax)]


def main():
    ok = True

    print("=== A. Leray 谱序列：Hopf 纤维化 S^1 -> S^3 -> S^2 ===")
    SS = LeraySS(base_betti=[1, 0, 1], fiber_betti=[1, 1], name="hopf")
    print("  E_2 表 (行 p=0,1,2 ; 列 q=0,1):")
    for p in range(3):
        print(f"    p={p}: " + str([SS.E.get((p, q), 0) for q in range(2)]))
    print("  非零格: " + str(sorted(SS.E.keys())))
    SS.apply_d2_iso(0, 1)                           # 关键的那一个微分
    Hs3 = SS.totals(4)
    show("H*(S^3) 由谱序列拼出", Hs3)
    ok &= check(Hs3 == [1, 0, 0, 1], "与已知 H*(S^3) = (1,0,0,1) 一致")

    print("\n=== B. 对照：平凡积 S^1 x S^2（E_2 退化，无微分）===")
    P = LeraySS(base_betti=[1, 0, 1], fiber_betti=[1, 1], name="product")
    Hs_prod = P.totals(4)
    show("H*(S^1 x S^2)", Hs_prod)
    ok &= check(Hs_prod == [1, 1, 1, 1], "= H*(S^2) (x) H*(S^1) = (1,1,1,1)")
    print("  ⟹ 同一个底、同一个纤维：差别只在【有没有那一个 d_2】。")

    print("\n=== C. Serre / Poincare 对偶的『两本账』：Betti 数回文 h^i = h^{n-i} ===")
    cases = {
        "P^2           (n=4)": [1, 0, 1, 0, 1],
        "亏格 2 曲线    (n=2)": [1, 4, 1],
        "P^1 x P^1     (n=4)": [1, 0, 2, 0, 1],
        "K3 曲面       (n=4)": [1, 0, 22, 0, 1],
    }
    for name, b in cases.items():
        n = len(b) - 1
        show(name, b)
        ok &= check(b == b[::-1], f"{name} 回文（h^i = h^{{n-i}}）")

    print("\n=== 结论 ===")
    print("  A ✓ 一个 d_2 微分，把『底⊗纤维』修正成 S^3 的真实上同调")
    print("  B ✓ 有无该微分，决定整体上同调 = 张量积（退化） 还是被『扭曲』")
    print("  C ✓ 对偶把上同调配成两列『回文』——同一组数，两种读法（正/反）")
    print("  ⟹ 层上同调/谱序列 = 『局部 -> 整体』的标准机器；对偶 = 『两本账』的原型。")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
