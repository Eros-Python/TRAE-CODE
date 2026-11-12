"""Word cloud from Veeva Safety related pages."""
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import re
import numpy as np

# ---------- 关键词库 ----------
# 聚合：产品卖点 + 客户案例 + 行业报告 + 日语/韩语/西语页关键词
keywords = {
    # ---------- 产品 / 功能 ----------
    'pharmacovigilance': 22,
    'case processing': 20,
    'signal detection': 19,
    'Adverse Event': 18,
    'ICSR reporting': 17,
    'PSMF / PVA': 16,
    'MedDRA coding': 15,
    'safety gateway': 14,
    'workflow automation': 13,
    'aggregates & reports': 12,
    'literature monitoring': 11,
    'single source of truth': 11,
    'patient safety': 10,
    'cloud platform': 10,
    'data model unification': 10,
    'workbench analytics': 9,
    'SafetyDocs': 9,
    'SafetySignal': 9,
    'regulatory compliance': 9,
    'submission rules': 8,
    'health authorities': 8,
    'WHODrug / EDQM': 8,
    'medical dictionary': 7,
    'audit trail': 7,
    'electronic signatures': 7,
    'change control': 7,
    'validation IQ/OQ/PQ': 7,
    '21 CFR Part 11': 6,
    'GxP validated': 6,
    'multi-tenancy': 5,
    'E2B(R2) E2B(R3)': 8,
    'drug data review': 6,
    'complex analyses': 5,
    'volume processing': 5,
    'SaaS native': 6,
    # ---------- 客户 / 场景 ----------
    'UCB': 9,
    'emerging biotech': 11,
    'small biopharma': 10,
    'growth phase': 9,
    'M&A due diligence': 7,
    'CRO collaboration': 9,
    'sponsor CRO one team': 7,
    'real-time visibility': 8,
    'data ownership control': 8,
    'regulatory submissions': 6,
    # ---------- 市场侧 ----------
    'Veeva vs IQVIA': 10,
    'IDC MarketScape': 6,
    'Gartner evaluation': 5,
    'G2 reviews': 5,
    'Japan pharma adoption': 5,
    'Korea pharma adoption': 4,
    'LATAM pharma adoption': 3,
    'Sumitomo Dainippon': 3,
    'Kyowa Kirin': 3,
    'Taiho Pharmaceutical': 2,
    # ---------- 竞争 / 对比 ----------
    'Oracle Argus': 6,
    'ArisGlobal': 5,
    'RxLogix': 4,
    'top 10 PV tools': 4,
    'AI signal detection': 8,
    'automation maturity': 5,
    'low-touch processing': 6,
    'touchless AI target': 7,
    # ---------- 日语侧 ----------
    '安全性情報管理システム': 6,
    '有害事象収集処理届出': 5,
    'スポンサー・CRO': 4,
    'グローバル対応': 4,
    # ---------- 韩语侧 ----------
    '이상사례 관리': 4,
    # ---------- 西班牙语侧 ----------
    'evento adverso': 3,
}

# ---------- 词云生成 ----------
NAVY = (22, 44, 92)
CREAM = (243, 236, 216)
ACCENT = (206, 80, 52)
GRAY = (95, 99, 104)

def veeva_color_func(word=None, font_size=None, position=None,
                      orientation=None, font_path=None, random_state=None):
    if random_state is None:
        random_state = np.random.RandomState()
    # 高频词 = 深蓝主色，中频词 = 橙色高亮，低频词 = 深灰
    if font_size > 70:
        return NAVY
    if font_size > 45:
        return ACCENT
    if font_size > 25:
        return (60, 80, 130)  # 偏蓝的灰
    return GRAY

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'

wc = WordCloud(
    width=1600,
    height=900,
    background_color='white',
    max_words=100,
    prefer_horizontal=0.68,
    collocations=False,
    color_func=veeva_color_func,
    min_font_size=14,
    max_font_size=130,
    margin=12,
    random_state=42,
    scale=2,
    font_path=FONT,
)
wc.generate_from_frequencies(keywords)
out = '/workspace/Veeva_Safety_关键词词云.png'
wc.to_file(out)
print('saved', out)
print('total words:', len(keywords))
print('top 15 by weight:')
for k, v in sorted(keywords.items(), key=lambda x: -x[1])[:15]:
    print(f'  {v:3d}  {k}')
