"""Veeva 发展脉络图 —— 突出 Safety 与 AI 时间节点。"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
from matplotlib.dates import date2num
import numpy as np
from datetime import date

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ---------- 颜色 ----------
NAVY = '#162C5C'
ACCENT = '#CE5034'
GRAY = '#5F6368'
MILESTONE = '#8B4513'  # 棕
WHITE = '#FFFFFF'

# ---------- 事件 ----------
events = [
    (date(2007, 1, 1), 'company', '公司成立', 'Peter Gassner + Matt Wallach · Vault CRM 同年上线'),
    (date(2010, 1, 1), 'company', 'Vault CRM 美国市占第一', '启动 Vault 第二条产品线'),
    (date(2011, 1, 1), 'company', 'Veeva Vault 上线 · 进入中国', '上海总部'),
    (date(2013, 1, 1), 'milestone', '纽交所上市 VEEV', '市值 $13B（2023）'),
    (date(2018, 1, 1), 'safety', 'Vault Safety Datasheet 发布', '"唯一现代的 Adverse Event 管理应用"'),
    (date(2019, 8, 13), 'ai', 'Vault Safety.AI 发布', 'NLP 自动 Case Intake'),
    (date(2019, 1, 1), 'safety', 'Veeva Safety Suite 整体 Announced', 'Safety + SafetyDocs · 同 Vault 数据模型 · 客户 51–100'),
    (date(2021, 2, 1), 'milestone', '全球首家上市公司转 PBC', 'Public Benefit Corporation'),
    (date(2022, 11, 1), 'safety', '22R3 Safety 数据模型大改', 'MedDRA 新版 · 数据结构现代化'),
    (date(2023, 7, 1), 'safety', 'Safety Workbench 上线', 'Amazon Redshift · 每日全量 reload · 实施 3 个月'),
    (date(2023, 7, 1), 'safety', 'Safety Signal 上线', 'FAERS/VAERS/EVDAS 每日同步'),
    (date(2023, 8, 17), 'safety', '23R2 Release', 'Vault Release Notes'),
    (date(2025, 1, 1), 'ai', 'Veeva AI for Safety', 'Case Intake Agent · Case Narrative Agent · Veeva AI Chat'),
    (date(2025, 10, 14), 'ai', 'Vault AI Agents 全产品线铺开', 'Falcon + Vault AI · 2026 R&D 全栈'),
    (date(2026, 3, 1), 'safety', 'Safety-EDC Connection', 'Clinical SAE 双向同步至 Safety'),
    (date(2026, 6, 9), 'milestone', 'UCB 全球 Safety 全面迁移', 'Cory Gilbert / Adrian Maynier 具名引述'),
]

events.sort(key=lambda e: e[0])

# ---------- 画布 ----------
fig, ax = plt.subplots(figsize=(24, 14))

x_start = date2num(date(2006, 10, 1))
x_end = date2num(date(2027, 3, 1))
ax.set_xlim(x_start, x_end)
ax.set_ylim(-1, 14)
ax.set_aspect('auto')

# ---------- 时间轴线 ----------
timeline_y = 6.2
ax.axhline(y=timeline_y, xmin=0.01, xmax=0.99, color=NAVY, linewidth=5, zorder=1)

# ---------- 年份刻度 ----------
for yr in range(2007, 2027):
    x = date2num(date(yr, 1, 1))
    ax.axvline(x=x, ymin=0.45, ymax=0.55, color=NAVY, linewidth=1.5, zorder=2)
    ax.text(x, timeline_y - 0.7, str(yr), ha='center', va='top',
            fontsize=11, fontweight='bold', color=NAVY)

# ---------- 事件节点 ----------
side = 0  # 0=上, 1=下
prev_dn = None

for i, (d, etype, title, sub) in enumerate(events):
    dn = date2num(d)

    # 颜色
    if etype == 'safety':
        color = NAVY
        dot_size = 180
    elif etype == 'ai':
        color = ACCENT
        dot_size = 220
    elif etype == 'milestone':
        color = MILESTONE
        dot_size = 260
    else:
        color = GRAY
        dot_size = 80

    # 节点圆点
    ax.scatter(dn, timeline_y, s=dot_size, color=color, zorder=5,
               edgecolors=WHITE, linewidths=2)

    # 大事件加星号
    if etype == 'milestone':
        ax.scatter(dn, timeline_y, s=50, color='gold', marker='*', zorder=6)

    # 位置：交替上下
    if side == 0:
        label_base_y = timeline_y + 2.2
        dir_sign = 1
    else:
        label_base_y = timeline_y - 2.2
        dir_sign = -1

    # 垂直连接线
    connector_y = timeline_y + dir_sign * 1.0
    ax.plot([dn, dn], [timeline_y + dir_sign * 0.25, connector_y],
            color=color, lw=1.5, zorder=3)
    ax.plot([dn, dn], [connector_y, label_base_y + dir_sign * 0.2],
            color=color, lw=1.5, zorder=3)

    # 日期
    date_str = d.strftime('%Y.%m') if d.month > 1 else d.strftime('%Y')
    date_y = label_base_y + dir_sign * 0.55
    ax.text(dn, date_y, date_str, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color=color)

    # 标题（带白色底框）
    title_y = label_base_y
    ax.text(dn, title_y, title, ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=color,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=WHITE, edgecolor=color,
                      alpha=0.95, linewidth=1.3, joinstyle='miter'))

    # 副标题
    if sub:
        sub_y = label_base_y + dir_sign * 0.7
        ax.text(dn, sub_y, sub, ha='center', va='center',
                fontsize=7.8, color=GRAY, style='italic')

    # 切换方向
    if prev_dn and (dn - prev_dn) < 400:
        side = 1 - side
    else:
        side = 1 - side
    prev_dn = dn

# ---------- 标题 ----------
ax.text(0.5, 0.975, 'Veeva 发展脉络（2007–2026）· 突出 Safety 与 AI 时间节点',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=22, fontweight='bold', color=NAVY)
ax.text(0.5, 0.948,
        'Pantheon 产品卡 + 官方新闻稿 + Vault Release Notes 交叉验证    |    NAVY=Safety · ORANGE=AI · BROWN=Milestone · GRAY=常规',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=10, color=GRAY)

# ---------- 图例 ----------
legend_elements = [
    mpatches.Patch(facecolor=NAVY, label='Safety 里程碑'),
    mpatches.Patch(facecolor=ACCENT, label='AI 里程碑'),
    mpatches.Patch(facecolor=MILESTONE, label='关键里程碑（★ 标记）'),
    mpatches.Patch(facecolor=GRAY, label='公司常规事件'),
]
legend = ax.legend(handles=legend_elements, loc='lower right', fontsize=11,
                  frameon=True, facecolor=WHITE, edgecolor=NAVY,
                  framealpha=0.95, ncol=2)

# ---------- 清理 ----------
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
for label in ax.get_xticklabels():
    label.set_fontsize(10)

plt.tight_layout(pad=2.5)
out = '/workspace/Veeva发展脉络_Safety与AI时间线.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=WHITE)
print(f'saved {out}')
