"""
1) 把 IQVIA 卖点提炼卡片页的配色从 Veeva 橙 → IQVIA 蓝 (teal #0C7BC0)
2) 在 PPT 末尾插入 IQVIA 词云图页面（放在 Veeva 词云之后、致谢之前）
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from lxml import etree
import re

PPT_PATH = '/workspace/PV数据库市场调研总结-20261111.pptx'
WORDCLOUD_PATH = '/workspace/IQVIA_Vigilance_产品卖点词云.png'

prs = Presentation(PPT_PATH)

# ---------- IQVIA 品牌配色 ----------
# IQVIA 官网主色：Teal/Aqua（无橙色，和 Veeva 视觉明显区分）
IQVIA_TEAL = RGBColor(12, 123, 192)    # #0C7BC0 Denim 主色（替代 Veeva 橙色）
IQVIA_DARK = RGBColor(0, 84, 135)      # #005487 深蓝
IQVIA_ACCENT = RGBColor(0, 161, 223)   # #00A1DF Aqua（高亮用，最亮）
IQVIA_GRAY = RGBColor(95, 99, 104)
WHITE = RGBColor(255, 255, 255)

SLIDE_W = prs.slide_width
SLIDE_H = prs.slide_height

# ---------- Step 1: 更新 IQVIA 卡片页配色 ----------
# 找到 "IQVIA Vigilance Platform 核心卖点提炼" 页，替换其中的橙色 Rectangle
for slide in prs.slides:
    all_text = ''
    for sh in slide.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            all_text += sh.text
    if 'IQVIA Vigilance Platform 核心卖点提炼' not in all_text:
        continue
    
    # 在这个 slide 里，找到背景为橙色（RGBColor 206,80,52）的 AUTO_SHAPE
    # 替换成 IQVIA Teal
    for sh in slide.shapes:
        if sh.shape_type == 1:  # AUTO_SHAPE Rectangle
            try:
                fill = sh.fill.fore_color.rgb
                # Veeva 橙色 = 206, 80, 52
                if fill == RGBColor(206, 80, 52):
                    sh.fill.fore_color.rgb = IQVIA_TEAL
                    print(f'  替换橙色 Rectangle → IQVIA Teal: {sh.name}')
            except Exception as e:
                pass

prs.save(PPT_PATH)
print('IQVIA 卡片配色已更新')

# ---------- Step 2: 追加 IQVIA 词云图片 slide ----------
def add_textbox(slide, left, top, width, height, text, size=11, bold=False,
                color=IQVIA_DARK, align=PP_ALIGN.LEFT, font_name='微软雅黑'):
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

def add_title(slide, text, bar_color=IQVIA_DARK):
    """用 IQVIA 深蓝做标题条（区别于 Veeva 用的 Navy）"""
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), SLIDE_W, Inches(0.85))
    bar.fill.solid()
    bar.fill.fore_color.rgb = bar_color
    bar.line.fill.background()
    add_textbox(slide, Inches(0.5), Inches(0.18), SLIDE_W - Inches(1), Inches(0.55),
                text, size=18, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

def add_page_number(slide, current, total, section_label='附录 · 03'):
    add_textbox(slide, SLIDE_W - Inches(2.8), SLIDE_H - Inches(0.45),
                Inches(2.5), Inches(0.35),
                f'{section_label}  ｜  {current} / {total}',
                size=8.5, color=IQVIA_GRAY, align=PP_ALIGN.RIGHT)

new_slide = prs.slides.add_slide(prs.slide_layouts[5])  # 自动追加到末尾

add_title(new_slide, 'IQVIA Vigilance Platform 产品卖点词云', bar_color=IQVIA_DARK)

# 插入图片（居中，同 Veeva 词云页的布局）
img_margin_top = Inches(0.95)
img_margin_bottom = Inches(0.55)
img_margin_side = Inches(0.4)
img_w = SLIDE_W - img_margin_side * 2
img_h = SLIDE_H - img_margin_top - img_margin_bottom

native_ratio = 1600 / 900
slide_ratio = img_w / img_h
if slide_ratio > native_ratio:
    final_h = img_h
    final_w = final_h * native_ratio
else:
    final_w = img_w
    final_h = final_w / native_ratio

img_x = (SLIDE_W - final_w) / 2
img_y = img_margin_top + (img_h - final_h) / 2

new_slide.shapes.add_picture(WORDCLOUD_PATH, img_x, img_y, final_w, final_h)

# 图注（IQVIA 灰色）
add_textbox(
    new_slide, Inches(0.5), SLIDE_H - Inches(0.42),
    SLIDE_W - Inches(1), Inches(0.3),
    '来源：IQVIA Vigilance Platform 产品页 + End-to-End Safety Solutions 事实表 + Biovac/Sanofi 案例卖点词频',
    size=8, color=IQVIA_GRAY, align=PP_ALIGN.CENTER
)

prs.save(PPT_PATH)

# ---------- Step 3: 把致谢空页移到绝对末尾 ----------
prs2 = Presentation(PPT_PATH)
sldIdLst = prs2.slides._sldIdLst
# 致谢是空页（0 shapes）
for i, s in enumerate(prs2.slides):
    if len(s.shapes) == 0:
        target = sldIdLst[i]
        sldIdLst.remove(target)
        sldIdLst.append(target)
        print(f'把致谢（slide {i+1}）移到末尾')
        break

# ---------- Step 4: 更新页码（23 → 24） ----------
TOTAL_OLD = 23
TOTAL_NEW = len(prs2.slides)
print(f'总页数: {TOTAL_OLD} → {TOTAL_NEW}')

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
            t = sh.text.strip()[:45]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else '(no text)'
    print(f'  {i+1:2d}. {first}')
