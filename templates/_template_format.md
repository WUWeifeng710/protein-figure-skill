# Template YAML Format Spec

A template = one `.yaml` file with 3 top-level keys: `meta` (metadata), `params` (overridable parameters), `render` (rendering script description).

## Format

```yaml
meta:
  name: <template English id, snake_case>    # required, used as file name and option-card key
  title: <display title>                     # required, shown on the option card
  scene: <one-line scene description>        # required
  reference: <reference image source or "original">  # for sedimented templates: reference image path; for preset templates: "PyMOL-PUB cases"
  created: <ISO date YYYY-MM-DD>
  created_by: <preset | user-sedimented | agent-authored>

params:                                      # overridable params, caller passes by key
  manuscript_format: Nature                  # journal layout (8 choices)
  occupied_columns: 2
  aspect_ratio: [606, 358]
  cache_contents: ["residue:HOH"]            # items to hide
  representation_plan: []                    # [(select, repr), ...]
  rotate: [330, 10, 270]
  coloring_plan: []                          # [(select, color), ...]
  save_width: 1280
  save_ratio: 0.9

render:
  description: |
    <explain how this template renders from params>
    Example: HighlightStructureImage → set_cache → set_shape → set_state → set_color → save
  entry_class: HighlightStructureImage       # which molpub class the template primarily uses
  extra_steps: |                             # optional: template-specific extra render logic (e.g. widget icons, multi-structure alignment)
    none
```

## Parameter override convention
- `params` passed by the caller are **merged key-by-key** into the template `params`; keys not passed keep the template defaults.
- `coloring_plan` / `representation_plan` may contain placeholders (e.g. `{chain_A}`, `{residues}`) that the caller substitutes with the actual PDB chain names / residue numbers.
- A template must **not hardcode** specific chain numbers or residue numbers from one particular PDB run — parameterise them.

## Rendering script convention
- `render.entry_class` names the main class; `render.description` gives the call-order explanation.
- If the template needs multiple steps (structure figure + widget icon + layout), describe them in `extra_steps`; the rendering script (generated on the fly) follows that description.
- The rendering script **always**: `close()` every `*StructureImage` instance; `Figure.save` dpi ≥ journal `minimum_dpi`.

## Two rendering paradigms (validated on 2.5.0 strict API)

The template's `render.entry_class` determines the path:

### Paradigm A: molpub class (`entry_class` is not null)
`nature_highlight` / `rmsd_compare` / `science_publication_layout` follow this. Chain `set_cache → set_state → set_shape → set_color → save` per `description`; `close()` the instance.

### Paradigm B: direct cmd (`entry_class: null`)
User-sedimented recipes (`pastel_cartoon_surface` + 3 ss-family) follow this. **Mandatory: `pymol2.PyMOL()` call layer + 2.5.0 strict API**, skeleton:

```python
from pymol2 import PyMOL
mol = PyMOL(); mol.start(); cmd = mol.cmd
cmd.load(PDB, OBJECT, quiet=1)
cmd.set_color("soft_blue", [0.63, 0.75, 0.94])     # palette: set_color is a command, not set("color",...)
cmd.bg_color("white")                                  # white bg: bg_color, not set("background_color",...)
# soft-light parameter group: ambient / two_sided_lighting / ray_trace_mode /
#   ray_shadows / antialias / depth_cue / ray_trace_gain / orthoscopic / cartoon_fancy_helices...
cmd.set("ambient", 0.5)
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")   # strict: first arg must be a legal representation (everything OK, all NOT OK)
cmd.hide("everything")
cmd.create(CART, OBJECT); cmd.create(SURF, OBJECT)   # split objects (needed for cartoon/surface colour separation)
cmd.hide("everything", OBJECT)
cmd.show("cartoon", CART)
cmd.show("surface", SURF)
# colouring: per-chain (CART and chain A) or per-secondary-structure (CART and ss h / ss s / not(ss h or ss s))
cmd.orient(CART); cmd.ray()
cmd.png(SAVE, width=1600, height=1600, dpi=300, quiet=1)
mol.stop()   # stop() not close()
```

**Pitfall quick-reference (all back-ported to SKILL.md "Recipe migration pitfalls")**:
- `import pymol` as call layer has no `.load` → must use `from pymol2 import PyMOL`.
- `cmd.hide("hetatm")` / `cmd.hide("all", ...)` errors → `hide` first arg must be a legal representation.
- `cmd.set("color", ...)` / `cmd.set("background_color", ...)` errors → use `set_color` / `bg_color`.
- `ss_only` does not split objects: directly `show cartoon` + colour the loaded object by ss, `orient(OBJECT)`.

## Naming convention
- Template name: `<scene>_<visual_feature>`, e.g. `nature_binding_site`, `cell_membrane_cartoon`, `rmsd_compare`.
- File name = `meta.name` + `.yaml`.
