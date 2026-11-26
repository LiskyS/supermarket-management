import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

FONT_PATH = fm.findfont('Microsoft YaHei')
if not FONT_PATH:
    FONT_PATH = fm.findfont('SimHei')
FONT_PROP = fm.FontProperties(fname=FONT_PATH) if FONT_PATH else None

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

COLORS10 = ['#4ECDC4', '#FF6B6B', '#45B7D1', '#96CEB4', '#FFEAA7',
            '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']


def _set_title(ax, title):
    ax.set_title(title, fontsize=16, fontweight='bold', pad=15)


def _show(fig):
    fig.tight_layout()
    plt.show(block=False)


# ========================================
# 饼图
# ========================================

def pie_chart(title, labels, values):
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#F5F6FA')
    colors = COLORS10[:len(labels)]
    explode = [0.02] * len(labels)
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.1f%%',
        startangle=90, colors=colors, explode=explode,
        pctdistance=0.75, labeldistance=1.1
    )
    for t in autotexts:
        t.set_fontsize(12)
        t.set_fontweight('bold')
    for t in texts:
        t.set_fontsize(13)
    _set_title(ax, title)
    _show(fig)


def donut_chart(title, labels, values):
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#F5F6FA')
    colors = COLORS10[:len(labels)]
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.1f%%',
        startangle=90, colors=colors,
        pctdistance=0.82, wedgeprops=dict(width=0.35)
    )
    for t in autotexts:
        t.set_fontsize(12)
        t.set_fontweight('bold')
    for t in texts:
        t.set_fontsize(13)
    _set_title(ax, title)
    _show(fig)


# ========================================
# 柱状图
# ========================================

def bar_chart(title, labels, values, xlabel='', ylabel='', color='#4ECDC4', horizontal=False):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F5F6FA')
    ax.set_facecolor('#F5F6FA')
    colors = [COLORS10[i % len(COLORS10)] for i in range(len(labels))] if len(labels) > 1 else [color]

    if horizontal:
        bars = ax.barh(range(len(labels)), values, color=colors, edgecolor='white', linewidth=0.8, height=0.6)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels, fontsize=11)
        for bar, val in zip(bars, values):
            ax.text(bar.get_width() + max(values) * 0.01, bar.get_y() + bar.get_height() / 2,
                    f'{val:,.0f}', va='center', fontsize=10, fontweight='bold', color='#2C3E50')
    else:
        bars = ax.bar(range(len(labels)), values, color=colors, edgecolor='white', linewidth=0.8)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=10, rotation=30, ha='right')
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.01,
                    f'{val:,.0f}', ha='center', fontsize=10, fontweight='bold', color='#2C3E50')

    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', colors='#2C3E50')
    _set_title(ax, title)
    _show(fig)


def grouped_bar_chart(title, labels, group1_vals, group2_vals, label1='', label2=''):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F5F6FA')
    ax.set_facecolor('#F5F6FA')
    x = np.arange(len(labels))
    width = 0.35
    bars1 = ax.bar(x - width / 2, group1_vals, width, label=label1, color='#4ECDC4', edgecolor='white')
    bars2 = ax.bar(x + width / 2, group2_vals, width, label=label2, color='#FF6B6B', edgecolor='white')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10, rotation=30, ha='right')
    for bar in bars1:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + max(max(group1_vals), max(group2_vals)) * 0.01,
                    f'{h:,.0f}', ha='center', fontsize=9, fontweight='bold', color='#2C3E50')
    for bar in bars2:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + max(max(group1_vals), max(group2_vals)) * 0.01,
                    f'{h:,.0f}', ha='center', fontsize=9, fontweight='bold', color='#2C3E50')
    ax.legend(loc='upper right', fontsize=11, facecolor='white', edgecolor='#DDD')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    _set_title(ax, title)
    _show(fig)


def bar_with_line_chart(title, labels, bar_vals, line_vals, bar_label='', line_label='', bar_color='#4ECDC4'):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F5F6FA')
    ax1.set_facecolor('#F5F6FA')
    bars = ax1.bar(range(len(labels)), bar_vals, color=bar_color, edgecolor='white',
                   label=bar_label, alpha=0.8)
    ax1.set_xticks(range(len(labels)))
    ax1.set_xticklabels(labels, fontsize=10, rotation=30, ha='right')
    for bar, val in zip(bars, bar_vals):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(bar_vals) * 0.01,
                 f'{val:,.0f}', ha='center', fontsize=9, fontweight='bold', color='#2C3E50')
    ax2 = ax1.twinx()
    ax2.plot(range(len(labels)), line_vals, 'o-', color='#FF6B6B', linewidth=2.5,
             markersize=8, label=line_label)
    for i, val in enumerate(line_vals):
        ax2.annotate(f'{val:,.0f}', (i, val), textcoords="offset points", xytext=(0, 12),
                     ha='center', fontsize=10, fontweight='bold', color='#FF6B6B')
    ax1.legend(loc='upper left', fontsize=11, facecolor='white', edgecolor='#DDD')
    ax2.legend(loc='upper right', fontsize=11, facecolor='white', edgecolor='#DDD')
    ax1.spines['top'].set_visible(False)
    _set_title(ax1, title)
    _show(fig)


