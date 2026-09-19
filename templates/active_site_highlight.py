# active_site_highlight 模板渲染脚本参考（2.5.0 严格 API，已对 1AY7 出样图验证）
# 活性位点特写：关键残基 sticks + 半透明 cartoon 环境 + 极性接触虚线
# 运行：在装有 PyMOL 2.5.0 + PyMOL-PUB 的环境里跑，例如 `conda run -n pymol_pub python active_site_highlight.py`
# 用法：改 PDB / OBJECT / CAT_RESI / CUTOFF / SAVE_PATH 后跑
import os, sys
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
CAT_RESI = [35, 52, 62, 63]   # 关键残基号（按目标 PDB 实际改）
CUTOFF = 5.0                  # 周边环境半径（Å）
SAVE_PATH = "nice_fig_active_site.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

# 0) 加载 + 校验
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

# 3) 关键残基选区（逐个 select + extend，2.5.0 select 严格不吃 +/or 拼接）
cmd.select("catalytic", f"{OBJECT} and resi {CAT_RESI[0]}")
for r in CAT_RESI[1:]:
    cmd.select("_t", f"{OBJECT} and resi {r}")
    cmd.extend("catalytic", "_t")

# 4) 周边环境（byres 必须在 hide everything 之后做，hide 会清空选区）
cmd.select("cat_env", f"byres (catalytic around {CUTOFF}) and not catalytic")
cmd.show("cartoon", "cat_env")
cmd.set("cartoon_transparency", 0.7)

# 5) 关键残基 sticks + CA 球
cmd.show("sticks", f"sc. and (catalytic)")
cmd.show("spheres", f"n. CA and (catalytic)")
cmd.set("sphere_scale", 0.5)

# 6) 极性接触（mode=2：键+氢键；PDB 缺 H 时接触可能稀疏）
try:
    cmd.dist("cat_contacts", "catalytic", "catalytic", mode=2)
    cmd.hide("labels", "cat_contacts")
    cmd.set("dash_color", "black")
    cmd.set("dash_gap", 0.3)
    cmd.set("dash_radius", 0.06)
except Exception as e:
    print("dist warn:", e)

# 7) 构图 + 300dpi
cmd.orient("catalytic")
cmd.zoom("catalytic", 10)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)
mol.stop()
print("SAVED", SAVE_PATH)
