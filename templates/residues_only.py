# residues_only template render script reference (2.5.0 strict API)
# Fully hide the protein, show only key-residue sticks (soft pastels + white bg soft light)
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python residues_only.py`
# Usage: modify PDB / OBJECT / KEY_RESIDUES (residue selection → color) before running
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
# Key residues: (selection string, color name). Selection may carry a chain prefix, e.g. "A/35" or "chain A and resi 12"
KEY_RESIDUES = [
    ("resi 35", "sh_pink"),
    ("resi 52", "sh_blue"),
    ("resi 62", "sh_lav"),
    ("resi 63", "sh_cream"),
]
SAVE_PATH = "nice_fig_residues_only.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300
FOCUS_ZOOM_LEVEL = 4

mol = PyMOL()
mol.start()
cmd = mol.cmd

# 0) Load
cmd.load(PDB, OBJECT, quiet=1)

# 1) Soft pastel palette (set_color is a command)
cmd.set_color("sh_pink",  [0.91, 0.73, 0.76])
cmd.set_color("sh_blue",  [0.67, 0.75, 0.86])
cmd.set_color("sh_lav",   [0.80, 0.76, 0.86])
cmd.set_color("sh_cream", [0.98, 0.93, 0.80])

# 2) White background + soft light
cmd.bg_color("white")
cmd.set("ambient", 0.45)
cmd.set("two_sided_lighting", 1)
cmd.set("ray_trace_mode", 1)
cmd.set("ray_shadows", 1)
cmd.set("antialias", 2)
cmd.set("depth_cue", 0)
cmd.set("ray_trace_gain", 0.1)
cmd.set("orthoscopic", 1)

# 3) Stick parameters
cmd.set("stick_radius", 0.24)
cmd.set("stick_ball", 1)
cmd.set("stick_ball_ratio", 1.6)

# 4) Clear stage: remove water, hide miscellaneous atoms, fully hide the whole protein cartoon (key point of this recipe)
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# 5) Key residues: select then merge the selections, show sticks, color one by one
sel_names = []
for i, (sel, col) in enumerate(KEY_RESIDUES):
    nm = f"k{i+1}"
    cmd.select(nm, f"{OBJECT} and {sel}")
    sel_names.append(nm)
    cmd.color(col, nm)
merged = " + ".join(sel_names)          # PyMOL selection addition
cmd.show("sticks", merged)

# 6) Compose + zoom in + 300dpi
cmd.orient(merged)
cmd.zoom(merged, FOCUS_ZOOM_LEVEL)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)

mol.stop()
print("SAVED", SAVE_PATH)
