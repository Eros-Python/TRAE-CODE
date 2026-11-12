"""Veeva 发展脉络 v3.1 —— 所有主事件放上方，下方完全留给 Impact 框"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

NAVY = '#162C5C'
ACCENT = '#CE5034'
GRAY = '#5F6368'
MILESTONE = '#8B4513'
WHITE = '#FFFFFF'

# (idx, 年份, 主色, 主标题, 副标题)
events = [
    (0,  '2007', GRAY,      '公司成立',                       'Vault CRM 同年上线\nPeter Gassner + Matt Wallach'),
    (1,  '2010', GRAY,      'Vault CRM 美国市占第一',         '启动 Vault 第二条产品线'),
    (2,  '2011', GRAY,      'Veeva Vault 上线 · 进入中国',    '上海总部'),
    (3,  '2013', MILESTONE, '纽交所上市 VEEV',                 None),
    (4,  '2019', NAVY,      'Veeva Safety Suite 发布\nVault Safety.AI（NLP）', None),
    (5,  '2021', MILESTONE, '全球首家上市公司转 PBC',          None),
    (6,  '2022', NAVY,      '22R3 Safety 数据模型大改版',      None),
    (7,  '2023', NAVY,      'Safety Suite 分析层补全',          None),
    (8,  '2025', ACCENT,    'Veeva AI Agent 嵌入\nSafety 合规工作流', None),
    (9,  '2026', MILESTONE, 'UCB 全球 Safety 全面迁移',         None),
]

fig, ax = plt.subplots(figsize=(20, 10))
n = len(events)
ax.set_xlim(-0.6, n - 0.2)
ax.set_ylim(-1.5, 11)
ax.set_aspect('auto')

# 时间轴
timeline_y = 6.8
ax.axhline(y=timeline_y, xmin=0.02, xmax=0.98, color=NAVY, linewidth=5, zorder=1)

# 年份刻度
for idx, yr, *_ in events:
    ax.axvline(x=idx, ymin=0.43, ymax=0.57, color=NAVY, linewidth=2, zorder=2)
    ax.text(idx, timeline_y - 0.55, yr, ha='center', va='top',
            fontsize=12, fontweight='bold', color=NAVY)

# ---------- 节点布局：严格上下交替 ----------
# 10 个事件：0下 1上 2下 3上 4下 5上 6下 7上 8下 9上
# 这样里程碑也自然错开
upper = {1, 3, 5, 7, 9}   # 上：2010市占第一 / 2013上市 / 2021 PBC / 2023 Suite补全 / 2026 UCB
lower = {0, 2, 4, 6, 8}   # 下：2007成立 / 2011进中国 / 2019 Suite+NLP / 2022 22R3 / 2025 AI Agent

for idx, yr, color, title, sub in events:
    # 节点大小
    if color == MILESTONE: dot_size = 340
    elif color == NAVY:    dot_size = 260
    elif color == ACCENT:  dot_size = 300
    else:                  dot_size = 160

    ax.scatter(idx, timeline_y, s=dot_size, color=color, zorder=5,
               edgecolors=WHITE, linewidths=2.5)
    if color == MILESTONE:
        ax.scatter(idx, timeline_y, s=70, color='gold', marker='*', zorder=6)

    is_upper = idx in upper
    dir_sign = 1 if is_upper else -1
    base_y = timeline_y + dir_sign * (2.0 if is_upper else 1.8)

    # 连接线
    conn_y = timeline_y + dir_sign * 0.85
    ax.plot([idx, idx], [timeline_y + dir_sign * 0.28, conn_y],
            color=color, lw=1.5, zorder=3)
    ax.plot([idx, idx], [conn_y, base_y + dir_sign * 0.12],
            color=color, lw=1.5, zorder=3)

    # 主标题
    ax.text(idx, base_y, title, ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=color,
            bbox=dict(boxstyle='round,pad=0.38', facecolor=WHITE, edgecolor=color,
                      alpha=0.95, linewidth=1.3))

    # 下方公司事件自己的副标题
    if sub and not is_upper:
        ax.text(idx, base_y + dir_sign * 0.95, sub,
                ha='center', va='center', fontsize=7.5, color=GRAY, style='italic',
                multialignment='center')

# ---------- 右下角 Impact 框 ----------
# 完全在 timeline 下方（y: 0.0 ~ 3.8），不和任何下方节点冲突（只有 idx 0,1,2 有下方内容）
right_box_x = n - 0.15
right_box_y = 0.0
right_box_w = 4.6
right_box_h = 3.6

# 框在画布右边区域（x 从 5.25 到 9.85），避开 idx 0,1,2 下方区域（x=0~2）
right_box = FancyBboxPatch(
    (right_box_x - right_box_w, right_box_y),
    right_box_w, right_box_h,
    boxstyle='round,pad=0.15',
    facecolor='#F5F7FB', edgecolor=NAVY, linewidth=1.5, alpha=0.98, zorder=4
)
ax.add_patch(right_box)

ax.text(right_box_x - right_box_w / 2, right_box_y + right_box_h - 0.22,
        '关键 Impact（2013–2026）',
        ha='center', va='center', fontsize=11, fontweight='bold', color=NAVY)

impact_lines = [
    ('★', '2013', '纽交所上市 VEEV · 市值 $13B（2023）'),
    ('●', '2019', 'Safety Suite 发布 + NLP AI\nSafety + SafetyDocs 同 Vault 数据模型 · 客户 51–100'),
    ('★', '2021', '全球首家上市公司转 PBC · 重新定义公司目的'),
    ('●', '2022', '22R3 数据模型大改版：\nCase Promotion 打通 API · OTC 品类 · 重复 Case 智能检测 · 分两批 Rollout'),
    ('●', '2023', 'Suite 分析层补全：\nWorkbench（Redshift 每日 Reload）+ Signal（FAERS/VAERS 同步）'),
    ('▲', '2025', 'AI Agent 嵌入合规工作流：\nCase Intake / Narrative / Chat · 有 Safeguards · 10 月全产品线'),
    ('★', '2026', 'UCB 全球 Safety 全面迁移（最大单一客户迁移案）'),
]

bullet_colors = {'●': NAVY, '★': MILESTONE, '▲': ACCENT}
impact_start_y = right_box_y + right_box_h - 0.55
line_spacing = 0.46

for i, (bullet, yr, text) in enumerate(impact_lines):
    y = impact_start_y - i * line_spacing
    col = bullet_colors.get(bullet, GRAY)
    ax.text(right_box_x - right_box_w + 0.2, y, f'{bullet} {yr}',
            ha='left', va='center', fontsize=8.5, fontweight='bold', color=col)
    ax.text(right_box_x - right_box_w + 1.05, y, text,
            ha='left', va='center', fontsize=8, color=GRAY,
            multialignment='left', linespacing=1.28)

# ---------- 标题 + 图例 ----------
ax.text(0.5, 0.975, 'Veeva 发展脉络 · 突出 Safety 与 AI 节点（精简版）',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=20, fontweight='bold', color=NAVY)

legend_elements = [
    mpatches.Patch(facecolor=NAVY, label='Safety 里程碑'),
    mpatches.Patch(facecolor=ACCENT, label='AI 里程碑'),
    mpatches.Patch(facecolor=MILESTONE, label='关键里程碑（★）'),
    mpatches.Patch(facecolor=GRAY, label='公司常规事件'),
]
legend = ax.legend(handles=legend_elements, loc='lower left', fontsize=11,
                  frameon=True, facecolor=WHITE, edgecolor=NAVY,
                  framealpha=0.95, ncol=2)

ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

plt.tight_layout(pad=2.5)
out = '/workspace/Veeva发展脉络_v3_紧凑版.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=WHITE)
print(f'saved {out}')
