# Serre 上同调链 · 验证脚本

支撑 [serre_sheaf_cohomology_zeta.md](../../notes/topics/serre_sheaf_cohomology_zeta.md) 数值结论的 4 个独立单文件脚本，均为「先算后说」——运行即打印结论，无需输入参数。

## 怎么跑

```bash
python explore_local_vs_global.py   # §1 断点澄清
python explore_connes_path.py       # §2 Connes 路线
python explore_sheaf_ss.py          # §4 层上同调接口
python verify_scaling_site.py       # §5 Scaling Site 核查
```

## 依赖

- `explore_local_vs_global.py`、`explore_connes_path.py` 依赖 `mpmath`：`pip install mpmath`
- `explore_sheaf_ss.py`、`verify_scaling_site.py` 仅用标准库（纯 Python、无第三方依赖）

## 对照表

| 脚本 | 支撑章节 | 验证内容 | 依赖 |
| :-- | :-- | :-- | :-- |
| `explore_local_vs_global.py` | §1 断点性质澄清 | A 有限域零点直读（`|T|=1/√p`）；B 数域 300 个 ζ 零点的幂和爆炸（Newton 无从启动） | mpmath |
| `explore_connes_path.py` | §2 Connes 路线 | ① Δ=H(1+H) 谱全负实（临界零点）；①' 非临界零点谱虚部≠0；② ζ-cycle 圆长 2π/s；③ Σ_μ 尺度不变性 | mpmath |
| `explore_sheaf_ss.py` | §4 层上同调接口 | A Hopf 谱序列拼出 H\*(S³)；B 平凡积退化对照；C Serre/Poincaré 对偶回文 | 标准库 |
| `verify_scaling_site.py` | §5 Scaling Site 核查 | A 圆长 2π/s 整数倍（特征标下降）；B theta 恒等式；C 覆盖稳定性 | 标准库 |

## 诚实边界

- 4 份脚本验证的是**周边可算事实**（幂和发散、谱实性映射、圆长、theta 恒等式、对偶回文），**不是**「层上同调 ⟹ RH」。
- Scaling Site 的**真正的谱实现（Theorem 1.2 / 5.4）在文献里，本目录脚本不重证**（见 [verify_scaling_site.py](./verify_scaling_site.py) 末尾提示）。
- `explore_local_vs_global.py` 中 `mpmath.polyroots([p, -a, 1])` 按**降幂**读数（经输出验证 `|T|=1/√p` 正确）。

## 复现

```bash
python scripts/serre_cohomology_chain/explore_local_vs_global.py
python scripts/serre_cohomology_chain/explore_connes_path.py
python scripts/serre_cohomology_chain/explore_sheaf_ss.py
python scripts/serre_cohomology_chain/verify_scaling_site.py
```