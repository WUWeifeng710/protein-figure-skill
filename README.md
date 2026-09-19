# protein-figure — Publication-Ready Protein Structure Figures

A reusable agent skill for rendering **journal-quality** 3D protein / nucleic-acid
structure figures with PyMOL. Built on top of [PyMOL-PUB](https://github.com/BGI-SynBio/PyMOL-PUB)
(Bioinformatics 2024) and the open-source **PyMOL 2.5.0**, with 10 hand-tuned
"direct-cmd" style recipes + 3 standard-class templates, all validated against a
real PDB (1AY7).

## What you get

- **Two rendering paradigms** in one skill:
  - *Standard classes* (`HighlightStructureImage` / `PropertyStructureImage` /
    `Figure`) for journal-spec layouts, multi-panel publication figures, and RMSD overlays.
  - *Direct-cmd recipes* (`entry_class: null`) for custom pastel palettes, soft-light /
    flat-Goodsell looks, secondary-structure coloring, residue close-ups, active sites,
    distances, mutations, molecular surfaces, ensembles, dual-structure RMSD, and
    protein–protein interfaces.
- **14 out-of-the-box style recipes** (each a self-contained `.yaml` + validated `.py`).
- **Hardened 2.5.0 strict-API recipes**: every pitfall we hit is documented inline
  (`set_color` vs `set("color")`, `hide` arg rules, `spectrum` slots, named-selection
  operators, reserved object names, cross-instance colors…).
- **Smoketest** to verify your install in one line.

## Quick start

### 1. Install PyMOL 2.5.0 + PyMOL-PUB (conda, recommended)

```bash
conda create -n pymol_pub python=3.11 -c conda-forge -y
conda install -n pymol_pub -c conda-forge "pymol-open-source=2.5.0" -y
conda run -n pymol_pub python -m pip install PyMOL-PUB
```

Verify:

```bash
conda run -n pymol_pub python -c "import pymol2; print(pymol2.__version__)"   # 2.5.0
conda run -n pymol_pub python -c "from molpub import HighlightStructureImage; print('molpub OK')"
```

> **Version matters**: PyMOL must be **exactly 2.5.0** (open source). PyPI's
> `pymol-open-source` only has 3.x alphas — don't use it.

### 2. Run the smoketest

```bash
conda run -n pymol_pub python <this_skill>/smoke_test.py your_structure.pdb
# → produces smoke_default.png, smoke_highlight.png, smoke_arrow.png, smoke_figure.png
```

### 3. Use a style recipe

Pick a recipe from `templates/`, copy its `.py` as a starting point, point it at
your PDB, and run it in the same env:

```bash
cp <this_skill>/templates/goodsell_style.py ./my_figure.py
# edit my_figure.py: set PDB, CHAIN_COLORS, SAVE_PATH
conda run -n pymol_pub python my_figure.py
```

Every recipe is **parameterized** — chain names / residue numbers / colors are
variables at the top, not hardcoded.

## Installation into an AI agent

This skill is a **plain folder** (no build step). To hand it to any agent that
loads skills (WorkBuddy / Claude / custom harnesses), install it by one of:

```bash
# A) drop into the agent's skills dir
mkdir -p ~/.workbuddy/skills          # WorkBuddy convention; adapt to your agent
cp -r <this_dir> ~/.workbuddy/skills/protein-figure

# B) or point your agent at the folder directly
```

**Prompt to install + use in your agent chat:**

```
Install the protein-figure skill from <path-or-url>. Then:
1. Verify PyMOL 2.5.0 + PyMOL-PUB are installed in a conda env (create it if missing).
2. Run the skill's smoke_test.py against a local PDB I provide.
3. Use the "goodsell_style" template to render my structure into a journal-cover
   figure (white bg, 300 DPI, in-figure labels in English).
4. Save the result to ./output/goodsell_<name>.png.
```

That prompt is the **whole onboarding** — the agent reads `SKILL.md` for the
environment rules and the template directory for what each style does.

## What the skill borrows from

| Project | What we took |
|---|---|
| [BGI-SynBio/PyMOL-PUB](https://github.com/BGI-SynBio/PyMOL-PUB) (★97) | Core class API (`DefaultStructureImage` / `HighlightStructureImage` / `PropertyStructureImage` / `Figure` / `obtain_widget_icon`), journal format tables (Nature/Science/Cell/PNAS/ACS/Oxford/PLOS/IEEE), widget icons. Paper: Chen et al., Bioinformatics 2024, btae139. |
| [BioTender-max/PyMolClaw](https://github.com/BioTender-max/PyMolClaw) | All 13 rendering scene scripts (spectrum / active_site / distance / goodsell / mutation / surface / ensemble / align / ppi / …) — we rewrote each to the 2.5.0 strict API and shipped as the 10 "direct-cmd" recipes in `templates/`. |
| [google-deepmind/science-skills](https://github.com/google-deepmind/science-skills) | The `count_atoms("all")==0` load-check pattern (catches silent blank renders that PIL can't) and the "headless / no-GPU → fall back to `cmd.png`" lesson. |
| [schrodinger/pymol-open-source](https://github.com/schrodinger/pymol-open-source) | The 2.5.0 open-source PyMOL itself (conda-forge `pymol-open-source=2.5.0`). |
| [cgohlke/pymol-open-source-wheels](https://github.com/cgohlke/pymol-open-source-wheels) | Fallback wheel route when conda is unavailable (matched to your Python version). |
| OPIG (Open Protein Illustration Gallery) | Advanced render parameters: `surface_quality`, `cartoon_sampling`, `ray_opaque_background`, `field_of_view`, one-line `preset.publication`. |
| User `.pml` recipes | The pastel / secondary-structure / residues-only color families, distilled from hand-tuned `recipe*.pml` files into parameterized templates. |

## Repository layout

```
protein-figure/
├── SKILL.md               # agent-facing instructions: env, API pitfalls, templates,
│                          #   presets, publishing constraints, validation checklists
├── smoke_test.py          # one-line install diagnostic
├── README.md              # this file
└── templates/
    ├── _registry.md       # the preset-style catalog (what an agent offers the user)
    ├── _template_format.md# yaml schema (meta / params / render)
    ├── README.md          # template mechanism + "reproduce → confirm → save" flow
    ├── nature_highlight.yaml
    ├── rmsd_compare.yaml
    ├── science_publication_layout.yaml
    └── <10 direct-cmd recipes>/.yaml + .py   # each self-contained, validated on 1AY7
```

## Conventions we follow

- **In-figure labels default to English** (panel A/B/C, axes, arrows, legends);
  document body / captions may be in the user's language.
- **Deliverable**: PNG at 300–600 DPI (+ optional PDF/SVG); for journals needing
  TIFF, convert with PIL.
- **Sample-first rhythm**: no recipe enters the registry until it has produced a
  verifiable sample figure (PIL-checked for existence / size / non-blank).

## License

See the underlying projects for their licenses (PyMOL-PUB is MIT; the PyMOL
open-source edition is BSD-3-Clause). This skill is a thin layer of templates,
docs, and validated snippets on top of those.
