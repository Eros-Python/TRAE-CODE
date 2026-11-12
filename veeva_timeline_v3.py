"""Veeva 发展脉络 v3.2 —— Impact 框在 timeline 下方节点之下，彻底不重叠"""

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

# ---------- 画布 ----------
fig, ax = plt.subplots(figsize=(22, 13))
n = len(events)

# 画布分区：
#   y: 10.5 ~ 13.5  标题区
#   y:  8.5            timeline 上方
#   y:  7.2            timeline_y
#   y:  4.5 ~ 6.0      timeline 下方节点标题区（不会低于 y=4.0）
#   y: -3.0 ~  3.5     Impact 框区
ax.set_xlim(-0.7, n - 0.1)
ax.set_ylim(-4.8, 13.8)   # 底部再放 0.3，框底完整可见
ax.set_aspect('auto')

# ---------- 时间轴 ----------
timeline_y = 7.2
ax.axhline(y=timeline_y, xmin=0.02, xmax=0.98, color=NAVY, linewidth=5, zorder=1)

# ---------- 年份文字（不带垂直竖线） ----------
for idx, yr, *_ in events:
    ax.text(idx, timeline_y - 0.55, yr, ha='center', va='top',
            fontsize=12, fontweight='bold', color=NAVY)

# ---------- 节点布局：严格上下交替 ----------
upper = {1, 3, 5, 7, 9}   # 上：2010/2013/2021/2023/2026
lower = {0, 2, 4, 6, 8}   # 下：2007/2011/2019/2022/2025

label_dist = 2.5   # 标签离时间轴距离

for idx, yr, color, title, sub in events:
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
    base_y = timeline_y + dir_sign * label_dist

    # 只有一段连接线：标签 → 节点
    # 标签框边缘（大概 base_y ± 0.5）→ 节点边缘（timeline_y ± 0.2）
    label_edge_y = base_y - dir_sign * 0.50
    node_edge_y  = timeline_y + dir_sign * 0.2
    ax.plot([idx, idx], [label_edge_y, node_edge_y],
            color=color, lw=1.6, zorder=3)

    # 主标题（带白框）
    ax.text(idx, base_y, title, ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=color,
            bbox=dict(boxstyle='round,pad=0.40', facecolor=WHITE, edgecolor=color,
                      alpha=0.96, linewidth=1.3))

    # 下方公司事件（2013 前）自己的副标题
    if sub and not is_upper:
        ax.text(idx, base_y + dir_sign * 0.95, sub,
                ha='center', va='center', fontsize=7.8, color=GRAY, style='italic',
                multialignment='center')

# ---------- Impact 框：整体下移 + 高度缩小 + 内容下移 ----------
box_w = 5.0
box_center_x = (ax.get_xlim()[0] + ax.get_xlim()[1]) / 2
right_box_left = box_center_x - box_w / 2
right_box_w = box_w
right_box_y = -4.2              # 框底不动
right_box_h = 6.2               # 高度从 5.8 → 6.2，多给空间放标题+间距

right_box = FancyBboxPatch(
    (right_box_left, right_box_y),
    right_box_w, right_box_h,
    boxstyle='round,pad=0.20',
    facecolor='#F5F7FB', edgecolor=NAVY, linewidth=1.6, alpha=0.98, zorder=4
)
ax.add_patch(right_box)

# 框标题 —— 框顶下 0.30
ax.text(right_box_left + right_box_w / 2, right_box_y + right_box_h - 0.30,
        '关键 Impact（2013–2026）',
        ha='center', va='center', fontsize=12, fontweight='bold', color=NAVY, zorder=5)

# 7 条 Impact
impact_lines = [
    ('★', '2013', '纽交所上市 VEEV · 市值 $13B（2023）'),
    ('●', '2019', 'Safety Suite 发布 + NLP AI\nSafety + SafetyDocs 同 Vault 数据模型 · 客户 51–100'),
    ('★', '2021', '全球首家上市公司转 PBC · 重新定义公司目的'),
    ('●', '2022', '22R3 数据模型大改版：\nCase Promotion 打通 API · OTC 品类支持\n重复 Case 智能检测 · 分两批 Rollout（量大罕见）'),
    ('●', '2023', 'Suite 分析层补全：\nWorkbench（Redshift 每日 Reload）\nSignal（FAERS/VAERS/EVDAS 每日同步）'),
    ('▲', '2025', 'AI Agent 嵌入合规工作流：\nCase Intake / Narrative / Chat · 有 Built-in Safeguards\n10 月全产品线铺开'),
    ('★', '2026', 'UCB 全球 Safety 全面迁移（目前最大单一客户迁移案）'),
]

bullet_colors = {'●': NAVY, '★': MILESTONE, '▲': ACCENT}
# 标题 0.30 + 间距 0.55 = 从框顶下 0.85 开始第一条 Impact
impact_start_y = right_box_y + right_box_h - 0.85
line_spacing = 0.70

for i, (bullet, yr, text) in enumerate(impact_lines):
    y = impact_start_y - i * line_spacing
    col = bullet_colors.get(bullet, GRAY)
    # 全部左对齐，字体加大
    ax.text(right_box_left + 0.25, y, f'{bullet} {yr}',
            ha='left', va='center', fontsize=10.5, fontweight='bold', color=col, zorder=6)
    ax.text(right_box_left + 1.35, y, text,
            ha='left', va='center', fontsize=10, color=GRAY,
            multialignment='left', linespacing=1.35, zorder=6)

# ---------- 标题 + 图例 ----------
ax.text(0.5, 0.975, 'Veeva 发展脉络 · 突出 Safety 与 AI 节点',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=22, fontweight='bold', color=NAVY)

legend_elements = [
    mpatches.Patch(facecolor=NAVY, label='Safety 里程碑'),
    mpatches.Patch(facecolor=ACCENT, label='AI 里程碑'),
    mpatches.Patch(facecolor=MILESTONE, label='关键里程碑（★）'),
    mpatches.Patch(facecolor=GRAY, label='公司常规事件'),
]
legend = ax.legend(handles=legend_elements, loc='lower left', fontsize=12,
                  frameon=True, facecolor=WHITE, edgecolor=NAVY,
                  framealpha=0.95, ncol=2)

# ---------- 清理坐标轴 ----------
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

# 不用 tight_layout，不用 bbox_inches='tight'，直接保存原画布区域
out = '/workspace/Veeva发展脉络_v3_紧凑版.png'
plt.savefig(out, dpi=160, facecolor=WHITE)
print(f'saved {out}')
