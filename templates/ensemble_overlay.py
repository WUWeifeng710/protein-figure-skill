# ensemble_overlay 模板渲染脚本参考（2.5.0 严格 API，已对 1AY7 出样图验证）
# NMR / MD 多模型叠加（按 state 渐变 + 半透明）
# 运行：在装有 PyMOL 2.5.0 + PyMOL-PUB 的环境里跑，例如 `conda run -n pymol_pub python ensemble_overlay.py`
# 用法：改 PDB / OBJECT / STYLE / TRANSPARENCY 后跑
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

# 表示 + state 渐变（多模型 NMR 时生效；单帧退化可忽略报错）
cmd.show(STYLE, OBJECT)
try:
    cmd.spectrum("state", "rainbow", OBJECT)
except Exception as e:
    print("spectrum state warn:", e)
cmd.set("transparency", TRANSPARENCY)

# 构图 + 300dpi
cmd.orient(OBJECT)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
