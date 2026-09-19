---
name: protein-figure
description: >
  蛋白质三维结构发表级绘制。基于 PyMOL-PUB (Bioinformatics 2024, btae139) 的高层接口封装：
  期刊规格版式、结构图渲染（高亮/属性着色/对齐）、旋转与箭头控件图标、出版级 Figure 排版。
  触发词：蛋白质绘图、分子结构图、publication figure、PyMOL 出版图、蛋白质 3D 结构发表图、
  结构图期刊排版、分子高亮绘图、RMSD 结构对比图。
  支持预置风格模板选择（templates/ 目录）与自定义模板沉淀（看图复现→确认→保存）。
agent_created: true
created_at: 2026-09-18
---

# Protein-Figure 技能：蛋白质三维结构发表级绘制

## 何时使用

用户要生成**可用于论文发表**的蛋白质/核酸三维结构图（PNG/SVG），尤其是需要：
- 符合特定期刊（Nature/Science/Cell/PNAS/ACS/Oxford/PLOS/IEEE）字体、DPI、列宽规格；
- 突出显示特定区域（链/区段/残基）并配色；
- 双结构（expected vs predicted）叠合对齐，用颜色渐变 + cartoon 粗细表达差异（如 RMSD 谱）；
- 把多张结构图 + matplotlib 面板 + 文字/箭头控件拼成完整出版级 Figure。

**不适用**：纯 2D 结构示意（手绘/chemdraw 场景）、非蛋白质分子（小分子为主，可用 PyMOL 但非核心场景）、需要交互 3D 展示的场景。

## 前置依赖与安装

### 硬性约束
- **Python >= 3.7.3**；推荐 3.9~3.11。
- **PyMOL 版本必须等于 2.5.0**（开源版，`pip install pymol` 在 Windows 上可能拿不到 2.5.0；开源 PyMOL 官方下载页 https://pymol.org/2/#download）。
  - Linux 发行版与开源版安装依赖不同，**优先开源版**；分发版（2.5.7 捆绑 Python 3.9）会绑定特定 Python 环境，与 pip 装的 molpub 冲突。
- 其余依赖：`biopython>=1.78`、`matplotlib>=3.2.0`、`numpy>=1.21.2`、`pillow>=8.2.0`、`scipy>=1.4.1`、`sphinx-rtd-theme>=0.4.3`、`PyQt5>=5.15.9`（GUI 才需要）。

### 安装方式（三选一，按情况）

1. **conda-forge（推荐，默认就是 2.5.0，可复现）**
   ```bash
   conda create -n pymol_pub python=3.11 -c conda-forge -y
   conda install -n pymol_pub -c conda-forge "pymol-open-source=2.5.0" -y
   # 进入环境再装 PyMOL-PUB（conda activate 或直接用该环境的 python）
   conda run -n pymol_pub python -m pip install PyMOL-PUB
   ```
   - 环境名 `pymol_pub` 可任意；关键是把 `pymol-open-source` **锁到 2.5.0**。
   - envs 默认落在 `~/.conda/envs`（Windows）/`$CONDA_HOME/envs`（Linux/mac），**不在** conda 安装目录下。

2. **gohlke 第三方 wheel（无 conda 时的兜底，按 Python 版本匹配）**
   - `github.com/cgohlke/pymol-open-source-wheels`（releases 有 2.5.x 的 win_amd64 wheel）
   - 配 `Pmw` + `numpy(+mkl)` 三个 wheel 一起 `pip install --no-index --find-links`
   - 需对应 Python 版本（如 cp38/cp311）；装前确认本机 Python 与 wheel tag 匹配

3. **官网直接装 PyMOL 开源版**（`https://pymol.org/2/#download`，选 2.5.0），再 `pip install PyMOL-PUB`。

**装完验证**：
```bash
python -c "import pymol2; print(pymol2.__version__)"   # 期望 2.5.0
python -c "from molpub import HighlightStructureImage; print('molpub OK')"
```

**注意**：任何来源拿到的 2.5.x 都要确认锁定到 **2.5.0**（不是 2.5.7 等更新小版本）；PyPI 的 `pymol-open-source` 只有 3.x alpha，**别走那条**。

## 配方迁移踩坑（recipe.pml → 2.5.0 严格 API，已实测）

把 PyMOL 命令行配方迁到 `pymol2.PyMOL().cmd` 时，conda-forge 2.5.0 校验比老配方严（`pastel_cartoon_surface` 配方的实测结果）：

