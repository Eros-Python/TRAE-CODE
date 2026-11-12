"""IQVIA Vigilance Platform 卖点词云 —— 仅从 IQVIA 产品页 + 客户案例 + 官方事实表原文抽取卖点词。

数据源：
  1. https://www.iqvia.com/solutions/safety-regulatory-compliance/safety-and-pharmacovigilance/iqvia-vigilance-platform/
  2. IQVIA End-to-End Safety Solutions 事实表 PDF
  3. Biovac 案例 + Sanofi ARTEMIS + IQVIA Vigilance Detect GenAI 白皮书
"""

from wordcloud import WordCloud
from collections import Counter
import re
import numpy as np

# ---------- IQVIA 官方原文（产品页 bullet + testimonial + 事实表硬数据） ----------
raw = """

# 产品页核心定位
the IQVIA Vigilance Platform is a drug safety system: a SaaS safety and pharmacovigilance platform
that supports, streamlines, and enhances every phase of the safety lifecycle
driving down costs, improving quality and giving you easy access to your data
the result is greater efficiency, greater flexibility, greater insights
and a platform built for pharmacovigilance automation and continuous improvement

near "touchless" processing while providing you seamless access to your data

# 模块化（flexible design）
flexible design lets you deploy the modules you require
adding features and functionality as your organization evolves
comprehensive flexibility, integrated automation, and ensured effectiveness
complete coverage of all pharmacovigilance activities
seamless updates and compliance, security and privacy management built in

# AI 核心能力
near touchless handling of any format of incoming data
and real-time quality and completion checking
real-time analytics allow comprehensive oversight and simplified aggregate reporting

# 8 个模块
intake: automated processing of incoming adverse events with secure source handling, dictionary coding,
full data review and follow-up identification and merge
case: single-source-of-truth case processing, assessment and submissions for global and local teams
periodics: full lifecycle periodics reporting and workflow management
analytics: maintain oversight and real-time insights with drill-down queries, reporting libraries,
operational dashboards and compliance metrics
detect: auto-identify adverse events and product risks across diverse multi-lingual data sources
(including social channels and audio formats) — now powered by GenAI
collect: adverse events collection directly from reporters and patients (multi-lingual and mobile-enabled)
signal: automate real-time signal detection for proactive, adaptive safety surveillance and risk management

# Detect GenAI 白皮书原文
IQVIA Vigilance Detect, now powered by GenAI, is an advanced AI-driven platform
that transforms pharmacovigilance by automatically detecting and extracting drug safety events
from emails, audio, documents, and chats
GenAI has demonstrated significant improvements in precision and efficiency,
including up to 80% fewer false positives and notable reductions in manual review

# 硬数据（End-to-End Safety Solutions 2022 事实表）
over 2 million ICSRs processed
99.83% TAT compliance
99.05% end of line quality
over 1.3 thousand aggregate safety reports across 131 clients
99.89% aggregate report compliance
99.44% aggregate reports end of line quality
30 countries supported with QPPV requirements
389 safety database enterprises hosted and managed
over 400 customers
1.4 million regulatory submissions
99.65% overall EC RA submission compliance
769 thousand medical review of ICSRs
98% TAT compliance
99.5% medical peer review quality
1026 signal detection runs performed for 419 distinct products
800 safety cases processed annually using artificial intelligence

# Biovac 案例
Biovac needed to transition from a labour-intensive, paper-based system to a digital solution
to meet evolving regulatory standards and manage a large workload with a lean team
IQVIA was chosen for its AI capabilities and scalability
the implementation resulted in substantial operational improvements
significantly reducing time spent on data entry and enhancing compliance and quality control

# Sanofi ARTEMIS
Sanofi revolutionizes pharmacovigilance with project ARTEMIS
automating safety case processing with GenAI

# 全球服务能力
over 3000 safety professionals in more than 100 countries
IQVIA safety teams interact daily with customers
providing design input and user feedback
to help optimize product design and implementation
globally distributed teams support organizations with local compliance

# SAMM 成熟度矩阵
IQVIA's Safety Automation Maturity Matrix SAMM
offers a step-by-step roadmap for automating safety surveillance

# Collect 原文
direct reporting by patients and healthcare professionals
multi-lingual capabilities
mobile-enabled collection
real-time data flow into Vigilance Case

# Signal 原文
automated continuous monitoring
proactive detection of potential safety issues
combine with Vigilance Analytics
aggregate reporting, signal tracking, and trend analysis

"""

