# dual_align_rmsd template render script reference (2.5.0 strict API, validated with 1AY7 sample figure)
# Dual-structure overlay align + RMSD
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python dual_align_rmsd.py`
# Usage: modify PDB1 / PDB2 / NAME1 / NAME2 / CUTOFF before running
import os, sys
from pymol2 import PyMOL

PDB1 = "structure1.pdb"
PDB2 = "structure2.pdb"
N1, N2 = "s1", "s2"       # object names avoid reserved words (do not use a/b etc.)
CUTOFF = 5.0
C1, C2 = "lightblue", "salmon"
T2 = 0.5
SAVE_PATH = "nice_fig_align.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

cmd.load(PDB1, N1, quiet=1)
cmd.load(PDB2, N2, quiet=1)
if int(cmd.count_atoms("all")) == 0:
    print("LOAD FAILED: 0 atoms after load"); mol.stop(); sys.exit(1)

# align + RMSD
try:
    rmsd = cmd.align(f"{N2} and name CA", f"{N1} and name CA", cutoff=CUTOFF)
except Exception as e:
    print("align warn:", e); rmsd = None

# white bg soft light
cmd.bg_color("white")
cmd.set("ray_opaque_background", 1)
cmd.set("ambient", 0.5); cmd.set("two_sided_lighting", 1)
cmd.set("ray_trace_mode", 1); cmd.set("ray_shadows", 1)
cmd.set("antialias", 2); cmd.set("depth_cue", 0)
cmd.set("ray_trace_gain", 0.1); cmd.set("orthoscopic", 1)
cmd.set("cartoon_fancy_helices", 1); cmd.set("cartoon_smooth_loops", 1)
cmd.set("cartoon_flat_sheets", 1); cmd.set("cartoon_highlight_color", "grey50")

# clear stage (per-object hide, no `or` operator)
cmd.remove(f"{N1} and resn HOH"); cmd.remove(f"{N2} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything", N1)
cmd.hide("everything", N2)

# cartoon + per-structure color
cmd.show("cartoon", N1)
cmd.show("cartoon", N2)
cmd.color(C1, f"{N1} and elem C")
cmd.color(C2, f"{N2} and elem C")
cmd.set("cartoon_transparency", T2, N2)

# compose + 300dpi
cmd.orient(N1)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
if rmsd is not None:
    print(f"ALIGN RMSD={rmsd}")
print("SAVED", SAVE_PATH)