- **导入方式**：用 `from pymol2 import PyMOL; mol = PyMOL(); mol.start(); cmd = mol.cmd`。不要 `import pymol` 当调用层——模块本身无 `.load` 等命令。
- **`cmd.set("color", name, rgb)` 报错**：自定义调色板要用 `cmd.set_color(name, [r,g,b])`（`set_color` 是命令；`set` 的 color 槽走 bool 校验）。
- **`cmd.hide("hetatm")` / `cmd.hide("all", ...)` 报错**：`hide` 第一参必须是合法 representation（合法值含 `everything` 但不含 `all`），`hetatm` 是选区不是表示。正确：`cmd.hide("everything", "hetatm")` + `cmd.hide("everything")`。
- **`cmd.show("cartoon", obj)` / `cmd.color(...)` / `cmd.create(...)` / `cmd.orient` / `cmd.ray` / `cmd.png(dpi=300)` 正常**。
- 1AY7（A、B 两蛋白链）套粉彩前 2 色（soft_blue / rose_pink），`ray()` + `png(1600,1600,dpi=300)` 出图约 13s。
- **`cmd.spectrum("bfactor", ...)` 报 "Unknown expression: bfactor"**：2.5.0 的 `spectrum` 不认 `bfactor` 槽名。能跑通的是 `spectrum resi ...`（按残基位置）；PDB 带 b 列可试 `spectrum b ...`，带 plddt 列可试 `spectrum plddt ...`。想要"真 B-factor 渐变"用 `b` 槽（不是 `bfactor`）。
- **`cmd.select` 命名选区不吃 `+` 运算符拼接**（报 "Invalid selection name"，如 `m and (resi 35+resi 52)` 被解析错）；`count_atoms` 能吃但 `select` 不行。多残基合并选区用 **`cmd.select` + `cmd.extend`** 逐条加，或逐个 `select` 后 `extend`。`byres`/`around` 选区要在 `hide("everything")` **之后**做（hide 清空选区）。

## 一键预设与高级渲染参数（2.5.0 可复用）

### 官方内置 preset（一行出出版级卡通）
比手动 set 一堆柔光参数更省事。conda-forge 2.5.0 里 `preset` 命令仍可用（注意 1.x 的 `preset.pretty` 在 2.x 行为降级，`preset.publication` 内部叠了 cartoon 参数故 2.5.0 仍可用）：

| preset | 用途 | 2.5.0 注意点 |
|---|---|---|
| `preset.publication` | 一键出版级卡通（fancy helices + smooth loops + 灰高亮） | **首选**，2.5.0 可用 |
| `preset.pretty` | 通用美化卡通 | 2.x 中效果打折，单独用不如 publication |
| `preset.simple` | 仅骨架线 | 快、极简 |
| `preset.ball_and_stick` | 球棍 | 小分子 |
| `preset.b_factor_putty` | B-factor putty 粗细 | 对接 `PropertyStructureImage` 的 gauge |
| `preset.technical` | 极性接触线 + 残基 sticks | 结合位点分析 |
| `preset.ligand_sites` | 配体结合位点 | 配体场景 |

`cmd.preset("publication", "m")` 一行即可对对象 `m` 套出出版级外观，再叠自定义配色/选区。配方可用 preset 替代手写的柔光参数组（见"配方迁移踩坑"第 2 节的 set 串）。

### 高级渲染参数（OPIG 经验，比只有 antialias 更精细）
| 参数 | 作用 | 推荐值 |
|---|---|---|
| `surface_quality` | 表面法线/网格精度 | 10–40（默认 20，更高更平滑） |
| `cartoon_sampling` | 卡通采样密度 | 2–4（默认 2） |
| `cartoon_line_width` | 卡通描边粗细 | 0.6–2.0 |
| `ray_quality` / `ray_simplify` | 光线追踪质量/简化 | 0–1（1 更简快） |
| `zoom` / `zoom complete` | 视角拉近 | 配合 `orient` 用 |
| `ray_opaque_background` | 白底不透明 | 1（headless 无 GPU 时白底稳） |
| `field_of_view` (fov) | 透视变形 | 越大越近距；出版用默认 30–45 |

### 加载校验（出图前必做，补 PIL 验不出"选区命中 0 原子"的洞）
PIL 只能验"文件非空/尺寸对"，验不出**选区实际命中 0 个原子导致图是空白**。借鉴 deepmind pymol 的做法，出图脚本在 `cmd.load` 后立刻校验：
```python
if int(cmd.count_atoms("all")) == 0:
    print("LOAD FAILED: 0 atoms after load"); mol.stop(); sys.exit(1)
```
对关键选区（`k_residues`、高亮区段）也校验 `cmd.count_atoms(sel) > 0`，命中 0 就报错而非静默出空白图。

