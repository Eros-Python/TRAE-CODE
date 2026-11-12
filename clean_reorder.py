"""干净地重排 slide 顺序：
目标顺序（1-based）：
  1-19: 原内容（封面 → IQVIA 宣传图 2 张）
  20: 致谢空页（no text）—— 放在 IQVIA 宣传图之后
  21: Veeva Safety Suite 核心卖点提炼
  22: IQVIA Vigilance Platform 核心卖点提炼
  23: Veeva Safety 产品卖点词云
"""
from pptx import Presentation
from lxml import etree

PPT_PATH = '/workspace/PV数据库市场调研总结-20261111.pptx'
prs = Presentation(PPT_PATH)

print(f'当前 {len(prs.slides)} slides:')
for i, s in enumerate(prs.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:40]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else '(no text)'
    print(f'  [{i}] {first}')

# 目标顺序（0-based）
# 先找到关键 slide 的当前索引
target_names = [
    'IQVIA 官方宣传图：7 步骤 AI',  # slide 19 应该是最后一张 IQVIA 图
    '(no text)',                     # 致谢空页
    'Veeva Safety Suite 核心卖点',  # Veeva 卖点
    'IQVIA Vigilance Platform 核心卖点',  # IQVIA 卖点
    'Veeva Safety 产品卖点词云',    # 词云
]

key_indices = {}
for i, s in enumerate(prs.slides):
    all_text = ''
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            all_text += sh.text
    if 'IQVIA 官方宣传图' in all_text and '7 步骤' in all_text:
        key_indices['iqvia_img_2'] = i
    elif len(s.shapes) == 0:
        key_indices['thankyou'] = i
    elif 'Veeva Safety Suite 核心卖点提炼' in all_text:
        key_indices['veeva_sell'] = i
    elif 'IQVIA Vigilance Platform 核心卖点提炼' in all_text:
        key_indices['iqvia_sell'] = i
    elif 'Veeva Safety 产品卖点词云' in all_text:
        key_indices['veeva_wordcloud'] = i

print('\n关键 slide 当前索引:', key_indices)

# 目标顺序（0-based）：前 19 张不变 → Veeva 卖点 → IQVIA 卖点 → 词云 → 致谢（最后）
n = len(prs.slides)
desired = list(range(key_indices['iqvia_img_2'] + 1))  # 0-18 IQVIA 宣传图 2
desired.append(key_indices['veeva_sell'])
desired.append(key_indices['iqvia_sell'])
desired.append(key_indices['veeva_wordcloud'])
desired.append(key_indices['thankyou'])

# 重排
sldIdLst = prs.slides._sldIdLst
ordered = [sldIdLst[idx] for idx in desired]
# 清空 sldIdLst 重新加入
for child in list(sldIdLst):
    sldIdLst.remove(child)
for el in ordered:
    sldIdLst.append(el)

prs.save(PPT_PATH)

# 验证
prs2 = Presentation(PPT_PATH)
print(f'\n重排后 {len(prs2.slides)} slides:')
for i, s in enumerate(prs2.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:45]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else '(no text)'
    print(f'  {i+1:2d}. {first}')
