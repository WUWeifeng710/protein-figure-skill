---
name: protein-figure
description: >
  Publication-grade 3D protein structure figures. High-level wrapper around PyMOL-PUB (Bioinformatics 2024, btae139):
  journal-spec layouts, structure rendering (highlight / property colouring / alignment), rotation and arrow widget icons,
  publication-grade Figure composition.
  Triggers: protein figure, molecular structure figure, publication figure, PyMOL publication figure,
  protein 3D structure publication figure, journal figure layout, molecular highlight figure, RMSD structure comparison.
  Supports preset style template selection (templates/ dir) and custom template sedimentation (see figure → confirm → save).
agent_created: true
created_at: 2026-09-18
---

# Protein-Figure skill: publication-grade 3D protein structure figures

## When to use

When the user needs a **publication-ready** protein / nucleic-acid 3D structure figure (PNG/SVG), especially when:
- conforming to a specific journal's font / DPI / column-width spec (Nature / Science / Cell / PNAS / ACS / Oxford / PLOS / IEEE);
- highlighting a specific region (chain / segment / residues) with custom colours;
- dual-structure overlay (expected vs predicted) aligned, using colour gradient + cartoon thickness to encode differences (e.g. RMSD spectrum);
- composing multiple structure panels + matplotlib panels + text / widget icons into a complete publication-grade Figure.

**Not applicable**: purely 2D schematic figures (hand-drawn / chemdraw), non-protein molecules (small-molecule-centric — PyMOL can do it but it is not the core scene), interactive 3D display.

## Prerequisites & installation