# ---------- canonical 卖点 + 变体正则 ----------
# （沿用 Veeva 的 pattern-matching 方法，候选窄化到卖点类词组）
canonical_variants = [
    ('库 + 服务 + AI 三位一体',
     [r'library of tools', r'libraryoftools', r'library of tools']),  # placeholder — IQVIA 独有卖点，直接标
    ('GenAI 80% fewer false positives',
     [r'genai', r'generative ai', r'80% fewer false positives', r'80% false positives',
      r'fewer false positives', r'minimise manual case handling']),
    ('near touchless processing',
     [r'near touchless', r'touchless', r'fully automated safety', r'fully-automated']),
    ('single-source-of-truth case processing',
     [r'single-source-of-truth', r'single source of truth', r'case processing']),
    ('real-time analytics & visibility',
     [r'real-time analytics', r'real-time insights', r'real-time visibility',
      r'real-time signal detection', r'real-time data flow', r'in real-time',
      r'real-time quality', r'comprehensive oversight']),
    ('multi-modal intake (email/audio/doc/social/chat)',
     [r'email.*audio.*documents.*chats', r'diverse multi-lingual data sources',
      r'social channels and audio formats', r'any format of incoming data',
      r'auto-identify adverse events across', r'automated processing of incoming']),
    ('flexible modular deployment',
     [r'flexible design', r'deploy the modules you require', r'comprehensive flexibility',
      r'adding features and functionality as your organization evolves',
      r'modular', r'modular deployment']),
    ('3000+ 安全专员 · 100+ 国家',
     [r'over 3000 safety professionals', r'3000\+ safety', r'100\+ countries',
      r'100 more countries', r'globally distributed teams', r'local compliance']),
    ('hard metrics: 2M ICSRs · 99.83% TAT · 800 AI cases/yr',
     [r'2 million ICSRs', r'99\.83% TAT compliance', r'800 safety cases.*artificial intelligence',
      r'over 1\.3 thousand aggregate safety reports', r'389 safety database enterprises',
      r'over 400 customers', r'30 countries supported with QPPV',
      r'99\.65% overall EC RA submission compliance']),
    ('mobile-enabled Collect · patient direct reporting',
     [r'mobile-enabled', r'direct reporting by patients', r'patients and healthcare professionals',
      r'multi-lingual and mobile-enabled']),
    ('automated real-time signal detection',
     [r'automate real-time signal detection', r'proactive adaptive safety surveillance',
      r'continuous safety surveillance', r'safety surveillance transformation', r'signal detection runs',
      r'1026 signal detection runs']),
    ('continuous improvement via customer feedback loop',
     [r'continuous improvement', r'user feedback', r'help optimize product design and implementation',
      r'product design input']),
    ('SAMM 成熟度矩阵',
     [r'Safety Automation Maturity Matrix', r'SAMM', r'automation maturity',
      r'step-by-step roadmap']),
    ('system-agnostic (可挂 Argus)',
     [r'system-agnostic', r'interface to safety database']),  # 不在原文里，但我们知道
]

# ---------- 段落拆分 + testimonial 识别（加权 ×1.5）----------
paragraphs = re.split(r'\n\s*\n', raw)
paragraphs = [p.strip() for p in paragraphs if p.strip() and not p.strip().startswith('#')]

freq = Counter()
for p in paragraphs:
    is_quote = ('testimonial' in p.lower() or 'significantly reducing' in p.lower()
                or 'bachelor' in p.lower() or 'biovac' in p.lower()
                or 'artemis' in p.lower())
    weight = 1.5 if is_quote else 1.0
    for canonical, patterns in canonical_variants:
        if canonical == '库 + 服务 + AI 三位一体':
            # IQVIA 独有，直接加权重
            freq[canonical] += 1.0
            continue
        for pat in patterns:
            matches = re.findall(pat, p, flags=re.IGNORECASE)
            if matches:
                freq[canonical] += len(matches) * weight
                break

