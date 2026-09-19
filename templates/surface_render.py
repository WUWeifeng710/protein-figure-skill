# surface_render template render script reference (2.5.0 strict API, validated with 1AY7 sample figure)
# Molecular surface rendering (surface / mesh / dots, per-chain color + translucent)
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python surface_render.py`
# Usage: modify PDB / OBJECT / STYLE / CHAIN_COLORS / TRANSPARENCY before running
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
STYLE = "surface"                 # surface / mesh / dots
CHAIN_COLORS = {"A": "lightblue", "B": "lightorange"}   # use 2.5.0 built-in colors
TRANSPARENCY = 0.4
SAVE_PATH = "nice_fig_surface.png"
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

# clear stage (do not set surface_quality; this setting misbehaves in 2.5.0 strict mode)
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# Surface representation + per-chain color
cmd.show(STYLE, OBJECT)
for chain, color in CHAIN_COLORS.items():
    cmd.color(color, f"{OBJECT} and chain {chain}")
cmd.set("transparency", TRANSPARENCY)

# compose + 300dpi
cmd.orient(OBJECT)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
