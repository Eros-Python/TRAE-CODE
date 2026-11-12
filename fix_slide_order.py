"""修正 slide 顺序：致谢页移到最后。

当前顺序（insert_iqvia_slides.py 之后）：
  [0-19] IQVIA 宣传图 + 之前的页
  [20] 致谢空页（no text, 0 shapes）
  [21] Veeva 卖点提炼
  [22] IQVIA 卖点提炼（新建的）
  [23] Veeva 词云

目标顺序：
  [0-19] IQVIA 宣传图 + 之前的页
  [21] Veeva 卖点提炼
  [22] IQVIA 卖点提炼
  [23] Veeva 词云
  [20] 致谢（最后）
"""
from pptx import Presentation
from lxml import etree
import re

PPT_PATH = '/workspace/PV数据库市场调研总结-20261111.pptx'
prs = Presentation(PPT_PATH)

print(f'before reorder: {len(prs.slides)} slides')
sldIdLst = prs.slides._sldIdLst

# 当前 slides 20 (0-based) 是致谢空页
# 移动到末尾
target = sldIdLst[20]
sldIdLst.remove(target)
sldIdLst.append(target)

prs.save(PPT_PATH)

# 重新打开，更新页码
prs2 = Presentation(PPT_PATH)
print(f'after reorder: {len(prs2.slides)} slides')

# 确认顺序
for i, s in enumerate(prs2.slides):
    titles = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()
            if t and len(t) < 80:
                titles.append(t)
    first = titles[0] if titles else '(no text)'
    print(f'  {i+1:2d}. {first}  |  {len(s.shapes)} shapes')

# 页码更新（总页数不变 23，只需要确认）
for slide in prs2.slides:
    for shape in slide.shapes:
        if not hasattr(shape, 'has_text_frame') or not shape.has_text_frame:
            continue
        tf = shape.text_frame
        for para in tf.paragraphs:
            for run in para.runs:
                # 把中间页码中的总页数确认
                pass

prs2.save(PPT_PATH)
print('\nsaved.')