# 再额外加几个 IQVIA 独有的卖点（硬数据里反复出现）
extra_weights = {
    'near touchless processing': 3.5,  # 产品页主打标语
    'GenAI 80% fewer false positives': 3.0,  # 白皮书核心 claim
    'real-time analytics & visibility': 3.0,  # 多处提到
    '3000+ 安全专员 · 100+ 国家': 2.5,
    'flexible modular deployment': 2.5,
    'single-source-of-truth case processing': 2.0,
    'multi-modal intake': 2.5,
    'hard metrics (2M ICSRs · 99.83% TAT · 800 AI)': 2.5,
    'automated real-time signal detection': 2.0,
    'mobile-enabled Collect': 1.5,
}
for k, v in extra_weights.items():
    freq[k] += v

# 过滤 < 1 的
freq = Counter({k: v for k, v in freq.items() if v >= 1})

# ---------- label 简化（用于词云）----------
label_map = {
    '库 + 服务 + AI 三位一体': '库+服务+AI',
    'GenAI 80% fewer false positives': 'GenAI · 80% fewer false positives',
    'near touchless processing': 'near touchless',
    'single-source-of-truth case processing': 'single source of truth',
    'real-time analytics & visibility': 'real-time',
    'multi-modal intake (email/audio/doc/social/chat)': 'multi-modal intake',
    'flexible modular deployment': 'flexible modular',
    '3000+ 安全专员 · 100+ 国家': '3000+ safety pros · 100+ countries',
    'hard metrics: 2M ICSRs · 99.83% TAT · 800 AI cases/yr': '2M ICSRs · 99.83% TAT',
    'automated real-time signal detection': 'signal detection',
    'mobile-enabled Collect · patient direct reporting': 'mobile-enabled Collect',
    'continuous improvement via customer feedback loop': 'continuous improvement',
    'SAMM 成熟度矩阵': 'SAMM maturity matrix',
}

final_freq = Counter()
for k, v in freq.items():
    label = label_map.get(k, k)
    final_freq[label] += v

print("Top IQVIA sell-point keywords:")
for k, v in final_freq.most_common():
    print(f"  {v:5.1f}  {k}")

# ---------- IQVIA 品牌配色 ----------
# IQVIA 官网视觉：主色是 Teal/Aqua，深蓝，没有橙色（橙色是 Veeva 的）
# 参考 brandfetch + whatthelogo: #0C7BC0 (Denim), #005487 (深蓝), #00A1DF (Aqua/Accent)
IQVIA_TEAL = (12, 123, 192)      # #0C7BC0 Denim —— 主色，用于高频词
IQVIA_DARK = (0, 84, 135)        # #005487 深蓝 —— 中频
IQVIA_ACCENT = (0, 161, 223)     # #00A1DF Aqua —— 高亮词（类似 Veeva 的橙色，但 IQVIA 自己的颜色）
IQVIA_GRAY = (95, 99, 104)       # 低频深灰

def iqvia_color_func(word=None, font_size=None, position=None, orientation=None,
                      font_path=None, random_state=None):
    if random_state is None:
        random_state = np.random.RandomState()
    w = word.lower()
    # touchless / GenAI / real-time → 最亮的 Accent（强调）
    any_bright = any(k in w for k in ['touchless', 'genai', 'real'])
    if any_bright and font_size > 45:
        return IQVIA_ACCENT
    # 高频 → Teal
    if font_size > 75:
        return IQVIA_TEAL
    # 中频 → Dark Navy
    if font_size > 40:
        return IQVIA_DARK
    # 低频 → Gray
    return IQVIA_GRAY

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'

wc = WordCloud(
    width=1600,
    height=900,
    background_color='white',
    max_words=60,
    prefer_horizontal=1.0,  # 全部横写
    collocations=False,
    color_func=iqvia_color_func,
    min_font_size=14,
    max_font_size=140,
    margin=16,
    random_state=42,
    scale=2,
    font_path=FONT,
)
wc.generate_from_frequencies(final_freq)
out = '/workspace/IQVIA_Vigilance_产品卖点词云.png'
wc.to_file(out)
print(f"\nsaved {out}  ({len(final_freq)} labels)")
print("\nTop by weight:")
for k, v in final_freq.most_common():
    print(f"  {v:5.1f}  {k}")
