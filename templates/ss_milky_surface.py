# ss_milky_surface 模板渲染脚本参考（2.5.0 严格 API，已对 1AY7 出样图验证）
# cartoon 按二级结构上粉彩（ss h=soft_blue / ss s=rose_pink / loop=lavender）
# surface 中性 gray90 + 0.60 透（乳白壳）
# 运行：在装有 PyMOL 2.5.0 + PyMOL-PUB 的环境里跑，例如 `conda run -n pymol_pub python ss_milky_surface.py`
import os
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
CART, SURF = "cart", "surf"
SAVE_PATH = "nice_fig_ss_milky.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

# 0) 加载
cmd.load(PDB, OBJECT, quiet=1)

# 1) 粉彩调色板
cmd.set_color("soft_blue", [0.63, 0.75, 0.94])   # ss h
cmd.set_color("rose_pink", [0.94, 0.69, 0.75])   # ss s
cmd.set_color("lavender",  [0.78, 0.72, 0.84])   # loop

# 2) 白底柔光
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

# 3) 清场
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# 4) 拆对象
cmd.create(CART, OBJECT)
cmd.create(SURF, OBJECT)
cmd.hide("everything", OBJECT)

# 5) cartoon 按二级结构上色（对拆出的 cart 对象用 ss 选区）
cmd.show("cartoon", CART)
cmd.color("soft_blue", f"{CART} and ss h")
cmd.color("rose_pink", f"{CART} and ss s")
cmd.color("lavender",  f"{CART} and not (ss h or ss s)")

# 6) surface 中性 + 半透明（乳白壳）
cmd.show("surface", SURF)
cmd.color("gray90", SURF)
cmd.set("transparency", 0.60)

# 7) 构图 + 300dpi
cmd.orient(CART)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)

mol.stop()
print("SAVED", SAVE_PATH)
