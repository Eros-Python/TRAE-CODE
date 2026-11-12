"""在现有 PPT 最后（致谢之后）插入 Veeva Safety 卖点总结文字页 + 词云图片页。"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import copy

PPT_PATH = '/workspace/PV数据库市场调研总结-20261111.pptx'
WORDCLOUD_PATH = '/workspace/Veeva_Safety_产品卖点词云.png'

prs = Presentation(PPT_PATH)

# ---------- 颜色 ----------
NAVY = RGBColor(22, 44, 92)
ACCENT = RGBColor(206, 80, 52)
GRAY = RGBColor(95, 99, 104)
CREAM = RGBColor(243, 236, 216)
WHITE = RGBColor(255, 255, 255)
LIGHT_BLUE = RGBColor(220, 230, 245)

# ---------- 通用辅助 ----------
SLIDE_W = prs.slide_width
SLIDE_H = prs.slide_height

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

def add_multiline(slide, left, top, width, height, lines, size=10.5,
                  color=NAVY, bullet=False, line_spacing=1.4, font_name='微软雅黑'):
    """lines: list of (text, bold, color) tuples OR plain strings"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        p.line_spacing = line_spacing
        if isinstance(line, str):
            line = (line, False, color)
        text, bold, col = line
        if bullet and text:
            text = f"• {text}"
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = col
        run.font.name = font_name
    return txBox

