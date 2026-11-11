# -*- coding: utf-8 -*-
"""生成 PV 数据库市场调研总结文字稿 docx"""
import docx
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

NAVY = RGBColor(0x16, 0x28, 0x3C)
ACCENT = RGBColor(0xC0, 0x65, 0x2B)
GRAY = RGBColor(0x7A, 0x72, 0x64)
BODY = RGBColor(0x3A, 0x41, 0x49)

doc = Document()
style = doc.styles['Normal']
style.font.name = '微软雅黑'
style.font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

def para(text_runs, size=10.5, space_after=6, indent=False):
    """text_runs: str 或 [(text, bold, color)]"""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
    if indent:
        p.paragraph_format.left_indent = Inches(0.25)
    if isinstance(text_runs, str):
        text_runs = [(text_runs, False, BODY)]
    for t, b, c in text_runs:
        r = p.add_run(t)
        r.font.size = Pt(size); r.font.bold = b; r.font.color.rgb = c
    return p

def h1(text):
    p = doc.add_heading(level=1)
    r = p.add_run(text); r.font.size = Pt(16); r.font.bold = True
    r.font.color.rgb = NAVY
    r.font.name = '微软雅黑'; r.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

def h2(text):
    p = doc.add_heading(level=2)
    r = p.add_run(text); r.font.size = Pt(13); r.font.bold = True
    r.font.color.rgb = NAVY
    r.font.name = '微软雅黑'; r.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

def bullet(lead, rest, size=10.5):
    runs = [('· ' + lead, True, NAVY), (rest, False, BODY)] if rest else [('· ' + lead, False, BODY)]
    para(runs, size=size, space_after=4, indent=True)

def conclusion(text, prefix='结论：'):
    para([(prefix, True, ACCENT), (text, False, BODY)], space_after=10)

def add_table(header, rows, widths=None):
    t = doc.add_table(rows=1 + len(rows), cols=len(header))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, htxt in enumerate(header):
        cell = t.cell(0, j)
        cell.text = ''
        r = cell.paragraphs[0].add_run(htxt)
        r.font.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shd = docx.oxml.parse_xml(f'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="clear" w:fill="16283C"/>')
        cell._tc.get_or_add_tcPr().append(shd)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = t.cell(i + 1, j)
            cell.text = ''
            r = cell.paragraphs[0].add_run(val)
            r.font.size = Pt(9)
            if j == 0:
                r.font.bold = True; r.font.color.rgb = NAVY
    if widths:
        for j, w in enumerate(widths):
            for row in t.rows:
                row.cells[j].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ================= 封面信息 =================
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('PV 数据库（药物警戒系统）市场调研总结'); r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = NAVY
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('市场规模 × 竞品格局 × 自建决策建议'); r.font.size = Pt(12); r.font.color.rgb = BODY
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('2026 年 11 月 ｜ 依据《PV 数据库市场调研》与公开资料整理'); r.font.size = Pt(10); r.font.color.rgb = GRAY
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('口径说明：标注"推断"的数据为基于公开数据的测算，非直接统计；"未披露"不等于"没有"；厂商自述数字未经第三方审计。')
r.font.size = Pt(9); r.font.color.rgb = GRAY
doc.add_paragraph()

# ================= 一、市场规模与数据 =================
h1('一、市场规模与数据')

h2('1.1 全球与中国市场规模')
bullet('全球市场：', '2025 年全球 PV 系统/软件市场 $75.8 亿，CAGR 10.2%（2025–2034，Dataintelo）；含服务外包全链条的 PV 市场为 $93.5 亿（Ken Research）。')
bullet('纯软件 TAM：', '不含服务的 PV 软件子赛道 $20.9 亿（2025）→ $50.6 亿（2035E），CAGR 9.2%（Precedence Research）——是最接近"数据库产品"的可寻址市场。')
bullet('中国市场：', '2025 年中国 PV+药物安全软件市场 ¥48.6 亿（博研咨询，口径含解决方案）；海外纯软件口径中国约 ¥3 亿（GIA 2026）——真实区间在两者之间，中国增速高于全球。')
bullet('区域结构：', '亚太为增速最快区域（CAGR 12.74%，Straits Research），北美占 38.2%；软件占整体 PV 市场 58.3%，药企端收入占 42.1%（Dataintelo）。')
bullet('增量来源：', '新建 MAH 首次建库 + 存量系统替换 + AI 功能升级三类需求叠加。')
conclusion('PV 软件是产业链中增长最快的环节，自动化子赛道（CAGR 13.4%）跑赢整体（10.2%）——增量主战场在"软件 + AI 自动化"。')

