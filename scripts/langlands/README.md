# 朗兰兹纲领 · 验证脚本

支撑 [langlands_program_unification.md](../../notes/langlands_program_unification.md) 数值结论的 16 个独立单文件脚本。

## 怎么跑

全部为独立单文件 Python 脚本，无网络、无需 Sage/Magma；直接运行：

```bash
python demo_xxx.py
```

每个脚本自打印结论，无需输入参数（阈值/曲线表硬编码在文件内）。

## 依赖

仅需标准库或 `numpy` / `mpmath`：`pip install numpy mpmath`。

## 对照表

| 脚本 | 算什么 | 依赖 |
| :-- | :-- | :-- |
| `demo.py` | 显式公式「两本账」（von Mangoldt 求和 vs 零点求和）+ Weil 二次型结构 | mpmath |
| `demo2.py` | 显式公式两本账（ψ 算术侧 vs 谱侧，高精度） | mpmath |
| `demo_evidence.py` | theta 函数方程、Burnside/Pólya 计数、Gauss 和 | mpmath |
| `demo_ihara.py` | Ihara zeta 的「RH」⟺ Ramanujan 图（正例/负例） | numpy |
| `demo_ff.py` | 函数域：曲线 RH（α 模长 = √p）+ 两本账 | 标准库 |
| `demo_genus.py` | 亏格：P¹ 亏格 0 ⟹ RH 真空；椭圆曲线 α 模长 = √p | 标准库 |
| `demo_frob.py` | Frobenius 在哪些对象上非平凡（Freshman's Dream、Witt、Λ-结构） | numpy |
| `demo_frob_symbol.py` | K=ℚ(i)：Frobenius 符号 = 分裂行为 = p=a²+b² | 标准库 |
| `demo_tate.py` | Tate 曲线 j-不变量（模数 q=p^{-1}） | mpmath |
| `demo_phi.py` | B^{φ=p} 的「序」：弱可容许 + 交错型恒不定号 | numpy |
| `demo_positivity.py` | 「定号」形态：自卷积 ⟹ 正定核、screw 核、交错型对照 | numpy |
| `demo_tp.py` | 「序 ⟹ 定号」（路 b）：Toeplitz 核全正、Pólya 定理 | numpy + mpmath |
| `demo_R.py` | R 失败记录 0/6：谱密度建在素数测度上 | numpy + mpmath |
| `demo_R_success.py` | R 修正版 10/10：对象建在 ψ(e^t)−e^t 上，谱峰落在 ζ 零点处（数值） | numpy |
| `demo_R2.py` | R2：函数域 91/91 + 数域矩 Σγ^{2n} 发散 | numpy + mpmath |
| `demo_axiomII.py` | 公理 II：Θ=log Frobenius 谱落在 Re=½log q（107/107） | numpy |
