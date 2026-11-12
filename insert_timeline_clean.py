"""干净地插入 Veeva 时间线图：只新建一张 slide 并移动到指定位置，不动其他页。"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import re

PPT_PATH = '/workspace/PV数据库市场调研总结-20261111.pptx'
IMG = '/workspace/Veeva发展脉络_v3_紧凑版.png'

prs = Presentation(PPT_PATH)
SLIDE_W = prs.slide_width
SLIDE_H = prs.slide_height
NAVY = RGBColor(22, 44, 92)
GRAY = RGBColor(95, 99, 104)
WHITE = RGBColor(255, 255, 255)

# ---------- 确认当前结构 ----------
print(f'当前 {len(prs.slides)} slides:')
for i, s in enumerate(prs.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:50]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else f'(shapes={len(s.shapes)})'
    print(f'  {i+1:2d}. {first}')

# ---------- 新建 slide（追加到末尾） ----------
new_slide = prs.slides.add_slide(prs.slide_layouts[5])

def add_textbox(slide, left, top, width, height, text, size=11, bold=False,
                color=NAVY, align=PP_ALIGN.LEFT, font_name='微软雅黑'):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font_name
    return txBox

def add_title(slide, text):
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), SLIDE_W, Inches(0.85))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    add_textbox(slide, Inches(0.5), Inches(0.18), SLIDE_W - Inches(1), Inches(0.55),
                text, size=18, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

add_title(new_slide, 'Veeva 发展脉络：Safety Suite 与 AI 的关键节点（2007–2026）')

img_x = Inches(0.4)
img_top = Inches(0.95)
img_bottom_margin = Inches(0.5)
img_h = SLIDE_H - img_top - img_bottom_margin - Inches(0.15)
img_w = SLIDE_W - img_x * 2
new_slide.shapes.add_picture(IMG, img_x, img_top, img_w, img_h)

add_textbox(new_slide, Inches(0.5), SLIDE_H - Inches(0.42),
            SLIDE_W - Inches(1), Inches(0.3),
            '出处：Veeva 官网产品卡 / 新闻稿 / Release Notes / Pantheon · 2019 NLP / 2022 22R3 / 2025 AI Agent 为三大拐点',
            size=8, color=GRAY, align=PP_ALIGN.CENTER)

prs.save(PPT_PATH)
print(f'\n追加后 {len(prs.slides)} slides')

# ---------- 用 lxml 移动：新 slide 在末尾，移到索引 21（Veeva Signal 之后） ----------
prs2 = Presentation(PPT_PATH)
sldIdLst = prs2.slides._sldIdLst

# 确认 Veeva Signal 在索引 20
signal_shapes_info = []
for sh in prs2.slides[20].shapes:
    if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
        t = sh.text.strip()[:30]
        if t: signal_shapes_info.append(t)
print(f'索引 20 = {signal_shapes_info[0] if signal_shapes_info else "(无)"}')

# 移动新 slide（在末尾）到索引 21
new_sldId = sldIdLst[-1]
sldIdLst.remove(new_sldId)
sldIdLst.insert(21, new_sldId)
print(f'新 slide 已移到索引 21（Veeva Signal 之后）')

# ---------- 更新页码 ----------
TOTAL_NEW = len(sldIdLst)
TOTAL_OLD = TOTAL_NEW - 1
for slide in prs2.slides:
    for shape in slide.shapes:
        if not hasattr(shape, 'has_text_frame') or not shape.has_text_frame:
            continue
        tf = shape.text_frame
        for para in tf.paragraphs:
            for run in para.runs:
                new_text = re.sub(rf'(\d+)\s*/\s*{TOTAL_OLD}\b',
                                  rf'\1 / {TOTAL_NEW}',
                                  run.text)
                if new_text != run.text:
                    run.text = new_text

prs2.save(PPT_PATH)

print(f'\n最终 {TOTAL_NEW} slides:')
for i, s in enumerate(prs2.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:55]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else f'(shapes={len(s.shapes)})'
    marker = ' ★ 时间线' if '发展脉络' in first else ''
    print(f'  {i+1:2d}. {first}{marker}')
