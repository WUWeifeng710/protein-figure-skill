"""
Smoke test for the protein-figure skill.

Run in an environment with PyMOL-PUB + PyMOL 2.5.0 installed; verifies the
three core classes are usable.

Usage:   python smoke_test.py <path-to-a-local-PDB>
Example: python smoke_test.py <any-local-PDB> (e.g. 1AY7.pdb, downloadable from RCSB)
"""
import sys
from molpub import (DefaultStructureImage, HighlightStructureImage,
                    PropertyStructureImage, Figure, obtain_widget_icon)


def main(pdb: str):
    # 1) Base class: load + rotate + save
    d = DefaultStructureImage(structure_paths=[pdb])
    d.set_state(rotate=[30, 45, 0])
    d.save(save_path="smoke_default.png", width=800, ratio=1.0)
    d.close()

    # 2) Highlight class: hide water + surface/cartoon + coloring
    h = HighlightStructureImage(structure_paths=[pdb])
    h.set_cache(cache_contents=["residue:HOH"])
    h.set_shape(representation_plan=[("chain:A", "surface"), ("chain:B", "cartoon")],
                closed_surface=True)
    h.set_state(rotate=[330, 10, 270])
    h.set_color(coloring_plan=[("chain:A", "0xF2F2F2"), ("chain:B", "0x2D2F82")])
    h.save(save_path="smoke_highlight.png", width=1280, ratio=0.9)
    h.close()

    # 3) Widget icon
    obtain_widget_icon(save_path="smoke_arrow.png", widget_type="arrow",
                       params={"degree": 90})

    # 4) Figure layout (Science full-width)
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
