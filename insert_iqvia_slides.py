"""在 PPT 最后插入 IQVIA Vigilance Platform 卖点总结三栏卡片页。"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import re

PPT_PATH = '/workspace/PV数据库市场调研总结-20261111.pptx'
prs = Presentation(PPT_PATH)

# ---------- 颜色 ----------
NAVY = RGBColor(22, 44, 92)
ACCENT = RGBColor(206, 80, 52)
LIGHT_BLUE = RGBColor(60, 80, 130)
WHITE = RGBColor(255, 255, 255)
GRAY = RGBColor(95, 99, 104)

SLIDE_W = prs.slide_width
SLIDE_H = prs.slide_height

# ---------- 辅助 ----------
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
    bar = slide.shapes.add_shape(1, Inches(0), Inches(0), SLIDE_W, Inches(0.85))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    add_textbox(slide, Inches(0.5), Inches(0.18), SLIDE_W - Inches(1), Inches(0.55),
                text, size=18, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

def add_page_number(slide, current, total, section_label='附录 · 03'):
    add_textbox(slide, SLIDE_W - Inches(2.8), SLIDE_H - Inches(0.45),
                Inches(2.5), Inches(0.35),
                f'{section_label}  ｜  {current} / {total}',
                size=8.5, color=GRAY, align=PP_ALIGN.RIGHT)

# ---------- 1. 先追加新 slide（会在末尾） ----------
slide1 = prs.slides.add_slide(prs.slide_layouts[5])

# ---------- 2. 再把原最后一页（致谢）移到末尾 ----------
# python-pptx 不支持直接移动，用 XML 操作
from lxml import etree

def move_slide_to_end(prs, slide_index):
    """把 index 的 slide 移到末尾（python-pptx 原生不支持 move，用底层 XML）"""
    # 取 sldIdLst
    sldIdLst = prs.slides._sldIdLst
    # 找到要移动的元素
    target = sldIdLst[slide_index]
    # 先 remove 再 append
    sldIdLst.remove(target)
    sldIdLst.append(target)

# 现在 slides 顺序是 [0..21 原22页, 22 新slide]
# 原最后一页（致谢）现在是索引 21
# 移动它到末尾 → 新 slide 变倒数第二，致谢变最后
move_slide_to_end(prs, 21)

# 现在顺序正确：[原21页] → [新slide IQVIA卖点] → [致谢]

# ---------- 3. 画标题 ----------
add_title(slide1, 'IQVIA Vigilance Platform 核心卖点提炼')

# ---------- 4. 三栏卡片 ----------
col_w = Inches(3.1)
col_gap = Inches(0.18)
total_w = col_w * 3 + col_gap * 2
start_x = (SLIDE_W - total_w) / 2
card_top = Inches(1.1)
card_h = Inches(5.3)

# 和 Veeva 的卡片标题做区分：Veeva 是"成熟·生态型平台"，IQVIA 要突出它的独特卖点
cards = [
    {
        'title': '① 库 + 服务 + AI 三位一体',
        'title_color': WHITE,
        'bg': NAVY,
        'points': [
            ('唯一双持：自有安全数据库 + 3,000+ 全球安全专员（100+ 国家）', True, WHITE),
            ('8 个模块全链条覆盖：Intake → Case → Periodics → Analytics → Detect → Collect → Signal → Administration', False, WHITE),
            ('Detect 用 GenAI：多模态（email / audio / social / documents / chat），减少 80% false positives', False, WHITE),
            ('Collect：多语言 + mobile-enabled，直接向患者和 reporter 采集', False, WHITE),
            ('Signal：实时信号检测（real-time signal detection）', False, WHITE),
        ],
        'foot': '来源：IQVIA Vigilance Platform 产品页',
    },
    {
        'title': '② 硬数据（2022 交付）',
        'title_color': WHITE,
        'bg': ACCENT,
        'points': [
            ('>2M ICSRs processed ｜ 99.83% TAT compliance', True, WHITE),
            ('>1,300 aggregate safety reports across 131 clients', False, WHITE),
            ('30 国家 QPPV 支持 ｜ 389 safety databases hosted', False, WHITE),
            ('>400 customers ｜ >800 safety cases processed with AI annually', False, WHITE),
            ('客户案例：Biovac 从 paper-based 迁移，data entry 时间显著减少', False, WHITE),
            ('客户案例：Sanofi Project ARTEMIS 年处理 70 万+ AE', False, WHITE),
            ('"near touchless processing" —— 自动化目标比 Veeva 更激进', False, WHITE),
        ],
        'foot': '来源：IQVIA End-to-End Safety Solutions 事实表',
    },
    {
        'title': '③ 对 CRO 的启示',
        'title_color': WHITE,
        'bg': LIGHT_BLUE,
        'points': [
            ('IQVIA 护城河 = 全链条 AI + 全球合规能力 + 人力规模', True, WHITE),
            ('14.8% 中国市占来自"可拆可合"：Detect/Collect system-agnostic，可挂客户既有 Argus', False, WHITE),
            ('高价锁库 + 重量级实施 → 中小 MAH 天然买不起用不动', False, WHITE),
            ('我们对标 IQVIA，但做：轻量库 + 本土自动化 + 代运营', False, WHITE),
            ('Veeva 客户说"real-time"，IQVIA 客户说"减少 data entry 时间 / TAT"', False, WHITE),
        ],
        'foot': '来源：对 IQVIA 卖点与 CRO 客群痛点的交叉分析',
    },
]

for i, card in enumerate(cards):
    x = start_x + (col_w + col_gap) * i
    shape = slide1.shapes.add_shape(1, x, card_top, col_w, card_h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = card['bg']
    shape.line.fill.background()
    add_textbox(slide1, x + Inches(0.18), card_top + Inches(0.12),
                col_w - Inches(0.36), Inches(0.45),
                card['title'], size=13, bold=True, color=card['title_color'])
    divider = slide1.shapes.add_shape(1, x + Inches(0.18), card_top + Inches(0.58),
                                       col_w - Inches(0.36), Pt(2))
    divider.fill.solid()
    divider.fill.fore_color.rgb = card['title_color']
    divider.line.fill.background()
    add_multiline(
        slide1, x + Inches(0.18), card_top + Inches(0.72),
        col_w - Inches(0.36), card_h - Inches(1.1),
        [tuple(p) if isinstance(p, tuple) else (p, False, WHITE) for p in card['points']],
        size=9.2, color=WHITE, bullet=False, line_spacing=1.35
    )
    add_textbox(slide1, x + Inches(0.18), card_top + card_h - Inches(0.38),
                col_w - Inches(0.36), Inches(0.3),
                card['foot'], size=7.2, color=WHITE)

# ---------- 5. 保存 ----------
prs.save(PPT_PATH)

# ---------- 6. 更新所有页码 ----------
# 原总页数 22 → 23（新增 IQVIA 一页）
# python-pptx 新建 slide 自动追加到末尾，然后我把致谢移到末尾了
# 所以新 slide 是倒数第二，致谢是最后一页
TOTAL_NEW = len(prs.slides)
TOTAL_OLD = 22

prs2 = Presentation(PPT_PATH)
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

print(f'saved {PPT_PATH}  ({len(prs2.slides)} slides)')

# 验证
prs3 = Presentation(PPT_PATH)
for i, s in enumerate(prs3.slides):
    titles = [sh.text for sh in s.shapes if hasattr(sh, 'has_text_frame') and sh.has_text_frame and sh.text.strip() and len(sh.text.strip()) < 80]
    first = titles[0] if titles else '(no title)'
    print(f'  {i+1:2d}. {first}')
