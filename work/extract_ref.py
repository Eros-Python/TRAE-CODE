from pptx import Presentation
from pptx.util import Emu

prs = Presentation('/workspace/.uploads/1791a752-ca03-4dbb-aa21-f8effe3051ef_四家对比-泰格-太美-Sanofi-IQVIA.pptx')
print(f"Slide size: {prs.slide_width} x {prs.slide_height} ({Emu(prs.slide_width).inches:.2f} x {Emu(prs.slide_height).inches:.2f} in)")
print(f"Num slides: {len(prs.slides)}")
for i, slide in enumerate(prs.slides):
    print(f"\n=== SLIDE {i+1} (layout: {slide.slide_layout.name}) ===")
    for shape in slide.shapes:
        t = ""
        if shape.has_text_frame:
            t = " || ".join(p.text for p in shape.text_frame.paragraphs if p.text.strip())[:300]
        print(f"  [{shape.shape_type}] {shape.name!r} pos=({Emu(shape.left).inches:.2f},{Emu(shape.top).inches:.2f}) size=({Emu(shape.width).inches:.2f}x{Emu(shape.height).inches:.2f})")
        if t:
            print(f"    TEXT: {t}")
        if shape.has_table:
            tbl = shape.table
            print(f"    TABLE {len(tbl.rows)}x{len(tbl.columns)}:")
            for r in tbl.rows[:8]:
                print("      " + " | ".join(c.text.strip()[:30] for c in r.cells))
