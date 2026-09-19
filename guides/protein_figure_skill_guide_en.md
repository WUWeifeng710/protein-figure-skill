# Protein Structure Publication Figures · Skill Usage Guide (English)

> A `protein-figure` skill built on PyMOL-PUB (Bioinformatics 2024, btae139) and the PyMOL 2.5.0 open-source edition.
> Ships with 10 direct-cmd style recipes + 3 standard-class templates, all validated against 1AY7.

## 1. What This Skill Does

Renders protein/nucleic-acid 3D structures (PDB/PDBx) into **journal-ready** figures: white background, 300–600 DPI, in-figure labels default to English, publication-grade palettes. It covers three needs:

- **Journal-spec layouts**: Nature/Science/Cell/PNAS/ACS/Oxford/PLOS/IEEE fonts, column widths, minimum DPI handled automatically.
- **Highlighting regions**: binding sites, mutations, key residues, active centers with custom palettes.
- **Comparison & mechanism figures**: dual-structure RMSD overlays, residue-pair distances / polar contacts, protein–protein interfaces, NMR/MD ensembles.

## 2. Environment & Installation (one-time)

Hard constraint: Python 3.9–3.11 + **PyMOL must equal 2.5.0** (open source) + `PyMOL-PUB`.

Recommended conda-forge route (validated; env name `pymol_pub` is just a convention):

```
conda create -n pymol_pub python=3.11 -c conda-forge -y
conda install -n pymol_pub -c conda-forge "pymol-open-source=2.5.0" -y
conda run -n pymol_pub python -m pip install PyMOL-PUB
```

Verify:

```
conda run -n pymol_pub python -c "import pymol2; print(pymol2.__version__)"
# expected: 2.5.0
```

> Note: conda-forge's `pymol-open-source` is the reliable source for 2.5.0; the
> gohkle third-party wheels and PyPI's `pymol-open-source` (only 3.x alphas) cannot
> deliver 2.5.0 — avoid both.

## 3. Two Rendering Paradigms

| Paradigm | What | When |
|---|---|---|
| **A: standard classes (molpub)** | `HighlightStructureImage` / `PropertyStructureImage` / `Figure` | Journal layouts, multi-panel publication figures, RMSD property shading |
| **B: direct cmd (`entry_class: null`)** | `from pymol2 import PyMOL` + hand-written cmd sequence | Custom palettes / soft-light / flat look that exceed the class API (all 10 direct-cmd recipes) |

Calling-layer rule: `mol = PyMOL(); mol.start(); cmd = mol.cmd`, end with `mol.stop()`. Do **not** use `import pymol` as the calling layer.

### 2.5.0 Strict-API Cheatsheet (top 6 gotchas)

1. Custom palettes via `cmd.set_color(name, [r,g,b])`, **not** `set("color", ...)`.
2. White background via `cmd.bg_color("white")`, **not** `set("background_color", ...)`.
3. Cleanup via `cmd.hide("everything","hetatm")` + `cmd.hide("everything")`; first arg of `hide` must be a valid representation (`everything` ok, `all` not).
4. Merge multi-residue selections with `cmd.select` + `cmd.extend` step-by-step; named selections reject `+`/`or` concatenation.
5. `cmd.spectrum("bfactor", ...)` is not recognized → use `resi` (or `b` if the PDB has a B column, `plddt` if it has a pLDDT column).
6. Keep object names off reserved words (`a`/`b` get an underscore appended); prefer `s1`/`s2`.

## 4. Style Recipe Overview (10 direct-cmd + 3 standard)

### 4.1 Direct-cmd style recipes

| Recipe | Look | Typical use |
|---|---|---|
| `pastel_cartoon_surface` | Per-chain cartoon + milky translucent shell | Multi-chain pastel overview |
| `ss_milky_surface` | Per-secondary-structure cartoon + neutral gray shell | Emphasize α/β/loop |
| `ss_frosted_surface` | Per-secondary-structure cartoon + same-color frosted shell | Richer secondary-structure look |
| `ss_only_surface` | Pure secondary-structure cartoon, no shell | Clean, unobstructed lines |
| `residues_only` | Hide whole protein, show only key-residue sticks | Focused local site |
| `spectrum_resi` | Cartoon graded blue-white-red by residue index + CA spheres | B-factor / pLDDT / sequence-property spread |
| `active_site_highlight` | Key-residue sticks + translucent cartoon environment + polar-contact dashes | Active-site mechanism view |
| `distance_contact` | Two-residue sticks + CA spheres + distance dashes (`dist mode=2`) | Binding-site distance annotation |
| `goodsell_style` | Sphere model, per-chain Goodsell pastel, flat no-shadow white render | Journal-cover-grade illustration |
| `mutation_site` | Single mutation-residue sticks + CA spheres + env cartoon + salmon hue | Mutation-site analysis |
| `surface_render` | Per-chain independent surface/mesh/dots + transparency | Molecular-surface shape / pocket |
| `ensemble_overlay` | Multi-model state rainbow gradient + transparency | NMR/MD flexibility |
| `dual_align_rmsd` | Two structures CA-aligned + RMSD + overlaid cartoon | WT vs mutant / expected vs predicted |
| `ppi_interface` | Two chains `within` radius → interface residues + translucent interface surface | Protein–protein interface |