h2('1.2 中国 MAH 全景：刚需客群测算')
para('只有"临床阶段 Biotech + 有上市后产品的 MAH"对 PV 数据库有刚性需求。以下测算中，"确定"为有公开统计来源，"推断"为基于公开数据的测算：', space_after=4)
add_table(
    ['客群', '数量（家）', '口径与来源'],
    [
        ['MAH 持有人总数（A+B+纯B）', '5,832', '确定：博研咨询引药智网/NMPA，2025 年底；NMPA 生产型企业 5,581 家交叉验证'],
        ['其中：有上市后产品（持有效注册证）', '1,843', '确定：博研咨询 2025；其中创新药上市企业约 150–250 家（推断：2016–2023 年 142 个国产创新药涉及 108 家 MAH，2024/2025 再获批 48/76 个）'],
        ['其中：纯 B 证轻资产 MAH', '1,252 → 约 1,500', '确定：药智网 2025-03；2026 值为推断（2024 年 +16.2%，按 10–16% 增速外推）'],
        ['临床阶段 Biotech（有在研管线）', '1,000–1,500', '推断：中国在研创新药 4,751 个（医药魔方 2025，占全球 33.7%）÷ 每家 3–4 个管线'],
        ['2026 年刚需客群合计', '约 3,000–3,500', '推断：上市后 MAH 1,843 + 临床阶段 Biotech（去除少量重叠）'],
        ['2030 年预测', '约 4,500–5,000', '推断：临床阶段按 CAGR 8.5% 增长（原调研模型 2030 年约 3,049 家活跃治疗开发公司），叠加每年 70+ 个创新药获批转化为上市后 MAH'],
    ],
    widths=[2.2, 1.2, 3.6])
para('需求侧佐证：2025 年新药临床试验登记 2,997 项（同比 +18.0%，CDE 年报）；2025 年 NMPA 批准上市 1 类创新药 76 个；纯 B 证 MAH 年增速已从 +121.7%（2022）回落至 +16.2%（2024），行业从爆发进入稳态扩容。', size=9.5)
conclusion('刚需客群约 3,000+ 家、每年以 8–10% 扩容——这是 PV 数据库软件的目标客户基本盘；其中纯 B 证轻资产 MAH 对 SaaS 化轻量产品最敏感，是首选切入点。')

h2('1.3 自动化市场与集中度')
bullet('规模：', 'PV 自动化市场 $26.7 亿（2025）→ $30.3 亿（2026）→ $56.8 亿（2031），CAGR 13.42%（Mordor Intelligence）；其中软件占 65.82%，不良事件报告功能占 38.46%。')
bullet('集中度：', '市场处于"集中"与"分散"之间的中等集中度；Oracle / ArisGlobal / Veeva / IQVIA 以嵌入式工作流 + 多年期验证锁定 Top 20 药企。中国 PV 市场 CR5 为 58.4%，IQVIA 以 14.8% 居第一（博研咨询）。')
bullet('增长驱动：', '监管压力（+2.8）、AE 数据量增长（+3.1）、AI 平台普及（+2.5）、药企降本（+1.9）、CGT 监测（+1.2）、RWD 扩展（+1.4）——对 CAGR 的贡献（Mordor）。')
bullet('制约因素：', '数据隐私与跨境合规（-1.6）、遗留系统集成复杂（-1.1）、AI 供应商锁定担忧（-0.7）、多语言 NLP 偏差（-0.5）。')
bullet('技术热点：', 'PV 数字化研究关键词聚类显示，机器学习、深度学习、信息提取是研究主线（《中国现代应用药学》2022）——与产业界的 AI 自动化方向一致。')
conclusion('"中等集中"＝头部锁定大客户、长尾仍开放：面向中小 MAH 的轻量化、国产合规产品仍有结构性窗口。')

# ================= 二、竞品格局 =================
h1('二、竞品格局')