## 未覆盖场景的可扩展参考（PyMolClaw 13 脚本族）

`BioTender-max/PyMolClaw`（github: github.com/BioTender-max/PyMolClaw）提供 13 个可复用 PyMOL 脚本。**13 个场景已全部落地**（改写到 2.5.0 严格 API + 1AY7 出样图验证），无需再依赖该仓库——下列模板已自包含：

| 场景 | 脚本 | 我们的状态 |
|---|---|---|
| 序列位置属性谱着色 | `spectrum.py` | 已做 → `spectrum_resi` |
| 活性位点特写 | `active_site.py` | 已做 → `active_site_highlight` |
| Goodsell 风格科学插图 | `goodsell.py` | 已做 → `goodsell_style` |
| 距离 / 极性接触 | `distance.py` | 已做 → `distance_contact` |
| 突变位点结构分析 | `mutation.py` | 已做 → `mutation_site` |
| 分子面渲染 | `surface.py` | 已做 → `surface_render` |
| NMR / MD 系综 | `ensemble.py` | 已做 → `ensemble_overlay` |
| 结构对齐 + RMSD | `align.py` | 已做 → `dual_align_rmsd` |
| 蛋白-蛋白界面 | `ppi.py` | 已做 → `ppi_interface` |

**说明**：PyMolClaw 是 headless 路线（`pymol -c -q`），与我们的 conda PyMOL 2.5.0 + `cmd.ray()` 路线可共存；引它的脚本时按其 README 调整到 2.5.0 严格 API（同"配方迁移踩坑"那套）。

## 暂不采用的清单项（记录理由，避免反复评估）
- **pymolrc / EZ-Viz 交互式自动美化**：我们是"按需出图"而非"加载即美化"，不契合工作流，跳过。
- **deepmind 的 OSMesa 软件渲染路线**（uv + `pymol-open-source-whl` + 强制 `cmd.png` 不用 `cmd.ray`）：与我们 conda 2.5.0 + `cmd.ray()` 路线冲突，**只借其 `count_atoms` 加载校验与"无 GPU/headless 时 ray 不可靠、退 png"这条经验**，不整体改渲染引擎。

## 配方迁移踩坑补充（来自 deepmind pymol 经验，已纳入）
- headless / 无 GPU 环境：`cmd.ray()` 可能失效或慢，可退 `cmd.png`（普通 OpenGL 软件光栅化）+ `ray_opaque_background=1` 保白底。
- 每次出图脚本结尾 `mol.stop()`（pymol2 路线）；deepmind 的 `import pymol` 路线则 `cmd.quit()`，二者勿混用。

2. **gohlke 第三方 wheel（无 conda 时的兜底，按 Python 版本匹配）**
   - `github.com/cgohlke/pymol-open-source-wheels`（releases 有 2.5.x 的 win_amd64 wheel）
   - 配 `Pmw` + `numpy(+mkl)` 三个 wheel 一起 `pip install --no-index --find-links`
   - 需对应 Python 版本（如 cp38/cp311）；装前确认本机 Python 与 wheel tag 匹配

3. **PyPI `pymol-open-source` 包（仅 alpha，版本不匹配，不推荐）**
   - PyPI 上只有 3.1.0a0 / 3.2.0a0，且 3.2.0a0 才带 win_amd64 wheel——**3.x ≠ 2.5.0，与 PyMOL-PUB 要求冲突**，别走这条

4. **源码编译（最后手段）**
   - `github.com/schrodinger/pymol-open-source`，Windows 下编译成本高，不推荐

装完验证：`python -c "import pymol2; print(pymol2.__version__)"` 应输出 `2.5.0`。

**注意**：gohlke / conda 拿到的 2.5.x 也要确认锁定到 **2.5.0**（不是 2.5.7 等更新小版本）。

### 前置步骤判定（跑样图前先看这条）
**能否自动出图 = 取决于 PyMOL 是否已装好**，这是手工前置步骤：
- 本机若未装 PyMOL（`import pymol2` 报 ModuleNotFoundError）→ 先按上面装好 2.5.0，再跑 `pip install PyMOL-PUB`，最后运行 `smoke_test.py` 或按模板渲染脚本出图。
- 本机 `conda` 是否可用也需确认；若 conda 可用，`conda install -c schrodinger "pymol=2.5.0"` 比官网安装更省事。
- 出图脚本一律写成"接收 PDB 路径 + 模板名 + 覆写参数"的形式，环境就绪后直接跑。
### 字体
molpub 内置 TTF 字体目录 `molpub/fonts/`（"Times New Roman"、"Helvetica"、"Arial"、"Linux Libertine"、"Lucida Calligraphy"），import 时自动注册到 matplotlib，**无需手动装字体**。

