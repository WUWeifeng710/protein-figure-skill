# 预置风格注册表

> 这是"用户提出预置风格选择"时，我读取并提供选项的数据来源。
> 沉淀新模板时，**必须**同步在此加一行。

| 模板文件 | 显示名 | 适用场景 | 入口类 | 备注 |
|---|---|---|---|---|
| `nature_highlight.yaml` | Nature 高亮复合结构图 | 单结构多链高亮，突出结合位点 / 突变 / 关键区段 | `HighlightStructureImage` | 中性表面 + 活性卡通 + 高亮区段 |
| `rmsd_compare.yaml` | 双结构 RMSD / 属性对比图 | expected vs predicted / WT vs mutant 叠合对齐 + 残基差异渐变 | `PropertyStructureImage` | putty cartoon，彩虹谱 |
| `science_publication_layout.yaml` | Science 全宽多面板出版排版 | 多图 + 面板 + 文字 + 控件拼成出版级 Figure | `Figure` | 3 列全宽，子图 dpi ≥ 300 |
| `pastel_cartoon_surface.yaml` | 粉彩链着色 cartoon + 乳白半透明 surface | 单结构多链粉彩 cartoon + 乳白 surface 壳，白底柔光发表级 | 直接 `cmd`（不用 molpub 类） | 拆对象分色，自定义 4 色粉彩，用户沉淀自 recipe.pml |
| `ss_milky_surface.yaml` | 二级结构粉彩 cartoon + 乳白中性 surface | cartoon 按二级结构（h/s/loop）粉彩 + 中性 gray90 壳，适合突出二级结构 | 直接 `cmd`（不用 molpub 类） | 拆 cart/surf，ss 选区上色，用户沉淀自 recipe_1_ss_milky.pml，**已对 1AY7 出样图验证** |
| `ss_frosted_surface.yaml` | 二级结构粉彩 cartoon + 同色磨砂 surface | cartoon 按 ss 粉彩，surface 同色 0.60 透磨砂玻璃，色更饱满 | 直接 `cmd`（不用 molpub 类） | surface 与 cartoon 同色呼应，用户沉淀自 recipe_2_ss_frosted.pml，**已对 1AY7 出样图验证** |
| `ss_only_surface.yaml` | 纯二级结构粉彩 cartoon（无 surface） | 仅 cartoon 按 ss 粉彩、无壳，干净线条不遮挡 | 直接 `cmd`（不用 molpub 类） | 不拆对象直接对 m 上色，用户沉淀自 recipe_3_ss_only.pml，**已对 1AY7 出样图验证** |
| `residues_only.yaml` | 关键残基棒特写（隐藏蛋白只显 sticks） | 整条蛋白隐藏，只显若干关键残基柔和粉彩 sticks，视线聚焦局部位点 | 直接 `cmd`（不用 molpub 类） | 残基选区 + `show sticks`，用户沉淀自 recipe_5_residues_only.pml，**已对 1AY7 出样图验证** |
| `spectrum_resi.yaml` | 序列位置属性谱着色（蓝白红渐变 cartoon + CA 球） | cartoon 按残基位置连续渐变，展示 B-factor/pLDDT/序列属性分布 | 直接 `cmd`（不用 molpub 类） | `cmd.spectrum(resi,...)`，2.5.0 不认 bfactor 槽用 resi 替代，参考 PyMolClaw spectrum.py，**已对 1AY7 出样图验证** |
| `active_site_highlight.yaml` | 活性位点特写（sticks + 半透明 cartoon 环境 + 极性接触） | 关键残基 sticks + CA 球 + around 半径半透明环境 cartoon + 残基间极性接触虚线 | 直接 `cmd`（不用 molpub 类） | `select+extend` 合并选区，参考 PyMolClaw active_site.py，**已对 1AY7 出样图验证** |
| `distance_contact.yaml` | 残基对距离 / 极性接触标注 | 两残基 sticks+CA 球 + `dist mode=2` 距离虚线，适合结合位点距离标注 | 直接 `cmd`（不用 molpub 类） | `sc. and (s1 or s2)`，参考 PyMolClaw distance.py，**已对 1AY7 出样图验证** |
| `goodsell_style.yaml` | Goodsell 风格平面化粉彩球（按链） | 球状模型按链上 Goodsell 粉彩（gs_*），白底无阴影 flat 渲染，期刊封面级 | 直接 `cmd`（不用 molpub 类） | `ray_trace_mode=3` + `ambient=1.0` + `ray_shadows=0`，参考 PyMolClaw goodsell.py，**已对 1AY7 出样图验证** |
| `mutation_site.yaml` | 突变位点结构分析（单残基 + 环境 cartoon） | 指定突变残基 sticks+CA 球 + around 半径半透明环境 cartoon + salmon/red 色相区分 | 直接 `cmd`（不用 molpub 类） | 单残基特写，参考 PyMolClaw mutation.py，**已对 1AY7 出样图验证** |
| `surface_render.yaml` | 分子面渲染（按链分色 + 半透明） | 独立 surface / mesh / dots，按链分色 + 半透明，展示分子面形状 / 结合口袋 | 直接 `cmd`（不用 molpub 类） | 2.5.0 不 `set surface_quality`，内置色分链，参考 PyMolClaw surface.py，**已对 1AY7 出样图验证** |
| `ensemble_overlay.yaml` | NMR / MD 多模型叠加（state 渐变） | 多模型按 state 彩虹渐变 + 半透明，展示结构柔性 / 构象系综 | 直接 `cmd`（不用 molpub 类） | `spectrum state`（单帧退化可忽略），参考 PyMolClaw ensemble.py，**已对 1AY7 出样图验证** |
| `dual_align_rmsd.yaml` | 双结构叠合对齐 + RMSD | 两结构按 CA align + RMSD + 叠合 cartoon（color1/color2 + 半透明） | 直接 `cmd`（不用 molpub 类） | 对象名避保留字 s1/s2，参考 PyMolClaw align.py，**已对 1AY7 自叠合验证** |
| `ppi_interface.yaml` | 蛋白-蛋白界面（within 半径 + 界面残基 sticks） | 两链 within 半径取界面残基 + sticks+CA 球 + 界面半透明面 | 直接 `cmd`（不用 molpub 类） | `byres within` 选区，参考 PyMolClaw ppi.py，**已对 1AY7 出样图验证** |

