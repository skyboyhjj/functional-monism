# 朱载堉十二律 · 验证脚本

支撑本侦察链全部数值结论的**独立单文件脚本**，无网络、仅标准库。

## 怎么跑

```bash
# 逐个
python3 demo_twelve_tone.py

# 一次跑全套（逐条）
for f in demo_*.py; do python3 "$f"; echo; done
```

每个脚本自打印结论，无需输入参数。

## 一、逐条脚本（SOP S8）

| 脚本 | 算什么 | 对应结论 | 分级 |
| :-- | :-- | :-- | :-- |
| `demo_gougu_pi.py` | 勾股律管 10√2 / 5√2；π 密率 355/113 | 读解 §二 | 半严格（数值） |
| `demo_twelve_tone.py` | 十二律比 2^(n/12)、群结构 ℤ₁₂、单一生成元 | 十二律的一元形态 | 严格 |
| `demo_two_books.py` | 离散递推 = 连续螺旋整点采样 | 离散与连续的两本账 | 严格 |
| `demo_why_twelve.py` | log2(3/2) 连分数逼近 → "12" | 常数耦合的核查 §三 | 严格 |
| `demo_phi_refute.py` | φ / 斐波那契不"耦合"（**证伪记录**） | 常数耦合的核查 §二 | 严格否定 |
| `demo_pythagorean_comma.py` | 毕氏音差：三分损益 12 步 23.46 音分 | 常数耦合的核查 §2.3 | 严格 |

## 二、综合脚本（早期版本，保留）

| 脚本 | 作用 |
| :-- | :-- |
| `check.py` | 原文算例复算（含 K 常数 = 2^(1/6)、螺旋公式笔误核对） |
| `verify.py` | 侦察链全套复算（A–F 段：结构 / 两本账 / 连分数 / φ / 毕氏音差 / 五声） |

> `demo_*.py` 是 `verify.py` 的**逐条拆分**；`verify.py` 保留作"一次跑完"的入口。

## 三、与文档的对应

| 脚本 | 支撑文档 | 分级 |
| :-- | :-- | :-- |
| `demo_gougu_pi.py` | 读解 §二 | 半严格（数值） |
| `demo_twelve_tone.py` | `zhuzaiyu_structure.md` | 严格 |
| `demo_two_books.py` | `zhuzaiyu_two_books.md` | 严格 |
| `demo_why_twelve.py` | `zhuzaiyu_constant_check.md` §三 | 严格 |
| `demo_phi_refute.py` | `zhuzaiyu_constant_check.md` §二 | 严格否定 |
| `demo_pythagorean_comma.py` | `zhuzaiyu_constant_check.md` §2.3 | 严格 |

## 四、修正记录（诚实边界）

- v0.1 的 `verify.py` E 段误用**线性近似**算音分（1200×(r−1)），已改为**对数音分** 1200×log2(r)。
  修正后：单步差 **1.96 音分**、12 步累积 **23.46 音分**（毕氏音差）。
