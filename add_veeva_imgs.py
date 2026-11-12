"""插入 Veeva 官方宣传图（替代 IQVIA 宣传图之后的空位），和 IQVIA 那两张结构对称。

目标 slide 顺序：
  17 IQVIA 库+服务+AI
  18-19 IQVIA 宣传图 1+2
  20-21 Veeva 宣传图 1+2  ← 新增
  22 Veeva 卖点提炼
  23 IQVIA 卖点提炼
  24 Veeva 词云
  25 IQVIA 词云
  26 致谢
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from lxml import etree
import re

PPT_PATH = '/workspace/PV数据库市场调研总结-20261111.pptx'

# 使用 Veeva Safety Datasheet p1 和 Signal Features Brief p1
# 先把渲染好的 PNG 复制/重命名为有意义的名字
import shutil
shutil.copy('/workspace/veeva_safety_datasheet_2018_p1.png', '/workspace/Veeva_官方宣传图1_Vault_Safety_Dashboard.png')
shutil.copy('/workspace/veeva_safety_signal_brief_p1.png', '/workspace/Veeva_官方宣传图2_Signal_Analysis_Dashboard.png')

IMG1 = '/workspace/Veeva_官方宣传图1_Vault_Safety_Dashboard.png'
IMG2 = '/workspace/Veeva_官方宣传图2_Signal_Analysis_Dashboard.png'

prs = Presentation(PPT_PATH)

# ---------- 先确认当前结构 ----------
print(f'当前 {len(prs.slides)} slides:')
for i, s in enumerate(prs.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:50]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else '(no text)'
    print(f'  {i+1:2d}. {first}  |  shapes={len(s.shapes)}')

# ---------- 辅助 ----------
SLIDE_W = prs.slide_width
SLIDE_H = prs.slide_height
NAVY = RGBColor(22, 44, 92)
GRAY = RGBColor(95, 99, 104)
WHITE = RGBColor(255, 255, 255)

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

# ---------- 新建两张 slide ----------
slide1 = prs.slides.add_slide(prs.slide_layouts[5])  # 自动追加
slide2 = prs.slides.add_slide(prs.slide_layouts[5])

# ---------- 画 slide1：Veeva 官方宣传图 1 ----------
add_title(slide1, 'Veeva Vault Safety：实时 Adverse Event 管理 Dashboard')

# 图片区域：留出标题条和底部图注，居中放图
img_x = Inches(0.5)
img_top = Inches(1.0)
img_bottom_margin = Inches(0.5)
img_h = SLIDE_H - img_top - img_bottom_margin - Inches(0.15)  # 给图注留空间
img_w = SLIDE_W - img_x * 2

slide1.shapes.add_picture(IMG1, img_x, img_top, img_w, img_h)

# 图注
add_textbox(slide1, Inches(0.5), SLIDE_H - Inches(0.42),
            SLIDE_W - Inches(1), Inches(0.3),
            '来源：Veeva Vault Safety Datasheet 2018 · Vault Safety Dashboard 实时呈现 Case Processing、Submission Tracking 与 Risk Metrics',
            size=8, color=GRAY, align=PP_ALIGN.CENTER)

# ---------- 画 slide2：Veeva 官方宣传图 2 ----------
add_title(slide2, 'Veeva Safety Signal：Detection → Evaluation 全链路分析 Dashboard')

slide2.shapes.add_picture(IMG2, img_x, img_top, img_w, img_h)

add_textbox(slide2, Inches(0.5), SLIDE_H - Inches(0.42),
            SLIDE_W - Inches(1), Inches(0.3),
            '来源：Veeva Safety Signal Features Brief EU 2026 · 右侧 Dashboard 展示 Signal Analysis、Risk Management 与 Detection by Product',
            size=8, color=GRAY, align=PP_ALIGN.CENTER)

prs.save(PPT_PATH)
print(f'\n追加新 slide 后共 {len(prs.slides)} slides')

# ---------- 把致谢移到最后 ----------
prs2 = Presentation(PPT_PATH)
sldIdLst = prs2.slides._sldIdLst
for i, s in enumerate(prs2.slides):
    if len(s.shapes) == 0:
        target = sldIdLst[i]
        sldIdLst.remove(target)
        sldIdLst.append(target)
        print(f'致谢从 slide {i+1} 移到末尾')
        break

# ---------- 更新页码 ----------
TOTAL_NEW = len(prs2.slides)
TOTAL_OLD = TOTAL_NEW - 2  # 新增了2页
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
    first = shapes_info[0] if shapes_info else '(no text)'
    print(f'  {i+1:2d}. {first}')
