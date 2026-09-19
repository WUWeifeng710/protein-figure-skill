# pastel_cartoon_surface template render script reference (2.5.0 strict API, validated)
# Usage: replace PDB / OBJECT / CHAINS / SAVE_PATH before running.
# Run: execute in an environment with PyMOL 2.5.0 + PyMOL-PUB installed, e.g. `conda run -n pymol_pub python pastel_cartoon_surface.py`
# Pitfalls: see SKILL.md "Recipe migration pitfalls": set_color is a command, the first arg of hide must be a legal representation.
import os
from pymol2 import PyMOL

# —— params (overwritten from the template yaml) ——
PDB = "protein.pdb"               # input structure file
OBJECT = "m"                       # PDB load object name
CART, SURF = "cart", "surf"       # split cartoon / surface objects
CHAINS = {"A": "soft_blue", "B": "rose_pink", "C": "lavender", "D": "soft_cream"}
SURF_COLOR, SURF_TRANS = "gray90", 0.60
SAVE_PATH = "nice_fig.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

# 0) Load the structure (the recipe's default structure is loaded as object m; the script must load explicitly)
cmd.load(PDB, OBJECT, quiet=1)

# 1) Custom pastel palette (set_color is a command, not set("color",...))
cmd.set_color("soft_blue",  [0.63, 0.75, 0.94])
cmd.set_color("rose_pink",  [0.94, 0.69, 0.75])
cmd.set_color("lavender",   [0.78, 0.72, 0.84])
cmd.set_color("soft_cream", [0.98, 0.93, 0.80])

# 2) White background + soft light rendering params
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

# 3) Clear the stage (2.5.0 strict: the first argument of hide must be a legal representation; hetatm is a selection)
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# 4) Split objects (cart/surf colored independently without interfering each other)
cmd.create(CART, OBJECT)
cmd.create(SURF, OBJECT)
cmd.hide("everything", OBJECT)   # hide the original object too, showing only the two split ones

# 5) cartoon per-chain pastels (when fewer than 4 chains exist, CHAINS keeps only the existing ones)
cmd.show("cartoon", CART)
for chain, color in CHAINS.items():
    cmd.color(color, f"{CART} and chain {chain}")

# 6) Surface neutral + translucent
cmd.show("surface", SURF)
cmd.color(SURF_COLOR, SURF)
cmd.set("transparency", SURF_TRANS)

# 7) Compose + 300dpi output
cmd.orient(CART)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)

mol.stop()
print("SAVED", SAVE_PATH)
