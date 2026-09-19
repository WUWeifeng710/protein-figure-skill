# goodsell_style template render script reference (2.5.0 strict API, validated with 1AY7 sample figure)
# Goodsell-style flat pastel spheres (chain-colored, no-shadow soft light)
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python goodsell_style.py`
# Usage: modify PDB / OBJECT / CHAIN_COLORS / REPR before running
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
CHAIN_COLORS = {"A": "gs_blue", "B": "gs_red"}   # only list chains that actually exist in the target PDB
REPR = "spheres"                                   # spheres / surface
SAVE_PATH = "nice_fig_goodsell.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

cmd.load(PDB, OBJECT, quiet=1)
if int(cmd.count_atoms("all")) == 0:
    print("LOAD FAILED: 0 atoms after load"); mol.stop(); sys.exit(1)

# Goodsell flat rendering (flat / no-shadow / high ambient)
cmd.bg_color("white")
cmd.set("ray_trace_mode", 3)
cmd.set("ray_trace_color", "black")
cmd.set("ray_trace_gain", 0)
cmd.set("ambient", 1.0)
cmd.set("direct", 0.0)
cmd.set("reflect", 0.0)
cmd.set("ray_shadows", 0)
cmd.set("depth_cue", 0)
cmd.set("orthoscopic", 1)

# Goodsell pastel palette (must be defined within the same instance)
cmd.set_color("gs_blue",   [0.565, 0.714, 0.812])
cmd.set_color("gs_red",    [0.855, 0.475, 0.427])
cmd.set_color("gs_green",  [0.631, 0.792, 0.596])
cmd.set_color("gs_tan",    [0.871, 0.812, 0.682])
cmd.set_color("gs_orange", [0.871, 0.639, 0.376])

# clear stage
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# Representation + per-chain color
cmd.show(REPR, OBJECT)
for chain, color in CHAIN_COLORS.items():
    cmd.color(color, f"{OBJECT} and chain {chain}")

# compose + 300dpi
cmd.orient(OBJECT)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
