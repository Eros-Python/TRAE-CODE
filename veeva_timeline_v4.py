"""Veeva 发展脉络 v4 —— 彻底分离：
- 紧凑时间轴在左，Impact 框独立在右下（不覆盖时间轴下方区域）
- 2019 前保留节点各自小字
- 2019 后 Impact 收在右下独立框，用 2 列网格排布省空间
"""

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

# ---------- 事件 ----------
events = [
    (0,  '2007', GRAY,      '公司成立',
     'Vault CRM 同年上线\nPeter Gassner + Matt Wallach'),
    (1,  '2010', GRAY,      'Vault CRM 美国市占第一',
     '启动 Vault 第二条产品线'),
    (2,  '2011', GRAY,      'Veeva Vault 上线 · 进入中国',
     '上海总部'),
    (3,  '2013', MILESTONE, '纽交所上市 VEEV',
     '市值 $13B（2023）'),
    (4,  '2019', NAVY,      'Veeva Safety Suite 发布\nVault Safety.AI（NLP）',
     None),
    (5,  '2021', MILESTONE, '全球首家上市公司转 PBC',
     None),
    (6,  '2022', NAVY,      '22R3 Safety 数据模型大改版',
     None),
    (7,  '2023', NAVY,      'Safety Suite 分析层补全',
     None),
    (8,  '2025', ACCENT,    'Veeva AI Agent 嵌入\nSafety 合规工作流',
     None),
    (9,  '2026', MILESTONE, 'UCB 全球 Safety 全面迁移',
     None),
]

# ---------- 画布 ----------
fig, ax = plt.subplots(figsize=(20, 9))

n = len(events)
# x 轴给 Impact 框留右边独立区域（n-1 到 n+2 是 Impact 框区域）
ax.set_xlim(-0.6, n + 2.5)
ax.set_ylim(-1.5, 8.5)
ax.set_aspect('auto')

# ---------- 紧凑时间轴线（只覆盖到 n-0.5，不延伸到 Impact 框区） ----------
timeline_y = 4.2
ax.axhline(y=timeline_y, xmin=0.015, xmax=0.74, color=NAVY, linewidth=5, zorder=1)

# ---------- 年份刻度 ----------
for idx, yr, *_ in events:
    # 只给时间轴区域画刻度
    ax.axvline(x=idx, ymin=0.43, ymax=0.57, color=NAVY, linewidth=2, zorder=2)
    ax.text(idx, timeline_y - 0.55, yr, ha='center', va='top',
            fontsize=12, fontweight='bold', color=NAVY)

# ---------- 事件节点 ----------
upper_nodes = {4, 6, 8}
lower_nodes = {0, 1, 2, 3, 5, 7, 9}

for idx, yr, color, title, sub in events:
    if color == MILESTONE:
        dot_size = 320
    elif color == NAVY:
        dot_size = 240
    elif color == ACCENT:
        dot_size = 280
    else:
        dot_size = 140

    ax.scatter(idx, timeline_y, s=dot_size, color=color, zorder=5,
               edgecolors=WHITE, linewidths=2.5)
    if color == MILESTONE:
        ax.scatter(idx, timeline_y, s=60, color='gold', marker='*', zorder=6)

    is_upper = idx in upper_nodes
    label_base_y = timeline_y + 1.6 if is_upper else timeline_y - 1.6
    dir_sign = 1 if is_upper else -1

    # 连接线
    connector_y = timeline_y + dir_sign * 0.7
    ax.plot([idx, idx], [timeline_y + dir_sign * 0.25, connector_y],
            color=color, lw=1.5, zorder=3)
    ax.plot([idx, idx], [connector_y, label_base_y + dir_sign * 0.1],
            color=color, lw=1.5, zorder=3)

    # 主标题
    ax.text(idx, label_base_y, title, ha='center', va='center',
            fontsize=10, fontweight='bold', color=color,
            bbox=dict(boxstyle='round,pad=0.35', facecolor=WHITE, edgecolor=color,
                      alpha=0.95, linewidth=1.3))

    # 2013 前的小字（各自独立）
    if sub and idx <= 3:
        sub_y = label_base_y + dir_sign * 0.9
        ax.text(idx, sub_y, sub, ha='center', va='center',
                fontsize=7.2, color=GRAY, style='italic', multialignment='center')