> Note: `_registry.md` lists 17 template rows (3 standard classes + 10 direct-cmd + scene-level entries); the table above lists the 14 independently renderable recipes.

### 4.2 Standard-class templates (molpub)

| Template | Entry class | Purpose |
|---|---|---|
| `nature_highlight` | `HighlightStructureImage` | Multi-chain highlight, emphasize binding site / mutation / segment |
| `rmsd_compare` | `PropertyStructureImage` | Dual-structure RMSD/property overlay + putty cartoon residue difference |
| `science_publication_layout` | `Figure` | Multi-image + panels + text + widgets into a publication Figure |

## 5. Case 1: Goodsell cover-grade illustration (direct cmd)

Goal: render 1AY7's two chains as the "flat pastel spheres" look common on journal covers.

```python
# goodsell_style.py (validated on 1AY7)
from pymol2 import PyMOL
PDB, OBJECT = "1AY7.pdb", "m"
CHAIN_COLORS = {"A": "gs_blue", "B": "gs_red"}   # only chains that exist in the PDB
mol = PyMOL(); mol.start(); cmd = mol.cmd
cmd.load(PDB, OBJECT, quiet=1)
if int(cmd.count_atoms("all")) == 0:
    raise SystemExit("LOAD FAILED: 0 atoms")
# Flat: high ambient, zero reflect, no shadow
for k, v in {"ray_trace_mode":3, "ray_shadows":0, "depth_cue":0}.items():
    cmd.set(k, v)
cmd.set("ambient", 1.0); cmd.set("direct", 0.0); cmd.set("reflect", 0.0)
cmd.bg_color("white"); cmd.orthoscopic(1)
# Custom colors must be defined in the same instance
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

Result (1AY7, 1600×1600, 300 DPI):

![Goodsell flat pastel spheres (per-chain, white bg, no shadow)](1AY7_goodsell.png)

## 6. Case 2: Active-site close-up (direct cmd)

Goal: blow up a handful of key residues as sticks, keep a translucent cartoon environment, and draw polar-contact dashes between residues.

```python
# active_site_highlight.py key fragment
KEY = ["A/35", "A/52", "B/44"]            # key residues (with chain prefix)
cmd.show("cartoon", "m"); cmd.color("gray80", "m"); cmd.set("cartoon_transparency", 0.7)
merged = "msite"
for i, r in enumerate(KEY):
    cmd.select("tmp%d" % i, r)
    cmd.extend(merged, "tmp%d" % i)        # named selections merged via select+extend (no + concat)
cmd.show("sticks", merged); cmd.show("spheres", "byres merged and type c")
cmd.color("gs_red", "byres merged and type c")
for i in range(len(KEY)-1):                # polar-contact dashes
    cmd.dist("d%d" % i, "%s" % KEY[i], "%s" % KEY[i+1], mode=2, color="yellow")
cmd.orient(merged); cmd.zoom("m", 1.4); cmd.ray()
cmd.png("1AY7_active_site.png", width=1600, height=1600, dpi=300, quiet=1)
```

Result:

![Active-site close-up (sticks + translucent cartoon env + polar contacts)](1AY7_active_site.png)

## 7. Case 3: Dual-structure RMSD overlay (standard class)

Goal: expected vs predicted overlay with a putty cartoon rainbow map of residue differences.

```python
from molpub import PropertyStructureImage
img = PropertyStructureImage(structure_paths=["expected.pdb", "predicted.pdb"])
img.set_shape(representation_plan=[("model:predicted","cartoon"), ("model:expected","cartoon")])
img.set_state(rotate=[0,60,255], inner_align=True, target="expected")
img.set_color(target="model:predicted", color_map="rainbow",
              edge_color="0x000000", gauge_strengthen=True)   # cartoon only
