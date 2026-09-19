# Template Mechanism

## Template directory layout
```
templates/
├── _registry.md          # Preset style registry (data source when I present options)
├── _template_format.md   # Template yaml format spec
├── nature_highlight.yaml
├── rmsd_compare.yaml
├── science_publication_layout.yaml
└── <user-custom-template>.yaml   # produced by the "send me a nice figure → I reproduce → you confirm → save" flow
```

## Interaction protocol

### 1. User requests a preset style
**Triggers** (any one fires): "use a preset style", "pick a template", "any nice templates?", "apply a style", "draw in XX style".
**Action**: I read `templates/_registry.md` and present the available templates as option cards (each with name, scene, and a thumbnail preview if one exists) for the user to choose from.

### 2. User does not mention a preset style
**Default behaviour**: render free-form using the skill docs + the user's current input; no template is applied.
**Exception**: if the input matches a preset template very well (e.g. "draw an RMSD comparison"), I may proactively recommend one template with a short justification, but it is **not forced** — the user can decline.

### 3. Sediment a custom template ("see figure → reproduce → confirm → save")
**Triggers** (any one fires): "save as a template", "remember this style", "draw like this figure" (with an image), "reproduce this figure's style".
**Flow** (must complete all 4 steps, no skipping):
1. **Reproduce**: I read the user's reference figure (multimodal), decompose its selection / representation / colour / rotation / layout, generate a candidate yaml into `templates/<candidate>.yaml`, and **first render a sample figure from that yaml** for the user to inspect.
2. **Confirm**: the user reviews the sample; only when they explicitly say "OK / good / that's it" do we proceed; for tweaks I adjust the yaml and re-render, looping until satisfied.
3. **Name**: the user names the template; if none is given I suggest one from "scene + visual feature" (e.g. `nature_binding_site`, `cell_membrane_cartoon`).
4. **Register**: after confirm + naming, move the candidate yaml into `templates/` (rename if it was already in that dir) and **add a row to `_registry.md`** (template name, scene, reference figure source).

**Hard constraints**:
- A template must be **reusable parameters**, not code bound to one particular PDB run — selections use variables (e.g. `{chain_A}`, `{residues}`), never hardcoded "chain A 1-30".
- A template yaml must be **self-contained** with all drawing parameters; no dependency on external files.
- Each template ships a "usage example" section marking which parameters the caller may override in this run.

## Template yaml format (see `_template_format.md`)
Template = one param set + one Python render script + metadata (name, scene, reference figure, created time). The render script reads params, calls the molpub API to produce the figure; params may be overridden by the caller.