h2('2.1 四家 PV 系统横向对照')
add_table(
    ['维度', 'Veeva Safety Suite', 'IQVIA Vigilance Platform', '太美 eSafety', '百奥知 Bioknow PV'],
    [
        ['定位', 'Vault 云平台上的一体化 PV 应用组合', '模块化 SaaS：AI 为核心、客户数据自有', '国产 GVP 一体化 PV 数据库 + iPV 智能体', '国产"PV 数据中心"：eSAE+eADR+PV+Gateway'],
        ['组成', '5 应用：Safety / SafetyDocs / Workbench / Signal / AI', '8 模块：Intake / Case / Periodics / Analytics / Detect / Collect / Signal / Admin', 'eSafety + iPV Agent + 全球递交 Gateway', 'Bioknow PV + eSAE + eADR + 一体化门户 + Gateway'],
        ['AI 能力', 'AI for Safety 2025 上线，早期（1–10 客户）', 'AI at core，目标近"touchless"病例处理', 'iPV：自述重复任务自动化 80%、合规率 99.9%', '2026 起密集发布信号检测 / 文献 AI / Narrative 秒级生成'],
        ['客户证据', '8 家 Top 20 药企；18 家具名客户（Merck、诺和诺德、CRISPR 等）', '30+ 平台客户、20 家 Top 50；具名案例 Sanofi / Biovac', '自述 500 家申办方/CRO；具名 1 家（豪森医药）', '自述 300+/400+ 家；无具名客户'],
        ['商业条款', '未公开价格', '$49K 实施 + $65K/年（3 年、1,500 例/年、10 用户），12–15 周上线', '未公开价格', '未公开价格'],
        ['中国本地化', '全球统一平台，中国区能力未单列', '全球平台 + 本地服务；中国市占 14.8%', '直连 NMPA 直报；中英日双语；WHO-UMC 认证供应商', 'NMPA/FDA/EMA/MHRA 上报；等保三级'],
    ],
    widths=[0.7, 1.55, 1.6, 1.55, 1.6])
para('注：各家客户数口径不同（去重具名 vs 厂商自述），不可直接横比。', size=9)

h2('2.2 Veeva Safety Suite：平台生态型')
bullet('成熟双核：', 'Safety（51–100 客户）+ SafetyDocs（11–50）同库共存，覆盖 ICSR 处理与 PSMF / PVA / RMP / aRMM 全内容管理。')
bullet('平台锁定：', '与临床、EDC、RIM、质量系统打通——卖的是统一数据模型与生态，而非单点功能。')
bullet('增长曲线：', 'Workbench / Signal / AI for Safety 均为 1–10 客户的早期产品，正向存量客户交叉销售；AI for Safety（2025）把 AI 嵌入合规工作流。')
bullet('客群覆盖：', '大药企 + Biotech + CRO（Linical、Biomapas、Catalyst、Arriello 等 4 家 CRO 具名）——CRO 是其明确目标客群。')
para([('对 CRO 的启示：', True, ACCENT), ('黏性来自数据模型与多系统集成；百万美元级客单价与重量级实施使中小 MAH 市场天然留空；其 CRO 客群策略证明"CRO 用 PV 平台服务客户"模式成立。', False, BODY)], indent=True)
conclusion('Veeva = 平台生态型：强在数据模型与生态集成；价格与实施重量是其在中国中小客群的最大短板。')

h2('2.3 IQVIA Vigilance Platform：AI 优先 + 标准化下沉')
bullet('商业化最清晰：', '企业级 8 模块 + 面向新兴 Biotech 的预配置套餐（$49K 实施 + $65K/年、3 年 1,500 例/年、12–15 周上线），把 PV 系统从"百万美元项目"变成标准化产品。')
bullet('规模数据：', '30+ 平台客户、20 家 Top 50 药企；生产环境托管病例 1,200 万例（最大 60 万+/年，最小 5 例/月）；220 名技术支持、400+ PV 技术交付人员、200+ 技术客户。')
bullet('行业标杆：', 'Sanofi ARTEMIS 年处理 70 万+ AE 报告，AI 从 Intake 渗透至医疗评估核心环节；成本已降 15%，2027 年目标 -50%；2025 年底完成全系统替换。')
bullet('平台+服务捆绑：', '3,000+ 安全专员覆盖 100+ 国家本地合规，外包服务与软件互相导流；2025-08 与 Veeva 和解并打通数据流转，头部从竞争走向竞合。')
para([('对 CRO 的启示：', True, ACCENT), ('"平台 + 代运营"正是 CRO 自建 PV 的可行模式参照；公开入门价验证了中小客群付费意愿，可作定价锚点；中国市占 14.8% 居第一，是国产化替代的直接对标对象。', False, BODY)], indent=True)
conclusion('IQVIA = AI+服务双轮型：唯一公开定价的头部玩家，验证了 PV 系统产品化、下沉化的商业路径。')

