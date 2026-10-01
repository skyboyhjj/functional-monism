# 局部 → 整体 · 示性类 · 验证脚本

支撑 [local_global_characteristic_classes.md](../../notes/topics/local_global_characteristic_classes.md) 数值结论的 6 个独立单文件脚本，均为「先算后说」——运行即打印结论，无需输入参数。

## 怎么跑

```bash
python verify_fiber_bundle.py        # §1 纤维丛教科书核验
python verify_euler_obstruction.py   # §2 欧拉类只是「初级」障碍
python verify_monopole_bundle.py     # §3 莫比乌斯 → 磁单极
python verify_wuyang_patch.py        # §4 Wu–Yang 两补丁 = 转移函数的对数微分
python verify_section3_remaining.py  # §5 剩余三条核验（含夹具校验）
python explore_gongli3_h1_integral.py  # §6 整数化 · 度数版
```

## 依赖

6 份脚本均**零第三方依赖**——仅用 Python 标准库 `math` / `cmath` / `fractions` / `itertools`。

## 对照表

| 脚本 | 支撑章节 | 验证内容 |
| :-- | :-- | :-- |
| `verify_fiber_bundle.py` | §1、§3 | A 实线丛 $`\mathbb Z_2`$ 分类；B Hopf 丛绕数 = ±1 ⟹ $`c_1\neq0`$；C 和乐单值 ⟺ 整数；D 欧拉类与 $`\chi`$ |
| `verify_euler_obstruction.py` | §2 | A 障碍分级表；B $`\pi_3(S^2)=\mathbb Z`$（Hopf 不变量 = 环绕数 = 1.0000）；C 秩 2 特殊性 |
| `verify_monopole_bundle.py` | §3 | 任意纤维对环绕数 = ±1；绕数 = 陈数；$`\chi`$ 与截面 |
| `verify_wuyang_patch.py` | §4 | A 差为纯规范、同一曲率；B 差/转移函数绕数同；C ℝ-级多值；D $`\int F=2\pi c`$；E $`\mathbb Z_2`$ 和乐 |
| `verify_section3_remaining.py` | §5 | 夹具（Hopf 链）；环绕数随分辨率收敛；投影符号随定向翻转；四名字对照（和乐/2π 差因子 2）；Berry 两级 |
| `explore_gongli3_h1_integral.py` | §6 | A 度数 = 绕数 = $`sL/2\pi`$；B 两级（ℝ-级 / ℤ-级）；C 可离散化 ⟺ 旋转数有理；D `06` 范例 |

## 诚实边界

- 6 份脚本验证的是**周边可算事实**（$`\mathbb Z_2`$ 分类、环绕数、Hopf 不变量、绕数 = 陈数、和乐/2π 差因子 2、旋转数有理 ⟹ 闭），**不是**「示性类 ⟹ RH」。
- 「示性类 ↔ site 上同调」「cocycle 条件 ↔ 共格」「Weil 正性 ↔ RH 判据量」是**结构性对位**，**不是**等价（与 `09-并账检验` 纪律一致）。

## 复现

```bash
python scripts/local_global_characteristic_classes/verify_fiber_bundle.py
python scripts/local_global_characteristic_classes/verify_euler_obstruction.py
python scripts/local_global_characteristic_classes/verify_monopole_bundle.py
python scripts/local_global_characteristic_classes/verify_wuyang_patch.py
python scripts/local_global_characteristic_classes/verify_section3_remaining.py
python scripts/local_global_characteristic_classes/explore_gongli3_h1_integral.py
```