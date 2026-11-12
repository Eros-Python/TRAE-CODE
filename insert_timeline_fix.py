"""修复：重新插入时间线图，正确处理致谢位置。"""
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

# ---------- 确认当前状态 ----------
print(f'当前 {len(prs.slides)} slides:')
for i, s in enumerate(prs.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:50]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else f'(shapes={len(s.shapes)})'
    print(f'  {i+1:2d}. {first}')

# 当前状态：
#  1: 01        ← 原 slide 2
#  2-25: 原 slide 3-26（但位置乱了）
#  26: shapes=0  ← 原致谢
#  27: PHARMARON ← 原封面被错移到末尾

# ---------- 重新排好序 ----------
# 正确顺序应该是：
#  1. 封面 PHARMARON
#  2. 01 市场规模与数据
#  ...
#  26. IQVIA 词云
#  27. 致谢（shapes=0）

# 先把封面从末尾移回首位
sldIdLst = prs.slides._sldIdLst
cover = None
thanks = None
for i, s in enumerate(prs.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:30]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else ''
    if 'PHARMARON' in first.upper():
        cover = sldIdLst[i]
    if len(s.shapes) == 0:
        thanks = sldIdLst[i]

if cover and sldIdLst.index(cover) != 0:
    sldIdLst.remove(cover)
    sldIdLst.insert(0, cover)
    print(f'封面移到首位')

# 确保致谢在末尾
if thanks:
    idx = sldIdLst.index(thanks)
    if idx != len(sldIdLst) - 1:
        sldIdLst.remove(thanks)
        sldIdLst.append(thanks)
        print(f'致谢移到末尾')

prs.save(PPT_PATH)

# ---------- 现在插入时间线图到正确位置 ----------
prs2 = Presentation(PPT_PATH)
sldIdLst = prs2.slides._sldIdLst

# 找到 Veeva 宣传图 2 的位置（slide 名含 "Safety Signal"）
veeva_signal_idx = None
for i, s in enumerate(prs2.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else ''
    if 'Safety Signal' in first:
        veeva_signal_idx = i
        break

print(f'Veeva Signal slide 索引: {veeva_signal_idx}')

# 时间线图应该插在 Veeva Signal 之后
# 但首先要新建一张 slide 加时间线图
new_slide = prs2.slides.add_slide(prs2.slide_layouts[5])

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
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), prs2.slide_width, Inches(0.85))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    add_textbox(slide, Inches(0.5), Inches(0.18), prs2.slide_width - Inches(1), Inches(0.55),
                text, size=18, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

add_title(new_slide, 'Veeva 发展脉络：Safety Suite 与 AI 的关键节点（2007–2026）')

img_x = Inches(0.4)
img_top = Inches(0.95)
img_bottom_margin = Inches(0.5)
img_h = prs2.slide_height - img_top - img_bottom_margin - Inches(0.15)
img_w = prs2.slide_width - img_x * 2
new_slide.shapes.add_picture(IMG, img_x, img_top, img_w, img_h)

add_textbox(new_slide, Inches(0.5), prs2.slide_height - Inches(0.42),
            prs2.slide_width - Inches(1), Inches(0.3),
            '出处：Veeva 官网产品卡 / 新闻稿 / Release Notes / Pantheon · 2019 NLP / 2022 22R3 / 2025 AI Agent 为三大拐点',
            size=8, color=GRAY, align=PP_ALIGN.CENTER)

# 把新建的 slide（在末尾）移到 veeva_signal_idx + 1
new_sldId = sldIdLst[-1]
sldIdLst.remove(new_sldId)
sldIdLst.insert(veeva_signal_idx + 1, new_sldId)
print(f'时间线图已插入到索引 {veeva_signal_idx + 1}（Veeva Signal 之后）')

# ---------- 再次确保致谢在末尾 ----------
for i, s in enumerate(prs2.slides):
    if len(s.shapes) == 0:
        target = sldIdLst[i]
        sldIdLst.remove(target)
        sldIdLst.append(target)
        print(f'致谢移到末尾')
        break

# ---------- 更新页码 ----------
TOTAL_NEW = len(prs2.slides)
for slide in prs2.slides:
    for shape in slide.shapes:
        if not hasattr(shape, 'has_text_frame') or not shape.has_text_frame:
            continue
        tf = shape.text_frame
        for para in tf.paragraphs:
            for run in para.runs:
                new_text = re.sub(r'(\d+)\s*/\s*\d+\b',
                                  lambda m: f'{m.group(1)} / {TOTAL_NEW}',
                                  run.text)
                if new_text != run.text:
                    run.text = new_text

prs2.save(PPT_PATH)

print(f'\n最终 slide 列表 ({len(prs2.slides)}):')
for i, s in enumerate(prs2.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:55]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else f'(shapes={len(s.shapes)})'
    print(f'  {i+1:2d}. {first}')
