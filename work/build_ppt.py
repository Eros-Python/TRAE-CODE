# -*- coding: utf-8 -*-
"""基于康龙临床模板生成 PV 数据库市场调研总结 PPT（老板风格：eyebrow+标题+KPI卡片+结论条）"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

TPL = '/workspace/.uploads/69d8006b-ee89-4a24-827e-fdbb755c096d_03 康龙临床PPT模板(通用模板)-20220426【命名格式：题目-日期yyyyMMdd】.pptx'
OUT = '/workspace/PV数据库市场调研总结-20261111.pptx'
A = '/workspace/work/assets'

NAVY   = RGBColor(0x16,0x28,0x3C)
PNAVY  = RGBColor(0x28,0x25,0x62)
BODY   = RGBColor(0x3A,0x41,0x49)
ACCENT = RGBColor(0xC0,0x65,0x2B)
GRAY   = RGBColor(0x8E,0x99,0xA6)
GRAY2  = RGBColor(0x7A,0x72,0x64)
LINEC  = RGBColor(0xC9,0xCF,0xD6)
CREAM  = RGBColor(0xF7,0xF3,0xE8)
CREAM2 = RGBColor(0xED,0xE7,0xD9)
WHITE  = RGBColor(0xFF,0xFF,0xFF)
BLUE   = RGBColor(0x3D,0x64,0x91)
FONT = '微软雅黑'

def set_font(run, size, bold=False, color=BODY):
    f = run.font
    f.size = Pt(size); f.bold = bold; f.name = FONT
    f.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    for tag in ('a:ea','a:cs'):
        e = rPr.find(qn(tag))
        if e is None:
            e = rPr.makeelement(qn(tag), {}); rPr.append(e)
        e.set('typeface', FONT)

def tb(slide, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
       space_after=2, line_spacing=1.06):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(space_after); p.line_spacing = line_spacing
        for (t, sz, bd, col) in para:
            r = p.add_run(); r.text = t; set_font(r, sz, bd, col)
    return box

def rect(slide, x, y, w, h, fill, line_color=None, line_w=0.75):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line_color is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line_color; sh.line.width = Pt(line_w)
    sh.shadow.inherit = False
    return sh

def eyebrow(slide, left_text, page):
    tb(slide, 7.0, 0.30, 5.9, 0.3, [[(left_text + '  ｜  ' + page, 10, True, GRAY)]], align=PP_ALIGN.RIGHT)

def set_title(slide, text):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 10:
            tf = ph.text_frame; tf.clear()
            p = tf.paragraphs[0]
            r = p.add_run(); r.text = text
            set_font(r, 20, True, PNAVY)
            return

def divider(slide, y=1.90, x=0.42, w=12.49):
    rect(slide, x, y, w, 0.012, LINEC)

def kpi(slide, x, y, w, h, big, small, big_size=20):
    rect(slide, x, y, w, h, CREAM)
    tb(slide, x+0.14, y+0.09, w-0.28, 0.45, [[(big, big_size, True, ACCENT)]], line_spacing=1.0)
    tb(slide, x+0.14, y+0.52, w-0.28, h-0.58, [[(small, 8.5, False, GRAY2)]], line_spacing=1.04)

def callout(slide, text, prefix='结论：', y=6.32):
    rect(slide, 0.42, y, 12.49, 0.36, CREAM)
    rect(slide, 0.42, y, 0.055, 0.36, ACCENT)
    tb(slide, 0.62, y, 12.2, 0.36, [[(prefix, 10, True, ACCENT), (text, 10, False, BODY)]],
       anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0)

def set_cell_borders(cell, color='D9D2C2', w=9525):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ('a:lnB','a:lnT','a:lnR','a:lnL'):
        for e in tcPr.findall(qn(tag)):
            tcPr.remove(e)
    els = []
    for tag in ('a:lnL','a:lnR','a:lnT','a:lnB'):
        ln = tcPr.makeelement(qn(tag), {'w': str(w), 'cap': 'flat'})
        sf = ln.makeelement(qn('a:solidFill'), {})
        c = sf.makeelement(qn('a:srgbClr'), {'val': color})
        sf.append(c); ln.append(sf); els.append(ln)
    for i, el in enumerate(els):
        tcPr.insert(i, el)

def style_cell(cell, runs, fill=None, align=PP_ALIGN.LEFT):
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = Inches(0.06); cell.margin_right = Inches(0.05)
    cell.margin_top = Inches(0.03); cell.margin_bottom = Inches(0.03)
    tf = cell.text_frame; tf.word_wrap = True
    tf.clear()
    p = tf.paragraphs[0]; p.alignment = align; p.line_spacing = 1.0
    for (t, sz, bd, col) in runs:
        r = p.add_run(); r.text = t; set_font(r, sz, bd, col)
    if fill is not None:
        cell.fill.solid(); cell.fill.fore_color.rgb = fill
    else:
        cell.fill.solid(); cell.fill.fore_color.rgb = WHITE
    set_cell_borders(cell)

def make_table(slide, x, y, w, col_widths, rows_data, header_fill=NAVY,
               row_h=0.34, header_h=0.34, body_size=8.5, zebra=True, first_col_bold=True):
    n_r, n_c = len(rows_data), len(rows_data[0])
    gfx = slide.shapes.add_table(n_r, n_c, Inches(x), Inches(y), Inches(w), Inches(row_h*n_r))
    table = gfx.table
    # kill default banding style influence by explicit fills
    for j, cw in enumerate(col_widths):
        table.columns[j].width = Inches(cw)
    table.rows[0].height = Inches(header_h)
    for i in range(1, n_r):
        table.rows[i].height = Inches(row_h)
    for i, row in enumerate(rows_data):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            if i == 0:
                style_cell(cell, [(val, 9.5, True, WHITE)], fill=header_fill,
                           align=PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT)
            else:
                fill = CREAM if (zebra and i % 2 == 0) else WHITE
                bold = first_col_bold and j == 0
                col = NAVY if bold else BODY
                style_cell(cell, [(val, body_size, bold, col if not bold else NAVY)], fill=fill,
                           align=PP_ALIGN.LEFT)
    return gfx

def bullets(slide, x, y, w, h, items, size=10, gap=4, lead_color=ACCENT):
    paras = []
    for it in items:
        if isinstance(it, tuple):
            lead, rest = it
            paras.append([('· ' + lead, size, True, NAVY), (rest, size, False, BODY)])
        else:
            paras.append([('· ' + it, size, False, BODY)])
    tb(slide, x, y, w, h, paras, space_after=gap, line_spacing=1.12)

def section_header(slide, x, y, w, text):
    tb(slide, x, y, w, 0.28, [[(text, 12, True, NAVY)]])
    rect(slide, x, y+0.30, w, 0.014, LINEC)

# ============ build ============
prs = Presentation(TPL)
layouts = {l.name: l for l in prs.slide_masters[0].slide_layouts}

# delete all existing slides (drop relationships so orphan parts are not saved)
xml_slides = prs.slides._sldIdLst
for sldId in list(xml_slides):
    rId = sldId.get(qn('r:id'))
    prs.part.drop_rel(rId)
    xml_slides.remove(sldId)

TOTAL = 17

def content_slide(eyebrow_text, title_text, page):
    s = prs.slides.add_slide(layouts['正文1'])
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx == 11:
            ph._element.getparent().remove(ph._element)
    set_title(s, title_text)
    eyebrow(s, eyebrow_text, f'{page:02d} / {TOTAL}')
    divider(s)
    return s

# ---------- 1 cover ----------
s = prs.slides.add_slide(layouts['康龙临床封面'])
for ph in s.placeholders:
    if ph.placeholder_format.idx == 10:
        ph.text_frame.text = 'PHARMARON CLINICAL'
    elif ph.placeholder_format.idx == 11:
        ph.text_frame.text = 'PV 数据库市场调研总结'
tb(s, 3.34, 4.88, 9.9, 0.4, [[('——市场规模 × 竞品格局 × 自建决策建议', 15, False, BODY)]])
tb(s, 3.34, 5.38, 9.9, 0.35, [[('2026 年 11 月 ｜ 依据《PV 数据库市场调研》与公开资料整理；推断数据均已标注', 11, False, GRAY)]])

# ---------- 2 TOC ----------
s = prs.slides.add_slide(layouts['目录'])
toc_items = [
    ('01', '市场规模与数据', '全球与中国规模 · 中国 MAH 刚需客群测算 · 自动化市场与集中度'),
    ('02', '竞品格局', '四家横向对照 · Veeva / IQVIA 单页结论 · 软件梯队 · 实施差异与双维定位'),
    ('03', '结论与建议', '市场聚拢的底层逻辑 · 临床 CRO 是否自建 PV 数据库'),
]
for ph in list(s.placeholders):
    idx = ph.placeholder_format.idx
    if idx in (16, 17):
        ph._element.getparent().remove(ph._element)
for i, (num, t, desc) in enumerate(toc_items):
    y = 1.55 + i * 1.09
    for ph in s.placeholders:
        idx = ph.placeholder_format.idx
        if idx == 10 + i*2:
            ph.text_frame.text = num
        elif idx == 11 + i*2:
            ph.text_frame.text = t
    tb(s, 7.95, y+0.60, 4.9, 0.3, [[(desc, 8.5, False, GRAY)]])

# ---------- 3 PART 01 ----------
s = prs.slides.add_slide(layouts['标题页'])
for ph in s.placeholders:
    if ph.placeholder_format.idx == 12:
        ph.text_frame.text = '01'
    elif ph.placeholder_format.idx == 10:
        ph.text_frame.text = '市场规模与数据'

# ---------- 4 全球与中国市场规模 ----------
s = content_slide('市场规模 · 01', '全球与中国：百亿人民币赛道，自动化是增长最快的子赛道', 4)
kw, kg, ky, kh = 2.98, 0.19, 2.02, 1.04
kpi(s, 0.42, ky, kw, kh, '$75.8 亿', '全球 PV 系统/软件市场 2025（Dataintelo），CAGR 10.2%（2025–2034）')
kpi(s, 0.42+(kw+kg), ky, kw, kh, '¥48.6 亿', '中国 PV+药物安全软件市场 2025（博研咨询，口径含解决方案）')
kpi(s, 0.42+(kw+kg)*2, ky, kw, kh, '13.42%', 'PV 自动化市场 CAGR：$26.7 亿(2025)→$56.8 亿(2031)（Mordor）')
kpi(s, 0.42+(kw+kg)*3, ky, kw, kh, '58.3%', '软件占整体 PV 市场比例；药企端收入占 42.1%（Dataintelo）')
section_header(s, 0.42, 3.28, 7.2, '要点')
bullets(s, 0.42, 3.72, 7.2, 2.4, [
    ('纯软件 TAM：', '不含服务的 PV 软件子赛道 $20.9 亿(2025)→$50.6 亿(2035E)，CAGR 9.2%（Precedence）——最接近"数据库产品"的可寻址市场'),
    ('区域结构：', '亚太增速最快（CAGR 12.74%），北美占 38.2%；中国市场增速高于全球'),
    ('口径提示：', '中国 ¥48.6 亿含服务/解决方案成分；海外纯软件口径中国约 ¥3 亿（GIA 2026）——真实区间在两者之间'),
    ('增量来源：', '新建 MAH 首次建库 + 存量系统替换 + AI 功能升级三类需求叠加'),
], size=9.5, gap=5)
s.shapes.add_picture(f'{A}/img_automation.png', Inches(7.95), Inches(3.30), width=Inches(2.30))
tb(s, 7.95, 5.94, 2.4, 0.3, [[('PV 自动化市场规模（Mordor，CC BY 4.0）', 7.5, False, GRAY)]], line_spacing=1.0)
s.shapes.add_picture(f'{A}/img_region.png', Inches(10.45), Inches(3.55), width=Inches(2.45))
tb(s, 10.45, 4.72, 2.5, 0.3, [[('全球 PV 系统市场区域分布 2025（Dataintelo）', 7.5, False, GRAY)]], line_spacing=1.0)
callout(s, 'PV 软件是产业链中增长最快的环节，自动化子赛道（13.4%）跑赢整体（10.2%）——增量主战场在"软件 + AI 自动化"。')

# ---------- 5 中国 MAH ----------
s = content_slide('市场规模 · 02', '中国 MAH 全景：约 3,000+ 家刚需客群，每年 8–10% 扩容', 5)
rows = [
    ['客群', '数量（家）', '口径与来源（推断均已标注）'],
    ['MAH 持有人总数（A+B+纯B）', '5,832', '确定：博研咨询引药智网/NMPA，2025 年底；NMPA 生产型企业 5,581 家交叉验证'],
    ['　其中：有上市后产品（持有效注册证）', '1,843', '确定：博研咨询 2025；其中创新药上市企业约 150–250 家（推断）'],
    ['　其中：纯 B 证轻资产 MAH', '1,252 → 约1,500', '确定：药智网 2025-03；2026 值为推断（近年 +16%/年）'],
    ['临床阶段 Biotech（有在研管线）', '1,000–1,500', '推断：在研创新药 4,751 个（医药魔方 2025）÷ 每家 3–4 个管线'],
    ['2026 年刚需客群合计', '约 3,000–3,500', '推断：上市后 MAH 1,843 + 临床阶段 Biotech（去重）'],
    ['2030 年预测', '约 4,500–5,000', '推断：临床阶段 CAGR 8.5%，叠加每年 70+ 个创新药获批转化'],
]
make_table(s, 0.42, 2.02, 8.35, [2.75, 1.35, 4.25], rows, row_h=0.56, header_h=0.34, body_size=9)
rx = 8.98
section_header(s, rx, 2.02, 3.93, '需求侧佐证')
cards = [
    ('2,997 项', '2025 年新药临床试验登记，同比 +18.0%（CDE 年报）'),
    ('76 个', '2025 年 NMPA 批准上市 1 类创新药（NMPA 年度统计）'),
    ('4,751 个', '中国在研创新药数量，占全球 33.7%（医药魔方 2025）'),
    ('85% → 质量缺口', '已建 PV 系统的 MAH 占比；符合 GVP 数据质量要求的未必足数'),
]
cy = 2.46
for big, small in [('2,997 项','2025 年新药临床试验登记，同比 +18.0%（CDE 年报）'),
                   ('76 个','2025 年 NMPA 批准上市 1 类创新药（NMPA 年度统计）'),
                   ('4,751 个','中国在研创新药数量，占全球 33.7%（医药魔方 2025）'),
                   ('10–15%','纯 B 证 MAH 年增速（推断，已从 +121% 回落至 +16%）')]:
    rect(s, rx, cy, 3.93, 0.94, CREAM)
    tb(s, rx+0.13, cy+0.07, 3.7, 0.3, [[(big, 13, True, ACCENT)]], line_spacing=1.0)
    tb(s, rx+0.13, cy+0.38, 3.7, 0.52, [[(small, 8, False, GRAY2)]], line_spacing=1.03)
    cy += 1.04
callout(s, '只有"临床阶段 Biotech + 有上市后产品的 MAH"对 PV 数据库有刚性需求——合计约 3,000+ 家且持续扩容，构成目标客户基本盘。')

# ---------- 6 自动化市场与集中度 ----------
s = content_slide('市场规模 · 03', '自动化市场：中等集中度，头部锁定与结构性空档并存', 6)
kpi(s, 0.42, ky, kw, kh, '$26.7→56.8 亿', 'PV 自动化市场规模 2025→2031（Mordor）', big_size=15)
kpi(s, 0.42+(kw+kg), ky, kw, kh, '65.82%', '自动化市场中软件占比（2025，Mordor）')
kpi(s, 0.42+(kw+kg)*2, ky, kw, kh, '58.4%', '中国 PV 市场 CR5，中度集中（博研咨询）')
kpi(s, 0.42+(kw+kg)*3, ky, kw, kh, '14.8%', 'IQVIA 中国市占第一（博研咨询）')
s.shapes.add_picture(f'{A}/img_concentration.png', Inches(0.42), Inches(3.22), width=Inches(7.45))
tb(s, 0.42, 5.28, 7.4, 0.25, [[('市场集中度示意：处于"集中"与"分散"之间（Mordor，CC BY 4.0）', 7.5, False, GRAY)]], line_spacing=1.0)
bullets(s, 0.42, 5.58, 7.45, 0.75, [
    ('头部锁定：', 'Oracle / ArisGlobal / Veeva / IQVIA 以嵌入式工作流 + 多年期验证锁定 Top 20 药企；2025-08 IQVIA×Veeva 和解并打通数据'),
    ('增长驱动：', '监管压力 +2.8 · AE 数据量 +3.1 · AI 普及 +2.5 · 药企降本 +1.9（对 CAGR 贡献，Mordor）'),
], size=8.5, gap=3)
s.shapes.add_picture(f'{A}/img_cluster.png', Inches(8.35), Inches(3.10), width=Inches(2.42))
tb(s, 8.20, 5.40, 4.6, 0.5, [[('PV 数字化研究关键词聚类：机器学习 / 深度学习 / 信息提取为研究主线（《中国现代应用药学》2022）', 7.5, False, GRAY)]], line_spacing=1.05)
callout(s, '"中等集中"＝头部锁定大客户、长尾仍开放：面向中小 MAH 的轻量化、国产合规产品仍有结构性窗口。')

# ---------- 7 PART 02 ----------
s = prs.slides.add_slide(layouts['标题页'])
for ph in s.placeholders:
    if ph.placeholder_format.idx == 12:
        ph.text_frame.text = '02'
    elif ph.placeholder_format.idx == 10:
        ph.text_frame.text = '竞品格局'

# ---------- 8 四家对照 ----------
s = content_slide('竞品格局 · 01', '四家 PV 系统横向对照：平台派 vs 国产派', 8)
rows = [
    ['维度', 'Veeva Safety Suite', 'IQVIA Vigilance Platform', '太美 eSafety', '百奥知 Bioknow PV'],
    ['定位', 'Vault 云平台上的一体化 PV 应用组合', '自有安全数据库 + 模块化 SaaS（数据归客户）', '国产 GVP 一体化 PV 数据库 + iPV 智能体', '国产"PV 数据中心"：eSAE+eADR+PV+Gateway'],
    ['组成', '5 应用：Safety / SafetyDocs / Workbench / Signal / AI', '8 模块：Intake / Case / Periodics / Analytics / Detect 等', 'eSafety + iPV Agent + 全球递交 Gateway', 'Bioknow PV + eSAE + eADR + 一体化门户 + Gateway'],
    ['AI 能力', 'AI for Safety 2025 上线，早期（1–10 客户）', 'AI at core，目标近"touchless"病例处理', 'iPV：自述重复任务自动化 80%、合规率 99.9%', '2026 起密集发布信号检测 / 文献 AI / Narrative 秒级生成'],
    ['客户证据', '8 家 Top 20 药企；18 家具名客户', '30+ 平台客户、20 家 Top 50；Sanofi / Biovac', '自述 500 家申办方/CRO；具名 1 家（豪森）', '自述 300+/400+ 家；无具名客户'],
    ['商业条款', '未公开价格', '$49K 实施 + $65K/年（3 年、1,500 例/年、10 用户）', '未公开价格', '未公开价格'],
    ['中国本地化', '全球统一平台，中国区能力未单列', '全球平台+本地服务；中国市占 14.8%', '直连 NMPA 直报；中英日双语；WHO-UMC 认证', 'NMPA/FDA/EMA/MHRA 上报；等保三级'],
]
make_table(s, 0.42, 2.02, 12.49, [1.05, 2.86, 2.86, 2.86, 2.86], rows, row_h=0.60, header_h=0.32, body_size=8)
callout(s, '各家客户数口径不同（去重具名 vs 厂商自述），不可直接横比；"未披露 ≠ 没有"。', prefix='注：')

# ---------- 9 Veeva ----------
s = content_slide('竞品格局 · 02', 'Veeva Safety Suite：平台生态型，强在统一数据模型', 9)
kpi(s, 0.42, ky, kw, kh, '8 家', '全球 Top 20 药企选择 Veeva Safety（官网口径）')
kpi(s, 0.42+(kw+kg), ky, kw, kh, '18 家', '官网具名客户：Merck、诺和诺德、CRISPR 等')
kpi(s, 0.42+(kw+kg)*2, ky, kw, kh, '5 个', 'Suite 应用数，全部基于同一 Vault 数据模型')
kpi(s, 0.42+(kw+kg)*3, ky, kw, kh, '2025', 'AI for Safety 发布，AI 嵌入合规工作流')
section_header(s, 0.42, 3.28, 7.2, '结论')
bullets(s, 0.42, 3.72, 7.2, 2.4, [
    ('成熟双核：', 'Safety（51–100 客户）+ SafetyDocs（11–50）同库共存，覆盖 ICSR 处理与 PSMF/PVA/RMP 全内容管理'),
    ('平台锁定：', '与临床、EDC、RIM、质量系统打通——卖的是数据模型与生态，而非单点功能'),
    ('增长曲线：', 'Workbench / Signal / AI for Safety 均为 1–10 客户早期产品，正向存量客户交叉销售'),
    ('客群覆盖：', '大药企 + Biotech + CRO（Linical、Biomapas 等 4 家 CRO 具名）——CRO 是其明确目标客群'),
], size=9.5, gap=5)
rect(s, 7.95, 3.28, 4.96, 2.85, CREAM2)
tb(s, 8.15, 3.42, 4.6, 0.3, [[('对 CRO 的启示', 12, True, NAVY)]])
bullets(s, 8.15, 3.78, 4.6, 2.2, [
    '黏性来自数据模型与多系统集成，不在功能清单长短',
    '百万美元级客单价 + 重量级实施 → 中小 MAH 市场天然留空',
    '其 CRO 客群策略证明"CRO 用 PV 平台服务客户"模式成立',
], size=9, gap=4)
callout(s, 'Veeva = 平台生态型：强在数据模型与生态集成；价格与实施重量是其在中国中小客群的最大短板。')

# ---------- 10 IQVIA ----------
s = content_slide('竞品格局 · 03', 'IQVIA Vigilance Platform：AI 优先 + 标准化套餐下沉', 10)
kpi(s, 0.42, ky, kw, kh, '$49K+$65K/年', '唯一公开入门价：3 年约 $24.4 万、1,500 例/年、10 用户', big_size=15)
kpi(s, 0.42+(kw+kg), ky, kw, kh, '30+ / 20 家', '平台客户 / 全球 Top 50 药企客户（Fact Sheet）')
kpi(s, 0.42+(kw+kg)*2, ky, kw, kh, '1,200 万', '生产环境托管病例（最大 60 万+/年，最小 5 例/月）')
kpi(s, 0.42+(kw+kg)*3, ky, kw, kh, '-15%', 'Sanofi PV 成本已降，2027 目标 -50%（联合口径）')
section_header(s, 0.42, 3.28, 7.2, '结论')
bullets(s, 0.42, 3.72, 7.2, 2.4, [
    ('商业化最清晰：', '企业级 8 模块 + 面向新兴 Biotech 的预配置套餐（12–15 周上线），把 PV 系统从"百万美元项目"变成标准化产品'),
    ('行业标杆：', 'Sanofi ARTEMIS 年处理 70 万+ AE，AI 从 Intake 渗透至医疗评估核心环节，2025 年底完成全系统替换'),
    ('平台+服务捆绑：', '3,000+ 安全专员、100+ 国家本地合规，外包服务与软件互相导流'),
    ('竞合信号：', '2025-08 与 Veeva 和解并打通数据流转——头部玩家从竞争走向竞合'),
], size=9.5, gap=5)
rect(s, 7.95, 3.28, 4.96, 2.85, CREAM2)
tb(s, 8.15, 3.42, 4.6, 0.3, [[('对 CRO 的启示', 12, True, NAVY)]])
bullets(s, 8.15, 3.78, 4.6, 2.2, [
    '"平台 + 代运营"正是 CRO 自建 PV 的可行模式参照',
    '公开入门价验证了中小客群付费意愿，可作定价锚点',
    '中国市占 14.8% 居第一，是国产化替代的直接对标对象',
], size=9, gap=4)
callout(s, 'IQVIA = AI+服务双轮型：唯一公开定价的头部玩家，验证了 PV 系统产品化、下沉化的商业路径。')

# ---------- 11 PART 03 ----------
s = prs.slides.add_slide(layouts['标题页'])
for ph in s.placeholders:
    if ph.placeholder_format.idx == 12:
        ph.text_frame.text = '03'
    elif ph.placeholder_format.idx == 10:
        ph.text_frame.text = '结论与建议'

# ---------- 12 梯队全景 ----------
s = content_slide('结论与建议 · 01', 'PV 数据库软件全景：五个梯队，两种生存逻辑', 12)
rows = [
    ['梯队', '代表厂商', '生存逻辑 / 定位', '关键证据（口径：厂商自述均已标注）'],
    ['全球平台一线', 'Veeva · IQVIA · Oracle Argus · ArisGlobal', '完整工作流+数据库+申报一体化，多年期验证锁定 Top 20 药企', 'Veeva 8 家 Top20；IQVIA 20 家 Top50；ArisGlobal 220+ 客户，达索 18 亿美元收购（2026-07 签约）'],
    ['全球利基', 'RxLogix · Ennov · EXTEDO · AB Cube', '模块化 API 挂接遗留系统，区域/单点突破', 'RxLogix 105+ 客户、年千万级病例（自述）；Ennov 650+ 组织'],
    ['AI 原生新势力', 'Graph Safety 等', '知识图谱 + 可解释 AI，云原生按模块交付', '融资 $16.3M；自述 3 小时→10 分钟（未经审计）'],
    ['服务托管型', 'Genpact · Accenture · TCS', '自有 PV 平台 + 代运营捆绑，以人力规模压成本', 'Bayer（2018）｜UCB（2019）｜AstraZeneca（7 区域中心 / 130+ 国家）'],
    ['中国第一梯队', '太美 eSafety · 百奥知 · 洞悉 Holox · Clinflash', 'GVP 合规 + 国产替代 + 中文场景深耕', '太美自述 500 家客户（港股上市）；百奥知自述 300+ 家'],
    ['中国轻量化', 'PVwatch（南京天韬）· iDrugSafety（梅斯）', '轻量 SaaS、用户体验与性价比取胜', '面向国内中小 MAH，区域化服务'],
]
make_table(s, 0.42, 2.02, 12.49, [1.45, 2.90, 3.85, 4.29], rows, row_h=0.62, header_h=0.32, body_size=8.5)
callout(s, '全球拼"平台锁定"，中国拼"国产替代 + 轻量化"；AI 原生厂商是共同变量——梯队边界正在重排。')

# ---------- 13 服务托管型：无自有数据库 ----------
s = content_slide('竞品格局 · 04', '服务托管型三家：卖"自动化层 + 代运营"，数据库仍是客户的', 13)
cards = [
    ('Genpact', '"PVAI applied to Bayer\'s existing\npharmacovigilance database and IT systems"',
     '无自有安全数据库｜PVAI 为病例处理层，收购的 CVW 仅做信号检测分析'),
    ('Accenture', '"pre-processing ... output for import into\nenterprise safety systems"',
     '无自有安全数据库｜INTIENT PV 是数据库"上游"的提取与预处理层'),
    ('TCS', '"modular deployment with an\ninterface to safety database"',
     '无自有安全数据库｜ADD Safety 明确以接口对接客户既有数据库'),
]
cw = 4.02; cgap = 0.215
for i, (name, quote, verdict) in enumerate(cards):
    x = 0.42 + i * (cw + cgap)
    rect(s, x, 1.98, cw, 1.32, CREAM)
    rect(s, x, 1.98, 0.055, 1.32, ACCENT)
    tb(s, x+0.16, 2.04, cw-0.3, 0.26, [[(name, 11, True, NAVY)]])
    qp = [[(ln, 8, False, GRAY2)] for ln in quote.split('\n')]
    tb(s, x+0.16, 2.32, cw-0.3, 0.53, qp, space_after=0, line_spacing=1.05)
    tb(s, x+0.16, 2.86, cw-0.3, 0.40, [[(verdict, 8, False, BODY)]], line_spacing=1.08)
rows = [
    ['维度', '平台厂商（Veeva / IQVIA / Argus）', '服务托管型（Genpact / Accenture / TCS）'],
    ['卖什么', '系统本身（system of record）：建库、存案、E2B 递交、定期报告', '人力 + 自动化能力：替客户处理病例，不卖数据库'],
    ['数据归属', '数据落在厂商自有数据模型内，迁移需转换', '数据留在客户已有库（Argus / Veeva / 自研），服务商只处理'],
    ['计价方式', '许可 / 订阅 + 实施费，按模块与用户数', '按病例量、FTE 或成果计费，随业务量弹性伸缩'],
    ['上线周期', '6–18 个月（配置、验证、数据迁移、接口联调）', '数周–数月：先接管流程，工具并行接入'],
    ['合规责任', '厂商交付验证包，客户自行完成 IQ/OQ 与放行', '服务商承担 SOP、质量体系与检查应对（TCS 经 FDA/MHRA 检查）'],
    ['切换成本', '高：数据 + 流程双锁定，换系统≈重建', '低：数据库不动，可随时增减或退出'],
]
make_table(s, 0.42, 3.42, 12.49, [1.30, 5.60, 5.59], rows, row_h=0.40, header_h=0.30, body_size=8.5)
callout(s, '三家只做库之上的自动化与服务，本身不拥有数据库；既有库又有服务的是 IQVIA、泰格、太美（太美智研）。')

# ---------- 14 双维定位矩阵 ----------
s = content_slide('竞品格局 · 05', '三类 PV 供给形态：谁有数据库，谁只有人', 14)
tb(s, 0.42, 2.02, 12.2, 0.26, [[('Genpact · Accenture · TCS 均无自有 PV 数据库，只提供托管运营与插件式自动化', 9.5, False, GRAY)]])
card_x = [0.42, 4.69, 8.96]; cw3, cy3, ch3 = 3.95, 2.52, 3.34
forms = [
    ('① 只有库', '卖软件，不接运营', 'Veeva · Oracle Argus\nArisGlobal · 百奥知',
     '交付验证包与实施；客户自建团队，或另找服务商代运营', False),
    ('② 库 + 服务', '既卖系统，也接病例处理', 'IQVIA · 泰格 ClinFlash Safety\n太美 eSafety（太美智研）',
     'IQVIA 3,000+ 安全专员；泰格 PV 团队 190+ 人；太美以智研承接服务', False),
    ('③ 没有库', '只做托管与插件', 'Genpact · Accenture · TCS',
     '数据仍在客户的库里；它们提供自动化插件 + 人力代运营', True),
]
for i, (lab, ttl, vend, note, hi) in enumerate(forms):
    x = card_x[i]
    rect(s, x, cy3, cw3, ch3, CREAM if hi else WHITE,
         line_color=ACCENT if hi else LINEC, line_w=1.6 if hi else 0.75)
    tb(s, x + 0.2, cy3 + 0.15, cw3 - 0.4, 0.24, [[(lab, 9, True, ACCENT if hi else GRAY)]])
    tb(s, x + 0.2, cy3 + 0.44, cw3 - 0.4, 0.34, [[(ttl, 12.5, True, NAVY)]])
    rect(s, x + 0.2, cy3 + 0.88, 0.55, 0.03, ACCENT if hi else LINEC)
    vp = [[(ln, 9.5, True, NAVY)] for ln in vend.split('\n')]
    tb(s, x + 0.2, cy3 + 1.06, cw3 - 0.4, 0.70, vp, space_after=3, line_spacing=1.12)
    tb(s, x + 0.2, cy3 + 2.34, cw3 - 0.4, 0.85, [[(note, 9, False, BODY)]], line_spacing=1.18)
callout(s, '关键差别：前两类卖"系统的归属"，第三类卖"人手与效率"——不拥有数据库，因此不构成对数据库厂商的替代。')

# ---------- 15 聚拢逻辑 ----------
s = content_slide('结论与建议 · 02', '为什么 PV 系统市场在聚拢：四股力量', 15)
quad = [
    ('① 监管刚性收敛', 'GVP 强制电子化 + 2024–25 飞检密集 + 2026 新条例压实 MAH 责任：合规预算只流向"经过验证"的系统，信任即壁垒'),
    ('② 数据网络效应', '信号检测价值随数据量增长；IQVIA OneKey 与 Veeva 的 MDM 十年诉讼本质是数据资产之争，2025-08 以和解+互通收场'),
    ('③ AI 规模经济', '病例自动化需海量标注训练 + 持续合规验证，固定成本高、边际成本低；Sanofi 成本 -15%→-50% 只有规模化玩家做得到'),
    ('④ 资本并购整合', '达索 2019 收 Medidata、2026 再以 18 亿美元收 ArisGlobal（对价挂钩 AI 收入里程碑）——PV 能力正被并入大平台'),
]
qx = [0.42, 6.72]; qy = [2.10, 4.10]; qw2, qh2 = 6.19, 1.86
for i, (h, b) in enumerate(quad):
    x, y = qx[i % 2], qy[i // 2]
    rect(s, x, y, qw2, qh2, CREAM)
    rect(s, x, y, 0.055, qh2, ACCENT)
    tb(s, x+0.18, y+0.12, qw2-0.35, 0.32, [[(h, 12.5, True, NAVY)]])
    tb(s, x+0.18, y+0.50, qw2-0.35, qh2-0.6, [[(b, 9.5, False, BODY)]], line_spacing=1.12)
callout(s, '聚拢本质 = 合规信任 + 数据资产 + AI 规模经济三重壁垒成形；中等集中度下，中小 MAH 与中国本地化仍有结构性空档。')

# ---------- 14 CRO 决策 ----------
s = content_slide('结论与建议 · 03', '临床 CRO 要不要自建 PV 数据库？——要：轻量做、从痛点做', 16)
section_header(s, 0.42, 2.02, 7.35, '为什么要做（四个理由）')
bullets(s, 0.42, 2.46, 7.35, 3.8, [
    ('客户刚需外溢：', '3,000+ 家刚需 MAH 中，中小 MAH / Biotech 买不起也用不动 Veeva / Argus——他们要"系统 + 代运营"一起买'),
    ('CRO 的天然位置：', 'SAE→ICSR 数据同源，PV 是临床链条的自然延伸；手握项目入口，PV 数据库是提升客户生命周期价值与黏性的最佳载体'),
    ('竞争卡位：', '太美已从临床 SaaS 延伸进 PV，IQVIA"平台+服务"验证模式成立；我们不建，客户数据与 PV 预算就被平台商拿走'),
    ('AI 平权窗口：', 'AI/NLP 把病例处理成本降低一个数量级，新进入者首次可能以 1/10 成本提供合规系统——窗口约 2–3 年'),
], size=9.5, gap=6)
rect(s, 8.05, 2.02, 4.86, 4.10, CREAM2)
tb(s, 8.22, 2.16, 4.5, 0.3, [[('怎么做（边界与路径）', 12, True, NAVY)]])
bullets(s, 8.22, 2.52, 4.52, 3.5, [
    ('定位：', '面向中小 MAH / Biotech 的"轻量 PV 数据库 + CRO 代运营"，不与头部正面争 Top 20'),
    ('差异化三件套：', '原生双语 E2B(R3) 自动翻译 ｜ NMPA/FDA/EMA Gateway 合规校验 ｜ 对接 EDC 的实时行列表与可视化'),
    ('路径：', '先做 1–2 个痛点亮点（E2B 翻译、一键递交），绑定自有临床项目验证，再扩为平台'),
    ('红线：', '不重造 Argus 式大平台；不自建 MDM 等重数据资产'),
], size=9, gap=5)
callout(s, '自建 PV 数据库不是做软件生意，而是用系统锁住临床客户的全生命周期——建议做：轻量做、从痛点做。', prefix='一句话：')

# ---------- 15 thanks ----------
prs.slides.add_slide(layouts['答谢页'])

prs.save(OUT)
print('saved', OUT, 'slides:', len(prs.slides._sldIdLst))
