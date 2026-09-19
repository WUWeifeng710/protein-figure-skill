# pastel_cartoon_surface 模板渲染脚本参考（2.5.0 严格 API 实测版）
# 用法：替换 PDB / OBJECT / CHAINS / SAVE_PATH 后跑。
# 运行：在装有 PyMOL 2.5.0 + PyMOL-PUB 的环境里跑，例如 `conda run -n pymol_pub python pastel_cartoon_surface.py`
# 坑点见 SKILL.md「配方迁移踩坑」：set_color 用命令式、hide 第一参必须合法 representation。
import os
from pymol2 import PyMOL

# —— params（从模板 yaml 覆写而来）——
PDB = "protein.pdb"               # 输入结构文件
OBJECT = "m"                       # PDB 加载对象名
CART, SURF = "cart", "surf"       # 拆出的 cartoon / surface 对象
CHAINS = {"A": "soft_blue", "B": "rose_pink", "C": "lavender", "D": "soft_cream"}
SURF_COLOR, SURF_TRANS = "gray90", 0.60
SAVE_PATH = "nice_fig.png"
SAVE_WIDTH, SAVE_RATIO, SAVE_DPI = 1600, 1.0, 300

mol = PyMOL()
mol.start()
cmd = mol.cmd

# 0) 加载结构（配方默认结构已加载为对象 m；脚本里需显式 load）
cmd.load(PDB, OBJECT, quiet=1)

# 1) 自定义粉彩调色板（set_color 是命令，不是 set("color",...)）
cmd.set_color("soft_blue",  [0.63, 0.75, 0.94])
cmd.set_color("rose_pink",  [0.94, 0.69, 0.75])
cmd.set_color("lavender",   [0.78, 0.72, 0.84])
cmd.set_color("soft_cream", [0.98, 0.93, 0.80])

# 2) 白底 + 柔光渲染参数
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

# 3) 清场（2.5.0 严格：hide 第一参必须合法 representation，hetatm 是选区）
cmd.remove(f"{OBJECT} and resn HOH")
cmd.hide("everything", "hetatm")
cmd.hide("everything")

# 4) 拆对象（cart/surf 分色互不干扰）
cmd.create(CART, OBJECT)
cmd.create(SURF, OBJECT)
cmd.hide("everything", OBJECT)   # 再藏掉原对象，只显示拆出的两个

# 5) cartoon 按链上粉彩（实际链数不足 4 条时 CHAINS 只保留存在的链）
cmd.show("cartoon", CART)
for chain, color in CHAINS.items():
    cmd.color(color, f"{CART} and chain {chain}")

# 6) surface 中性 + 半透明
cmd.show("surface", SURF)
cmd.color(SURF_COLOR, SURF)
cmd.set("transparency", SURF_TRANS)

# 7) 构图 + 300dpi 输出
cmd.orient(CART)
cmd.ray()
cmd.png(SAVE_PATH, width=SAVE_WIDTH, height=int(SAVE_WIDTH * SAVE_RATIO), dpi=SAVE_DPI, quiet=1)

mol.stop()
print("SAVED", SAVE_PATH)