# ---------- Impact 框（独立在画布右侧，不覆盖时间轴） ----------
# 位置：右边独立区域，y 在 timeline 下方区域
impact_box_x = n - 0.2      # 左边缘（从时间轴右端开始）
impact_box_y = 1.8
impact_box_w = 2.6
impact_box_h = 4.5

right_box = FancyBboxPatch(
    (impact_box_x, impact_box_y),
    impact_box_w, impact_box_h,
    boxstyle='round,pad=0.15',
    facecolor='#F5F7FB', edgecolor=NAVY, linewidth=1.5, alpha=0.98, zorder=4
)
ax.add_patch(right_box)

# 框标题
ax.text(impact_box_x + impact_box_w / 2, impact_box_y + impact_box_h - 0.25,
        '2019+ Impact',
        ha='center', va='center', fontsize=11, fontweight='bold', color=NAVY)
# 副标题说明
ax.text(impact_box_x + impact_box_w / 2, impact_box_y + impact_box_h - 0.55,
        '（各节点详细信息）',
        ha='center', va='center', fontsize=7.5, color=GRAY, style='italic')

# Impact 条目（上下堆叠）
impact_items = [
    ('●', '2019', 'Safety Suite 发布\nSafety + SafetyDocs 同 Vault 数据模型\nNLP 自动 Case Intake（Vault Safety.AI）', NAVY),
    ('★', '2021', '全球首家上市公司转 PBC\n法律上从"只为股东"\n改成"为所有利益相关方"', MILESTONE),
    ('●', '2022', '22R3 数据模型大改版\nCase Promotion 打通 API\nOTC 品类支持 · 重复 Case 智能检测', NAVY),
    ('●', '2023', 'Suite 分析层补全\nWorkbench（Redshift 每日 Reload）\n+ Signal（FAERS/VAERS/EVDAS 每日同步）', NAVY),
    ('▲', '2025', 'AI Agent 嵌入合规工作流\nCase Intake / Narrative / AI Chat\n有 Built-in Safeguards', ACCENT),
    ('★', '2026', 'UCB 全球 Safety 全面迁移\n目前最大单一客户迁移案', MILESTONE),
]

item_start_y = impact_box_y + impact_box_h - 0.85
item_spacing = 0.62

for i, (bullet, yr, text, col) in enumerate(impact_items):
    y = item_start_y - i * item_spacing
    # Bullet + 年份
    ax.text(impact_box_x + 0.2, y, f'{bullet} {yr}',
            ha='left', va='top', fontsize=8, fontweight='bold', color=col)
    # 正文
    ax.text(impact_box_x + 0.9, y - 0.08, text,
            ha='left', va='top', fontsize=6.5, color=GRAY, multialignment='left',
            linespacing=1.25)

# ---------- 标题 ----------
ax.text(0.37, 0.975, 'Veeva 发展脉络 · 突出 Safety 与 AI 节点（精简版）',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=20, fontweight='bold', color=NAVY)

# ---------- 图例（在右下 Impact 框下方） ----------
legend_elements = [
    mpatches.Patch(facecolor=NAVY, label='Safety 里程碑'),
    mpatches.Patch(facecolor=ACCENT, label='AI 里程碑'),
    mpatches.Patch(facecolor=MILESTONE, label='关键里程碑（★）'),
    mpatches.Patch(facecolor=GRAY, label='公司常规事件'),
]
legend = ax.legend(handles=legend_elements, loc='lower right', fontsize=10,
                  frameon=True, facecolor=WHITE, edgecolor=NAVY,
                  framealpha=0.95, ncol=1,
                  bbox_to_anchor=(0.985, 0.02))

# ---------- 清理坐标轴 ----------
ax.set_yticks([])
ax.set_xticks([e[0] for e in events])
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

plt.tight_layout(pad=2.0)
out = '/workspace/Veeva发展脉络_v4_紧凑版.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=WHITE)
print(f'saved {out}')
