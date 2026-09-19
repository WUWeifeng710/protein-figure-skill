"""
protein-figure 技能冒烟测试（smoke test）。
在安装了 PyMOL-PUB + PyMOL 2.5.0 的环境中运行，验证 3 个核心类可用。
运行：python smoke_test.py <一个本地 PDB 文件路径>
示例：python smoke_test.py <任意本地 PDB 文件路径>（如 1AY7.pdb，可从 RCSB 下载）
"""
import sys
from molpub import (DefaultStructureImage, HighlightStructureImage,
                    PropertyStructureImage, Figure, obtain_widget_icon)


def main(pdb: str):
    # 1) 基类：加载 + 旋转 + 保存
    d = DefaultStructureImage(structure_paths=[pdb])
    d.set_state(rotate=[30, 45, 0])
    d.save(save_path="smoke_default.png", width=800, ratio=1.0)
    d.close()

    # 2) 高亮类：隐藏水 + surface/cartoon + 配色
    h = HighlightStructureImage(structure_paths=[pdb])
    h.set_cache(cache_contents=["residue:HOH"])
    h.set_shape(representation_plan=[("chain:A", "surface"), ("chain:B", "cartoon")],
                closed_surface=True)
    h.set_state(rotate=[330, 10, 270])
    h.set_color(coloring_plan=[("chain:A", "0xF2F2F2"), ("chain:B", "0x2D2F82")])
    h.save(save_path="smoke_highlight.png", width=1280, ratio=0.9)
    h.close()

    # 3) 控件图标
    obtain_widget_icon(save_path="smoke_arrow.png", widget_type="arrow",
                       params={"degree": 90})

    # 4) Figure 版式（Science 全宽）
    fig = Figure(manuscript_format="Science", occupied_columns=3)
    fig.set_image(image_path="smoke_highlight.png", layout=(1, 1, 1))
    fig.set_image(image_path="smoke_arrow.png", locations=[0.85, 0.8, 0.1, 0.1],
                  transparent=True)
    fig.save_figure("smoke_figure.png")

    print("OK: 4 objects verified")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