# ========================================
# 折线图
# ========================================

def line_chart(title, labels, values, xlabel='', ylabel='', color='#FF6B6B', marker='o'):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F5F6FA')
    ax.set_facecolor('#F5F6FA')
    ax.plot(range(len(labels)), values, marker=marker, color=color, linewidth=2.5,
            markersize=10, markerfacecolor='white', markeredgewidth=2, markeredgecolor=color)
    ax.fill_between(range(len(labels)), values, alpha=0.1, color=color)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=10, rotation=30, ha='right')
    for i, val in enumerate(values):
        ax.annotate(f'{val:,.0f}', (i, val), textcoords="offset points", xytext=(0, 14),
                     ha='center', fontsize=11, fontweight='bold', color='#2C3E50')
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    _set_title(ax, title)
    _show(fig)


def dual_line_chart(title, labels, vals1, vals2, label1='', label2='', color1='#4ECDC4', color2='#FF6B6B'):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F5F6FA')
    ax.set_facecolor('#F5F6FA')
    ax.plot(range(len(labels)), vals1, 's-', color=color1, linewidth=2.5,
            markersize=10, markerfacecolor='white', markeredgewidth=2, label=label1)
    ax.plot(range(len(labels)), vals2, 'o-', color=color2, linewidth=2.5,
            markersize=10, markerfacecolor='white', markeredgewidth=2, label=label2)
    ax.fill_between(range(len(labels)), vals1, alpha=0.05, color=color1)
    ax.fill_between(range(len(labels)), vals2, alpha=0.05, color=color2)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=10, rotation=30, ha='right')
    for i, (v1, v2) in enumerate(zip(vals1, vals2)):
        ax.annotate(f'{v1:,.0f}', (i, v1), textcoords="offset points", xytext=(-15, -15),
                     ha='center', fontsize=9, fontweight='bold', color=color1)
        ax.annotate(f'{v2:,.0f}', (i, v2), textcoords="offset points", xytext=(15, 12),
                     ha='center', fontsize=9, fontweight='bold', color=color2)
    ax.legend(loc='upper right', fontsize=11, facecolor='white', edgecolor='#DDD')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    _set_title(ax, title)
    _show(fig)


# ========================================
# 具体业务图表
# ========================================

def render_payment_pie(stats):
    labels = list(stats.keys())
    values = list(stats.values())
    pie_chart('支付方式占比', labels, values)


def render_cost_pie(breakdown):
    labels = list(breakdown.keys())
    values = list(breakdown.values())
    donut_chart('成本构成分析', labels, values)


def render_member_level_pie(dist):
    order = ['钻石会员', '金卡会员', '银卡会员', '普通会员']
    labels, values = [], []
    for level in order:
        if level in dist:
            labels.append(level)
            values.append(dist[level])
    for level, val in dist.items():
        if level not in order:
            labels.append(level)
            values.append(val)
    donut_chart('会员等级分布', labels, values)


def render_dept_pie(dist):
    sorted_items = sorted(dist.items(), key=lambda x: x[1], reverse=True)
    labels = [x[0] for x in sorted_items]
    values = [x[1] for x in sorted_items]
    pie_chart('各部门人数分布（在职）', labels, values)


def render_salary_dist_bar(ranges):
    order = ['<3000', '3k-4k', '4k-5k', '5k-6k', '6k-8k', '>=8k']
    labels = order
    values = [ranges.get(r, 0) for r in order]
    bar_chart('薪资区间分布（在职员工）', labels, values, ylabel='人数（人）')


def render_employee_status_bar(dist):
    labels = list(dist.keys())
    values = list(dist.values())
    bar_chart('员工在职状态分布', labels, values, ylabel='人数（人）')


def render_daily_sales_bar(trend):
    from datetime import datetime, timedelta
    days = [(datetime.now() - timedelta(days=13 - i)).strftime('%m-%d') for i in range(14)]
    labels, values = [], []
    for i in range(14):
        date = (datetime.now() - timedelta(days=13 - i)).strftime('%Y-%m-%d')
        data = trend.get(date, {'amount': 0, 'count': 0})
        labels.append(days[i])
        values.append(data['amount'])
    bar_chart('近14天每日销售额', labels, values, ylabel='销售额（元）')


def render_monthly_sales_bar(monthly):
    sorted_items = sorted(monthly.items())
    labels = [x[0] for x in sorted_items]
    values = [x[1] for x in sorted_items]
    bar_chart('月度销售额统计', labels, values, ylabel='销售额（元）')


