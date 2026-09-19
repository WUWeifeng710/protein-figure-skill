# Preset Style Registry

> This is the data source I read and present options from when the user requests a preset style.
> When onboarding a new template, **always** add a row here in the same commit.

| Template file | Display name | Scene | Entry class | Notes |
|---|---|---|---|---|
| `nature_highlight.yaml` | Nature highlight composite figure | Single-structure multi-chain highlight; emphasise binding site / mutation / key segment | `HighlightStructureImage` | Neutral surface + active cartoon + highlighted segments |
| `rmsd_compare.yaml` | Dual-structure RMSD / property comparison | Expected vs predicted / WT vs mutant, aligned overlay + per-residue gradient | `PropertyStructureImage` | Putty cartoon, rainbow spectrum |
| `science_publication_layout.yaml` | Science full-width multi-panel publication layout | Multi-image + panels + text + widgets composed into a publication-grade Figure | `Figure` | 3-column full width, sub-figure dpi ≥ 300 |
| `pastel_cartoon_surface.yaml` | Pastel chain-coloured cartoon + milky translucent surface | Single-structure multi-chain pastel cartoon + milky surface shell, white-bg soft-light publication-grade | Direct `cmd` (no molpub class) | Split objects, custom 4-colour pastel palette; user-sedimented from recipe.pml |
| `ss_milky_surface.yaml` | Secondary-structure pastel cartoon + milky neutral surface | Cartoon coloured by secondary structure (h/s/loop) in pastel tones + neutral gray90 shell; ideal for highlighting secondary structure | Direct `cmd` (no molpub class) | Split cart/surf, colour by ss selection; user-sedimented from recipe_1_ss_milky.pml, **validated with 1AY7 sample figure** |
| `ss_frosted_surface.yaml` | Secondary-structure pastel cartoon + same-colour frosted surface | Cartoon in pastel ss tones, same-colour 0.60-opacity frosted glass surface; richer colour | Direct `cmd` (no molpub class) | Surface echoes cartoon colour; user-sedimented from recipe_2_ss_frosted.pml, **validated with 1AY7 sample figure** |
| `ss_only_surface.yaml` | Pure secondary-structure pastel cartoon (no surface) | Cartoon-only in pastel ss tones, no shell; clean lines, no occlusion | Direct `cmd` (no molpub class) | No object split, colour the loaded object directly; user-sedimented from recipe_3_ss_only.pml, **validated with 1AY7 sample figure** |
| `residues_only.yaml` | Key-residue stick close-up (protein hidden, sticks only) | Hide the whole protein, show only a few key residues as soft pastel sticks; focus the eye on local sites | Direct `cmd` (no molpub class) | Residue selection + `show sticks`; user-sedimented from recipe_5_residues_only.pml, **validated with 1AY7 sample figure** |
| `spectrum_resi.yaml` | Sequence-position property spectrum (blue-white-red gradient cartoon + CA spheres) | Cartoon with continuous gradient by residue position; display B-factor / pLDDT / sequence property distribution | Direct `cmd` (no molpub class) | `cmd.spectrum(resi,...)`; 2.5.0 does not accept a `bfactor` slot — use `resi` instead. Ref: PyMolClaw spectrum.py. **Validated with 1AY7 sample figure** |
| `active_site_highlight.yaml` | Active-site close-up (sticks + translucent cartoon environment + polar contacts) | Key residues as sticks + CA spheres + `around`-radius translucent cartoon environment + dashed polar contacts between residues | Direct `cmd` (no molpub class) | `select+extend` merged selection. Ref: PyMolClaw active_site.py. **Validated with 1AY7 sample figure** |
| `distance_contact.yaml` | Residue-pair distance / polar contact annotation | Two residues as sticks + CA spheres + `dist mode=2` dashed lines; ideal for binding-site distance callouts | Direct `cmd` (no molpub class) | `sc. and (s1 or s2)`. Ref: PyMolClaw distance.py. **Validated with 1AY7 sample figure** |
| `goodsell_style.yaml` | Goodsell-style flat pastel spheres (per chain) | Sphere model in Goodsell pastels (gs_*), white bg no-shadow flat rendering, journal-cover quality | Direct `cmd` (no molpub class) | `ray_trace_mode=3` + `ambient=1.0` + `ray_shadows=0`. Ref: PyMolClaw goodsell.py. **Validated with 1AY7 sample figure** |
| `mutation_site.yaml` | Mutation-site structural analysis (single residue + environment cartoon) | Specified mutation residue as sticks + CA spheres + `around`-radius translucent environment cartoon + salmon/red hue distinction | Direct `cmd` (no molpub class) | Single-residue close-up. Ref: PyMolClaw mutation.py. **Validated with 1AY7 sample figure** |
| `surface_render.yaml` | Molecular surface rendering (per-chain colour + translucency) | Independent surface / mesh / dots, per-chain colour + translucent; display molecular surface shape / binding pocket | Direct `cmd` (no molpub class) | 2.5.0 does not support `set surface_quality`; built-in per-chain colour. Ref: PyMolClaw surface.py. **Validated with 1AY7 sample figure** |
| `ensemble_overlay.yaml` | NMR / MD multi-model overlay (state gradient) | Multi-model rainbow gradient by state + translucent; display structural flexibility / conformational ensemble | Direct `cmd` (no molpub class) | `spectrum state` (single-model degenerate case is harmless). Ref: PyMolClaw ensemble.py. **Validated with 1AY7 sample figure** |
| `dual_align_rmsd.yaml` | Dual-structure overlay alignment + RMSD | Two structures aligned by CA + RMSD + overlaid cartoon (color1/color2 + translucent) | Direct `cmd` (no molpub class) | Avoid reserved names s1/s2 for object names. Ref: PyMolClaw align.py. **Validated with 1AY7 self-overlay** |
| `ppi_interface.yaml` | Protein-protein interface (within radius + interface residue sticks) | Two chains `within` radius to extract interface residues + sticks + CA spheres + translucent interface surface | Direct `cmd` (no molpub class) | `byres within` selection. Ref: PyMolClaw ppi.py. **Validated with 1AY7 sample figure** |

