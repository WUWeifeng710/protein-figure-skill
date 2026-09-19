# 蛋白质结构发表级绘图 · 技能使用指南（中文版）

> 基于 PyMOL-PUB（Bioinformatics 2024, btae139）与 PyMOL 2.5.0 开源版封装的 `protein-figure` 技能。
> 配套：10 个"直接 cmd"风格配方 + 3 个标准类模板，均对 1AY7 出样图验证。

## 一、这套技能解决什么问题

把蛋白质/核酸三维结构（PDB/PDBx）快速渲染成**可直接进论文**的图：白底、300–600 DPI、图内标注默认英文、期刊级配色。覆盖三类需求：

- **按期刊规格排版**：Nature/Science/Cell/PNAS/ACS/Oxford/PLOS/IEEE 字体、列宽、最小 DPI 自动对齐。
- **突出特定区域**：结合位点、突变、关键残基、活性中心，配自定义调色板。
- **对比与机制图**：双结构 RMSD 叠合、残基对距离/极性接触、蛋白-蛋白界面、NMR/MD 系综。

## 二、环境与安装（一次性）

硬性约束：Python 3.9~3.11 + **PyMOL 必须 = 2.5.0**（开源版）+ `PyMOL-PUB`。

推荐 conda-forge 路线（已验证；环境名 `pymol_pub` 仅为约定，可任意）：

```
conda create -n pymol_pub python=3.11 -c conda-forge -y
conda install -n pymol_pub -c conda-forge "pymol-open-source=2.5.0" -y
conda run -n pymol_pub python -m pip install PyMOL-PUB
```

验证：

```
conda run -n pymol_pub python -c "import pymol2; print(pymol2.__version__)"
# 期望输出 2.5.0
```

> 坑：conda-forge 的 `pymol-open-source` 是 2.5.0 的可靠来源；gohlke 第三方 wheel 与 PyPI 的 `pymol-open-source`（只有 3.x alpha）都拿不到 2.5.0，别走那两条。

## 三、两种渲染范式

| 范式 | 用什么 | 何时用 |
|---|---|---|
| **A：标准类（molpub）** | `HighlightStructureImage` / `PropertyStructureImage` / `Figure` | 走期刊版式、多面板出版排版、RMSD 属性着色 |
| **B：直接 cmd（`entry_class: null`）** | `from pymol2 import PyMOL` + 手写 cmd 串 | 自定义调色板/柔光/平面化等超纲风格（10 个直接 cmd 配方全属此类） |

调用层铁律：`mol = PyMOL(); mol.start(); cmd = mol.cmd`，结尾 `mol.stop()`。不要用 `import pymol` 当调用层。

### 2.5.0 严格 API 速查（最常踩的 6 个坑）

1. 自定义调色板用 `cmd.set_color(name, [r,g,b])`，**不是** `set("color", ...)`。
2. 白底用 `cmd.bg_color("white")`，**不是** `set("background_color", ...)`。
3. 清场用 `cmd.hide("everything","hetatm")` + `cmd.hide("everything")`；`hide` 第一参必须是合法 representation（`everything` 合法、`all` 不合法）。
4. 多残基合并选区用 `cmd.select` + `cmd.extend` 逐条加，**命名选区不吃 `+`/`or` 拼接**。
5. `cmd.spectrum("bfactor", ...)` 不认 `bfactor` 槽 → 用 `resi`（或带 b 列试 `b`、带 plddt 列试 `plddt`）。
6. 对象名避开保留字（`a`/`b` 会被加 `_`），建议 `s1`/`s2`。

## 四、风格配方总览（10 个直接 cmd + 3 个标准类）

### 4.1 直接 cmd 风格配方

| 配方 | 视觉特征 | 典型场景 |
|---|---|---|
| `pastel_cartoon_surface` | 按链上色 cartoon + 乳白半透明壳 | 多链蛋白粉彩概览 |
| `ss_milky_surface` | 按二级结构上色 + 中性灰壳 | 突出 α/β/loop |
| `ss_frosted_surface` | 按二级结构上色 + 同色磨砂壳 | 色更饱满的二级结构图 |
| `ss_only_surface` | 纯二级结构 cartoon，无壳 | 干净线条不遮挡 |
| `residues_only` | 整条蛋白隐藏，只显关键残基 sticks | 局部位点聚焦 |
| `spectrum_resi` | cartoon 按残基位置蓝白红渐变 + CA 球 | B-factor/pLDDT/序列属性分布 |
| `active_site_highlight` | 关键残基 sticks + 半透明环境 cartoon + 极性接触虚线 | 活性位点机制图 |
| `distance_contact` | 两残基 sticks+CA 球 + 距离虚线（`dist mode=2`） | 结合位点距离标注 |
| `goodsell_style` | 球状模型按链 Goodsell 粉彩 + 白底无阴影平面渲染 | 期刊封面级科学插图 |
| `mutation_site` | 单突变残基 sticks+CA 球 + 环境 cartoon + salmon 色相 | 突变位点结构分析 |
| `surface_render` | 按链分色独立 surface/mesh/dots + 半透明 | 分子面形状/结合口袋 |
| `ensemble_overlay` | 多模型 state 彩虹渐变 + 半透明 | NMR/MD 结构柔性 |
| `dual_align_rmsd` | 两结构 CA align + RMSD + 叠合 cartoon | WT vs mut / expected vs predicted |
| `ppi_interface` | 两链 within 半径取界面残基 + 界面半透明面 | 蛋白-蛋白界面 |

