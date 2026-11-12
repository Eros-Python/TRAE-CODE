"""重排：Veeva 宣传图插到 IQVIA 宣传图之后。"""
from pptx import Presentation

PPT_PATH = '/workspace/PV数据库市场调研总结-20261111.pptx'
prs = Presentation(PPT_PATH)

def find_idx(keyword):
    for i, s in enumerate(prs.slides):
        all_text = ''
        for sh in s.shapes:
            if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
                all_text += sh.text
        if keyword in all_text:
            return i
    return None

idx_iqvia_img2 = find_idx('IQVIA 官方宣传图：7 步骤')
idx_veeva_img1 = find_idx('Veeva Vault Safety：实时')
idx_veeva_img2 = find_idx('Veeva Safety Signal：Detection')
idx_veeva_sell = find_idx('Veeva Safety Suite 核心卖点提炼')
idx_iqvia_sell = find_idx('IQVIA Vigilance Platform 核心卖点提炼')
idx_veeva_wc = find_idx('Veeva Safety 产品卖点词云')
idx_iqvia_wc = find_idx('IQVIA Vigilance Platform 产品卖点词云')
idx_thankyou = None
for i, s in enumerate(prs.slides):
    if len(s.shapes) == 0:
        idx_thankyou = i

print('关键索引:')
print(f'  IQVIA 宣传图2={idx_iqvia_img2}, Veeva宣传图1={idx_veeva_img1}, Veeva宣传图2={idx_veeva_img2}')
print(f'  Veeva卖点={idx_veeva_sell}, IQVIA卖点={idx_iqvia_sell}')
print(f'  Veeva词云={idx_veeva_wc}, IQVIA词云={idx_iqvia_wc}, 致谢={idx_thankyou}')

# 目标顺序
front = list(range(idx_iqvia_img2 + 1))  # 0..18
veeva_imgs = [idx_veeva_img1, idx_veeva_img2]
sell = [idx_veeva_sell, idx_iqvia_sell]
wc = [idx_veeva_wc, idx_iqvia_wc]
ty = [idx_thankyou]
desired = front + veeva_imgs + sell + wc + ty

print(f'\n目标顺序: {desired}')

sldIdLst = prs.slides._sldIdLst
ordered = [sldIdLst[idx] for idx in desired]
for child in list(sldIdLst):
    sldIdLst.remove(child)
for el in ordered:
    sldIdLst.append(el)

prs.save(PPT_PATH)

# 验证
prs2 = Presentation(PPT_PATH)
print(f'\n最终顺序 ({len(prs2.slides)}):')
for i, s in enumerate(prs2.slides):
    shapes_info = []
    for sh in s.shapes:
        if hasattr(sh, 'has_text_frame') and sh.has_text_frame:
            t = sh.text.strip()[:55]
            if t: shapes_info.append(t)
    first = shapes_info[0] if shapes_info else '(no text)'
    print(f'  {i+1:2d}. {first}')