def add_title(slide, text):
    """左上角标题栏（参考已有页面的标题样式）"""
    # 标题条背景
    bar = slide.shapes.add_shape(
        1,  # Rectangle
        Inches(0), Inches(0), SLIDE_W, Inches(0.85)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    # 标题文字
    add_textbox(
        slide,
        Inches(0.5), Inches(0.18), SLIDE_W - Inches(1), Inches(0.55),
        text, size=18, bold=True, color=WHITE, align=PP_ALIGN.LEFT
    )

def add_page_number(slide, current, total, section_label='附录 · 03'):
    """右下角页码"""
    add_textbox(
        slide,
        SLIDE_W - Inches(2.8), SLIDE_H - Inches(0.45),
        Inches(2.5), Inches(0.35),
        f'{section_label}  ｜  {current} / {total}',
        size=8.5, color=GRAY, align=PP_ALIGN.RIGHT
    )

# ---------- Step 1: 计算新总页数 ----------
old_total = len(prs.slides)
# 需要把新页插到最后一页（致谢，old_total - 1）之后
# python-pptx 不支持直接 append 到末尾，需要用 layout 新建然后移动
# 简单方法：直接新建 slide（自动追加到末尾）
new_slide_1_idx = old_total  # 0-based 索引（新 slide 会自动追加）
new_slide_2_idx = old_total + 1

# ---------- Step 2: 新建 slide 21 —— Veeva Safety 卖点提炼 ----------
# 先新建一个临时 slide（会被放在末尾），之后再调整顺序
slide1 = prs.slides.add_slide(prs.slide_layouts[5])  # 正文1

add_title(slide1, 'Veeva Safety Suite 核心卖点提炼')

# 三栏卡片
col_w = Inches(3.1)
col_gap = Inches(0.18)
total_w = col_w * 3 + col_gap * 2
start_x = (SLIDE_W - total_w) / 2
card_top = Inches(1.1)
card_h = Inches(5.3)

# 卡片数据
cards = [
    {
        'title': '① 成熟 · 生态型平台',
        'title_color': WHITE,
        'bg': NAVY,
        'points': [
            ('统一数据模型', True, WHITE),
            ('5 个 Suite 应用同库共存（Safety / SafetyDocs / Safety Signal / Safety Workbench / Safety Gateway）', False, WHITE),
            ('Vault Safety 是核心 ICSR system of record', False, WHITE),
            ('SafetyDocs 承接 PSMF / PVA / RMP 全内容管理', False, WHITE),
            ('Safety Workbench 做分析，Safety Signal 做信号检测', False, WHITE),
        ],
        'foot': '来源：Veeva Pantheon 产品卡 + 官网',
    },
    {
        'title': '② 客户说的高频词',
        'title_color': WHITE,
        'bg': ACCENT,
        'points': [
            ('real-time 实时可见', True, WHITE),
            ('"I can see my data in real-time" —— 3 位 CRO / 药企 PV 负责人原话', False, WHITE),
            ('single unified platform / one system / work as one team', False, WHITE),
            ('intuitive & easy-to-use', False, WHITE),
            ('save time / streamline ops / reduce back-and-forth', False, WHITE),
            ('direct data access（不用等别人拉数据）', False, WHITE),
        ],
        'foot': '来源：Veeva CRO 访谈合集 + UCB / CRISPR / Linical testimonial',
    },
    {
        'title': '③ 我们该怎么卖',
        'title_color': WHITE,
        'bg': RGBColor(60, 80, 130),
        'points': [
            ('不要喊"自动化"，要喊"你再也不用等数据"', True, WHITE),
            ('Veeva 客户说的是结果（real-time / save time），不是自动化', False, WHITE),
            ('数据模型 + 多系统集成才是黏性来源，不是功能清单', False, WHITE),
            ('百万美元级客单价 + 重量级实施 → 中小 MAH 天然留空', False, WHITE),
            ('对标 IQVIA 14.8% 市占，我们可以做"轻量库 + 自动化 + 代运营"', False, WHITE),
        ],
        'foot': '来源：对 CRO 客户 testimonial 的卖点归并',
    },
]

for i, card in enumerate(cards):
    x = start_x + (col_w + col_gap) * i
    # 卡片背景
    shape = slide1.shapes.add_shape(1, x, card_top, col_w, card_h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = card['bg']
    shape.line.fill.background()
    # 标题
    add_textbox(
        slide1, x + Inches(0.18), card_top + Inches(0.12),
        col_w - Inches(0.36), Inches(0.45),
        card['title'], size=13, bold=True, color=card['title_color']
    )
    # 分隔线
    divider = slide1.shapes.add_shape(1, x + Inches(0.18), card_top + Inches(0.58),
                                       col_w - Inches(0.36), Pt(2))
    divider.fill.solid()
    divider.fill.fore_color.rgb = card['title_color']
    divider.line.fill.background()
    # 要点
    add_multiline(
        slide1, x + Inches(0.18), card_top + Inches(0.75),
        col_w - Inches(0.36), card_h - Inches(1.15),
        [tuple(p) if isinstance(p, tuple) else (p, False, WHITE) for p in card['points']],
        size=9.5, color=WHITE, bullet=False, line_spacing=1.35
    )
    # 页脚小字
    add_textbox(
        slide1, x + Inches(0.18), card_top + card_h - Inches(0.38),
        col_w - Inches(0.36), Inches(0.3),
        card['foot'], size=7.5, color=WHITE
    )

add_page_number(slide1, 21, 22)

# ---------- Step 3: 新建 slide 22 —— 词云图片 ----------
slide2 = prs.slides.add_slide(prs.slide_layouts[5])

add_title(slide2, 'Veeva Safety 产品卖点词云')

# 插入词云图片（居中，留出标题和页脚空间）
img_margin_top = Inches(0.95)
img_margin_bottom = Inches(0.55)
img_margin_side = Inches(0.4)
img_w = SLIDE_W - img_margin_side * 2
img_h = SLIDE_H - img_margin_top - img_margin_bottom

# 保持 1600x900 比例，按宽或高限制
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

slide2.shapes.add_picture(WORDCLOUD_PATH, img_x, img_y, final_w, final_h)

# 图注
add_textbox(
    slide2, Inches(0.5), SLIDE_H - Inches(0.42),
    SLIDE_W - Inches(1), Inches(0.3),
    '来源：Veeva Safety Suite 产品页 + CRO testimonial（UCB / CRISPR / Linical / Biomapas 等）卖点词频提取',
    size=8, color=GRAY, align=PP_ALIGN.CENTER
)

add_page_number(slide2, 22, 22)

# ---------- Step 4: 把新 slide 移动到正确位置（致谢之后） ----------
# python-pptx 新建 slide 自动追加到末尾，所以现在顺序是：
#   [0..19] 原20页 → [20] 新slide1 → [21] 新slide2
# 原第20页（致谢）现在是索引 19，新页已经在它后面了 ✓
# 不需要额外移动

# ---------- Step 5: 更新所有原有页面的页码（19 页 → 22 页） ----------
# 遍历所有 shape，找到包含 "XX / 20" 或 "XX/20" 模式的文本框，替换总页数
import re
TOTAL_OLD = 20
TOTAL_NEW = 22

for slide in prs.slides:
    for shape in slide.shapes:
        if not hasattr(shape, 'has_text_frame') or not shape.has_text_frame:
            continue
        tf = shape.text_frame
        for para in tf.paragraphs:
            for run in para.runs:
                # 匹配 "数字 / 20" 或 "数字/20" 或 "20 / 20" 等
                new_text = re.sub(rf'(\d+)\s*/\s*{TOTAL_OLD}\b',
                                  rf'\1 / {TOTAL_NEW}',
                                  run.text)
                if new_text != run.text:
                    run.text = new_text

# ---------- Step 6: 保存 ----------
prs.save(PPT_PATH)
print(f'saved {PPT_PATH}  ({len(prs.slides)} slides)')

# 验证
prs2 = Presentation(PPT_PATH)
print('slide list:')
for i, s in enumerate(prs2.slides):
    titles = [sh.text for sh in s.shapes if hasattr(sh, 'has_text_frame') and sh.has_text_frame and sh.text.strip() and len(sh.text.strip()) < 60]
    first = titles[0] if titles else '(no title)'
    print(f'  {i+1:2d}. {first}')
