"""Veeva Safety 产品卖点词云 v2 —— 在候选生成阶段就窄化到卖点模式，
直接从页面原文里匹配 canonical 卖点词 + 它们的变体，避免后置黑名单堆叠。

数据源与上次相同：
  1. https://www.veeva.com/products/veeva-safety-suite/
  2. https://www.veeva.com/cro-collaboration-with-veeva-safety/
  3. https://eu.veeva.com/safety-for-emerging-and-small-biotechs/
"""

from wordcloud import WordCloud
from collections import Counter
import re
import numpy as np

# ---------- Step 1: 原始文本池（三个页面的产品卖点 bullet + testimonial 引述 + 产品功能描述） ----------
# 全部小写，合并为一个大字符串
raw = """

# 页面 1 产品页 https://www.veeva.com/products/veeva-safety-suite/
safety suite of applications operate as a unified pharmacovigilance system on a single cloud platform
to maximize operational efficiencies and improve patient safety
safety applications share a common data model which enables the end-to-end management of safety processes
case processing, signal detection, advanced reporting, and safety content management
global safety case intake, processing, and ICSR reporting
safety pharmacovigilance-related content and process management
standard ai agents that do the work for you
automate safety intake and triage for faster, more efficient case processing
enhance case narratives by correcting grammar, consolidating information, and improving readability

cory gilbert senior director pv operations:
with a single collaborative safety platform, we can standardize terminology, increase data quality and accessibility,
and improve communications to health authorities

adrian maynier head of systems:
our partnership with veeva allows us to stay at the forefront of technological advancements in the industry.
we are now streamlining our operations and improving efficiency.

# veeva connections 集成卖点
automates flow of clinical serious adverse event data, and provides safety teams direct access to subject data
enables seamless flow of safety letters to veeva etmf, and with ctms and siteconnect, distribution to sites with tracking
streamlines intake of adverse event data from medical
shares registered product data

# 页面 2 https://www.veeva.com/cro-collaboration-with-veeva-safety/
gain control and real-time visibility when outsourcing safety operations
one end-to-end solution from intake to case processing with seamless submissions
future proof validated releases 3 times per year to keep up with new regulations and capabilities
real-time collaboration improve data quality and reduce risk and overhead with direct data access

pradnya gunjotikar pv manager cg oncology:
real-time dashboards and reports are intuitive. i can easily present high-level data to leadership
and the review board, or drill into the data for more information.

pharmacovigilance director dermatology biopharma:
with veeva safety, i don't have to wait for someone to pull my data for me. i can see my data in real-time.
i know how it's flowing and how long it takes to process a case.

biomapas testimonial:
involving sponsors within the workflow in veeva safety saves back and forth communication outside the system.
this is key to saving a lot of time. work as one team, one system.

cg oncology testimonial:
we leverage veeva safety to deliver high-quality, patient-centered pharmacovigilance services.
our case processors use clinical expertise to craft meaningful narratives that tell the patient's story.

linical testimonial:
the ability to rapidly configure and deploy new studies and projects in veeva safety saves our team
significant time compared to other systems.

another cro testimonial:
veeva safety's ability to accommodate clinical and post-marketing workflows within a unified platform
is a significant advantage.

another testimonial:
veeva safety has enhanced collaboration with our sponsors by enabling real-time access to case data
and streamlined query resolution.

# 页面 3 https://eu.veeva.com/safety-for-emerging-and-small-biotechs/
oversee and control your data
direct oversight and control with cro flexibility
establish foundation for scalability
automation and operational efficiency
simplify safety operational reporting flexible reports and dashboards for better oversight and compliance
and faster decision-making

hanssar chacon senior director global pv crispr therapeutics:
veeva safety beats a lot of the competition by a long shot. it's intuitive and easy to use, and having
first-hand access to our safety data is irreplaceable.

catalyst clinical research testimonial:
validated safety solution in weeks
cloud-based safety solution from case processing to reporting and submissions

cancer research uk testimonial:
how implementing veeva safety drives case processing efficiency and streamlines safety operations

veeva blog:
reduce clinical trial costs by connecting safety and clinical systems
simplifying pharmacovigilance processes automation dashboards and reports

"""

