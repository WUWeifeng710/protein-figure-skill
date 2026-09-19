# active_site_highlight template render script reference (2.5.0 strict API, validated with 1AY7 sample figure)
# Active site close-up: key residues as sticks + translucent cartoon environment + polar contacts dashes
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python active_site_highlight.py`
# Usage: modify PDB / OBJECT / CAT_RESI / CUTOFF / SAVE_PATH before running
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
CAT_RESI = [35, 52, 62, 63]   # key residue numbers (modify per the target PDB)
CUTOFF = 5.0                  # environment radius (Å)
SAVE_PATH = "nice_fig_active_site.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

# 0) Load + validate
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

# 3) Key residue selection (select + extend one at a time; 2.5.0 select strict mode does not accept +/or concatenation)
cmd.select("catalytic", f"{OBJECT} and resi {CAT_RESI[0]}")
for r in CAT_RESI[1:]:
    cmd.select("_t", f"{OBJECT} and resi {r}")
    cmd.extend("catalytic", "_t")

# 4) Surrounding environment (byres MUST be done after hide everything, since hide clears the selection)
cmd.select("cat_env", f"byres (catalytic around {CUTOFF}) and not catalytic")
cmd.show("cartoon", "cat_env")
cmd.set("cartoon_transparency", 0.7)

# 5) Key residues as sticks + CA spheres
cmd.show("sticks", f"sc. and (catalytic)")
cmd.show("spheres", f"n. CA and (catalytic)")
cmd.set("sphere_scale", 0.5)

# 6) polar contacts (mode=2: bonds + H-bonds; contacts may be sparse when PDB lacks H)
try:
    cmd.dist("cat_contacts", "catalytic", "catalytic", mode=2)
    cmd.hide("labels", "cat_contacts")
    cmd.set("dash_color", "black")
    cmd.set("dash_gap", 0.3)
    cmd.set("dash_radius", 0.06)
except Exception as e:
    print("dist warn:", e)

# 7) compose + 300dpi
cmd.orient("catalytic")
cmd.zoom("catalytic", 10)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