img.save(save_path="1AY7_align.png", width=1800, ratio=0.5)
img.close()   # always close to free the PyMOL process when batching
```

Result (self-overlay demo):

![Dual-structure overlay + RMSD](1AY7_align.png)

## 8. Case 4: Journal layout (standard class Figure)

Goal: compose several structure images + rotation widget icons + text into a Nature two-column publication figure.

```python
from molpub import Figure, obtain_widget_icon
obtain_widget_icon(save_path="arrow.png", widget_type="arrow",
                   params={"degree": 90, "color": "black", "width": 0.02})
fig = Figure(manuscript_format="Nature", occupied_columns=2,
             aspect_ratio=(606,358), mathtext=False, row_number=2, column_number=2)
fig.set_image(image_path="1AY7_goodsell.png", layout=(1,1,1))
fig.set_image(image_path="arrow.png", locations=[0.85,0.8,0.1,0.1], transparent=True)
fig.set_text(annotation="(a)", locations=[0.02,0.97,0.08,0.03])
fig.save_figure("final_figure.png")   # sub-figure dpi must be >= journal minimum_dpi
```

## 9. Publication Quality Constraints (check these)

| Journal | Font | Min DPI | Max cols |
|---|---|---|---|
| Nature | Arial | 300 | 2 |
| Science | Helvetica | 300 | 3 |
| Cell | Arial | 300 | 2(3) |
| PNAS | Helvetica | **600** | 2 |
| ACS | Arial | **600** | 2 |
| Oxford | Arial | 350 | 2 |

- `save` defaults to `dpi=1200`; `Figure.minimum_dpi` is journal-driven — if a sub-figure PNG's real DPI is below it, `paste_bitmap` raises ValueError.
- Cell must be passed `column_format=2` or `3`.
- `set_image` accepts only `.png`; rasterize SVG/PDF widget icons before embedding.

## 10. Advanced Rendering Parameters (OPIG)

| Parameter | Effect | Suggested |
|---|---|---|
| `surface_quality` | Surface normal / mesh precision | 10–40 (**not settable in 2.5.0 strict mode — known gotcha**) |
| `cartoon_sampling` | Cartoon sampling density | 2–4 |
| `cartoon_line_width` | Cartoon outline width | 0.6–2.0 |
| `ray_quality` / `ray_simplify` | Ray-trace quality / simplification | 0–1 |
| `ray_opaque_background` | Opaque white background | 1 (stable when headless, no GPU) |
| `field_of_view` | Perspective distortion | default 30–45 for publication |

One-line publication cartoon: `cmd.preset("publication", "m")` (works in 2.5.0; `preset.pretty` is degraded in 2.x).

## 11. Deliverables & Preferences

- **In-figure labels default to English** (panel A/B/C, axes, arrow notes, colorbars; gene/species names stay English); document body & captions in Chinese.
- Deliverables: PNG (300–600 DPI) + optional PDF/SVG; for journals requiring TIFF, convert from PNG with PIL.
- Rhythm rule: **no recipe enters `_registry.md` before a verifiable sample render** — first render a real PDB, PIL-validate (exists / size / non-blank), then register.

## 12. Sample Gallery (all 1AY7, 1600×1600, 300 DPI)

### Direct-cmd recipe results

![pastel per-chain cartoon + milky shell](1AY7_pastel.png)
![ss_milky secondary-structure cartoon + neutral shell](1AY7_ss_milky.png)
![ss_frosted secondary-structure cartoon + same-color frosted shell](1AY7_ss_frosted.png)
![ss_only pure secondary-structure cartoon](1AY7_ss_only.png)
![residues_only key-residue sticks close-up](1AY7_residues_only.png)
![spectrum residue-position blue-white-red gradient](1AY7_spectrum_bfactor.png)
![distance residue-pair annotation](1AY7_distance.png)
![mutation site structural analysis](1AY7_mutation.png)
![surface molecular surface per-chain](1AY7_surface.png)
![ensemble multi-model overlay](1AY7_ensemble.png)
![ppi protein-protein interface](1AY7_ppi.png)

### Standard-class results

![rmsd dual-structure overlay](1AY7_align.png)

## Citation

Chen, Y., Zhang, H., Wang, W., Shen, Y., Ping, Z. (2024). Rapid generation of high-quality structure figures for publication with PyMOL-PUB. *Bioinformatics*, 40(3), btae139. https://doi.org/10.1093/bioinformatics/btae139
