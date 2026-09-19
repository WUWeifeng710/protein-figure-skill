# ppi_interface template render script reference (2.5.0 strict API, validated with 1AY7 sample figure)
# Protein-protein interface (two chains within radius to pick interface residues + sticks + translucent surface)
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python ppi_interface.py`
# Usage: modify PDB / OBJECT / CHAIN_A / CHAIN_B / CUTOFF before running
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
CHAIN_A, CHAIN_B = "A", "B"
CUTOFF = 4.0
CA_COLOR, CB_COLOR = "lightblue", "lightorange"
SAVE_PATH = "nice_fig_ppi.png"
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

# cartoon + per-chain color
cmd.show("cartoon", OBJECT)
cmd.color(CA_COLOR, f"{OBJECT} and chain {CHAIN_A} and elem C")
cmd.color(CB_COLOR, f"{OBJECT} and chain {CHAIN_B} and elem C")

# Interface residues (within radius + byres extension)
cmd.select("ifaceA", f"byres ({OBJECT} and chain {CHAIN_A} within {CUTOFF} of {OBJECT} and chain {CHAIN_B})")
cmd.select("ifaceB", f"byres ({OBJECT} and chain {CHAIN_B} within {CUTOFF} of {OBJECT} and chain {CHAIN_A})")
cmd.show("sticks", "sc. and (ifaceA or ifaceB)")
cmd.show("spheres", "n. CA and (ifaceA or ifaceB)")
cmd.set("sphere_scale", 0.4)

# Interface translucent surface (optional)
cmd.create("surfA", "ifaceA")
cmd.create("surfB", "ifaceB")
cmd.show("surface", "surfA")
cmd.show("surface", "surfB")
cmd.set("transparency", 0.6)
cmd.color(CA_COLOR, "surfA")
cmd.color(CB_COLOR, "surfB")

# compose + 300dpi
cmd.orient(OBJECT)
cmd.zoom("ifaceA or ifaceB", 8)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
