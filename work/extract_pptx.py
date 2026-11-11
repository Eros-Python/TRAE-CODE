from pptx import Presentation
from pptx.util import Emu
import sys

def describe(path, name):
    print(f"\n########## {name} ##########")
    prs = Presentation(path)
    print(f"Slide size: {prs.slide_width} x {prs.slide_height} ({Emu(prs.slide_width).inches:.2f}in x {Emu(prs.slide_height).inches:.2f}in)")
    print(f"Num slides: {len(prs.slides)}")
    print(f"Num slide layouts: {sum(len(m.slide_layouts) for m in prs.slide_masters)}")
    for i, slide in enumerate(prs.slides):
        print(f"\n--- SLIDE {i+1} (layout: {slide.slide_layout.name}) ---")
        for shape in slide.shapes:
            t = ""
            if shape.has_text_frame:
                t = " | ".join(p.text for p in shape.text_frame.paragraphs if p.text.strip())[:150]
            print(f"  [{shape.shape_type}] name={shape.name!r} pos=({Emu(shape.left).inches:.2f},{Emu(shape.top).inches:.2f}) size=({Emu(shape.width).inches:.2f}x{Emu(shape.height).inches:.2f}) text={t!r}")
            if shape.has_table:
                tbl = shape.table
                print(f"    TABLE {len(tbl.rows)}x{len(tbl.columns)}")
                for r in tbl.rows[:6]:
                    print("    " + " | ".join(c.text.strip()[:25] for c in r.cells))

describe('/workspace/.uploads/69d8006b-ee89-4a24-827e-fdbb755c096d_03 康龙临床PPT模板(通用模板)-20220426【命名格式：题目-日期yyyyMMdd】.pptx', 'TEMPLATE')