# ---------- Step 2: 从原始文本里做 pattern matching，直接抽卖点类词组 ----------
# 每个 canonical 卖点 → 它的所有英文变体（原文里实际出现的词形）
# 统计命中次数作为权重；来自 testimonial 引述的 ×1.5
canonical_variants = [
    # (canonical_name, [所有英文变体正则 pattern])
    ('real-time access / visibility',
     [r'real[- ]time visibility', r'real[- ]time access', r'real[- ]time oversight',
      r'see my data in real[- ]time', r'real[- ]time dashboards and reports',
      r'enabling real[- ]time access', r'in real[- ]time', r'real-time',
      r'first-hand access to our safety data', r'direct access to subject data']),
    ('unified / single platform',
     [r'unified pharmacovigilance system', r'single cloud platform', r'single collaborative safety platform',
      r'unified platform', r'one system', r'one platform', r'one end-to-end solution',
      r'accommodate clinical and post-marketing workflows within a unified platform',
      r'shared a common data model']),
    ('automation',
     [r'standard ai agents', r'automate safety intake', r'ai for safety', r'falcon',
      r'ai-driven', r'automates?', r'automating', r'automat', r'ai and machine learning',
      r'automation and operational efficiency', r'automation dashboards']),
    ('seamless integration',
     [r'seamless flow', r'seamless submissions', r'seamless', r'seamlessly',
      r'connecting safety and clinical systems', r'veeva connections',
      r'provides safety teams direct access', r'enables seamless']),
    ('streamline operations',
     [r'streamlining our operations', r'streamlined query resolution', r'streamlines intake',
      r'streamline[s]?', r'streamlining', r'streamlined', r'simplif[y|ies|ying|ied]',
      r'reduces? time', r'saves? time', r'saving a lot of time', r'significant time']),
    ('collaboration',
     [r'collaborative safety platform', r'real-time collaboration', r'enhanced collaboration',
      r'work as one team, one system', r'within the workflow', r'workflow in veeva safety',
      r'back and forth communication', r'communication outside the system']),
    ('efficiency improvements',
     [r'operational efficiencies', r'improving efficiency', r'faster case processing',
      r'case processing efficiency', r'improves? efficiency', r'operational efficiency',
      r'do more with less', r'drives case processing efficiency']),
    ('data quality',
     [r'increase data quality', r'data quality and accessibility',
      r'high-quality patient-centered', r'patient-centered pharmacovigilance services',
      r'tell the patient\'s story', r'clinical expertise to craft meaningful narratives']),
    ('control / oversight',
     [r'gain control', r'oversee and control your data', r'direct oversight and control',
      r'direct oversight', r'control and real-time visibility',
      r'oversight and compliance', r'better oversight']),
    ('validated / future-proof',
     [r'validated releases 3 times per year', r'validated safety solution in weeks',
      r'validated safety solution', r'future proof', r'future-proof',
      r'keep up with new regulations', r'regulatory requirements']),
    ('scalability',
     [r'establish foundation for scalability', r'for scalability', r'scalable']),
    ('intuitive / easy to use',
     [r'intuitive and easy to use', r'intuitive', r'easy to use', r'easily present', r'intuitively']),
    ('end-to-end',
     [r'end-to-end management of safety processes', r'end-to-end solution',
      r'intake to case processing', r'from intake to case processing',
      r'case processing to reporting and submissions']),
    ('standardization / unified data model',
     [r'standardize terminology', r'standardized', r'common data model',
      r'single source of truth', r'data model']),
    ('dashboards & analytics',
     [r'dashboards and reports', r'flexible reports and dashboards', r'operational reporting',
      r'reporting and analytics', r'reporting tool', r'advanced reporting',
      r'real-time analytics', r'drill into the data', r'transform data into action']),
    ('case processing',
     [r'case processing', r'case processors?', r'process a case',
      r'how long it takes to process a case', r'faster more efficient case processing']),
    ('regulatory submissions',
     [r'communicates? to health authorities', r'health authorities', r'submissions',
      r'seamless submissions', r'reporting and submissions', r'global submissions',
      r'compliance', r'better oversight and compliance']),
    ('patient safety',
     [r'improve patient safety', r'patient safety is irreplaceable',
      r'tell the patient\'s story', r'patient-centered']),
    ('cloud-based',
     [r'single cloud platform', r'cloud-based safety solution', r'cloud native', r'saas']),
    ('rapid deployment',
     [r'rapidly configure and deploy', r'rapid configuration', r'rapid deployment',
      r'deploy new studies and projects in veeva safety', r'configure and deploy']),
    ('cost reduction',
     [r'reduce clinical trial costs', r'reduces? risk and overhead', r'reduce costs',
      r'overhead', r'resources to focus on innovation']),
]