## API 调用方式

所有类/函数从 `molpub` 或 `molpub.layouts` 导入：
```python
from molpub import (DefaultStructureImage, HighlightStructureImage,
                    PropertyStructureImage, Figure, obtain_widget_icon)
```

### 核心类与能力

| 类/函数 | 用途 | 关键方法 |
|---|---|---|
| `DefaultStructureImage` | 结构图基类：加载 PDB、旋转/缩放/对齐/隐藏 | `set_cache` `set_zoom` `set_state` `set_shape` `save` `save_pymol` `load_pymol` `clear` `close` |
| `HighlightStructureImage` | **高亮特定区域**（论文最常用） | 继承基类 + `set_color(coloring_plan)` |
| `PropertyStructureImage` | **属性驱动着色**（RMSD、理化性质） | 继承基类 + `set_color(target, properties, color_map, gauge_strengthen)` |
| `Figure` | **出版级排版图**（多面板 + 结构图嵌入 + 文字 + 控件图标） | `set_image` `set_panel` `set_text` `set_panel_grid` `save_figure` |
| `obtain_widget_icon` | 旋转/箭头 SVG 控件图标 | `widget_type` + `params` |

### 推荐调用顺序（官方建议，非强制）

```
set_cache(隐藏不必要部分) → set_state(空间旋转/对齐) → set_shape(表示方式)
→ set_color(着色) → save(保存)
```

## 预置风格选择（模板机制）

### 交互协议（核心，按此执行）

**触发判断**（每轮绘图请求先看这条）：
- **用户提到预置风格 / 模板** → 进入"选项模式"：读 `templates/_registry.md`，把可用模板以选项形式呈现，等用户挑选。
- **用户没提** → 进入"自由模式"：按技能文档 + 用户本次输入的参数绘制，不套模板。
  - 例外：若输入与某预置模板高度吻合（如"画 RMSD 对比"匹配 `rmsd_compare`），可**主动推荐 1 个**并说明理由，用户可拒绝；不强制。

**选项呈现格式**（"选项模式"时这样给）：
```
可用预置风格：
[1] Nature 高亮复合结构图 — 单结构多链高亮，突出结合位点/突变/区段
[2] 双结构 RMSD 对比图 — expected vs predicted 叠合 + 残基差异渐变
[3] Science 全宽多面板出版排版 — 多图+文字+控件拼成出版级 Figure
回复编号，或说"都不合适，按我的要求画"。
```

**模板参数化覆写**：用户挑模板后，仍需给 PDB 文件路径 + 实际链名/残基号（替换模板里的 `{chain_A}` 等占位符）。模板给的是"视觉风格骨架"，调用方覆写业务参数。

### 模板目录
```
templates/
├── _registry.md            # 预置风格清单（选项模式的数据源）
├── _template_format.md     # 模板 yaml 格式规范
├── README.md               # 机制说明 + 沉淀流程
├── nature_highlight.yaml
├── rmsd_compare.yaml
├── science_publication_layout.yaml
├── pastel_cartoon_surface.yaml   # 按链上色 cartoon + 乳白壳（用户沉淀 recipe.pml）
├── ss_milky_surface.yaml       # 按二级结构上色 cartoon + 中性壳
├── ss_frosted_surface.yaml     # 按二级结构上色 cartoon + 同色磨砂壳
├── ss_only_surface.yaml        # 纯二级结构 cartoon，无 surface
├── residues_only.yaml          # 关键残基棒特写（隐藏蛋白只显 sticks）
├── spectrum_resi.yaml          # 序列位置属性谱着色（蓝白红渐变 cartoon + CA 球）
├── active_site_highlight.yaml  # 活性位点特写（sticks + 半透明 cartoon 环境 + 极性接触）
├── distance_contact.yaml       # 残基对距离 / 极性接触标注（dist mode=2 虚线）
├── goodsell_style.yaml         # Goodsell 风格平面化粉彩球（按链 + 白底无阴影）
├── mutation_site.yaml          # 突变位点结构分析（单残基 + 环境 cartoon + salmon 色相）
├── surface_render.yaml         # 分子面渲染（按链分色 + 半透明 surface/mesh/dots）
├── ensemble_overlay.yaml       # NMR / MD 多模型叠加（state 渐变 + 半透明）
├── dual_align_rmsd.yaml       # 双结构叠合对齐 + RMSD（CA align + color1/color2）
└── ppi_interface.yaml         # 蛋白-蛋白界面（within 半径 + 界面残基 sticks + 界面面）
```