h2('2.4 PV 数据库软件梯队全景')
add_table(
    ['梯队', '代表厂商', '生存逻辑 / 定位', '关键证据'],
    [
        ['全球平台一线', 'Veeva · IQVIA · Oracle Argus · ArisGlobal', '完整工作流+数据库+申报一体化，多年期验证锁定 Top 20 药企', 'Veeva 8 家 Top20；IQVIA 20 家 Top50；ArisGlobal 220+ 客户，达索 18 亿美元收购（2026-07 签约）'],
        ['全球利基', 'RxLogix · Ennov · EXTEDO · AB Cube', '模块化 API 挂接遗留系统，区域/单点突破', 'RxLogix 105+ 客户、年千万级病例（自述）；Ennov 650+ 组织'],
        ['AI 原生新势力', 'Graph Safety 等', '知识图谱 + 可解释 AI，云原生按模块交付', '融资 $16.3M；自述 3 小时→10 分钟（未经审计）'],
        ['服务托管型', 'Genpact · Accenture · TCS', '自有 PV 平台 + 代运营捆绑，以人力规模压成本', 'Bayer（2018）｜UCB（2019）｜AstraZeneca（7 区域中心 / 130+ 国家）'],
        ['中国第一梯队', '太美 eSafety · 百奥知 · 洞悉 Holox · Clinflash', 'GVP 合规 + 国产替代 + 中文场景深耕', '太美自述 500 家客户（港股上市 02576.HK）；百奥知自述 300+ 家'],
        ['中国轻量化', 'PVwatch（南京天韬）· iDrugSafety（梅斯）', '轻量 SaaS、用户体验与性价比取胜', '面向国内中小 MAH，区域化服务'],
    ],
    widths=[0.95, 1.7, 2.2, 2.15])
para([('服务托管型补充说明（含出处）：', True, NAVY)], space_after=4)
bullet('Genpact：', '2018-11 与 Bayer 签多年期协议，PVAI 套件接入 Bayer 现有 PV 数据库与 IT 系统，Bayer 为 AI Case Management 模块首批上线客户（early adopter）。原文：https://media.genpact.com/2018-11-01-Genpact-and-Bayer-to-Co-innovate-to-Leverage-Artificial-Intelligence-Capabilities-for-Patient-Safety ｜同稿 PR Newswire：https://www.prnewswire.com/news-releases/genpact-and-bayer-to-co-innovate-to-leverage-artificial-intelligence-capabilities-for-patient-safety-300741980.html')
bullet('Genpact 与 MHRA 的关系（更正）：', 'MHRA 不是 Genpact 的 PV 实施客户。Genpact 2018-06 收购 Commonwealth Informatics，其产品 CVW（Commonwealth Vigilance Workbench）被 FDA、MHRA 等监管机构使用——属"被收购产品的用户"，与"PV 系统实施项目"性质不同，不应并入案例证据。原文：https://media.genpact.com/2018-06-11-Genpact-Accelerates-Strategy-to-Establish-New-Industry-Standard-for-Pharmacovigilance-Using-AI-and-Machine-Learning-Technologies')
bullet('Accenture：', '2019-12-16 与 UCB 合作，UCB 上线 INTIENT™ Pharmacovigilance；由 Accenture 运营团队代管病例处理、平台提供 AI 增强——是"平台 + 代运营"模式的直接样本。原文：https://newsroom.accenture.com/news/ucb-and-accenture-collaborate-to-accelerate-data-processing-and-help-improve-patient-safety.htm ｜服务介绍 PDF：https://www.accenture.com/content/dam/accenture/final/a-com-migration/pdf/pdf-105/accenture-pharmacovigilance-services2.pdf')
bullet('TCS：', 'AstraZeneca 案例——整合 7 个区域中心的患者安全与法规流程，覆盖 70+ 已上市产品、100+ 在研产品、130+ 国家，投入 500+ 药师/医师；其 AE 病例处理经 FDA、MHRA、瑞典药监检查无重大缺陷。原文：https://www.tcs.com/what-we-do/industries/life-sciences/case-study/astrazeneca-enhance-patient-safety-regulatory-services ；另有罗氏中国 PV testimonial：https://www.tcs.com/cn-zh/what-we-do/services/cognitive-business-operations/video/roche-china-pharmacovigilance-testimonial')
bullet('分类提示：', 'Accenture（INTIENT Pharmacovigilance）与 TCS（TCS ADD™ Safety）均有自有的 PV 自动化平台，但均不含自有安全数据库——"平台"与"数据库"是两件事，详见 2.5。TCS ADD Safety：https://www.tcs.com/what-we-do/products-platforms/tcs-add/solution/tcs-add-safety-solution')
conclusion('全球拼"平台锁定"，中国拼"国产替代 + 轻量化"；AI 原生厂商是共同变量——梯队边界正在重排。')