## Residue-stick (residues_only) colour-family note

- `residues_only` belongs to the "sticks-only" family: orthogonal to the ss/pastel "cartoon + shell" family — the protein body is completely hidden, only the residues in `key_residues` are shown as `show sticks` in soft pastel tones (`sh_*` prefix, distinct from the ss family's `soft_blue` / `rose_pink`).
- Ideal for highlighting catalytic / binding / mutation sites; `key_residues` may carry chain prefixes (e.g. `A/35`); residue numbers must actually exist in the target PDB.

## Secondary-structure (ss) colour-family note

- `ss_milky` / `ss_frosted` / `ss_only` all belong to the "colour by secondary structure" family: soft_blue = ss h (α-helix), rose_pink = ss s (β-strand), lavender = loop.
- The only difference among the three is the surface: milky = neutral grey shell, frosted = same-colour frosted shell, only = no shell.
- Distinct from `pastel_cartoon_surface` (colour by chain): the ss family colours by structural element and does not split chains.

## Property / site close-up family (spectrum_resi / active_site_highlight)

- `spectrum_resi`: continuous gradient by residue position (blue-white-red); ideal for B-factor / pLDDT / sequence property distribution. **2.5.0 pitfall: `spectrum` does not accept a `bfactor` slot — use `resi` instead; if PDB has a B-factor column try `b`, if it has pLDDT try `plddt`.**
- `active_site_highlight`: local-site mechanism figure — key residues as sticks + CA spheres, `byres around` for translucent cartoon environment, `dist mode=2` for polar contacts. **2.5.0 pitfall: `select` in strict mode rejects `+` / `or` concatenation — use `select` + `extend` for selection addition.**

## Ordering convention (when presenting options)

1. Most scene-relevant first (I judge this from the user's current input).
2. Within the same scene, newest first.
3. Preset templates before user-sedimented ones (sedimented templates are "personal styles", presets are "generic styles" — generic first so habits are not overridden).

## Maintenance rules

- Adding a template: write the yaml → add a row in this table → sync the "Preset Style Selection" section in `SKILL.md`.
- Removing / renaming a template: update this table and `SKILL.md` in the same commit.
- A template yaml must **not** reference resources outside this table; keep it self-contained.