### 自定义模板沉淀（"看图复现 → 确认 → 保存"流程）
**触发词**（任一即触发）："保存成模板"、"这个风格记住"、"按这张图画"（发图）、"复现这张图的风格"。

**4 步流程（不可跳步）**：
1. **复现**：读用户参考图（多模态）→ 拆解选区/表示方式/配色/旋转/版式 → 写候选 yaml 到 `templates/<候选名>.yaml` → **先按该 yaml 写渲染脚本并用真实 PDB 跑出样图**（直接 cmd 配方须过 2.5.0 严格 API，见「验证检查清单」额外检查项）→ 用 PIL 校验样图 → 给用户看。
2. **确认**：用户审样图，明确"可以/OK"才进入下一步；有微调就改脚本/yaml 重画，循环到满意。
3. **命名**：用户给模板名；未给则我按"场景 + 视觉特征"建议（如 `nature_binding_site`、`cell_membrane_cartoon`、`ss_milky_surface`）。
4. **入库**：确认 + 命名后，把候选 yaml 定稿存 `templates/`（直接 cmd 配方同时存验证过的 `<名>.py` 参考脚本），并**在 `_registry.md` 加一行**（模板名 / 场景 / 参考图来源）+ 同步本 SKILL.md 章节。

> **节奏铁律**：未跑出可验证样图前，配方不得进 `_registry.md`。本次 ss 配色族（recipe_1/2/3）即"先按配方出样图验证、再入库"。

**硬性约束**：
- 模板 = **可复用参数**，不是绑定某次 PDB 的具体代码；选区/残基必须参数化（`{chain_A}` 占位符），不能写死"A 链 1-30"。
- 模板 yaml 自包含，不依赖外部文件。
- 每个模板配一段"使用示例"，标出哪些参数调用方可覆写。

## 输入输出格式

### 输入
- 结构文件：`.pdb`（也支持 `.mmcif`/`.cif`，PyMOL 自动识别）
- 选择字符串：`"type:target,target,..."`，type ∈ {`position`, `range`, `residue`, `segment`, `chain`, `model`}；多链可 `"A+10-20"` 表示 A 链 10-20 残基
- 颜色：`"0xRRGGBB"` 十六进制字符串
- 旋转角度：`[x_deg, y_deg, z_deg]`（0-360 度）

### 输出
- 结构图：PNG（`save` 方法），指定 `width`（像素）+ `ratio`（高/宽比）+ `dpi`（默认 1200）
- 出版图：PNG/SVG/PDF（`save_figure` 保存时按 `Figure` 的 `minimum_dpi` 决定精度）
- 控件图标：PNG（`obtain_widget_icon` 默认 dpi=1200，`transparent=True` 透明背景）
- PyMOL 会话：`.pse` 文件（`save_pymol` / `load_pymol`，可复用会话）

**排序约定**（我提供选项时按此排）：
1. 场景最贴切的排前。
2. 预置模板（`created_by: 我自建`）优先于用户沉淀模板（`created_by: 用户沉淀`），避免覆盖通用风格。

### 特殊配方说明：不走 molpub 类 API 的模板
- 一组"直接 cmd"配方（`entry_class: null`），均含**自定义 `set_color` 调色板 + 白底柔光参数**，超出 `HighlightStructureImage` 等标准类能力：
  - `pastel_cartoon_surface`（源自 `recipe.pml`）：按**链**上色 cartoon + 中性灰 surface 壳，拆 cart/surf 对象。参考 `templates/pastel_cartoon_surface.py`。
  - `ss_milky_surface` / `ss_frosted_surface` / `ss_only_surface`（用户 ss 配色族）：按**二级结构**（ss h/s/loop）上色，区别仅在 surface（中性壳 / 同色磨砂壳 / 无壳）。参考对应 `.py`。
  - 通用规则：**模板若 `entry_class: null`，渲染脚本按 `render.extra_steps` 直接 cmd 串起，不套 molpub 类**；其余模板走对应类。
  - 链上色 vs 二级结构上色：前者按 `chain X` 选区拆对象；后者按 `ss h`/`ss s`/`loop` 选区，可对单一对象整体上色（ss_only 甚至不拆对象）。

## 关键参数与出版质量约束

