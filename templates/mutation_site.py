# mutation_site template render script reference (2.5.0 strict API, validated with 1AY7 sample figure)
# Mutation-site structural analysis (single-residue sticks + CA spheres + environment cartoon + color distinction)
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python mutation_site.py`
# Usage: modify PDB / OBJECT / MUT_RESI / CUTOFF before running
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
MUT_RESI = 35
CUTOFF = 5.0
SAVE_PATH = "nice_fig_mutation.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

cmd.load(PDB, OBJECT, quiet=1)
if int(cmd.count_atoms("all")) == 0:
    print("LOAD FAILED: 0 atoms after load"); mol.stop(); sys.exit(1)

# white bg soft light
cmd.bg_color("white")
cmd.set("ray_opaque_background", 1)
cmd.set("ambient", 0.5); cmd.set("two_sided_lighting", 1)
cmd.set("ray_trace_mode", 1); cmd.set("ray_shadows", 1)
cmd.set("antialias", 2); cmd.set("depth_cue", 0)
cmd.set("ray_trace_gain", 0.1); cmd.set("orthoscopic", 1)
cmd.set("cartoon_fancy_helices", 1); cmd.set("cartoon_smooth_loops", 1)
cmd.set("cartoon_flat_sheets", 1); cmd.set("cartoon_highlight_color", "grey50")

# clear stage
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# Mutation residue + environment (byres done after hide)
cmd.select("mut_site", f"{OBJECT} and resi {MUT_RESI}")
cmd.select("context", f"byres (mut_site around {CUTOFF}) and not mut_site")
cmd.show("cartoon", "context")
cmd.set("cartoon_transparency", 0.6)

# Mutation residue sticks + CA spheres
cmd.show("sticks", f"sc. and (m and resi {MUT_RESI})")
cmd.show("spheres", f"n. CA and (m and resi {MUT_RESI})")
cmd.set("sphere_scale", 0.6)

# Hue distinction (lightorange=WT, red=mutation focus)
cmd.color("lightorange", "mut_site")
cmd.color("red", f"{OBJECT} and resi {MUT_RESI} and elem C")

# Clear the unselected portion
cmd.hide("everything", f"{OBJECT} and not (mut_site or context)")

# compose + 300dpi
cmd.orient("mut_site")
cmd.zoom("mut_site", 8)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
