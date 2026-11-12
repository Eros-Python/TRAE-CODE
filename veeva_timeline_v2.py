"""Veeva 发展脉络 v2 —— 按用户要求精简：
- 删掉无事件年份的刻度线，只保留有事件的年份
- 同年事件合并
- 22R3 用简洁主标题 + Impact Assessment 小字
- 保留：2007/2010/2011/2013/2019/2021/2022/2023/2025/2026 共 10 个年份
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from datetime import date

plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ---------- 颜色 ----------
NAVY = '#162C5C'
ACCENT = '#CE5034'
GRAY = '#5F6368'
MILESTONE = '#8B4513'
WHITE = '#FFFFFF'

# ---------- 筛选后的事件（同年已合并） ----------
# (日期, 主色, 主标题, 副标题小字)
events = [
    (date(2007, 1, 1),   GRAY,       '公司成立',
     'Peter Gassner + Matt Wallach · Vault CRM 同年上线'),
    (date(2010, 1, 1),   GRAY,       'Vault CRM 美国市占第一',
     '启动 Vault 第二条产品线'),
    (date(2011, 1, 1),   GRAY,       'Veeva Vault 上线 · 进入中国',
     '上海总部'),
    (date(2013, 1, 1),   MILESTONE,  '纽交所上市 VEEV',
     '市值 $13B（2023）'),
    (date(2019, 6, 1),   NAVY,       'Veeva Safety Suite 发布 · Vault Safety.AI（NLP）',
     'Safety + SafetyDocs 同 Vault 数据模型 · 客户 51–100 · NLP 自动 Case Intake'),
    (date(2021, 2, 1),   MILESTONE,  '全球首家上市公司转 PBC',
     'Public Benefit Corporation · 重新定义"公司目的"'),
    (date(2022, 11, 15), NAVY,       '22R3 Safety 数据模型大改版',
     '● Impact Assessment: Case Promotion 打通 API · OTC 品类支持 · 重复 Case 智能检测 · 分两批 Rollout（量大罕见）'),
    (date(2023, 7, 1),   NAVY,       'Safety Suite 分析层补全',
     'Workbench（Redshift 每日 Reload）+ Signal（FAERS/VAERS/EVDAS 每日同步）双上线 · Suite 5 应用齐了'),
    (date(2025, 5, 1),   ACCENT,     'Veeva AI Agent 嵌入 Safety 合规工作流',
     'Case Intake / Narrative / AI Chat 三大 Agent · 有 Built-in Safeguards · 10 月全产品线铺开'),
    (date(2026, 6, 9),   MILESTONE,  'UCB 全球 Safety 全面迁移至 Veeva',
     '目前最大单一客户迁移案 · Cory Gilbert / Adrian Maynier 具名引述'),
]

events.sort(key=lambda e: e[0])

# ---------- 画布 ----------
fig, ax = plt.subplots(figsize=(22, 11))

x_start = date2num(date(2006, 10, 15))
x_end = date2num(date(2026, 10, 15))
ax.set_xlim(x_start, x_end)
ax.set_ylim(-1.5, 14)
ax.set_aspect('auto')

# ---------- 时间轴线 ----------
timeline_y = 6.2
ax.axhline(y=timeline_y, xmin=0.02, xmax=0.98, color=NAVY, linewidth=5, zorder=1)

# ---------- 年份刻度（只显示有事件的年份） ----------
event_years = sorted({e[0].year for e in events})
for yr in event_years:
    x = date2num(date(yr, 1, 1))
    ax.axvline(x=x, ymin=0.43, ymax=0.57, color=NAVY, linewidth=1.8, zorder=2)
    ax.text(x, timeline_y - 0.7, str(yr), ha='center', va='top',
            fontsize=11.5, fontweight='bold', color=NAVY)

# ---------- 事件节点 ----------
side = 0
prev_dn = None

for i, (d, color, title, sub) in enumerate(events):
    dn = date2num(d)

    # 节点大小
    if color == MILESTONE:
        dot_size = 300
    elif color == NAVY:
        dot_size = 220
    elif color == ACCENT:
        dot_size = 260
    else:
        dot_size = 120

    ax.scatter(dn, timeline_y, s=dot_size, color=color, zorder=5,
               edgecolors=WHITE, linewidths=2.5)

    if color == MILESTONE:
        ax.scatter(dn, timeline_y, s=60, color='gold', marker='*', zorder=6)

    # 交替上下
    if side == 0:
        label_base_y = timeline_y + 2.0
        dir_sign = 1
    else:
        label_base_y = timeline_y - 2.0
        dir_sign = -1

    # 垂直连接线（两段折线避免太硬）
    connector_y = timeline_y + dir_sign * 0.9
    ax.plot([dn, dn], [timeline_y + dir_sign * 0.3, connector_y],
            color=color, lw=1.5, zorder=3)
    ax.plot([dn, dn], [connector_y, label_base_y + dir_sign * 0.15],
            color=color, lw=1.5, zorder=3)

    # 日期（简写）
    date_str = d.strftime('%Y.%m') if d.month > 1 else d.strftime('%Y')
    date_y = label_base_y + dir_sign * 0.5
    ax.text(dn, date_y, date_str, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color=color)

    # 主标题
    title_y = label_base_y
    title_wrapped = '\n'.join(title.split(' · '))
    ax.text(dn, title_y, title_wrapped, ha='center', va='center',
            fontsize=10.5, fontweight='bold', color=color,
            bbox=dict(boxstyle='round,pad=0.35', facecolor=WHITE, edgecolor=color,
                      alpha=0.95, linewidth=1.3))

    # 副标题
    if sub:
        sub_y = label_base_y + dir_sign * 0.85
        ax.text(dn, sub_y, sub, ha='center', va='center',
                fontsize=7.5, color=GRAY, style='italic',
                wrap=True)

    prev_dn = dn
    side = 1 - side

# ---------- 标题 ----------
ax.text(0.5, 0.975, 'Veeva 发展脉络 · 突出 Safety 与 AI 节点（精简版）',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=22, fontweight='bold', color=NAVY)
ax.text(0.5, 0.948,
        '2019 之前全是 CRM/Vault 通用线 · 2019 Safety Suite 发布为转折点 · 22R3 数据模型大改版是 Suite 全链路自动化拐点 · 2025 AI Agent 嵌入合规工作流',
        transform=ax.transAxes, ha='center', va='top',
        fontsize=10, color=GRAY)

# ---------- 图例 ----------
legend_elements = [
    mpatches.Patch(facecolor=NAVY, label='Safety 里程碑'),
    mpatches.Patch(facecolor=ACCENT, label='AI 里程碑'),
    mpatches.Patch(facecolor=MILESTONE, label='关键里程碑（★）'),
    mpatches.Patch(facecolor=GRAY, label='公司常规事件'),
]
legend = ax.legend(handles=legend_elements, loc='lower right', fontsize=11,
                  frameon=True, facecolor=WHITE, edgecolor=NAVY,
                  framealpha=0.95, ncol=2)

# ---------- 清理坐标轴 ----------
ax.set_yticks([])
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

plt.tight_layout(pad=2.5)
out = '/workspace/Veeva发展脉络_Safety与AI时间线_v2.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor=WHITE)
print(f'saved {out}')
