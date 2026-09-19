# 模板 YAML 格式规范

一个模板 = 一份 `.yaml` 文件，含 3 个顶层键：`meta`（元信息）、`params`（可覆写参数）、`render`（渲染脚本说明）。

## 格式

```yaml
meta:
  name: <模板英文标识，snake_case>        # 必给，用作文件名与选项卡片 key
  title: <中文标题>                       # 必给，用作选项卡片显示名
  scene: <适用场景一句话>                 # 必给
  reference: <参考图来源或"原创">         # 沉淀模板时填参考图路径；预置模板填"PyMOL-PUB cases"
  created: <ISO 日期 YYYY-MM-DD>
  created_by: <预置 | 用户沉淀 | 我自建>

params:                                    # 可覆写参数，调用方按 key 传入
  manuscript_format: Nature               # 期刊版式（8 选 1）
  occupied_columns: 2
  aspect_ratio: [606, 358]
  cache_contents: ["residue:HOH"]         # 隐藏项
  representation_plan: []                 # [(select, repr), ...]
  rotate: [330, 10, 270]
  coloring_plan: []                       # [(select, color), ...]
  save_width: 1280
  save_ratio: 0.9

render:
  description: |
    <说明该模板如何用 params 生成图>
    示例：HighlightStructureImage → set_cache → set_shape → set_state → set_color → save
  entry_class: HighlightStructureImage     # 该模板主用哪个 molpub 类
  extra_steps: |                          # 可选：模板专属的额外渲染逻辑（如控件图标、多结构对齐）
    无
```

## 参数覆写约定
- 调用方传入的 `params` **逐 key 合并**到模板 `params`，未传的保留模板默认。
- `coloring_plan` / `representation_plan` 里允许用占位符（如 `{chain_A}`、`{residues}`），调用方按 PDB 实际链名/残基替换。
- 模板内**不得写死**某次 PDB 的具体链号或残基号——必须参数化。

## 渲染脚本约定
- `render.entry_class` 指定主类，`render.description` 给调用顺序说明。
- 若模板需要多步骤（结构图 + 控件图标 + 排版），在 `extra_steps` 描述，渲染脚本（由我现场生成）按描述串起。
- 渲染脚本**始终**：每个 `*StructureImage` 实例 `close()`，`Figure.save` 的 dpi ≥ 期刊 `minimum_dpi`。

## 两种渲染范式（2.5.0 严格 API 实测）

模板的 `render.entry_class` 决定走哪条路：

### 范式 A：molpub 类（`entry_class` 非 null）
`nature_highlight` / `rmsd_compare` / `science_publication_layout` 走这条。按 `description` 顺序串 `set_cache → set_state → set_shape → set_color → save`，实例 `close()`。

### 范式 B：直接 cmd（`entry_class: null`）
用户沉淀配方（`pastel_cartoon_surface` + ss 配色族 3 个）走这条。**必用 `pymol2.PyMOL()` 调用层 + 2.5.0 严格 API**，骨架：

```python
from pymol2 import PyMOL
mol = PyMOL(); mol.start(); cmd = mol.cmd
cmd.load(PDB, OBJECT, quiet=1)
cmd.set_color("soft_blue", [0.63, 0.75, 0.94])     # 调色板：set_color 是命令，不是 set("color",...)
cmd.bg_color("white")                                  # 白底：bg_color，不是 set("background_color",...)
# 柔光参数一组：ambient / two_sided_lighting / ray_trace_mode /
#   ray_shadows / antialias / depth_cue / ray_trace_gain / orthoscopic / cartoon_fancy_helices...
cmd.set("ambient", 0.5)
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")   # 严格：第一参必须合法 representation（everything 合法、all 不合法）
cmd.hide("everything")
cmd.create(CART, OBJECT); cmd.create(SURF, OBJECT)   # 拆对象（需要 cartoon/surface 分色时）
cmd.hide("everything", OBJECT)
cmd.show("cartoon", CART)
cmd.show("surface", SURF)
# 上色：按链（CART and chain A）或按二级结构（CART and ss h / ss s / not(ss h or ss s)）
cmd.orient(CART); cmd.ray()
cmd.png(SAVE, width=1600, height=1600, dpi=300, quiet=1)
mol.stop()   # 是 stop() 不是 close()
```

**踩坑速查（都已回填 SKILL.md「配方迁移踩坑」）**：
- `import pymol` 当调用层无 `.load` → 必须 `from pymol2 import PyMOL`。
- `cmd.hide("hetatm")` / `cmd.hide("all", ...)` 报错 → `hide` 第一参合法 representation。
- `cmd.set("color", ...)` / `cmd.set("background_color", ...)` 报错 → 用 `set_color` / `bg_color`。
- `ss_only` 不拆对象：直接 `show cartoon` + 对 `OBJECT` 按 ss 上色，`orient(OBJECT)`。

## 命名规范
- 模板名：`<场景>_<视觉特征>`，如 `nature_binding_site`、`cell_membrane_cartoon`、`rmsd_compare`。
- 文件名 = `meta.name` + `.yaml`。
