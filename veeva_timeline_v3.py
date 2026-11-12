"""Veeva 发展脉络 v3 —— 按用户要求：
- 10 事件紧凑等距，不限年份间隔，只体现前后关系
- 2013 年前保留各节点自己的小字副标题
- 2019 年后所有小字收在右下角一个统一框里，避免重叠
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

# ---------- 事件（紧凑等距，用整数 idx 作 x 轴） ----------
# (idx, 年份, 主色, 主标题, 副标题_2019后统一右下)
events = [
    (0,  '2007', GRAY,      '公司成立',                    'Vault CRM 同年上线\nPeter Gassner + Matt Wallach'),
    (1,  '2010', GRAY,      'Vault CRM 美国市占第一',      '启动 Vault 第二条产品线'),
    (2,  '2011', GRAY,      'Veeva Vault 上线 · 进入中国', '上海总部'),
    (3,  '2013', MILESTONE, '纽交所上市 VEEV',              '市值 $13B（2023）'),
    (4,  '2019', NAVY,      'Veeva Safety Suite 发布\nVault Safety.AI（NLP）', None),
    (5,  '2021', MILESTONE, '全球首家上市公司转 PBC',       None),
    (6,  '2022', NAVY,      '22R3 Safety 数据模型大改版',   None),
    (7,  '2023', NAVY,      'Safety Suite 分析层补全',      None),
    (8,  '2025', ACCENT,    'Veeva AI Agent 嵌入\nSafety 合规工作流', None),
    (9,  '2026', MILESTONE, 'UCB 全球 Safety 全面迁移',    None),
]

# ---------- 画布（更紧凑） ----------
fig, ax = plt.subplots(figsize=(19, 8))

n = len(events)
ax.set_xlim(-0.6, n - 0.2)
ax.set_ylim(-1.5, 8)
ax.set_aspect('auto')

# ---------- 紧凑时间轴线 ----------
timeline_y = 4.2
ax.axhline(y=timeline_y, xmin=0.02, xmax=0.98, color=NAVY, linewidth=5, zorder=1)

# ---------- 年份刻度 ----------
for idx, yr, *_ in events:
    ax.axvline(x=idx, ymin=0.43, ymax=0.57, color=NAVY, linewidth=2, zorder=2)
    ax.text(idx, timeline_y - 0.55, yr, ha='center', va='top',
            fontsize=12, fontweight='bold', color=NAVY)

# ---------- 事件节点 ----------
# 交替上下，但因为紧凑，上放节点 + 主标题，下方留空间给 2013 前的小字
# 2019 后统一放上方，下方给右下副标题框让位

upper_nodes = {4, 6, 8}   # 2019/2022/2025 放上方
lower_nodes = {0, 1, 2, 3, 5, 7, 9}  # 2007/2010/2011/2013/2021/2023/2026 放下方

for idx, yr, color, title, sub in events:
    # 节点大小
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

    # 位置
    is_upper = idx in upper_nodes
    if is_upper:
        label_base_y = timeline_y + 1.6
        dir_sign = 1
    else:
        label_base_y = timeline_y - 1.6
        dir_sign = -1

    # 垂直连接线
    connector_y = timeline_y + dir_sign * 0.7
    ax.plot([idx, idx], [timeline_y + dir_sign * 0.25, connector_y],
            color=color, lw=1.5, zorder=3)
    ax.plot([idx, idx], [connector_y, label_base_y + dir_sign * 0.1],
            color=color, lw=1.5, zorder=3)

    # 主标题（带白框）
    title_wrapped = title
    ax.text(idx, label_base_y, title_wrapped, ha='center', va='center',
            fontsize=10, fontweight='bold', color=color,
            bbox=dict(boxstyle='round,pad=0.35', facecolor=WHITE, edgecolor=color,
                      alpha=0.95, linewidth=1.3))

    # 2013 前的小字副标题（各自独立）
    if sub and idx <= 3:
        sub_y = label_base_y + dir_sign * 0.9
        ax.text(idx, sub_y, sub, ha='center', va='center',
                fontsize=7.2, color=GRAY, style='italic',
                multialignment='center')

# ---------- 右下角统一框：2019 后所有事件的 Impact 小字 ----------
# 往上挪，避开 2023/2026 节点下方的区域
right_box_x = n - 0.30  # 右边缘（离画布右边留点边）
right_box_y = 2.0       # 往上挪到 timeline 下方区域中间
right_box_w = 4.5
right_box_h = 2.8

# 背景框
right_box = FancyBboxPatch(
    (right_box_x - right_box_w, right_box_y),
    right_box_w, right_box_h,
    boxstyle='round,pad=0.15',
    facecolor='#F5F7FB', edgecolor=NAVY, linewidth=1.5, alpha=0.98, zorder=4
)
ax.add_patch(right_box)

# 框标题
ax.text(right_box_x - right_box_w / 2, right_box_y + right_box_h - 0.22,
        '2019 后关键 Impact',
        ha='center', va='center', fontsize=10, fontweight='bold', color=NAVY)

# Impact 条目（带 bullet point）
impact_lines = [
    ('●', '2019', 'Safety Suite 发布（Safety + SafetyDocs 同 Vault 数据模型 · 客户 51–100）\nVault Safety.AI：NLP 自动 Case Intake'),
    ('★', '2021', '全球首家上市公司转 PBC · 法律上从"只为股东"改成"为所有利益相关方"'),
    ('●', '2022', '22R3 数据模型大改版：Case Promotion 打通 API、OTC 品类支持、\n重复 Case 智能检测 · 分两批 Rollout（量大罕见）'),
    ('●', '2023', 'Suite 分析层补全：Workbench（Redshift 每日 Reload）+ Signal\n（FAERS/VAERS/EVDAS 每日同步）· Suite 5 应用齐了'),
    ('▲', '2025', 'AI Agent 嵌入合规工作流：Case Intake / Narrative / AI Chat\n有 Built-in Safeguards · 10 月全产品线铺开'),
    ('★', '2026', 'UCB 全球 Safety 全面迁移（目前最大单一客户迁移案）'),
]

impact_start_y = right_box_y + right_box_h - 0.45
line_spacing = 0.42

bullet_colors = {
    '●': NAVY,
    '★': MILESTONE,
    '▲': ACCENT,
}

for i, (bullet, yr, text) in enumerate(impact_lines):
    y = impact_start_y - i * line_spacing
    col = bullet_colors.get(bullet, GRAY)
    # 年份 + bullet
    ax.text(right_box_x - right_box_w + 0.25, y, f'{bullet} {yr}',
            ha='left', va='center', fontsize=7.5, fontweight='bold', color=col)
    # 正文（用空格对齐，fontsize 更小）
    ax.text(right_box_x - right_box_w + 1.0, y, text,
            ha='left', va='center', fontsize=6.8, color=GRAY,
            multialignment='left', linespacing=1.25)

# ---------- 上方统一框：标题 + 图例 ----------
ax.text(0.5, 0.975, 'Veeva 发展脉络 · 突出 Safety 与 AI 节点（精简版）',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=20, fontweight='bold', color=NAVY)

# ---------- 图例 ----------
legend_elements = [
    mpatches.Patch(facecolor=NAVY, label='Safety 里程碑'),
    mpatches.Patch(facecolor=ACCENT, label='AI 里程碑'),
    mpatches.Patch(facecolor=MILESTONE, label='关键里程碑（★）'),
    mpatches.Patch(facecolor=GRAY, label='公司常规事件'),
]
legend = ax.legend(handles=legend_elements, loc='lower left', fontsize=10,
                  frameon=True, facecolor=WHITE, edgecolor=NAVY,
                  framealpha=0.95, ncol=2)

# ---------- 清理 ----------
ax.set_yticks([])
ax.set_xticks([e[0] for e in events])
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

plt.tight_layout(pad=2.0)
out = '/workspace/Veeva发展脉络_v3_紧凑版.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=WHITE)
print(f'saved {out}')