### 1. 期刊版式规格（`Figure.__init__`）

| 期刊 | 字体 | 数学字体 | 最小 DPI | 最大列 | 1列宽(in) | 2列宽(in) | 3列宽(in) |
|---|---|---|---|---|---|---|---|
| Nature | Arial | Linux Libertine & Lucida Calligraphy | 300 | 2 | 3.54 | 7.08 | - |
| Science | Helvetica | 同上 | 300 | 3 | 2.24 | 4.76 | 7.24 |
| Cell | Arial | 同上 | 300 | 2(3) | 3.35 / 2.17 | 6.85 / 4.49 | - / 6.85 |
| PNAS | Helvetica | 同上 | **600** | 2 | 3.42 | 7.00 | - |
| ACS | Arial | 同上 | **600** | 2 | 3.25 | 7.00 | - |
| Oxford | Arial | 同上 | 350 | 2 | 3.39 | 7.00 | - |
| PLOS | Arial | 同上 | 300 | 1 | 5.20 | - | - |
| IEEE | Times New Roman | 同上 | 300 | 2 | 3.50 | 7.25 | - |

**Cell 期刊必须传 `column_format=2` 或 `column_format=3`**，否则抛 ValueError。

### 2. 高亮结构图典型调用（`HighlightStructureImage`）

```python
image = HighlightStructureImage(structure_paths=["structure.pdb"])
image.set_cache(cache_contents=["residue:HOH"])            # 隐藏水分子
image.set_shape(representation_plan=[("chain:A", "surface"), ("chain:B", "cartoon")],
                independent_color=True, closed_surface=True)
image.set_state(rotate=[240, 340, 90])
image.set_color(coloring_plan=[("chain:A", "0xF2F2F2"), ("chain:B", "0x2D2F82")])
image.save(save_path="structure.png", width=1280, ratio=0.8)  # 高 = 1280*0.8=1024
image.close()   # 批量时务必 close() 释放 PyMOL 进程
```

### 3. 属性驱动结构图（`PropertyStructureImage`）

```python
image = PropertyStructureImage(structure_paths=["expected.pdb", "predicted.pdb"])
image.set_shape(representation_plan=[("model:predicted", "cartoon"), ("model:expected", "cartoon")])
image.set_state(rotate=[0, 60, 255], inner_align=True, target="expected")
image.set_color(target="model:predicted", color_map="rainbow", edge_color="0x000000",
                gauge_strengthen=True)   # putty 卡通，按属性值变化粗细
image.save(save_path="aligned.png", width=1800, ratio=0.5)
```

### 4. 出版级 Figure 排版

```python
fig = Figure(manuscript_format="Nature", occupied_columns=2, aspect_ratio=(606, 358),
             mathtext=False, row_number=2, column_number=2)
fig.set_image(image_path="1F34.png", layout=(1, 2, 1))           # 第1行第1列，占2行2列之一
fig.set_image(image_path="1AY7.png", layout=(2, 2, 3))
fig.set_image(image_path="1YCR.png", layout=(2, 2, 4))
fig.set_text(annotation="Stable Complex", locations=[0.5, 0.96, 0.4, 0.05])
fig.save_figure("fig.png")
```

### 5. 控件图标（旋转箭头/角度示意图）

```python
# 风格1：旋转方向 + 角度
obtain_widget_icon(save_path="arrow(90).png", widget_type="arrow",
                   params={"degree": 90, "color": "black", "linestyle": "-",
                           "width": 0.02, "head_width": 0.3, "head_length": 0.4})
# 风格2：方位角 + 仰角（分子旋转状态描述）
obtain_widget_icon(save_path="rot.png", widget_type="rotation",
                   params={"elevation": 30, "azimuth": 30}, dpi=1200)
```

**角度范围约束**：`arrow` 的 degree ∈ [0, 360]；`rotation` 风格1 degree ∈ [0, 180]，`turn` ∈ {"right","left"}；风格2 的 elevation/azimuth ∈ [-180, 180]，**不可同时为 0**（抛 ValueError）。

## 常见踩坑（必须提醒用户）