h2('2.5 服务托管型三家（Genpact / Accenture / TCS）：有没有自己的 PV 数据库？')
para([('结论：三家均未推出自有的 PV 安全数据库（system of record）。', True, ACCENT),
      ('他们做的是数据库之上的"AI 自动化层 + 人力代运营"，客户的病例数据仍存放在客户已有的安全数据库里（Oracle Argus、Veeva、或自研系统）。以下为各家官方表述的直接证据：', False, BODY)], space_after=6)
bullet('Genpact（无自有数据库）：', '2018-11 与 Bayer 的协议明确写"Genpact\'s PVAI suite of capabilities will be applied to Bayer\'s existing pharmacovigilance database and IT systems"——是"应用于客户既有数据库"，不是替换它。其 AI 产品 Cora PharmacoVigilance 定位为病例处理层；2018 年收购 Commonwealth Informatics 获得的 CVW（Commonwealth Vigilance Workbench）是信号检测/信号评估分析工具，同样不是安全数据库。')
bullet('Accenture（无自有数据库）：', 'INTIENT Pharmacovigilance 官网对"Machine pre-processing"的描述是"generate well-formed, quality output for import into enterprise safety systems"——产出物是"导入企业安全系统"，即位于数据库的上游。UCB 案例中，Accenture 提供的是"平台 + 运营团队代管病例处理"，UCB 的系统并未被替换。')
bullet('TCS（无自有数据库）：', 'TCS ADD™ Safety 官网 Features 第一条即"Modular deployment with an interface to safety database"——模块化部署 + 对接安全数据库，明确定位为数据库的前端自动化，而非数据库本身。')
para([('实施模式差异（平台厂商 vs 服务托管型）：', True, NAVY)], space_after=4)
add_table(
    ['维度', '平台厂商（Veeva / IQVIA / Argus）', '服务托管型（Genpact / Accenture / TCS）'],
    [
        ['卖什么', '系统本身：建库、存案、E2B 递交、定期报告', '人力 + 自动化能力：替客户处理病例，不卖数据库'],
        ['数据归属', '数据落在厂商自有数据模型内，迁移需格式转换', '数据留在客户已有库，服务商只读取/处理'],
        ['计价方式', '许可/订阅 + 实施费，按模块与用户数', '按病例量、FTE 或成果计费，随业务量弹性伸缩'],
        ['上线周期', '6–18 个月（配置、验证、数据迁移、接口联调）', '数周–数月：先接管流程，自动化工具并行接入'],
        ['合规责任', '厂商交付验证包，客户自行完成 IQ/OQ 与系统放行', '服务商承担 SOP、质量体系与监管检查应对'],
        ['切换成本', '高：数据 + 流程双锁定，换系统近乎重建', '低：数据库不动，可随时增减服务范围或退出'],
    ],
    widths=[0.95, 2.75, 2.75])
