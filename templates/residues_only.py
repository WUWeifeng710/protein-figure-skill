# residues_only 模板渲染脚本参考（2.5.0 严格 API）
# 完全隐藏蛋白，只显关键残基 sticks（柔和粉彩 + 白底柔光）
# 运行：在装有 PyMOL 2.5.0 + PyMOL-PUB 的环境里跑，例如 `conda run -n pymol_pub python residues_only.py`
# 用法：改 PDB / OBJECT / KEY_RESIDUES（残基选区→颜色）后跑
from pymol2 import PyMOL

PDB = "protein.pdb"
OBJECT = "m"
# 关键残基：(选区字符串, 颜色名)。选区可带链前缀，如 "A/35" 或 "chain A and resi 12"
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

# 0) 加载
cmd.load(PDB, OBJECT, quiet=1)

# 1) 柔和粉彩调色板（set_color 是命令）
cmd.set_color("sh_pink",  [0.91, 0.73, 0.76])
cmd.set_color("sh_blue",  [0.67, 0.75, 0.86])
cmd.set_color("sh_lav",   [0.80, 0.76, 0.86])
cmd.set_color("sh_cream", [0.98, 0.93, 0.80])

# 2) 白底 + 柔光
cmd.bg_color("white")
cmd.set("ambient", 0.45)
cmd.set("two_sided_lighting", 1)
cmd.set("ray_trace_mode", 1)
cmd.set("ray_shadows", 1)
cmd.set("antialias", 2)
cmd.set("depth_cue", 0)
cmd.set("ray_trace_gain", 0.1)
cmd.set("orthoscopic", 1)

# 3) 棒状参数
cmd.set("stick_radius", 0.24)
cmd.set("stick_ball", 1)
cmd.set("stick_ball_ratio", 1.6)

# 4) 清场：去水、藏杂原子、整条蛋白卡通全藏（本配方要点）
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# 5) 关键残基：select 后合并选区 show sticks，逐个上色
sel_names = []
for i, (sel, col) in enumerate(KEY_RESIDUES):
    nm = f"k{i+1}"
    cmd.select(nm, f"{OBJECT} and {sel}")
    sel_names.append(nm)
    cmd.color(col, nm)
merged = " + ".join(sel_names)          # PyMOL 选区加法
cmd.show("sticks", merged)

# 6) 构图 + 拉近 + 300dpi
cmd.orient(merged)
cmd.zoom(merged, FOCUS_ZOOM_LEVEL)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)

mol.stop()
print("SAVED", SAVE_PATH)
