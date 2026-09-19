# distance_contact template render script reference (2.5.0 strict API, validated with 1AY7 sample figure)
# Residue-pair distance / polar contacts annotation
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python distance_contact.py`
# Usage: modify PDB / OBJECT / SEL1 / SEL2 / MODE before running
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
SEL1 = "resi 35"
SEL2 = "resi 52"
MODE = 2                # 0=all, 1=polar, 2=hbond+key
SAVE_PATH = "nice_fig_distance.png"
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

# background cartoon
cmd.show("cartoon", OBJECT)

# two selections (independently named)
cmd.select("s1", f"{OBJECT} and {SEL1}")
cmd.select("s2", f"{OBJECT} and {SEL2}")

# sticks + CA spheres
cmd.show("sticks", "sc. and (s1 or s2)")
cmd.show("spheres", "n. CA and (s1 or s2)")
cmd.set("sphere_scale", 0.5)

# distance lines + contacts
cmd.dist("d1", "s1", "s2", mode=MODE)
cmd.set("dash_color", "black")
cmd.set("dash_gap", 0.3)
cmd.set("dash_radius", 0.08)

# compose + 300dpi
cmd.orient("s1")
cmd.zoom("s1 or s2", 12)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
