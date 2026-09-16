# 归档规范：`axioms/` 与 `notes/`

文档写完之后，放哪里决定了它的**地位**。放错会导致别人引用错东西。

## 两个目录的分工

### `axioms/` —— 公理本体与正稿
放**体系本身**：公理陈述、正稿、正式修订。
- 特征：别的东西会**引用**它；改动需要走版本（v1.1、v1.2…）；
- 例：`axiom_III_curvature.md`、`axiom_IV_correspondence.md`。

### `notes/` —— 衍生材料
放**围绕正稿的工作**：补注、读解、形式化、综述、实例库、否证记录。
- 特征：是**解释、展开、试探**，可以随时增删；
- 例：`axiom_IV_note_gamma_renormalization.md`、`spinor_notes.md`、
  `yinyang_wuxing_unification.md`、`slime_mold_intelligence.md`。

> **判据**：如果这份文档"被别处引用为权威"，归 `axioms/`；否则归 `notes/`。
> 补注（note）即便在讨论公理，也放 `notes/`——它是**关于**公理的工作，不是公理本身。

## 命名

- 仓库文件名用**语义化英文 + 下划线**：`axiom_IV_note_gamma_renormalization.md`；
- 工作区（本地草稿）可以用中文名，提交前再决定仓库名；
- 版本用后缀：`_v1.1`、`_v1.2`；不要覆盖旧版，保留可追溯。

## 图片

- 图片放在文档**同目录**的 `figures/` 下；
- 文档内用相对路径引用：`![说明](figures/xxx.png)`；
- 不同文档共享同一张图时，`figures/` 就在共同的父目录。

## 提交

提交前**给用户看清单**，包含：
1. 本次涉及的**文件名与目录**；
2. 一句 **commit message 草案**。

commit message 建议格式：
```
<动作> <对象>: <要点>

- 新增 notes/xxx.md（...）
- 更新 notes/figures/yyy.png
```

**不要在用户确认前提交。**

## 确认门清单

| 节点 | 要确认什么 |
| :-- | :-- |
| 订正他人断言 | 改动前报告"这是订正" |
| 归档位置 | `axioms/` 还是 `notes/` |
| 提交 | 文件清单 + commit message |