1. **PyMOL 进程泄漏**：每个 `*StructureImage` 实例都会 `PyMOL()` + `.start()` 起一个独立进程。**批量生成务必 `close()`**，否则几十个 PDB 会堆几十个进程把内存吃光。
2. **GUI 启动失败**：`windows.py` 必须在包含 `molpub` 目录的工作目录下运行；从其他目录直接跑会报模块找不到。解决：把 `windows.py` 拷到项目根目录再运行，或用 PyCharm/VSCode 加载整个项目运行。
3. **`set_state` 默认行为**：`only_rotate=False`（默认）会先 `center` + `orient` + `zoom(complete=1)`，再叠加 `rotate`；**若只想纯旋转不调视角**，传 `only_rotate=True`。
4. **`inner_align=True` 需要 ≥2 个结构**，否则无对齐对象。
5. **`PropertyStructureImage` 的 `gauge_strengthen` 只对 cartoon 表示生效**，surface/stick 下无效果。
6. **`save` 的 `dpi` 默认 1200**，**`Figure` 的 `minimum_dpi` 由期刊决定**（Nature=300, PNAS/ACS=600）。若插入的 PNG 实际 DPI 低于 `minimum_dpi`，`paste_bitmap` 会抛 ValueError——即 `image.save` 的 dpi 参数要 ≥ 期刊规格。
7. **`set_image` 只支持 `.png`**（代码里 `if image_format == ".png"` 硬判断），SVG/PDF 控件图标要手动栅格化后再嵌入。
8. **`locations` vs `layout` 二选一**，同时传会抛 ValueError；`layout` 是 (n_row, n_col, 顺序号) 元组。
9. **`set_panel_grid` 的占用检查**：`grid_params["l"]/["t"]` 是 0-based 行列偏移，`w`/`h` 是宽高；重叠位置会抛 ValueError。
10. **`mathtext=False`** 才启用 Linux Libertine / Lucida Calligraphy 数学字体；`mathtext=True` 用默认 mathtext（Arial/Helvetica 风格）。

## 最小可运行模板

> 以下为"自由模式"（不套预置风格）的最小示例；"选项模式"选模板后，按对应 yaml 的 `render.description` 现场生成等价脚本。

```python
from molpub import HighlightStructureImage, Figure, obtain_widget_icon

# 1) 结构图
img = HighlightStructureImage(structure_paths=["protein.pdb"])
img.set_cache(cache_contents=["residue:HOH"])
img.set_shape(representation_plan=[("chain:A", "cartoon"), ("chain:B", "surface")],
              closed_surface=True)
img.set_state(rotate=[30, 45, 0])
img.set_color(coloring_plan=[("chain:A", "0x2D2F82"), ("chain:B", "0xF2F2F2")])
img.save(save_path="protein.png", width=1280, ratio=0.9)
img.close()

# 2) 控件图标
obtain_widget_icon(save_path="arrow.png", widget_type="arrow", params={"degree": 90})

# 3) 出版级排版（Science 全宽）
fig = Figure(manuscript_format="Science", occupied_columns=3)
fig.set_image(image_path="protein.png", layout=(1, 1, 1))
fig.set_image(image_path="arrow.png", locations=[0.85, 0.8, 0.1, 0.1], transparent=True)
fig.set_text(annotation="(a)", locations=[0.02, 0.97, 0.08, 0.03])
fig.save_figure("final_figure.png")
```

## 调用方式速查（决策树）

```
用户提出绘图请求
   ├─ 提到"预置风格 / 选模板 / 套个风格"
   │     → 读 templates/_registry.md → 以选项呈现 → 用户挑
   │     → 按该 yaml params + 用户 PDB/链名/残基号 覆写占位符 → 现场生成脚本 → 出图
   │
   ├─ 提到"保存成模板 / 这风格记住 / 按这张图复现"
   │     → 4 步沉淀流程（复现→确认→命名→入库）
   │
   └─ 没提任何风格相关词
         → 自由模式：按输入内容 + 技能文档绘制（若高度匹配预置模板，可主动推荐 1 个）
```

## 技能自带资产

- `smoke_test.py`（本技能目录下）：冒烟测试脚本，验证 4 个核心类/函数（Default/Highlight/Property/Figure + obtain_widget_icon）在已装 PyMOL-PUB 的环境中可用。
  - 运行：`python <skill_dir>/smoke_test.py <本地 pdb 文件路径>`
  - 输出：`smoke_default.png`、`smoke_highlight.png`、`smoke_arrow.png`、`smoke_figure.png` 到当前工作目录。
  - 用作安装后"是否可用"的快速诊断（PyMOL 版本不对/字体缺/进程泄漏都能在这里暴露）。
