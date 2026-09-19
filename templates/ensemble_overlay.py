# ensemble_overlay template render script reference (2.5.0 strict API, validated with 1AY7 sample figure)
# NMR / MD multi-model overlay (state-based gradient + translucent)
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python ensemble_overlay.py`
# Usage: modify PDB / OBJECT / STYLE / TRANSPARENCY before running
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
STYLE = "cartoon"
TRANSPARENCY = 0.3
SAVE_PATH = "nice_fig_ensemble.png"
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

# Representation + state gradient (effective for multi-model NMR; single-frame degradation: errors can be ignored)
cmd.show(STYLE, OBJECT)
try:
    cmd.spectrum("state", "rainbow", OBJECT)
except Exception as e:
    print("spectrum state warn:", e)
cmd.set("transparency", TRANSPARENCY)

# compose + 300dpi
cmd.orient(OBJECT)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
