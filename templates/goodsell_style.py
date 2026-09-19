# goodsell_style 模板渲染脚本参考（2.5.0 严格 API，已对 1AY7 出样图验证）
# Goodsell 风格平面化粉彩球（按链分色，无阴影柔光）
# 运行：在装有 PyMOL 2.5.0 + PyMOL-PUB 的环境里跑，例如 `conda run -n pymol_pub python goodsell_style.py`
# 用法：改 PDB / OBJECT / CHAIN_COLORS / REPR 后跑
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
CHAIN_COLORS = {"A": "gs_blue", "B": "gs_red"}   # 只写目标 PDB 实际存在的链
REPR = "spheres"                                   # spheres / surface
SAVE_PATH = "nice_fig_goodsell.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

cmd.load(PDB, OBJECT, quiet=1)
if int(cmd.count_atoms("all")) == 0:
    print("LOAD FAILED: 0 atoms after load"); mol.stop(); sys.exit(1)

# Goodsell 平面化渲染（flat / no-shadow / 高 ambient）
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

# Goodsell 粉彩调色板（必须在同一实例内定义）
cmd.set_color("gs_blue",   [0.565, 0.714, 0.812])
cmd.set_color("gs_red",    [0.855, 0.475, 0.427])
cmd.set_color("gs_green",  [0.631, 0.792, 0.596])
cmd.set_color("gs_tan",    [0.871, 0.812, 0.682])
cmd.set_color("gs_orange", [0.871, 0.639, 0.376])

# 清场
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# 表示 + 按链分色
cmd.show(REPR, OBJECT)
for chain, color in CHAIN_COLORS.items():
    cmd.color(color, f"{OBJECT} and chain {chain}")

# 构图 + 300dpi
cmd.orient(OBJECT)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
