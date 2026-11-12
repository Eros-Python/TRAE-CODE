"""在 PPT 中插入 Veeva 发展脉络时间线图，放在 Veeva 卖点卡之前（Veeva 特点组内）。

目标顺序：
  1-19  IQVIA 相关不变
  20-21 Veeva 官方宣传图 1+2
  22    Veeva 发展脉络时间线图  ← 新增
  23    Veeva 卖点提炼
  24    IQVIA 卖点提炼
  25    Veeva 词云
  26    IQVIA 词云
  27    致谢（自动移最后）
"""
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
            t = sh.text.strip()[:55]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else f'(图片/其他, {len(s.shapes)} shapes)'
    print(f'  {i+1:2d}. {first}')

# ---------- 辅助函数 ----------
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

# ---------- 新建 slide（追加到末尾） ----------
new_slide = prs.slides.add_slide(prs.slide_layouts[5])
add_title(new_slide, 'Veeva 发展脉络：Safety Suite 与 AI 的关键节点（2007–2026）')

# 图片区域
img_x = Inches(0.4)
img_top = Inches(0.95)
img_bottom_margin = Inches(0.5)
img_h = SLIDE_H - img_top - img_bottom_margin - Inches(0.15)
img_w = SLIDE_W - img_x * 2
new_slide.shapes.add_picture(IMG, img_x, img_top, img_w, img_h)

# 图注
add_textbox(new_slide, Inches(0.5), SLIDE_H - Inches(0.42),
            SLIDE_W - Inches(1), Inches(0.3),
            '出处：Veeva 官网产品卡 / 新闻稿 / Release Notes / Pantheon · 2019 NLP / 2022 22R3 / 2025 AI Agent 为三大拐点',
            size=8, color=GRAY, align=PP_ALIGN.CENTER)

prs.save(PPT_PATH)
print(f'\n追加新 slide 后共 {len(prs.slides)} slides')

# ---------- 用 lxml 把新 slide 从末尾移动到第 21 位（索引 20） ----------
# 顺序：新 slide 应该在 Veeva 宣传图 2（当前第 21 页，索引 20）之后
# sldIdLst 里最后一个是新 slide，把它插到索引 21 的位置
from lxml import etree

prs2 = Presentation(PPT_PATH)
sldIdLst = prs2.slides._sldIdLst
new_sldId = sldIdLst[-1]  # 最后一个是刚加的
sldIdLst.remove(new_sldId)
# 插入到索引 21（Veeva 宣传图 2 之后，即原第 22 页 Veeva 卖点卡之前）
sldIdLst.insert(21, new_sldId)
print(f'新 slide 已移到索引 21（第 22 位）')

# ---------- 把致谢移到最后 ----------
for i, s in enumerate(prs2.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else ''
    if 'PHARMARON' in first.upper() and i != len(prs2.slides) - 1:
        target = sldIdLst[i]
        sldIdLst.remove(target)
        sldIdLst.append(target)
        print(f'致谢从 slide {i+1} 移到末尾')
        break

# ---------- 更新页码 ----------
TOTAL_NEW = len(prs2.slides)
TOTAL_OLD = TOTAL_NEW - 1  # 新增了1页
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

print(f'\n最终 slide 列表 ({len(prs2.slides)}):')
for i, s in enumerate(prs2.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:55]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else f'(图片/其他, {len(s.shapes)} shapes)'
    print(f'  {i+1:2d}. {first}')