bullet('注意：IQVIA 不在此列（常见误判）：', 'IQVIA Vigilance Platform 官网明确定位为"a drug safety system"，其 Vigilance Case 模块提供"single-source-of-truth case processing, assessment and submissions"，Vigilance Administration 提供 PLS 配置与用户安全管理——即具备完整的 system of record 能力，Biovac 案例亦是从纸质系统迁移到该平台。因此 IQVIA 属"平台厂商"侧，且同时拥有 3,000+ 安全专员的 BPO，是全球范围内"自有库 + 代运营"的双持者。补充：其 Vigilance Detect / Collect 为 system agnostic 模块，可挂接客户既有数据库，故 IQVIA 既能卖整库、也能只卖模块或只卖人力。')
bullet('本土双持者：泰格 ClinFlash Safety：', '泰格医药官网将 ClinFlash Safety 明确列为"Pharmacovigilance safety database"，clinflash.com 产品页称之为"安全数据库"，支持 E2B R3 标准、可通过 Gateway 或 XML 对接各类监管机构，覆盖临床及上市后阶段；泰格 2025 年半年报披露药物警戒专业团队超过 190 人，覆盖美国、欧洲、日本、东南亚与中国。即"自研数据库 + 自有 PV 团队"，结构与 IQVIA 一致，但价格带与服务半径更贴近国内中小 MAH——这是本土最值得对标的对手。')
bullet('有库但无代运营证据：百奥知 / 太美：', '百奥知官网产品为"药物安全管理系统（简称 PV）V4.7"，eADR 采集后"在 PV 系统中快速生成个例报告"；太美官网将 eSafety 称为"药物警戒数据库"，月处理 ICSR 9,000 例、服务 500 家申办方/CRO。两者均确认为自有数据库产品；本次检索未找到其提供 PV 代运营（外包人力）业务的一手证据，故仅列为"有库 · 无服务"，不补充服务类信息。')
bullet('对 CRO 的意义（关键）：', '这三家全球最大的服务商，都主动选择不做数据库、只做数据库之上的一层。原因不是能力不足，而是数据库位已被 Argus / Veeva / IQVIA 以验证成本和数据模型锁定，硬碰不划算。这恰好说明：CRO 若自建，不应瞄准"替代 Argus"，而应做"轻量数据库 + 自动化 + 代运营"的组合，去接他们不愿下沉的中小 MAH 客群。')
conclusion('服务托管型证明"在别人数据库上做自动化与服务"是可持续生意；但对中小 MAH 而言，他们仍缺一个买得起、用得动的数据库——这是留给 CRO 的真实空位。')

# ================= 三、结论与建议 =================
h1('三、结论与建议')

h2('3.1 为什么 PV 系统市场在聚拢：四股力量')
bullet('① 监管刚性收敛：', 'GVP（2021）强制 MAH 建立电子记录系统，2024–2025 进入飞检密集期，2026 年新《药品管理法实施条例》进一步压实 MAH 主体责任——合规预算只流向"经过验证"的系统，信任即壁垒。')
bullet('② 数据网络效应：', '信号检测价值随数据量增长（FAERS / VAERS / EVDAS / RWD 多源融合）；IQVIA OneKey 与 Veeva 的 MDM 十年诉讼本质是数据资产之争，2025-08 以和解 + 数据互通收场——头部数据越积越厚，小厂商无法追。')
bullet('③ AI 规模经济：', '病例自动化需要海量标注训练 + 持续合规验证，固定成本高、边际成本低；Sanofi 案例成本 -15% → 目标 -50%，只有规模化玩家做得到。')
bullet('④ 资本并购整合：', '达索 2019 年收购 Medidata、2026-07 再以 18 亿美元（+2 亿里程碑，挂钩 AI 收入）收购 ArisGlobal；IQVIA×Veeva 从诉讼走向全球合作——资本正把 PV 能力并入大平台。')
conclusion('聚拢本质 = 合规信任 + 数据资产 + AI 规模经济三重壁垒成形；中等集中度下，中小 MAH 与中国本地化等细分仍有结构性空档。')

