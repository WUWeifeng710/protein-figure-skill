# ss_frosted_surface template render script reference (2.5.0 strict API, validated with 1AY7 sample figure)
# cartoon pastels by secondary structure, surface uses the same color (echoing the cartoon) + 0.60 transparency (frosted glass)
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python ss_frosted_surface.py`
import os
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
CART, SURF = "cart", "surf"
SAVE_PATH = "nice_fig_ss_frosted.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

# 0) Load
cmd.load(PDB, OBJECT, quiet=1)

# 1) Pastel palette
cmd.set_color("soft_blue", [0.63, 0.75, 0.94])
cmd.set_color("rose_pink", [0.94, 0.69, 0.75])
cmd.set_color("lavender",  [0.78, 0.72, 0.84])

# 2) white bg soft light
cmd.bg_color("white")
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

# 3) clear stage
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# 4) Split objects
cmd.create(CART, OBJECT)
cmd.create(SURF, OBJECT)
cmd.hide("everything", OBJECT)

# 5) cartoon colored by secondary structure
cmd.show("cartoon", CART)
cmd.color("soft_blue", f"{CART} and ss h")
cmd.color("rose_pink", f"{CART} and ss s")
cmd.color("lavender",  f"{CART} and not (ss h or ss s)")

# 6) surface same color by ss (frosted-glass echo, richer color)
cmd.show("surface", SURF)
cmd.color("soft_blue", f"{SURF} and ss h")
cmd.color("rose_pink", f"{SURF} and ss s")
cmd.color("lavender",  f"{SURF} and not (ss h or ss s)")
cmd.set("transparency", 0.60)

# 7) compose + 300dpi
cmd.orient(CART)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)

mol.stop()
print("SAVED", SAVE_PATH)