## 残基棒（residues_only）配色族说明
- `residues_only` 属「只显残基棒」族：与 ss/pastel 的「cartoon + 壳」族正交——蛋白体完全不显示，仅对 `key_residues` 指定的残基 `show sticks` + 柔和粉彩（`sh_*` 前缀配色，区别于 ss 族的 `soft_blue/rose_pink`）。
- 适合突出催化/结合/突变位点；`key_residues` 选区可带链前缀（`A/35`），残基号需对目标 PDB 实际存在。

## 二级结构（ss）配色族说明
- `ss_milky` / `ss_frosted` / `ss_only` 三个同属「按二级结构上色」族：soft_blue=ss h（α 螺旋）、rose_pink=ss s（β 折叠）、lavender=loop。
- 三者差异仅在 surface：milky=中性灰壳，frosted=同色磨砂壳，only=无壳。
- 与 `pastel_cartoon_surface`（按链上色）不同：ss 族按结构元素上色，不拆链。

## 属性/位点特写族（spectrum_resi / active_site_highlight）
- `spectrum_resi`：按残基位置连续渐变（蓝白红），适合 B-factor/pLDDT/序列属性分布。**2.5.0 坑：`spectrum` 不认 `bfactor` 槽名，用 `resi` 替代；PDB 带 b 列可试 `b`、带 plddt 列可试 `plddt`。**
- `active_site_highlight`：局部位点机制图——关键残基 sticks+CA 球，`byres around` 取半透明 cartoon 环境，`dist mode=2` 画极性接触。**2.5.0 坑：`select` 严格模式不吃 `+`/`or` 拼接，用 `select`+`extend` 做选区加法。**

## 排序约定（提供选项时按此顺序）
1. 场景最贴切的排前面（我按用户本次输入判断）。
2. 同场景按创建时间倒序。
3. 预置模板优先于用户沉淀模板（沉淀模板是"个人风格"，预置是"通用风格"，通用在前避免覆盖习惯）。

## 维护规则
- 新增模板：写 yaml → 在本表加一行 → 同步 `SKILL.md` 的"预置风格选择"章节。
- 删除/重命名模板：本表与 `SKILL.md` 同步改。
- 模板 yaml 内**不得**引用本表外的资源；自包含。
