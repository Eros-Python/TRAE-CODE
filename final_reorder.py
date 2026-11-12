"""彻底重排 PPT：正确封面、删除重复时间线、时间线放 Veeva Signal 之后、致谢在末尾。"""
from pptx import Presentation
import re

PPT_PATH = '/workspace/PV数据库市场调研总结-20261111.pptx'

prs = Presentation(PPT_PATH)
sldIdLst = prs.slides._sldIdLst

print(f'当前 {len(prs.slides)} slides:')
for i, s in enumerate(prs.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:50]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else f'(shapes={len(s.shapes)})'
    print(f'  {i+1:2d}. {first}')

# ---------- 找到每个关键 slide ----------
cover_id = None          # PHARMARON 封面
thanks_id = None         # 致谢 shapes=0
veeva_signal_id = None   # Veeva Safety Signal（宣传图2）
timeline_ids = []        # 时间线图（可能有多张重复）

for i, s in enumerate(prs.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else ''
    
    sldId = sldIdLst[i]
    
    if 'PHARMARON' in first.upper() and cover_id is None:
        cover_id = sldId
    if len(s.shapes) == 0:
        thanks_id = sldId
    if 'Safety Signal' in first and '宣传图' in first:
        veeva_signal_id = sldId
    if '发展脉络' in first:
        timeline_ids.append(sldId)

print(f'\n找到: cover={cover_id is not None}, thanks={thanks_id is not None}, signal={veeva_signal_id is not None}, timelines={len(timeline_ids)}')

# ---------- 删掉重复的时间线图，只保留第一张 ----------
if len(timeline_ids) > 1:
    for tid in timeline_ids[1:]:
        sldIdLst.remove(tid)
        print(f'删掉重复时间线图')

# ---------- 重新排序 ----------
# 先全部拿出来，再按正确顺序放回去
current_order = list(sldIdLst)
sldIdLst.clear()

# 1. 封面在首位
if cover_id:
    sldIdLst.append(cover_id)
else:
    print('警告：没找到封面！')

# 2. 把除了封面、致谢、时间线之外的其他 slide 按原顺序放
timeline_id = timeline_ids[0] if timeline_ids else None
for sldId in current_order:
    if sldId in (cover_id, thanks_id, timeline_id):
        continue
    if sldId not in sldIdLst:
        sldIdLst.append(sldId)

# 3. 时间线图插到 Veeva Signal 之后
if timeline_id and veeva_signal_id:
    # 找到 Veeva Signal 现在的位置
    signal_idx = None
    for i, sid in enumerate(sldIdLst):
        if sid == veeva_signal_id:
            signal_idx = i
            break
    if signal_idx is not None:
        sldIdLst.insert(signal_idx + 1, timeline_id)
        print(f'时间线图插在 Veeva Signal（索引 {signal_idx}）之后')

# 4. 致谢在末尾
if thanks_id:
    if thanks_id in sldIdLst:
        sldIdLst.remove(thanks_id)
    sldIdLst.append(thanks_id)

# ---------- 更新页码 ----------
TOTAL = len(sldIdLst)
for slide in prs.slides:
    for shape in slide.shapes:
        if not hasattr(shape, 'has_text_frame') or not shape.has_text_frame:
            continue
        tf = shape.text_frame
        for para in tf.paragraphs:
            for run in para.runs:
                new_text = re.sub(r'(\d+)\s*/\s*\d+\b',
                                  lambda m: f'{m.group(1)} / {TOTAL}',
                                  run.text)
                if new_text != run.text:
                    run.text = new_text

prs.save(PPT_PATH)

print(f'\n最终 {TOTAL} slides:')
for i, s in enumerate(prs.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:55]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else f'(shapes={len(s.shapes)})'
    marker = ' ★' if '发展脉络' in first else ''
    print(f'  {i+1:2d}. {first}{marker}')