> 说明：`_registry.md` 共 17 个模板行（3 标准类 + 10 直接 cmd + 个别场景拆分），上表列出 14 个可独立出图的配方。

### 4.2 标准类模板（molpub 类）

| 模板 | 入口类 | 用途 |
|---|---|---|
| `nature_highlight` | `HighlightStructureImage` | 单结构多链高亮，突出结合位点/突变/区段 |
| `rmsd_compare` | `PropertyStructureImage` | 双结构 RMSD/属性叠合 + putty cartoon 残基差异 |
| `science_publication_layout` | `Figure` | 多图+面板+文字+控件拼成出版级 Figure |

## 五、案例 1：Goodsell 封面级科学插图（直接 cmd）

需求：把 1AY7 两条链渲染成期刊封面常用的"平面化粉彩球"。

```python
# goodsell_style.py（已对 1AY7 验证）
from pymol2 import PyMOL
PDB, OBJECT = "1AY7.pdb", "m"
CHAIN_COLORS = {"A": "gs_blue", "B": "gs_red"}   # 只写目标 PDB 实际存在的链
mol = PyMOL(); mol.start(); cmd = mol.cmd
cmd.load(PDB, OBJECT, quiet=1)
if int(cmd.count_atoms("all")) == 0:
    raise SystemExit("LOAD FAILED: 0 atoms")
# 平面化：高 ambient、零 reflect、无阴影
for k, v in {"ray_trace_mode":3, "ray_shadows":0, "depth_cue":0}.items():
    cmd.set(k, v)
cmd.set("ambient", 1.0); cmd.set("direct", 0.0); cmd.set("reflect", 0.0)
cmd.bg_color("white"); cmd.orthoscopic(1)
# 自定义色必须在本实例内定义
for name, rgb in {"gs_blue":[0.565,0.714,0.812], "gs_red":[0.855,0.475,0.427]}.items():
    cmd.set_color(name, rgb)
cmd.remove("m and resn HOH"); cmd.hide("everything","hetatm"); cmd.hide("everything")
cmd.show("spheres", OBJECT)
for c, col in CHAIN_COLORS.items():
    cmd.color(col, "m and chain %s" % c)
cmd.orient(OBJECT); cmd.ray()
cmd.png("1AY7_goodsell.png", width=1600, height=1600, dpi=300, quiet=1)
mol.stop()
```

效果图（1AY7，1600×1600，300 DPI）：

![Goodsell 平面化粉彩球（按链分色，白底无阴影）](1AY7_goodsell.png)

## 六、案例 2：活性位点特写（直接 cmd）

需求：把结合位点几个关键残基放大成 sticks，背景保留半透明 cartoon 环境，并画残基间极性接触虚线。

```python
# active_site_highlight.py 关键片段
KEY = ["A/35", "A/52", "B/44"]            # 关键残基（带链前缀）
cmd.show("cartoon", "m"); cmd.color("gray80", "m"); cmd.set("cartoon_transparency", 0.7)
merged = "msite"
for i, r in enumerate(KEY):
    cmd.select("tmp%d" % i, r)
    cmd.extend(merged, "tmp%d" % i)        # 命名选区用 select+extend 合并（不吃 + 拼接）
cmd.show("sticks", merged); cmd.show("spheres", "byres merged and type c")
cmd.color("gs_red", "byres merged and type c")
for i in range(len(KEY)-1):                # 极性接触虚线
    cmd.dist("d%d" % i, "%s" % KEY[i], "%s" % KEY[i+1], mode=2, color="yellow")
cmd.orient(merged); cmd.zoom("m", 1.4); cmd.ray()
cmd.png("1AY7_active_site.png", width=1600, height=1600, dpi=300, quiet=1)
```

效果图：

![活性位点特写（sticks + 半透明环境 cartoon + 极性接触）](1AY7_active_site.png)

## 七、案例 3：双结构 RMSD 叠合（标准类）

需求：expected vs predicted 叠合，按残基差异 putty cartoon 彩虹谱。