- `templates/`（本技能目录下）：预置风格模板库。
  - `_registry.md`：预置风格清单（选项模式数据源），新增模板**必须**在此登记。
  - `_template_format.md`：模板 yaml 格式规范（meta/params/render 三块）。
  - `README.md`：机制说明 + 沉淀流程。
  - 预置 3 个标准类模板：`nature_highlight` / `rmsd_compare` / `science_publication_layout`。
  - 用户沉淀"直接 cmd"配方 13 个：`pastel_cartoon_surface`（按链）+ ss 配色族 `ss_milky_surface` / `ss_frosted_surface` / `ss_only_surface`（按二级结构）+ `residues_only`（关键残基棒）+ `spectrum_resi`（序列属性谱）+ `active_site_highlight`（活性位点特写）+ `distance_contact`（距离/极性接触）+ `goodsell_style`（Goodsell 平面化球）+ `mutation_site`（突变位点）+ `surface_render`（分子面）+ `ensemble_overlay`（多模型叠加）+ `dual_align_rmsd`（双结构对齐 RMSD）+ `ppi_interface`（蛋白-蛋白界面），各配 `.py` 参考脚本，均对 1AY7 出样图验证。

## 交付物约定（用户偏好）

- 图内文字标注**默认英文**（用户 2026-09-14 偏好）：panel 字母 A/B/C、轴标签、箭头注释都走英文。
- 文档正文与图注（figure caption）保持中文。
- 交付格式：PNG（300-600 DPI）+ 可选 PDF/SVG 矢量版；附 Markdown 图注一段。
- 若期刊要求 TIFF（部分期刊拒收 PNG），在 `save` 后另用 PIL 转 TIFF。

## 引用

Chen, Y., Zhang, H., Wang, W., Shen, Y., Ping, Z. (2024). Rapid generation of high-quality structure figures for publication with PyMOL-PUB. *Bioinformatics*, 40(3), btae139. https://doi.org/10.1093/bioinformatics/btae139

## 验证检查清单

- [ ] PyMOL 版本 = 2.5.0（`import pymol2; print(pymol2.__version__)` 输出 `2.5.0`）
- [ ] `molpub/fonts/` 在 matplotlib font_manager 里能被识别（`matplotlib.font_manager.findfont("Arial")` 不抛错）
- [ ] 结构文件链名与 `set_shape` 里的 `chain:X` 一致（PyMOL 默认链名是 A/B/C，与 PDB 文件 SEQRES 无关）
- [ ] `save` 的 dpi ≥ 期刊 `minimum_dpi`
- [ ] 批量生成时每个 `*StructureImage` 实例都 `close()` 了
- [ ] `Figure` 的 `minimum_dpi` 与目标期刊匹配（PNAS/ACS=600，其余 300~350）
- [ ] 若套模板：模板占位符（`{chain_A}` 等）已按实际 PDB 替换，参数化未被写死
- [ ] 若沉淀新模板：yaml 已存 `templates/` + `_registry.md` 已登记 + SKILL.md 章节已同步

### 直接 cmd 配方（`entry_class: null`）额外检查
出图前对"按配方渲染脚本"逐项核对，避免重踩 2.5.0 严格 API 的坑：
- [ ] 调用层用 `from pymol2 import PyMOL`，不是 `import pymol`（后者无 `.load`）
- [ ] 自定义调色板用 `cmd.set_color(name, rgb)`，不是 `cmd.set("color", ...)`
- [ ] 白底用 `cmd.bg_color("white")`，不是 `set("background_color", ...)`
- [ ] `cmd.hide(...)` 第一参是合法 representation：`everything` 合法、`all` 不合法；`hetatm` 是选区需配第一参 `everything`
- [ ] 拆对象 `cmd.create(cart, obj)` / `cmd.create(surf, obj)` 后，原 `obj` 要 `hide("everything", obj)` 藏掉，避免显示三层
- [ ] 二级结构选区 `ss h` / `ss s` / `not (ss h or ss s)`（loop）；按链则 `chain X`
- [ ] 出图 `cmd.ray()` 后再 `cmd.png(..., dpi=300)`；结束用 `mol.stop()`（不是 `close()`）
- [ ] 出图后用 PIL 验证文件真实存在且尺寸符合（避免 `png` 静默失败）

### 沉淀新配方的验证节奏（"先出样图、再入库"）
新配方未跑出可验证样图前**不得**写进 `_registry.md`。流程：
1. 按配方写出渲染脚本 → 用真实 PDB（如 1AY7）跑出样图
2. 用 PIL 校验样图（存在 / 尺寸 / 非空白）
3. 把验证过的脚本沉淀为 `templates/<名>.py`
4. 再写 `templates/<名>.yaml` + `_registry.md` 一行 + SKILL.md 同步
（本次 ss 配色族即按此节奏，避免把没验证过的写法当预置。）