# 把 raw 文本拆成段落，判断哪些段落是 testimonial（引号 / 人名 + 职位）
paragraphs = re.split(r'\n\s*\n', raw)
paragraphs = [p.strip() for p in paragraphs if p.strip() and not p.strip().startswith('#')]

freq = Counter()
for p in paragraphs:
    # 判断是否 testimonial 引述（加权 1.5）
    is_quote = ('testimonial' in p.lower()
                or 'director' in p.lower() or 'manager' in p.lower()
                or 'head of' in p.lower() or 'senior' in p.lower()
                or 'paysages:'.encode().decode('ascii','ignore') in p.lower()
                or 'involving sponsors' in p.lower()
                or 'with veeva safety, i don' in p.lower()
                or 'real-time dashboards' in p.lower()
                or 'veeva safety beats a lot' in p.lower()
                or 'linical testimonial' in p.lower()
                or 'another testimonial' in p.lower()
                or 'another cro testimonial' in p.lower())
    weight = 1.5 if is_quote else 1.0

    for canonical, patterns in canonical_variants:
        for pat in patterns:
            matches = re.findall(pat, p, flags=re.IGNORECASE)
            if matches:
                freq[canonical] += len(matches) * weight
                break  # 一个段落里同一个 canonical 最多加一次权重

# 过滤权重 < 1 的（没命中任何 variant 的 canonical 不保留）
freq = Counter({k: v for k, v in freq.items() if v >= 1})

print("Top sell-point keywords (weighted, real quote ×1.5):")
for k, v in freq.most_common():
    print(f"  {v:5.1f}  {k}")

# ---------- Step 3: 词云 ----------
NAVY = (22, 44, 92)
CREAM = (243, 236, 216)
ACCENT = (206, 80, 52)
GRAY = (95, 99, 104)

# 把 canonical 的长标签换成更好看的短标签（词云宽度有限）
label_map = {
    'real-time access / visibility': 'real-time',
    'seamless integration': 'seamless integration',
    'control / oversight': 'control & oversight',
    'validated / future-proof': 'validated & future-proof',
    'intuitive / easy to use': 'intuitive & easy-to-use',
    'standardization / unified data model': 'standardization & data model',
    'dashboards & analytics': 'dashboards & analytics',
    'efficiency improvements': 'efficiency gains',
    'collaboration': 'collaboration',
    'automation': 'automation',
    'unified / single platform': 'single unified platform',
    'streamline operations': 'streamlined ops',
    'data quality': 'data quality',
    'end-to-end': 'end-to-end',
    'case processing': 'case processing',
    'scalability': 'scalability',
    'regulatory submissions': 'regulatory compliance',
    'patient safety': 'patient safety',
    'cloud-based': 'cloud native',
    'rapid deployment': 'rapid deployment',
    'cost reduction': 'cost reduction',
}

final_freq = Counter()
for k, v in freq.items():
    label = label_map.get(k, k)
    final_freq[label] += v

# real-time 再额外 +1.0 作为用户点名强调
final_freq['real-time'] = final_freq.get('real-time', 0) + 2.0

print("\nFinal labels for word cloud:")
for k, v in final_freq.most_common():
    print(f"  {v:5.1f}  {k}")

def color_func(word=None, font_size=None, position=None, orientation=None,
                font_path=None, random_state=None):
    if random_state is None:
        random_state = np.random.RandomState()
    w = word.lower()
    # real-time → 最强橙色
    if 'real' in w and 'time' in w:
        return ACCENT
    # 高频 → 橙色
    if font_size > 70:
        return ACCENT
    # 中频 → 深蓝主色
    if font_size > 40:
        return NAVY
    # 低频 → 深灰
    return GRAY

FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'

wc = WordCloud(
    width=1600,
    height=900,
    background_color='white',
    max_words=60,
    prefer_horizontal=0.62,
    collocations=False,
    color_func=color_func,
    min_font_size=14,
    max_font_size=140,
    margin=16,
    random_state=42,
    scale=2,
    font_path=FONT,
)
wc.generate_from_frequencies(final_freq)
out = '/workspace/Veeva_Safety_产品卖点词云.png'
wc.to_file(out)
print(f"\nsaved {out}  ({len(final_freq)} labels)")