h2('3.2 临床 CRO 要不要自建 PV 数据库？——要：轻量做、从痛点做')
para([('为什么要做（四个理由）：', True, NAVY)], space_after=4)
bullet('客户刚需外溢：', '3,000+ 家刚需 MAH 中，中小 MAH / Biotech 买不起也用不动 Veeva / Argus——他们要"系统 + 代运营"一起买。')
bullet('CRO 的天然位置：', 'SAE→ICSR 数据同源，PV 是临床链条的自然延伸；手握项目入口，PV 数据库是提升客户生命周期价值与黏性的最佳载体。')
bullet('竞争卡位：', '太美已从临床 SaaS 延伸进 PV，IQVIA"平台+服务"验证模式成立；我们不建，客户数据与 PV 预算就被平台商拿走。')
bullet('AI 平权窗口：', 'AI/NLP 把病例处理成本降低一个数量级，新进入者首次可能以 1/10 成本提供合规系统——窗口约 2–3 年。')
para([('怎么做（边界与路径）：', True, NAVY)], space_after=4)
bullet('定位：', '面向中小 MAH / Biotech 的"轻量 PV 数据库 + CRO 代运营"，不与头部正面争 Top 20。')
bullet('差异化三件套：', '原生双语 E2B(R3) 自动翻译 ｜ NMPA/FDA/EMA Gateway 合规校验 ｜ 对接 EDC 的实时行列表与可视化。')
bullet('路径：', '先做 1–2 个痛点亮点（E2B 翻译、一键递交），绑定自有临床项目验证，再扩为平台。')
bullet('红线：', '不重造 Argus 式大平台；不自建 MDM 等重数据资产。')
conclusion('自建 PV 数据库不是做软件生意，而是用系统锁住临床客户的全生命周期——建议做：轻量做、从痛点做。', prefix='一句话：')

# ================= 附 =================
h1('附：数据口径与主要来源')
bullet('', '全球规模：Dataintelo（2025）；Ken Research（2025）；Precedence Research；Mordor Intelligence《Pharmacovigilance Automation Market》（CC BY 4.0）；Straits Research。')
bullet('', '中国市场：博研咨询《2026 年中国药物警戒（PV）和药物安全软件行业报告》（口径含解决方案，可靠性中等，作上限参考）；Global Industry Analysts（2026-11，纯软件口径）。')
bullet('', 'MAH 与企业数：博研咨询引药智网/NMPA（2025 年底）；NMPA《药品监督管理统计年度数据（2025 年）》；中国药科大学学报 B 证研究（药智网，2025-03）；医药魔方（2025）；弗若斯特沙利文；Biotechgate。')
bullet('', '临床与获批：CDE《中国新药注册临床试验进展年度报告》（2024/2025）；NMPA 年度统计（2025）。')
bullet('', '竞品：Veeva 官网 Product Sheet / Customers 页（2026-04）；IQVIA 官网平台页（©2025）与 Fact Sheet（©2026）；IQVIA《Sanofi Revolutionizes Pharmacovigilance with Project ARTEMIS》（2025-06）；太美、百奥知官网（2026）；BioAI Agents Directory（2026-11 抓取）。')
bullet('', 'IQVIA Vigilance Platform 产品定位：https://www.iqvia.com/solutions/safety-regulatory-compliance/safety-and-pharmacovigilance/iqvia-vigilance-platform ；Vigilance Collect（E2B+ 写入 safety database）：https://www.iqvia.com/solutions/safety-regulatory-compliance/safety-and-pharmacovigilance/iqvia-vigilance-platform/iqvia-vigilance-collect ；Biovac 案例：https://www.iqvia.com/library/case-studies/biovacs-drive-for-innovation-partnering-with-iqvia-to-advance-healthcare')
bullet('', '服务托管型案例：Genpact×Bayer（2018-11，media.genpact.com）；Genpact 收购 Commonwealth Informatics / CVW（2018-06，media.genpact.com）；Accenture×UCB / INTIENT Pharmacovigilance（2019-12，newsroom.accenture.com）；TCS×AstraZeneca 案例研究（tcs.com）；TCS×罗氏中国 PV testimonial（tcs.com）；TCS ADD Safety 产品页（tcs.com）。注：Genpact 早期 PVAI 产品页 genpact.com/cora/pharmacovigilance-pvai 现已 404，案例主要存档于 media.genpact.com 新闻稿库。')
bullet('', '政策：GVP（国家药监局 2021 年第 65 号公告）；2026 年新《药品管理法实施条例》。')

doc.save('/workspace/PV数据库市场调研总结-文字稿-20261111.docx')
print('saved docx')
