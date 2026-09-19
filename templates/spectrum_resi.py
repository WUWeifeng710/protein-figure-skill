# spectrum_resi template render script reference (2.5.0 strict API, validated with 1AY7 sample figure)
# Sequence-position B-factor / pLDDT spectrum coloring (blue-white-red gradient cartoon + CA spheres)
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python spectrum_resi.py`
# Usage: modify PDB / OBJECT / PROPERTY / PALETTE before running
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
PROPERTY = "resi"              # default: by residue position; try "b" if PDB has a b column, "plddt" if it has a plddt column
PALETTE = "blue_white_red"     # blue_white_red / blue_green_red / rainbow / red_white_blue
SAVE_PATH = "nice_fig_spectrum.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

# 0) Load + validate (exit on 0 matches)
cmd.load(PDB, OBJECT, quiet=1)
if int(cmd.count_atoms("all")) == 0:
    print("LOAD FAILED: 0 atoms after load"); mol.stop(); sys.exit(1)

# 1) white bg soft light
cmd.bg_color("white")
cmd.set("ray_opaque_background", 1)
cmd.set("ambient", 0.5)
cmd.set("two_sided_lighting", 1)
cmd.set("ray_trace_mode", 1)
cmd.set("ray_shadows", 1)
cmd.set("antialias", 2)
cmd.set("depth_cue", 0)
cmd.set("ray_trace_gain", 0.1)
cmd.set("orthoscopic", 1)
cmd.set("cartoon_fancy_helices", 1)
cmd.set("cartoon_smooth_loops", 1)
cmd.set("cartoon_flat_sheets", 1)
cmd.set("cartoon_highlight_color", "grey50")

# 2) clear stage
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# 3) cartoon + spectrum gradient
cmd.show("cartoon", OBJECT)
cmd.spectrum(PROPERTY, PALETTE, OBJECT)

# 4) CA spheres (optional)
cmd.show("spheres", f"{OBJECT} and name CA")
cmd.set("sphere_scale", 0.5)

# 5) compose + 300dpi
cmd.orient(OBJECT)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
