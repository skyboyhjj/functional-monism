# 交付清单 ·「五条形式判据」线

**——读解 → 校订（原文）→ 自查（引擎）→ v1.2 → 刻度尺（v1.3）→ 算据补格（v1.4）**

> **目的**：这条线的**全部文档与脚本**（英文文件名版），供上 GitHub。
> **体检**：4 份文档 `check_display_format.py` **隐患 0**；3 份算据脚本 **exit 0**。

---

## 一、这条线是什么（一句话）

从一篇 FEP 批评长文（DWL Cognition，2026-09-30）的读解出发，把文中"**五条形式标准**"（维度／拓扑／范畴／类型／动力学）用成项目里"**机制是否落地**"的判据；经**原文校订**、**矛盾迭代引擎自查**、**五个一元实例逐格核**，最后给两处空心格补上算据。

**结论**：**五条无一为 ✓**，四实例的"亮"都只落在"给定载体上的现象"，**缺口在"生成"，不在"现象"**。

---

## 二、文件清单

| # | 文件 | 角色 |
| --: | :-- | :-- |
| 1 | `notes/five_criteria_reading_fep.md` | 起点读解（链首·承） |
| 2 | `notes/five_criteria_mechanism_landed.md` | **主稿 v1.4**（文首「修订说明」＝全链轨迹） |
| 3 | `notes/five_criteria_selfcheck_engine.md` | 引擎自查（体 → 相-开方 → 相-平方 → 玄 → 用） |
| 4 | `notes/five_criteria_evidence_appendix.md` | 算据汇编（由 #9 生成） |
| 5 | `notes/five_criteria_manifest.md` | 本清单 |
| 6 | `scripts/five_criteria/verify_fep_claims.py` | 链首算据（ELBO 重建；CCT 反例） |
| 7 | `scripts/five_criteria/verify_shaping_vs_five_criteria.py` | 势整形**两层**算据（策略层 vs 动力学层） |
| 8 | `scripts/five_criteria/verify_five_criteria_instances.py` | 刻度尺算据（五行 R／十二律／涡旋／八度圆） |
| 9 | `scripts/five_criteria/make_evidence_appendix.py` | 汇编生成器（带逐字节自校验） |

---

## 三、依赖与引用

```
[1] 起点读解 ──承──▶ [2] 主稿 v1.4
                        ▲
[3] 自查（引擎）────────┘      （v1.2 的六处修订即出自 [3]）
[2] ──引──▶ [4] 算据汇编
[1] ──算据──▶ [6]
[2] §四 ──算据──▶ [7]        [2] §五 ──算据──▶ [8]
[4] ──由──▶ [9] 生成
```

---

## 四、复算 / 复现

| 命令（在仓库根运行） | 期望 |
| :-- | :-- |
| `python3 scripts/five_criteria/verify_fep_claims.py` | exit 0（ELBO 恒等式偏差 3.55e−15；CCT 反例 21 个先验全不优） |
| `python3 scripts/five_criteria/verify_shaping_vs_five_criteria.py` | exit 0（策略不变；不动点移动 + $`c>c_*`$ 鞍结分岔） |
| `python3 scripts/five_criteria/verify_five_criteria_instances.py` | exit 0（$`R^5=I`$、谱＝5 次单位根；$`2^{n/12}`$ 采样 2e−16；绕数＝整数；$`\mathbb R/(\ln 2\mathbb Z)\cong S^1`$） |
| `python3 scripts/five_criteria/make_evidence_appendix.py` | 重新生成 `notes/five_criteria_evidence_appendix.md`，并报 "byte-identical: True" |

> 脚本仅依赖 `numpy`（生成器只用标准库）。

---

## 五、说明

- 本线原名是中文；本包已按仓库约定**改为英文文件名**，并**同步了全部交叉引用**（`yi/` → `scripts/`）。
- **不随包传** `fep_yuanwen.txt`（原文 PDF 的本地转写）。为避免版权问题**请勿入库**；需要时从公众号原文重新生成即可。

---

*清单版本 v1.0　2026-10-01*
