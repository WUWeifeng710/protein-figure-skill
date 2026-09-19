# spectrum_resi 模板渲染脚本参考（2.5.0 严格 API，已对 1AY7 出样图验证）
# 序列位置 B-factor/pLDDT 谱着色（蓝白红渐变 cartoon + CA 小球）
# 运行：在装有 PyMOL 2.5.0 + PyMOL-PUB 的环境里跑，例如 `conda run -n pymol_pub python spectrum_resi.py`
# 用法：改 PDB / OBJECT / PROPERTY / PALETTE 后跑
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
PROPERTY = "resi"              # 默认按残基位置；PDB 带 b 列可试 "b"，带 plddt 列可试 "plddt"
PALETTE = "blue_white_red"     # blue_white_red / blue_green_red / rainbow / red_white_blue
SAVE_PATH = "nice_fig_spectrum.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

# 0) 加载 + 校验（命中 0 即退出）
cmd.load(PDB, OBJECT, quiet=1)
if int(cmd.count_atoms("all")) == 0:
    print("LOAD FAILED: 0 atoms after load"); mol.stop(); sys.exit(1)

# 1) 白底柔光
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

# 2) 清场
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# 3) cartoon + spectrum 渐变
cmd.show("cartoon", OBJECT)
cmd.spectrum(PROPERTY, PALETTE, OBJECT)

# 4) CA 小球（可选）
cmd.show("spheres", f"{OBJECT} and name CA")
cmd.set("sphere_scale", 0.5)

# 5) 构图 + 300dpi
cmd.orient(OBJECT)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