def render_monthly_costs_bar(months, totals):
    bar_chart('月度成本统计', months, totals, ylabel='成本（元）', color='#FF6B6B')


def render_sales_vs_costs_bar(data):
    sorted_items = sorted(data.items())
    labels = [x[0] for x in sorted_items]
    sales_vals = [x[1]['sales'] for x in sorted_items]
    costs_vals = [x[1]['costs'] for x in sorted_items]
    grouped_bar_chart('月度销售 vs 成本对比', labels, sales_vals, costs_vals,
                      label1='销售额', label2='成本')


def render_sales_trend_line(trend):
    from datetime import datetime, timedelta
    days = [(datetime.now() - timedelta(days=13 - i)).strftime('%Y-%m-%d') for i in range(14)]
    labels, values = [], []
    for i in range(14):
        date = (datetime.now() - timedelta(days=13 - i)).strftime('%Y-%m-%d')
        data = trend.get(date, {'amount': 0, 'count': 0})
        labels.append(days[i])
        values.append(data['amount'])
    line_chart('近14天销售趋势', labels, values, ylabel='销售额（元）', marker='o')


def render_sales_vs_costs_line(data):
    sorted_items = sorted(data.items())
    labels = [x[0] for x in sorted_items]
    sales_vals = [x[1]['sales'] for x in sorted_items]
    costs_vals = [x[1]['costs'] for x in sorted_items]
    dual_line_chart('月度销售 vs 成本趋势', labels, sales_vals, costs_vals,
                    label1='销售额', label2='成本')


def render_low_stock_bar(products):
    if not products:
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor('#F5F6FA')
        ax.text(0.5, 0.5, '无库存预警商品\n库存状态良好！', ha='center', va='center',
                fontsize=16, color='#27AE60', fontweight='bold', transform=ax.transAxes)
        ax.axis('off')
        _set_title(ax, '库存预警')
        plt.show(block=False)
        return
    labels = [f'{p["name"]} (¥{float(p["price"]):.1f})' for p in products]
    values = [int(p['stock']) for p in products]
    bar_chart('库存预警（库存 < 10）', labels, values, ylabel='剩余库存', horizontal=True)


def render_category_count_bar(dist):
    sorted_items = sorted(dist.items(), key=lambda x: x[1]['count'], reverse=True)
    labels = [x[0] for x in sorted_items]
    values = [x[1]['count'] for x in sorted_items]
    bar_chart('商品分类分布 - 商品数', labels, values, ylabel='商品数（件）')


def render_category_stock_bar(dist):
    sorted_items = sorted(dist.items(), key=lambda x: x[1]['total_stock'], reverse=True)
    labels = [x[0] for x in sorted_items]
    values = [x[1]['total_stock'] for x in sorted_items]
    bar_chart('商品分类分布 - 库存量', labels, values, ylabel='库存量（件）')


def render_category_value_bar(dist):
    sorted_items = sorted(dist.items(), key=lambda x: x[1]['total_value'], reverse=True)
    labels = [x[0] for x in sorted_items]
    values = [x[1]['total_value'] for x in sorted_items]
    bar_chart('库存价值分析', labels, values, ylabel='库存价值（元）', horizontal=True)


def render_gift_stats_bar(stats):
    labels = list(stats.keys())
    counts = [s['count'] for s in stats.values()]
    points = [s['total_points'] for s in stats.values()]
    bar_with_line_chart('礼品兑换统计', labels, counts, points,
                        bar_label='兑换次数', line_label='消耗积分', bar_color='#45B7D1')


def render_member_points_bar(members):
    labels = [f'{m["name"]}({m["member_id"]})' for m in members]
    values = [int(m['points']) for m in members]
    bar_chart('会员积分排行', labels, values, ylabel='积分', horizontal=True)


def render_member_spending_bar(top):
    labels = [f'{t["name"]}({t["member_id"]})' for t in top]
    values = [t['amount'] for t in top]
    bar_chart('会员消费排行', labels, values, ylabel='累计消费（元）', horizontal=True)


def render_daily_customers_bar(date_counts):
    from datetime import datetime, timedelta
    days = []
    counts = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6 - i)).strftime('%Y-%m-%d')
        days.append((datetime.now() - timedelta(days=6 - i)).strftime('%m-%d'))
        counts.append(date_counts.get(date, 0))
    bar_chart('近7天每日顾客数', days, counts, ylabel='顾客数（人）')


def render_avg_transaction_line(date_data):
    from datetime import datetime, timedelta
    days = []
    avgs = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6 - i)).strftime('%Y-%m-%d')
        days.append((datetime.now() - timedelta(days=6 - i)).strftime('%m-%d'))
        data = date_data.get(date, {'total': 0, 'count': 0})
        avg = data['total'] / data['count'] if data['count'] > 0 else 0
        avgs.append(avg)
    line_chart('近7天客单价走势', days, avgs, ylabel='客单价（元）', marker='s', color='#45B7D1')