```python
from molpub import PropertyStructureImage
img = PropertyStructureImage(structure_paths=["expected.pdb", "predicted.pdb"])
img.set_shape(representation_plan=[("model:predicted","cartoon"), ("model:expected","cartoon")])
img.set_state(rotate=[0,60,255], inner_align=True, target="expected")
img.set_color(target="model:predicted", color_map="rainbow",
              edge_color="0x000000", gauge_strengthen=True)   # 仅 cartoon 生效
img.save(save_path="1AY7_align.png", width=1800, ratio=0.5)
img.close()   # 批量务必 close 释放进程
```

效果图（自叠合演示）：

![双结构叠合对齐 + RMSD](1AY7_align.png)

## 八、案例 4：期刊版式排版（标准类 Figure）

需求：把多张结构图 + 旋转控件图标 + 文字拼成 Nature 双列出版级 Figure。

```python
from molpub import Figure, obtain_widget_icon
obtain_widget_icon(save_path="arrow.png", widget_type="arrow",
                   params={"degree": 90, "color": "black", "width": 0.02})
fig = Figure(manuscript_format="Nature", occupied_columns=2,
             aspect_ratio=(606,358), mathtext=False, row_number=2, column_number=2)
fig.set_image(image_path="1AY7_goodsell.png", layout=(1,1,1))
fig.set_image(image_path="arrow.png", locations=[0.85,0.8,0.1,0.1], transparent=True)
fig.set_text(annotation="(a)", locations=[0.02,0.97,0.08,0.03])
fig.save_figure("final_figure.png")   # 子图 dpi 需 ≥ 期刊 minimum_dpi
```

## 九、出版质量约束（务必核对）

| 期刊 | 字体 | 最小 DPI | 最大列 |
|---|---|---|---|
| Nature | Arial | 300 | 2 |
| Science | Helvetica | 300 | 3 |
| Cell | Arial | 300 | 2(3) |
| PNAS | Helvetica | **600** | 2 |
| ACS | Arial | **600** | 2 |
| Oxford | Arial | 350 | 2 |

- `save` 的 `dpi` 默认 1200；`Figure.minimum_dpi` 由期刊决定，子图 PNG 实际 DPI 低于它，`paste_bitmap` 会抛 ValueError。
- Cell 必须传 `column_format=2` 或 `3`。
- `set_image` 只支持 `.png`；SVG/PDF 控件图标要手动栅格化再嵌。

## 十、高级渲染参数（OPIG 经验）

| 参数 | 作用 | 推荐值 |
|---|---|---|
| `surface_quality` | 表面法线/网格精度 | 10–40（**2.5.0 严格模式不可 set，已踩坑**） |
| `cartoon_sampling` | 卡通采样密度 | 2–4 |
| `cartoon_line_width` | 卡通描边粗细 | 0.6–2.0 |
| `ray_quality` / `ray_simplify` | 光线追踪质量/简化 | 0–1 |
| `ray_opaque_background` | 白底不透明 | 1（headless 无 GPU 时稳） |
| `field_of_view` | 透视变形 | 出版用默认 30–45 |

一键出出版级卡通：`cmd.preset("publication", "m")`（2.5.0 可用；`preset.pretty` 在 2.x 已降级）。

## 十一、交付物与偏好

- **图内文字标注默认英文**（panel A/B/C、轴、箭头注释、色标、基因/品种名保持英文）；文档正文与图注用中文。
- 交付：PNG（300–600 DPI）+ 可选 PDF/SVG；期刊要 TIFF 时出 PNG 后用 PIL 转。
- 节奏铁律：**未跑出可验证样图前，配方不进 `_registry.md`**——先对真实 PDB 出样图、PIL 校验（存在/尺寸/非空白），再入库。

## 十二、14 张样图速览（均为 1AY7，1600×1600，300 DPI）

### 直接 cmd 配方效果图

![pastel 按链粉彩 cartoon + 乳白壳](1AY7_pastel.png)
![ss_milky 二级结构粉彩 + 中性壳](1AY7_ss_milky.png)
![ss_frosted 二级结构粉彩 + 同色磨砂壳](1AY7_ss_frosted.png)
![ss_only 纯二级结构 cartoon](1AY7_ss_only.png)
![residues_only 关键残基棒特写](1AY7_residues_only.png)
![spectrum 残基位置蓝白红渐变](1AY7_spectrum_bfactor.png)
![distance 残基对距离标注](1AY7_distance.png)
![mutation 突变位点结构分析](1AY7_mutation.png)
![surface 分子面按链分色](1AY7_surface.png)
![ensemble 多模型叠加](1AY7_ensemble.png)
![ppi 蛋白-蛋白界面](1AY7_ppi.png)

### 标准类效果图

![rmsd 双结构叠合](1AY7_align.png)

## 引用

Chen, Y., Zhang, H., Wang, W., Shen, Y., Ping, Z. (2024). Rapid generation of high-quality structure figures for publication with PyMOL-PUB. *Bioinformatics*, 40(3), btae139. https://doi.org/10.1093/bioinformatics/btae139
