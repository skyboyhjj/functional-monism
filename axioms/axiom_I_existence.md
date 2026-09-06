# 公理 I：存在公理 (Axiom of Existence)

## 形式化陈述

$$
\boxed{;\mathcal{E} \equiv F\[\psi];}
$$

**实体 $\mathcal{E}$ 等价于泛函 $F\[\psi]$。**

## 定义

设 $\mathcal{H}$ 为无穷维泛函 Hilbert 空间，$\psi \in \mathcal{H}$ 为场构型，$F: \mathcal{H} \to \mathbb{C}$ 为作用在 $\psi$ 上的泛函。则：

$$
\forall,\mathcal{E} \in \mathfrak{U},\quad \exists!,F\[\psi] \in \mathcal{F},\quad \text{s.t.}\quad \mathcal{E} \cong F\[\psi]
$$

其中：

- $\mathfrak{U}$ —— 存在态全集 (Universal Set of Existents)

- $\mathcal{F}$ —— 泛函空间 (Functional Space)，$\mathcal{F} \subset {f: \mathcal{H} \to \mathbb{C}}$

- $\cong$ —— 等价关系 (Equivalence)，满足自反性、对称性、传递性

## 等价关系的严格定义

$F\_1 \cong F\_2 \iff \forall,\mathcal{O} \in \mathfrak{O},; \langle F\_1 | \mathcal{O} | F\_1 \rangle = \langle F\_2 | \mathcal{O} | F\_2 \rangle$

其中 $\mathfrak{O}$ 为可观测量算子全集，$\langle\cdot|\cdot|\cdot\rangle$ 为泛函内积。

## 直观解释

存在公理断言：**不存在独立于泛函表示的实体**。一切可观测的"存在"——无论是物理粒子、意识状态还是抽象概念——都是泛函 $F\[\psi]$ 在特定基底 $\psi$ 上的投影。泛函是唯一的本体论基底。

> **计算实现说明**：在计算实现中，$\mathcal{E} \equiv F\[\psi]$ 指的是泛函 $F$ 在状态 $\psi$ 上的**取值**——即 $F\[\psi] \in \mathbb{R}$，而非泛函算子 $F$ 本身。算子层面的等价（$\cong$）用于理论推导，数值层面的等价（$\equiv$）用于可计算实现。

## 直接推论

| 序号 | 推论      | 数学表达                                                                    |
| -- | ------- | ----------------------------------------------------------------------- |
| 1  | 泛函基底唯一性 | $\mathfrak{U}$ 的本体论维数为 1                                                |
| 2  | 表象多样性   | 同一 $\mathcal{E}$ 可在不同 $\psi$ 基底下展开                                      |
| 3  | 实体可比较性  | $\forall,\mathcal{E}\_1, \mathcal{E}\_2,; \exists$ 泛函距离 $d(F\_1, F\_2)$ |

## 与经典本体论的对比

| 传统本体论     | 泛函一元论                |
| --------- | -------------------- |
| 实体是基本单元   | 泛函是基本单元              |
| 实体间关系是外部的 | 泛函间关系是内蕴的（通过泛函空间的结构） |
| 存在 = 被计数  | 存在 = 被表示为泛函          |