### Hard constraints
- **Python >= 3.7.3**; 3.9–3.11 recommended.
- **PyMOL version must equal 2.5.0** (open-source; `pip install pymol` on Windows may not yield 2.5.0; the official open-source download page is https://pymol.org/2/#download).
  - Linux distro and open-source install paths differ; **prefer the open-source build**; the distributed build (2.5.7 bundles Python 3.9) pins a specific Python env and conflicts with pip-installed molpub.
- Other deps: `biopython>=1.78`, `matplotlib>=3.2.0`, `numpy>=1.21.2`, `pillow>=8.2.0`, `scipy>=1.4.1`, `sphinx-rtd-theme>=0.4.3`, `PyQt5>=5.15.9` (GUI only).

### Install routes (pick one of three, situation-dependent)

1. **conda-forge (recommended, defaults to 2.5.0, reproducible)**
   ```bash
   conda create -n pymol_pub python=3.11 -c conda-forge -y
   conda install -n pymol_pub -c conda-forge "pymol-open-source=2.5.0" -y
   # enter the env then install PyMOL-PUB (conda activate, or just run the env's python directly)
   conda run -n pymol_pub python -m pip install PyMOL-PUB
   ```
   - Env name `pymol_pub` is arbitrary; the key is to **pin `pymol-open-source` to 2.5.0**.
   - envs land under `~/.conda/envs` (Windows) / `$CONDA_HOME/envs` (Linux/mac) by default — **not** inside the conda install dir.

2. **gohlke third-party wheel (fallback when no conda, match Python version)**
   - `github.com/cgohlke/pymol-open-source-wheels` (releases carry 2.5.x win_amd64 wheels)
   - Bundle `Pmw` + `numpy(+mkl)` — install all three with `pip install --no-index --find-links`
   - Must match the Python version (e.g. cp38/cp311); before install, confirm the local Python tag matches the wheel.

3. **Download the open-source PyMOL directly from the official site** (`https://pymol.org/2/#download`, pick 2.5.0), then `pip install PyMOL-PUB`.

**Post-install check**:
```bash
python -c "import pymol2; print(pymol2.__version__)"   # expect 2.5.0
python -c "from molpub import HighlightStructureImage; print('molpub OK')"
```

**Note**: any source that delivers a 2.5.x build must be verified as **2.5.0** (not 2.5.7 or a newer minor); PyPI's `pymol-open-source` only carries 3.x alphas — **do not use that route**.

## Recipe migration pitfalls (recipe.pml → 2.5.0 strict API, all validated)

When migrating PyMOL command-line recipes to `pymol2.PyMOL().cmd`, conda-forge 2.5.0 enforces stricter validation than older recipes (empirical results from the `pastel_cartoon_surface` recipe):

- **Import**: use `from pymol2 import PyMOL; mol = PyMOL(); mol.start(); cmd = mol.cmd`. Do **not** use `import pymol` as the call layer — the module itself has no `.load` and other commands.
- **`cmd.set("color", name, rgb)` errors**: for a custom palette use `cmd.set_color(name, [r,g,b])` (`set_color` is a command; the color slot of `set` does a bool check).
- **`cmd.hide("hetatm")` / `cmd.hide("all", ...)` errors**: the first arg of `hide` must be a legal representation (legal values include `everything` but not `all`); `hetatm` is a selection, not a representation. Correct: `cmd.hide("everything", "hetatm")` + `cmd.hide("everything")`.
- **`cmd.show("cartoon", obj)` / `cmd.color(...)` / `cmd.create(...)` / `cmd.orient` / `cmd.ray` / `cmd.png(dpi=300)` work fine**.
- Applying the first two pastel colours to 1AY7 (chains A & B): soft_blue / rose_pink, `ray()` + `png(1600,1600,dpi=300)` renders in about 13 s.
- **`cmd.spectrum("bfactor", ...)` reports "Unknown expression: bfactor"**: 2.5.0's `spectrum` does not accept the `bfactor` slot. What works is `spectrum resi ...` (by residue position); if the PDB has a b column try `spectrum b ...`, if it has a plddt column try `spectrum plddt ...`. For a "true B-factor gradient" use the `b` slot (not `bfactor`).
- **`cmd.select` with named selections does not accept `+` operator concatenation** (reports "Invalid selection name", e.g. `m and (resi 35+resi 52)` is mis-parsed); `count_atoms` accepts it but `select` does not. For merged multi-residue selections use **`cmd.select` + `cmd.extend`** step by step, or `select` each one then `extend`. `byres`/`around` selections must be made **after** `hide("everything")` (hide clears the selection).

## One-line presets & advanced render parameters (reusable on 2.5.0)

### Official built-in presets (one line for publication-grade cartoon)
Simpler than manually setting a whole group of soft-light parameters. In conda-forge 2.5.0 the `preset` command is still available (note: 1.x's `preset.pretty` has degraded behaviour on 2.x; `preset.publication` internally stacks cartoon parameters, so it still works on 2.5.0):

| preset | Use | 2.5.0 note |
|---|---|---|
| `preset.publication` | One-line publication cartoon (fancy helices + smooth loops + grey highlight) | **Preferred**, works on 2.5.0 |
| `preset.pretty` | General pretty cartoon | Effect is discounted on 2.x; on its own inferior to publication |
| `preset.simple` | Skeleton lines only | Fast, minimal |
| `preset.ball_and_stick` | Ball & stick | Small molecules |
| `preset.b_factor_putty` | B-factor putty thickness | Pairs with the `PropertyStructureImage` gauge |
| `preset.technical` | Polar contact lines + residue sticks | Binding-site analysis |
| `preset.ligand_sites` | Ligand binding sites | Ligand scenes |

`cmd.preset("publication", "m")` applies a publication-grade look to object `m` in one line, then layer custom colour / selection on top. Recipes can use presets to replace the hand-written soft-light parameter group (see the set-string in "Recipe migration pitfalls" §2).

### Advanced render parameters (OPIG experience, finer than just antialias)
| Param | Effect | Recommended value |
|---|---|---|
| `surface_quality` | Surface normal / mesh precision | 10–40 (default 20, higher = smoother) |
| `cartoon_sampling` | Cartoon sampling density | 2–4 (default 2) |
| `cartoon_line_width` | Cartoon outline thickness | 0.6–2.0 |
| `ray_quality` / `ray_simplify` | Ray-trace quality / simplification | 0–1 (1 = simpler, faster) |
| `zoom` / `zoom complete` | Move the camera closer | Use together with `orient` |
| `ray_opaque_background` | Opaque white background | 1 (stable white bg when headless with no GPU) |
| `field_of_view` (fov) | Perspective distortion | Larger = closer; use the default 30–45 for publication |

### Load verification (mandatory before rendering; fills the hole PIL cannot catch)
PIL can only verify "file is not empty / correct size"; it cannot catch the case where **the selection actually hits 0 atoms, resulting in a blank figure**. Following deepmind's pymol approach, the render script verifies immediately after `cmd.load`:
```python
if int(cmd.count_atoms("all")) == 0:
    print("LOAD FAILED: 0 atoms after load"); mol.stop(); sys.exit(1)
```
For critical selections (`k_residues`, highlight segments) also verify `cmd.count_atoms(sel) > 0`; if 0, raise an error instead of silently outputting a blank figure.

## Expandable reference for uncovered scenes (PyMolClaw 13-script family)

`BioTender-max/PyMolClaw` (github.com/BioTender-max/PyMolClaw) provides 13 reusable PyMOL scripts. **All 13 scenes have been delivered** (rewritten to 2.5.0 strict API + validated with 1AY7 sample figures), so there is no longer a dependency on that repo — the templates below are self-contained:

| Scene | Script | Status |
|---|---|---|
| Sequence-position property spectrum colouring | `spectrum.py` | Done → `spectrum_resi` |
| Active-site close-up | `active_site.py` | Done → `active_site_highlight` |
| Goodsell-style scientific illustration | `goodsell.py` | Done → `goodsell_style` |
| Distance / polar contact | `distance.py` | Done → `distance_contact` |
| Mutation-site structural analysis | `mutation.py` | Done → `mutation_site` |
| Molecular surface rendering | `surface.py` | Done → `surface_render` |
| NMR / MD ensemble | `ensemble.py` | Done → `ensemble_overlay` |
| Structure alignment + RMSD | `align.py` | Done → `dual_align_rmsd` |
| Protein-protein interface | `ppi.py` | Done → `ppi_interface` |

**Note**: PyMolClaw follows a headless route (`pymol -c -q`), which can coexist with our conda PyMOL 2.5.0 + `cmd.ray()` route; when importing its scripts, adapt to the 2.5.0 strict API per that README (same set as "Recipe migration pitfalls").

## Items deliberately not adopted (reasons recorded to avoid re-evaluation)
- **pymolrc / EZ-Viz interactive auto-beautify**: we "render on demand" rather than "beautify on load" — does not fit the workflow, skip.
- **deepmind's OSMesa software-render route** (uv + `pymol-open-source-whl` + forced `cmd.png` instead of `cmd.ray`): conflicts with our conda 2.5.0 + `cmd.ray()` route. **We only borrow two ideas: the `count_atoms` load verification, and "when headless / no GPU, ray is unreliable → fall back to png".** No wholesale change of the render engine.

## Recipe migration pitfalls supplement (from deepmind pymol experience, now incorporated)
- Headless / no-GPU environments: `cmd.ray()` may fail or be slow; fall back to `cmd.png` (standard OpenGL software rasterisation) + `ray_opaque_background=1` to keep a white background.
- At the end of every render script call `mol.stop()` (pymol2 route); the deepmind `import pymol` route calls `cmd.quit()` — do not mix the two.

2. **gohlke third-party wheel (fallback when no conda, match Python version)**
   - `github.com/cgohlke/pymol-open-source-wheels` (releases carry 2.5.x win_amd64 wheels)
   - Bundle `Pmw` + `numpy(+mkl)` — install all three with `pip install --no-index --find-links`
   - Must match the Python version (e.g. cp38/cp311); before installing, confirm the local Python tag matches the wheel

3. **PyPI `pymol-open-source` package (alpha only, version mismatch, not recommended)**
   - PyPI only has 3.1.0a0 / 3.2.0a0, and only 3.2.0a0 ships a win_amd64 wheel — **3.x ≠ 2.5.0, conflicts with the PyMOL-PUB requirement**, do not use this route

4. **Compile from source (last resort)**
   - `github.com/schrodinger/pymol-open-source`, Windows compile cost is high, not recommended

Post-install check: `python -c "import pymol2; print(pymol2.__version__)"` should print `2.5.0`.

**Note**: any 2.5.x obtained via gohkle / conda must also be confirmed pinned to **2.5.0** (not a newer minor like 2.5.7).

### Prerequisite check (read this before rendering any sample)
**Whether auto-rendering works = depends on whether PyMOL is installed** — this is a manual prerequisite:
- If PyMOL is not installed locally (`import pymol2` raises ModuleNotFoundError) → first install 2.5.0 following the routes above, then `pip install PyMOL-PUB`, finally run `smoke_test.py` or the template render script.
- Also confirm whether `conda` is available locally; if conda is available, `conda install -c schrodinger "pymol=2.5.0"` is more convenient than downloading from the official site.
- All render scripts follow the form "receive PDB path + template name + override params"; once the environment is ready, run directly.

### Fonts
molpub ships a built-in TTF font directory `molpub/fonts/` ("Times New Roman", "Helvetica", "Arial", "Linux Libertine", "Lucida Calligraphy"), auto-registered with matplotlib on import — **no manual font installation needed**.

## API call style

All classes / functions are imported from `molpub` or `molpub.layouts`:
```python
from molpub import (DefaultStructureImage, HighlightStructureImage,
                    PropertyStructureImage, Figure, obtain_widget_icon)
```

### Core classes & capabilities

| Class / function | Use | Key methods |
|---|---|---|
| `DefaultStructureImage` | Structure-image base: load PDB, rotate / zoom / align / hide | `set_cache` `set_zoom` `set_state` `set_shape` `save` `save_pymol` `load_pymol` `clear` `close` |
| `HighlightStructureImage` | **Highlight a specific region** (most common in papers) | Inherit base + `set_color(coloring_plan)` |
| `PropertyStructureImage` | **Property-driven colouring** (RMSD, physico-chemical properties) | Inherit base + `set_color(target, properties, color_map, gauge_strengthen)` |
| `Figure` | **Publication-grade layout figure** (multiple panels + structure images embedded + text + widget icons) | `set_image` `set_panel` `set_text` `set_panel_grid` `save_figure` |
| `obtain_widget_icon` | Rotation / arrow SVG widget icons | `widget_type` + `params` |

### Recommended call order (official advice, not mandatory)

```
set_cache(hide unwanted parts) → set_state(spatial rotation / alignment) → set_shape(representation)
→ set_color(colouring) → save(persist)
```

## Preset style selection (template mechanism)

### Interaction protocol (core, follow this)

**Trigger check** (for every drawing request, check this first):
- **User mentions a preset style / template** → enter "options mode": read `templates/_registry.md`, present the available templates as options, wait for the user to pick.
- **User does not mention one** → enter "free mode": render per the skill doc + the user's input parameters; no template is applied.
  - Exception: if the input closely matches a preset template (e.g. "draw an RMSD comparison" matches `rmsd_compare`), you may **proactively recommend 1** with a justification; the user can decline. Not forced.

**Options-presentation format** (when in "options mode"):
```
Available preset styles:
[1] Nature highlight composite figure — single structure, multi-chain highlight, emphasising binding site / mutation / segment
[2] Dual-structure RMSD comparison — expected vs predicted overlay + residue-difference gradient
[3] Science full-width multi-panel publication layout — multi-image + text + widgets composed into a publication-grade Figure
Reply with the number, or say "none fit, draw to my spec".
```

**Template parameterisation & override**: after the user picks a template, the PDB file path + actual chain names / residue numbers are still required (to replace the template's `{chain_A}` etc. placeholders). The template provides the "visual style skeleton"; the caller overrides the business parameters.

### Template directory
```
templates/
├── _registry.md            # Preset style registry (data source for options mode)
├── _template_format.md     # Template yaml format spec
├── README.md               # Mechanism description + sedimentation flow
├── nature_highlight.yaml
├── rmsd_compare.yaml
├── science_publication_layout.yaml
├── pastel_cartoon_surface.yaml   # Per-chain colour cartoon + milky shell (user-sedimented from recipe.pml)
├── ss_milky_surface.yaml       # Per-secondary-structure colour cartoon + neutral shell
├── ss_frosted_surface.yaml     # Per-secondary-structure colour cartoon + same-colour frosted shell
├── ss_only_surface.yaml        # Pure secondary-structure cartoon, no surface
├── residues_only.yaml          # Key-residue stick close-up (protein hidden, only sticks shown)
├── spectrum_resi.yaml          # Sequence-position property spectrum colouring (blue-white-red gradient cartoon + CA spheres)
├── active_site_highlight.yaml  # Active-site close-up (sticks + translucent cartoon environment + polar contacts)
├── distance_contact.yaml       # Residue-pair distance / polar contact annotation (dist mode=2 dashed lines)
├── goodsell_style.yaml         # Goodsell-style flat pastel spheres (per chain + white bg, no shadow)
├── mutation_site.yaml          # Mutation-site structural analysis (single residue + environment cartoon + salmon hue)
├── surface_render.yaml         # Molecular surface rendering (per-chain colour + translucent surface/mesh/dots)
├── ensemble_overlay.yaml       # NMR / MD multi-model overlay (state gradient + translucent)
├── dual_align_rmsd.yaml       # Dual-structure overlay alignment + RMSD (CA align + color1/color2)
└── ppi_interface.yaml         # Protein-protein interface (within radius + interface residue sticks + interface surface)
```

### Custom template sedimentation ("see figure → reproduce → confirm → save" flow)
**Triggers** (any one fires): "save as a template", "remember this style", "draw like this figure" (with image), "reproduce this figure's style".

**4-step flow (no skipping)**:
1. **Reproduce**: read the user's reference figure (multimodal) → decompose selection / representation / colour / rotation / layout → write candidate yaml to `templates/<candidate_name>.yaml` → **first write a render script from that yaml and produce a sample figure using a real PDB** (direct-cmd recipes must pass the 2.5.0 strict API; see the extra items in the "Verification checklist") → verify the sample with PIL → show it to the user.
2. **Confirm**: the user reviews the sample; only on an explicit "OK / that's it" do we proceed; for tweaks, adjust the script / yaml and re-render, looping until satisfied.
3. **Name**: the user names the template; if not given, I suggest one from "scene + visual feature" (e.g. `nature_binding_site`, `cell_membrane_cartoon`, `ss_milky_surface`).
4. **Register**: after confirm + naming, finalise the candidate yaml into `templates/` (for direct-cmd recipes, also save the validated `<name>.py` reference script) and **add a row to `_registry.md`** (template name / scene / reference-figure source) + sync this SKILL.md section.

> **Pacing rule**: a recipe must not be registered in `_registry.md` until a verifiable sample figure has been produced. The ss colouring family (recipe_1/2/3) in this run followed "produce a sample figure to validate first, then register".

**Hard constraints**:
- A template = **reusable parameters**, not code bound to a specific PDB run; selections / residues must be parameterised (`{chain_A}` placeholder); do not hardcode "chain A 1-30".
- Template yaml is self-contained; no dependency on external files.
- Each template ships a "usage example" section marking which parameters the caller may override.

## Input / output formats

### Input
- Structure file: `.pdb` (`.mmcif` / `.cif` also supported; PyMOL auto-detects)
- Selection string: `"type:target,target,..."`, type ∈ {`position`, `range`, `residue`, `segment`, `chain`, `model`}; for multi-chain, `"A+10-20"` means residues 10–20 of chain A
- Colour: `"0xRRGGBB"` hex string
- Rotation angles: `[x_deg, y_deg, z_deg]` (0–360 degrees)

### Output
- Structure figure: PNG (the `save` method), specifying `width` (pixels) + `ratio` (height / width) + `dpi` (default 1200)
- Publication figure: PNG/SVG/PDF (`save_figure` determines resolution according to the `Figure`'s `minimum_dpi`)
- Widget icon: PNG (`obtain_widget_icon` defaults to dpi=1200, `transparent=True` for transparent background)
- PyMOL session: `.pse` file (`save_pymol` / `load_pymol`, reusable session)

**Ordering convention** (when I present options, sort by this order):
1. Most scene-relevant first.
2. Preset templates (`created_by: agent-authored`) take priority over user-sedimented templates (`created_by: user-sedimented`), to avoid overriding generic styles.

### Special recipe notes: templates that do not use the molpub class API
- A group of "direct cmd" recipes (`entry_class: null`), all containing **a custom `set_color` palette + white-bg soft-light parameters**, exceeding the capabilities of the standard class `HighlightStructureImage`:
  - `pastel_cartoon_surface` (from `recipe.pml`): colour cartoon by **chain** + neutral grey surface shell, split into cart/surf objects. See `templates/pastel_cartoon_surface.py` for reference.
  - `ss_milky_surface` / `ss_frosted_surface` / `ss_only_surface` (user ss colouring family): colour by **secondary structure** (ss h/s/loop); the only difference is the surface (neutral shell / same-colour frosted shell / no shell). See the corresponding `.py` for reference.
  - General rule: **if a template has `entry_class: null`, the render script connects via the direct cmd string per `render.extra_steps` and does not wrap a molpub class**; all other templates use the corresponding class.
  - Per-chain colouring vs per-secondary-structure colouring: the former splits objects with a `chain X` selection; the latter uses `ss h`/`ss s`/`loop` selections, and can colour a single object as a whole (ss_only does not even split objects).

## Key parameters & publication-quality constraints

### 1. Journal layout specs (`Figure.__init__`)

| Journal | Font | Math font | Min DPI | Max columns | 1-col width (in) | 2-col width (in) | 3-col width (in) |
|---|---|---|---|---|---|---|---|
| Nature | Arial | Linux Libertine & Lucida Calligraphy | 300 | 2 | 3.54 | 7.08 | - |
| Science | Helvetica | same as above | 300 | 3 | 2.24 | 4.76 | 7.24 |
| Cell | Arial | same as above | 300 | 2(3) | 3.35 / 2.17 | 6.85 / 4.49 | - / 6.85 |
| PNAS | Helvetica | same as above | **600** | 2 | 3.42 | 7.00 | - |
| ACS | Arial | same as above | **600** | 2 | 3.25 | 7.00 | - |
| Oxford | Arial | same as above | 350 | 2 | 3.39 | 7.00 | - |
| PLOS | Arial | same as above | 300 | 1 | 5.20 | - | - |
| IEEE | Times New Roman | same as above | 300 | 2 | 3.50 | 7.25 | - |

**Cell journal requires passing `column_format=2` or `column_format=3`**, otherwise a ValueError is raised.

### 2. Typical call for a highlighted structure figure (`HighlightStructureImage`)

```python
image = HighlightStructureImage(structure_paths=["structure.pdb"])
image.set_cache(cache_contents=["residue:HOH"])            # hide water molecules
image.set_shape(representation_plan=[("chain:A", "surface"), ("chain:B", "cartoon")],
                independent_color=True, closed_surface=True)
image.set_state(rotate=[240, 340, 90])
image.set_color(coloring_plan=[("chain:A", "0xF2F2F2"), ("chain:B", "0x2D2F82")])
image.save(save_path="structure.png", width=1280, ratio=0.8)  # height = 1280*0.8 = 1024
image.close()   # for batch runs always call close() to release the PyMOL process
```

### 3. Property-driven structure figure (`PropertyStructureImage`)

```python
image = PropertyStructureImage(structure_paths=["expected.pdb", "predicted.pdb"])
image.set_shape(representation_plan=[("model:predicted", "cartoon"), ("model:expected", "cartoon")])
image.set_state(rotate=[0, 60, 255], inner_align=True, target="expected")
image.set_color(target="model:predicted", color_map="rainbow", edge_color="0x000000",
                gauge_strengthen=True)   # putty cartoon, thickness varies with property value
image.save(save_path="aligned.png", width=1800, ratio=0.5)
```

### 4. Publication-grade Figure layout

```python
fig = Figure(manuscript_format="Nature", occupied_columns=2, aspect_ratio=(606, 358),
             mathtext=False, row_number=2, column_number=2)
fig.set_image(image_path="1F34.png", layout=(1, 2, 1))           # row 1 col 1, occupies one of a 2-row 2-col grid
fig.set_image(image_path="1AY7.png", layout=(2, 2, 3))
fig.set_image(image_path="1YCR.png", layout=(2, 2, 4))
fig.set_text(annotation="Stable Complex", locations=[0.5, 0.96, 0.4, 0.05])
fig.save_figure("fig.png")
```

### 5. Widget icons (rotation arrow / angle schematic)

```python
# Style 1: rotation direction + angle
obtain_widget_icon(save_path="arrow(90).png", widget_type="arrow",
                   params={"degree": 90, "color": "black", "linestyle": "-",
                           "width": 0.02, "head_width": 0.3, "head_length": 0.4})
# Style 2: azimuth + elevation (molecular rotation state description)
obtain_widget_icon(save_path="rot.png", widget_type="rotation",
                   params={"elevation": 30, "azimuth": 30}, dpi=1200)
```

**Angle range constraints**: `arrow` degree ∈ [0, 360]; `rotation` style 1 degree ∈ [0, 180], `turn` ∈ {"right","left"}; style 2 elevation/azimuth ∈ [-180, 180], **must not both be 0** (raises ValueError).

## Common pitfalls (must alert the user)

1. **PyMOL process leak**: every `*StructureImage` instance spawns an independent process via `PyMOL()` + `.start()`. **For batch generation, always call `close()`**, otherwise a few dozen PDBs will accumulate a few dozen processes and exhaust memory.
2. **GUI launch failure**: `windows.py` must be run from a working directory that contains the `molpub` directory; running it directly from another directory will report a module-not-found. Fix: copy `windows.py` to the project root before running, or load the entire project in PyCharm/VSCode and run from there.
3. **Default behaviour of `set_state`**: `only_rotate=False` (default) first does `center` + `orient` + `zoom(complete=1)`, then overlays `rotate`; **if you only want a pure rotation without adjusting the camera, pass `only_rotate=True`**.
4. **`inner_align=True` requires ≥ 2 structures**, otherwise there is no alignment target.
5. **`PropertyStructureImage`'s `gauge_strengthen` only works on the cartoon representation**; it has no effect on surface/stick.
6. **`save`'s `dpi` defaults to 1200**; **`Figure`'s `minimum_dpi` is determined by the journal** (Nature=300, PNAS/ACS=600). If the actual DPI of the inserted PNG is lower than `minimum_dpi`, `paste_bitmap` will raise a ValueError — that is, the dpi parameter of `image.save` must be ≥ the journal spec.
7. **`set_image` only supports `.png`** (the code has a hard check `if image_format == ".png"`); SVG/PDF widget icons must be manually rasterised before embedding.
8. **`locations` vs `layout`: pick one**, passing both raises a ValueError; `layout` is an (n_row, n_col, order-number) tuple.
9. **Occupancy check in `set_panel_grid`**: `grid_params["l"]/["t"]` are 0-based row/column offsets, `w`/`h` are width/height; overlapping positions raise a ValueError.
10. **Only `mathtext=False`** enables the Linux Libertine / Lucida Calligraphy math fonts; `mathtext=True` uses the default mathtext (Arial/Helvetica style).

## Minimal runnable template

> Below is the minimal example for "free mode" (no preset style applied). After selecting a template in "options mode", generate the equivalent script on the fly per the corresponding yaml's `render.description`.

```python
from molpub import HighlightStructureImage, Figure, obtain_widget_icon

# 1) structure figure
img = HighlightStructureImage(structure_paths=["protein.pdb"])
img.set_cache(cache_contents=["residue:HOH"])
img.set_shape(representation_plan=[("chain:A", "cartoon"), ("chain:B", "surface")],
              closed_surface=True)
img.set_state(rotate=[30, 45, 0])
img.set_color(coloring_plan=[("chain:A", "0x2D2F82"), ("chain:B", "0xF2F2F2")])
img.save(save_path="protein.png", width=1280, ratio=0.9)
img.close()

# 2) widget icon
obtain_widget_icon(save_path="arrow.png", widget_type="arrow", params={"degree": 90})

# 3) publication-grade layout (Science full-width)
fig = Figure(manuscript_format="Science", occupied_columns=3)
fig.set_image(image_path="protein.png", layout=(1, 1, 1))
fig.set_image(image_path="arrow.png", locations=[0.85, 0.8, 0.1, 0.1], transparent=True)
fig.set_text(annotation="(a)", locations=[0.02, 0.97, 0.08, 0.03])
fig.save_figure("final_figure.png")
```

## Quick reference for call style (decision tree)

```
User submits a drawing request
   ├─ Mentions "preset style / pick a template / apply a style"
   │     → read templates/_registry.md → present as options → user picks
   │     → per that yaml's params + user's PDB/chain/residue numbers, override placeholders → generate script on the fly → render
   │
   ├─ Mentions "save as template / remember this style / reproduce this figure"
   │     → 4-step sedimentation flow (reproduce → confirm → name → register)
   │
   └─ No style-related mention
         → free mode: render per input + skill doc (if it closely matches a preset template, proactively recommend 1)
```

## Skill-bundled assets

- `smoke_test.py` (in this skill directory): smoke-test script that verifies 4 core classes / functions (Default/Highlight/Property/Figure + obtain_widget_icon) are usable in an environment where PyMOL-PUB is installed.
  - Run: `python <skill_dir>/smoke_test.py <local pdb file path>`
  - Output: `smoke_default.png`, `smoke_highlight.png`, `smoke_arrow.png`, `smoke_figure.png` to the current working directory.
  - Use as a quick "is it usable after install" diagnostic (a wrong PyMOL version / missing fonts / process leak all surface here).
- `templates/` (in this skill directory): preset style template library.
  - `_registry.md`: preset style registry (data source for options mode); new templates **must** be registered here.
  - `_template_format.md`: template yaml format spec (three sections: meta/params/render).
  - `README.md`: mechanism description + sedimentation flow.
  - 3 standard class templates: `nature_highlight` / `rmsd_compare` / `science_publication_layout`.
  - 13 user-sedimented "direct cmd" recipes: `pastel_cartoon_surface` (per chain) + ss colouring family `ss_milky_surface` / `ss_frosted_surface` / `ss_only_surface` (per secondary structure) + `residues_only` (key-residue sticks) + `spectrum_resi` (sequence property spectrum) + `active_site_highlight` (active-site close-up) + `distance_contact` (distance / polar contacts) + `goodsell_style` (Goodsell flat spheres) + `mutation_site` (mutation site) + `surface_render` (molecular surface) + `ensemble_overlay` (multi-model overlay) + `dual_align_rmsd` (dual-structure alignment RMSD) + `ppi_interface` (protein-protein interface), each with a `.py` reference script, all validated with 1AY7 sample figures.

## Deliverable conventions (user preferences)

- In-figure text annotations default to **English** (user preference dated 2026-09-14): panel letters A/B/C, axis labels, and arrow callouts all in English.
- Body text and figure captions (outside the figure) remain in Chinese.
- Delivery format: PNG (300–600 DPI) + optional PDF/SVG vector version; one Markdown caption paragraph attached.
- If the journal requires TIFF (some journals reject PNG), convert from the `save` output to TIFF with PIL.

## Citation

Chen, Y., Zhang, H., Wang, W., Shen, Y., Ping, Z. (2024). Rapid generation of high-quality structure figures for publication with PyMOL-PUB. *Bioinformatics*, 40(3), btae139. https://doi.org/10.1093/bioinformatics/btae139

## Verification checklist

- [ ] PyMOL version = 2.5.0 (`import pymol2; print(pymol2.__version__)` outputs `2.5.0`)
- [ ] `molpub/fonts/` is recognised by matplotlib's font_manager (`matplotlib.font_manager.findfont("Arial")` does not raise)
- [ ] The chain names in the structure file match the `chain:X` in `set_shape` (PyMOL's default chain names are A/B/C, unrelated to the PDB file's SEQRES)
- [ ] `save` dpi ≥ the journal's `minimum_dpi`
- [ ] For batch generation, every `*StructureImage` instance has `close()` called
- [ ] `Figure`'s `minimum_dpi` matches the target journal (PNAS/ACS=600, others 300–350)
- [ ] If using a template: placeholders (`{chain_A}`, etc.) have been replaced with the actual PDB; parameterisation has not been hardcoded
- [ ] If sedimenting a new template: the yaml has been saved to `templates/` + registered in `_registry.md` + the SKILL.md section has been synced

### Additional checks for direct-cmd recipes (`entry_class: null`)
Before rendering, verify the "recipe-based render script" item by item to avoid repeating the 2.5.0 strict-API pitfalls:
- [ ] The call layer uses `from pymol2 import PyMOL`, not `import pymol` (the latter has no `.load`)
- [ ] Custom palette uses `cmd.set_color(name, rgb)`, not `cmd.set("color", ...)`
- [ ] White background uses `cmd.bg_color("white")`, not `set("background_color", ...)`
- [ ] The first arg of `cmd.hide(...)` is a legal representation: `everything` is legal, `all` is not; `hetatm` is a selection and must be paired with the first arg `everything`
- [ ] After splitting objects with `cmd.create(cart, obj)` / `cmd.create(surf, obj)`, the original `obj` must be hidden via `hide("everything", obj)` to avoid showing three layers
- [ ] Secondary-structure selections `ss h` / `ss s` / `not (ss h or ss s)` (loop); for chain-based use `chain X`
- [ ] After `cmd.ray()`, then `cmd.png(..., dpi=300)`; end with `mol.stop()` (not `close()`)
- [ ] After rendering, verify with PIL that the file actually exists and its dimensions are correct (avoid a silent `png` failure)

### Verification pace for sedimenting new recipes ("sample figure first, then register")
A new recipe **must not** be written into `_registry.md` before a verifiable sample figure is produced. Flow:
1. Write the render script per the recipe → run it on a real PDB (e.g. 1AY7) to produce a sample figure
2. Verify the sample figure with PIL (exists / size / not blank)
3. Save the validated script as `templates/<name>.py`
4. Then write `templates/<name>.yaml` + one row in `_registry.md` + sync SKILL.md
(The ss colouring family in this run followed this pace, to avoid passing unvalidated code off as a preset.)
