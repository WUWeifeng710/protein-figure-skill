# ppi_interface 模板渲染脚本参考（2.5.0 严格 API，已对 1AY7 出样图验证）
# 蛋白-蛋白界面（两链 within 半径取界面残基 + sticks + 半透明面）
# 运行：在装有 PyMOL 2.5.0 + PyMOL-PUB 的环境里跑，例如 `conda run -n pymol_pub python ppi_interface.py`
# 用法：改 PDB / OBJECT / CHAIN_A / CHAIN_B / CUTOFF 后跑
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

# 白底柔光
cmd.bg_color("white")
cmd.set("ray_opaque_background", 1)
cmd.set("ambient", 0.5); cmd.set("two_sided_lighting", 1)
cmd.set("ray_trace_mode", 1); cmd.set("ray_shadows", 1)
cmd.set("antialias", 2); cmd.set("depth_cue", 0)
cmd.set("ray_trace_gain", 0.1); cmd.set("orthoscopic", 1)
cmd.set("cartoon_fancy_helices", 1); cmd.set("cartoon_smooth_loops", 1)
cmd.set("cartoon_flat_sheets", 1); cmd.set("cartoon_highlight_color", "grey50")

# 清场
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# 卡通 + 按链分色
cmd.show("cartoon", OBJECT)
cmd.color(CA_COLOR, f"{OBJECT} and chain {CHAIN_A} and elem C")
cmd.color(CB_COLOR, f"{OBJECT} and chain {CHAIN_B} and elem C")

# 界面残基（within 半径 + byres 扩展）
cmd.select("ifaceA", f"byres ({OBJECT} and chain {CHAIN_A} within {CUTOFF} of {OBJECT} and chain {CHAIN_B})")
cmd.select("ifaceB", f"byres ({OBJECT} and chain {CHAIN_B} within {CUTOFF} of {OBJECT} and chain {CHAIN_A})")
cmd.show("sticks", "sc. and (ifaceA or ifaceB)")
cmd.show("spheres", "n. CA and (ifaceA or ifaceB)")
cmd.set("sphere_scale", 0.4)

# 界面半透明面（可选）
cmd.create("surfA", "ifaceA")
cmd.create("surfB", "ifaceB")
cmd.show("surface", "surfA")
cmd.show("surface", "surfB")
cmd.set("transparency", 0.6)
cmd.color(CA_COLOR, "surfA")
cmd.color(CB_COLOR, "surfB")

# 构图 + 300dpi
cmd.orient(OBJECT)
cmd.zoom("ifaceA or ifaceB", 8)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
