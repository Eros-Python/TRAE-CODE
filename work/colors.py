from pptx import Presentation
from pptx.util import Pt
prs = Presentation('/workspace/.uploads/1791a752-ca03-4dbb-aa21-f8effe3051ef_四家对比-泰格-太美-Sanofi-IQVIA.pptx')

def color_of(fmt):
    try:
        if fmt.type is not None and hasattr(fmt, 'fore_color') and fmt.fore_color and fmt.fore_color.type is not None:
            return str(fmt.fore_color.rgb)
    except Exception:
        pass
    return None

for i, slide in enumerate(prs.slides):
    if i > 2: break
    print(f"=== SLIDE {i+1} ===")
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                for r in p.runs:
                    f = r.font
                    col = color_of(f.color) if f.color else None
                    print(f"  sz={f.size.pt if f.size else None} bold={f.bold} name={f.name} color={col} text={r.text[:40]!r}")
                    break
                break
        try:
            fill = shape.fill
            if fill.type is not None and str(fill.type) == 'MSO_FILL_TYPE.SOLID (1)':
                print(f"  SHAPE {shape.name} fill={fill.fore_color.rgb}")
        except Exception as e:
            pass
