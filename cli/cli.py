import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'handler'))
import data_handler as dh

SEP = '=' * 50


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def press_enter():
    input('\n按回车键返回...')


def safe_int(prompt, default=None):
    val = input(prompt).strip()
    if val == '' and default is not None:
        return default
    try:
        return int(val)
    except ValueError:
        print('输入无效，请输入数字。')
        return None


def safe_float(prompt, default=None):
    val = input(prompt).strip()
    if val == '' and default is not None:
        return default
    try:
        return float(val)
    except ValueError:
        print('输入无效，请输入数字。')
        return None


def display_products(products):
    if not products:
        print('暂无商品数据。')
        return
    print(f'\n{"ID":<5} {"名称":<12} {"价格":<10} {"库存":<8} {"分类":<10} {"描述":<16}')
    print('-' * 65)
    for p in products:
        print(f'{p["id"]:<5} {p["name"]:<12} {float(p["price"]):<10.2f} {int(p["stock"]):<8} '
              f'{p["category"]:<10} {p["description"]:<16}')


def display_employees(employees):
    if not employees:
        print('暂无员工数据。')
        return
    print(f'\n{"ID":<5} {"姓名":<10} {"部门":<10} {"职位":<10} {"薪资":<10} {"入职日期":<12} {"状态":<6} {"门店":<10}')
    print('-' * 75)
    for emp in employees:
        print(f'{emp["id"]:<5} {emp["name"]:<10} {emp["department"]:<10} {emp["position"]:<10} '
              f'{float(emp["salary"]):<10.0f} {emp["hire_date"]:<12} {emp["status"]:<6} {emp["store_id"]:<10}')


def display_members(members):
    if not members:
        print('暂无会员数据。')
        return
    print(f'\n{"ID":<5} {"会员号":<10} {"姓名":<10} {"等级":<10} {"积分":<8} {"生日":<12} {"入会日期":<12}')
    print('-' * 70)
    for m in members:
        print(f'{m["id"]:<5} {m["member_id"]:<10} {m["name"]:<10} {m["level"]:<10} '
              f'{int(m["points"]):<8} {m["birthday"]:<12} {m["join_date"]:<12}')


def display_gifts(gifts):
    if not gifts:
        print('暂无礼品数据。')
        return
    print(f'\n{"ID":<5} {"名称":<16} {"所需积分":<10} {"库存":<8} {"描述":<20}')
    print('-' * 60)
    for g in gifts:
        print(f'{g["id"]:<5} {g["name"]:<16} {int(g["points_required"]):<10} {int(g["stock"]):<8} {g["description"]:<20}')


# ==================== 商品管理 ====================

def products_menu():
    while True:
        clear_screen()
        print(SEP)
        print('  商品管理')
        print(SEP)
        print('  1. 查看所有商品')
        print('  2. 搜索商品')
        print('  3. 添加商品')
        print('  4. 编辑商品')
        print('  5. 删除商品')
        print('  0. 返回主菜单')
        print(SEP)
        choice = input('请选择: ').strip()

        if choice == '1':
            do_view_products()
        elif choice == '2':
            do_search_products()
        elif choice == '3':
            do_add_product()
        elif choice == '4':
            do_edit_product()
        elif choice == '5':
            do_delete_product()
        elif choice == '0':
            break
        else:
            print('无效选择，请重试。')
            press_enter()


def do_view_products():
    clear_screen()
    print(SEP)
    print('  全部商品')
    print(SEP)
    products = dh.get_products()
    display_products(products)
    press_enter()


def do_search_products():
    clear_screen()
    print(SEP)
    print('  搜索商品')
    print(SEP)
    keyword = input('请输入搜索关键词（名称或分类）: ').strip()
    if not keyword:
        print('关键词不能为空。')
        press_enter()
        return
    products = dh.search_products(keyword)
    display_products(products)
    press_enter()


def do_add_product():
    clear_screen()
    print(SEP)
    print('  添加商品')
    print(SEP)
    name = input('商品名称: ').strip()
    if not name:
        print('名称不能为空。')
        press_enter()
        return
    price = safe_float('价格: ')
    if price is None:
        press_enter()
        return
    stock = safe_int('库存数量: ')
    if stock is None:
        press_enter()
        return
    category = input('分类: ').strip()
    if not category:
        print('分类不能为空。')
        press_enter()
        return
    description = input('描述: ').strip()
    dh.add_product(name, price, stock, category, description)
    print(f'\n商品 "{name}" 添加成功！')
    press_enter()


def do_edit_product():
    clear_screen()
    print(SEP)
    print('  编辑商品')
    print(SEP)
    products = dh.get_products()
    display_products(products)
    pid = safe_int('\n请输入要编辑的商品ID（输入0取消）: ')
    if pid is None or pid == 0:
        return
    product = dh.get_product_by_id(pid)
    if not product:
        print('商品不存在！')
        press_enter()
        return
    print(f'\n正在编辑: {product["name"]}')
    name = input(f'名称 ({product["name"]}): ').strip() or product['name']
    price_str = input(f'价格 ({product["price"]}): ').strip()
    price = float(price_str) if price_str else float(product['price'])
    stock_str = input(f'库存 ({product["stock"]}): ').strip()
    stock = int(stock_str) if stock_str else int(product['stock'])
    category = input(f'分类 ({product["category"]}): ').strip() or product['category']
    description = input(f'描述 ({product["description"]}): ').strip() or product['description']
    dh.update_product(pid, name, price, stock, category, description)
    print(f'\n商品 "{name}" 更新成功！')
    press_enter()


def do_delete_product():
    clear_screen()
    print(SEP)
    print('  删除商品')
    print(SEP)
    products = dh.get_products()
    display_products(products)
    pid = safe_int('\n请输入要删除的商品ID（输入0取消）: ')
    if pid is None or pid == 0:
        return
    product = dh.get_product_by_id(pid)
    if not product:
        print('商品不存在！')
        press_enter()
        return
    confirm = input(f'确认删除商品 "{product["name"]}"？(y/n): ').strip().lower()
    if confirm == 'y':
        dh.delete_product(pid)
        print(f'商品 "{product["name"]}" 已删除！')
    else:
        print('已取消。')
    press_enter()


# ==================== 商品结算 ====================

def checkout_menu():
    clear_screen()
    print(SEP)
    print('  商品结算')
    print(SEP)
    print('  第一步：选择商品加入购物车')
    print(SEP)

    products = dh.get_products()
    display_products(products)

    cart = []
    while True:
        print(f'\n当前购物车：{cart if cart else "空"}')
        print('\n1. 添加商品到购物车  2. 移除商品  3. 确认结算  0. 取消并返回')
        choice = input('请选择: ').strip()

        if choice == '0':
            return
        elif choice == '1':
            pid = safe_int('商品ID: ')
            if pid is None:
                continue
            product = dh.get_product_by_id(pid)
            if not product:
                print('商品不存在！')
                continue
            if int(product['stock']) <= 0:
                print('该商品库存不足！')
                continue
            qty = safe_int(f'数量（库存{product["stock"]}）: ')
            if qty is None or qty <= 0:
                continue
            if qty > int(product['stock']):
                print(f'库存不足！当前库存: {product["stock"]}')
                continue
            cart.append({'product_id': pid, 'quantity': qty, 'name': product['name'],
                         'price': float(product['price'])})
            print(f'已添加 {product["name"]} x{qty}')
        elif choice == '2':
            if not cart:
                print('购物车为空。')
                continue
            for i, item in enumerate(cart):
                print(f'{i + 1}. {item["name"]} x{item["quantity"]} 单价 {item["price"]:.2f}')
            idx = safe_int('请输入要移除的序号（0取消）: ')
            if idx is None or idx == 0:
                continue
            if 1 <= idx <= len(cart):
                removed = cart.pop(idx - 1)
                print(f'已移除 {removed["name"]}')
            else:
                print('序号无效。')
        elif choice == '3':
            if not cart:
                print('购物车为空，无法结算。')
                press_enter()
                return
            do_confirm_checkout(cart)
            return
        else:
            print('无效选择。')


def do_confirm_checkout(cart):
    clear_screen()
    print(SEP)
    print('  确认结算')
    print(SEP)

    original_amount = sum(item['price'] * item['quantity'] for item in cart)
    print('\n购物清单:')
    for item in cart:
        subtotal = item['price'] * item['quantity']
        print(f'  {item["name"]} x{item["quantity"]} 单价 {item["price"]:.2f} 小计 {subtotal:.2f}')
    print(f'\n原价合计: ¥{original_amount:.2f}')

    customer_id = input('\n会员编号（非会员直接回车）: ').strip()
    member = dh.get_member_by_id(customer_id) if customer_id else None

    discount = 1.0
    is_birthday = False
    if member:
        level = member['level']
        if level == '钻石会员':
            discount = 0.88
        elif level == '金卡会员':
            discount = 0.90
        elif level == '银卡会员':
            discount = 0.92
        else:
            discount = 0.95

        from datetime import datetime
        try:
            birthday = datetime.strptime(member['birthday'], '%Y-%m-%d')
            today = datetime.now()
            if today.month == birthday.month and today.day == birthday.day:
                is_birthday = True
                discount *= 0.95
        except Exception:
            pass

        print(f'会员: {member["name"]}  等级: {member["level"]}  当前积分: {member["points"]}')
        discount_pct = int((1 - discount) * 100)
        if is_birthday:
            print(f'🎂 今天是{member["name"]}的生日！享受额外折扣！')
        print(f'享受 {discount_pct} 折优惠')
    else:
        print('非会员，不享受折扣。')

    final_amount = round(original_amount * discount, 2)
    print(f'\n折后合计: ¥{final_amount:.2f}')

    print('\n支付方式: 1.现金  2.微信  3.支付宝')
    pay_choice = input('请选择: ').strip()
    pay_map = {'1': '现金', '2': '微信', '3': '支付宝'}
    payment_method = pay_map.get(pay_choice, '现金')

    confirm = input(f'\n确认结算 ¥{final_amount:.2f}？(y/n): ').strip().lower()
    if confirm != 'y':
        print('已取消结算。')
        press_enter()
        return

    cart_items = [{'product_id': item['product_id'], 'quantity': item['quantity']} for item in cart]
    dh.add_sale(customer_id or '', final_amount, payment_method, cart_items)

    print('\n' + '=' * 50)
    print('  结算成功！')
    if member:
        print(f'  会员: {member["name"]} ({member["level"]})')
        if discount < 1.0:
            print(f'  优惠: ¥{original_amount - final_amount:.2f}')
    print(f'  实付: ¥{final_amount:.2f}')
    print(f'  支付方式: {payment_method}')
    print('=' * 50)
    press_enter()


# ==================== 数据分析 ====================

def analytics_menu():
    while True:
        clear_screen()
        print(SEP)
        print('  数据分析')
        print(SEP)
        print('  1. 每日顾客数统计')
        print('  2. 客单价统计')
        print('  3. 月度成本统计')
        print('  4. 成本构成分析')
        print('  5. 销售综合分析')
        print('  6. 商品库存分析')
        print('  7. 会员数据分析')
        print('  8. 员工数据分析')
        print('  V. 可视化图表总览')
        print('  0. 返回主菜单')
        print(SEP)
        choice = input('请选择: ').strip().upper()

        if choice == '1':
            do_daily_customers()
        elif choice == '2':
            do_average_transaction()
        elif choice == '3':
            do_monthly_costs()
        elif choice == '4':
            do_cost_breakdown()
        elif choice == '5':
            sales_analysis_menu()
        elif choice == '6':
            inventory_analysis_menu()
        elif choice == '7':
            member_analysis_menu()
        elif choice == '8':
            employee_analysis_menu()
        elif choice == 'V':
            do_visual_dashboard()
        elif choice == '0':
            break
        else:
            print('无效选择。')
            press_enter()


def do_daily_customers():
    clear_screen()
    print(SEP)
    print('  每日顾客数统计（近7天）')
    print(SEP)
    from datetime import datetime, timedelta
    date_counts = dh.get_sales_count_by_date()
    total = 0
    for i in range(7):
        date = (datetime.now() - timedelta(days=6 - i)).strftime('%Y-%m-%d')
        count = date_counts.get(date, 0)
        total += count
        bar = '█' * min(count, 50)
        print(f'  {date} | {count:>4} 人 | {bar}')
    print(f'\n  近7天总计: {total} 人')
    _show_visual_prompt(lambda cr: cr.render_daily_customers_bar(date_counts))
    press_enter()


def do_average_transaction():
    clear_screen()
    print(SEP)
    print('  客单价统计（近7天）')
    print(SEP)
    from datetime import datetime, timedelta
    date_data = dh.get_sales_amount_by_date()
    all_avgs = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6 - i)).strftime('%Y-%m-%d')
        data = date_data.get(date, {'total': 0, 'count': 0})
        avg = round(data['total'] / data['count'], 2) if data['count'] > 0 else 0
        all_avgs.append(avg)
        bar = '█' * min(int(avg / 2), 40) if avg > 0 else ''
        print(f'  {date} | ¥{avg:>8.2f} | {bar}')
    if all_avgs:
        valid = [a for a in all_avgs if a > 0]
        if valid:
            print(f'\n  最高客单价: ¥{max(all_avgs):.2f}')
            print(f'  最低客单价: ¥{min(valid):.2f}')
            print(f'  平均客单价: ¥{sum(valid) / len(valid):.2f}')
    _show_visual_prompt(lambda cr: cr.render_avg_transaction_line(date_data))
    press_enter()


def do_monthly_costs():
    clear_screen()
    print(SEP)
    print('  月度成本统计')
    print(SEP)
    months, totals = dh.get_costs_by_month()
    for month, total in zip(months, totals):
        bar = '█' * int(total / 1000)
        print(f'  {month} | ¥{total:>10,.0f} | {bar}')
    _show_visual_prompt(lambda cr: cr.render_monthly_costs_bar(months, totals))
    press_enter()


def do_cost_breakdown():
    clear_screen()
    print(SEP)
    print('  成本构成分析')
    print(SEP)
    breakdown = dh.get_cost_breakdown()
    if not breakdown:
        print('暂无成本数据。')
        press_enter()
        return
    total = sum(breakdown.values())
    for name, amount in breakdown.items():
        pct = amount / total * 100 if total > 0 else 0
        bar = '█' * int(pct / 2)
        print(f'  {name:<8} | ¥{amount:>10,.0f} | {pct:>5.1f}% | {bar}')
    print(f'\n  总成本: ¥{total:,.0f}')
    _show_visual_prompt(lambda cr: cr.render_cost_pie(breakdown))
    press_enter()


# ==================== 销售综合分析 ====================

def sales_analysis_menu():
    while True:
        clear_screen()
        print(SEP)
        print('  销售综合分析')
        print(SEP)
        print('  1. 销售趋势图')
        print('  2. 支付方式分析')
        print('  3. 月度销售额统计')
        print('  4. 月度销售vs成本对比')
        print('  V. 可视化图表')
        print('  0. 返回数据分析')
        print(SEP)
        choice = input('请选择: ').strip().upper()

        if choice == '1':
            do_sales_trend()
        elif choice == '2':
            do_payment_analysis()
        elif choice == '3':
            do_monthly_sales()
        elif choice == '4':
            do_sales_vs_costs()
        elif choice == 'V':
            do_visual_sales()
        elif choice == '0':
            break
        else:
            print('无效选择。')
            press_enter()


def do_sales_trend():
    clear_screen()
    print(SEP)
    print('  销售趋势图（每日销售额）')
    print(SEP)
    from datetime import datetime, timedelta
    trend = dh.get_daily_sales_trend()
    max_amount = max([d['amount'] for d in trend.values()]) if trend else 1
    for i in range(14):
        date = (datetime.now() - timedelta(days=13 - i)).strftime('%Y-%m-%d')
        data = trend.get(date, {'amount': 0, 'count': 0})
        bar_len = int(data['amount'] / max(max_amount, 1) * 40) if max_amount > 0 else 0
        bar = '█' * bar_len
        print(f'  {date} | ¥{data["amount"]:>12,.0f} ({data["count"]}单) | {bar}')
    print(f'\n  统计周期: 近14天')
    print(f'  最高单日销售额: ¥{max_amount:,.0f}')
    total_amount = sum(d['amount'] for d in trend.values())
    total_count = sum(d['count'] for d in trend.values())
    print(f'  期间总销售额: ¥{total_amount:,.0f}  |  总订单数: {total_count}')
    _show_visual_prompt(lambda cr: cr.render_sales_trend_line(trend))
    press_enter()


def do_payment_analysis():
    clear_screen()
    print(SEP)
    print('  支付方式分析')
    print(SEP)
    stats = dh.get_payment_method_stats()
    if not stats:
        print('暂无销售数据。')
        press_enter()
        return
    total = sum(stats.values())
    sorted_methods = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    for method, count in sorted_methods:
        pct = count / total * 100 if total > 0 else 0
        bar = '█' * int(pct)
        print(f'  {method:<6} | {count:>4} 单 | {pct:>5.1f}% | {bar}')
    print(f'\n  总订单数: {total}')
    _show_visual_prompt(lambda cr: cr.render_payment_pie(stats))
    press_enter()


def do_monthly_sales():
    clear_screen()
    print(SEP)
    print('  月度销售额统计')
    print(SEP)
    monthly = dh.get_monthly_sales_amount()
    if not monthly:
        print('暂无销售数据。')
        press_enter()
        return
    max_val = max(monthly.values()) if monthly else 1
    total_all = 0
    for month in sorted(monthly.keys()):
        amount = monthly[month]
        total_all += amount
        bar_len = int(amount / max_val * 35) if max_val > 0 else 0
        bar = '█' * bar_len
        print(f'  {month} | ¥{amount:>12,.0f} | {bar}')
    print(f'\n  总计销售额: ¥{total_all:,.0f}')
    count = len(monthly)
    if count > 0:
        print(f'  月均销售额: ¥{total_all / count:,.0f}')
    _show_visual_prompt(lambda cr: cr.render_monthly_sales_bar(monthly))
    press_enter()


def do_sales_vs_costs():
    clear_screen()
    print(SEP)
    print('  月度销售 vs 成本对比')
    print(SEP)
    data = dh.get_monthly_sales_vs_costs()
    if not data:
        print('暂无数据。')
        press_enter()
        return
    max_val = max(max(d['sales'], d['costs']) for d in data.values()) if data else 1
    print(f'  {"月份":<10} {"销售额":>12} {"成本":>12} {"利润":>12}  图表(S=收入 C=成本)')
    print('  ' + '-' * 70)
    total_sales = 0
    total_costs = 0
    for month in sorted(data.keys()):
        d = data[month]
        profit = d['sales'] - d['costs']
        total_sales += d['sales']
        total_costs += d['costs']
        s_bar = int(d['sales'] / max_val * 20) if max_val > 0 else 0
        c_bar = int(d['costs'] / max_val * 20) if max_val > 0 else 0
        s_chart = '█' * s_bar
        c_chart = '▓' * c_bar
        print(f'  {month:<10} ¥{d["sales"]:>10,.0f} ¥{d["costs"]:>10,.0f} ¥{profit:>10,.0f}')
        if s_bar > 0:
            print(f'  {"S:":<10} {s_chart}')
        if c_bar > 0:
            print(f'  {"C:":<10} {c_chart}')
        print()
    total_profit = total_sales - total_costs
    print(f'  总计: 销售额 ¥{total_sales:,.0f}  成本 ¥{total_costs:,.0f}  利润 ¥{total_profit:,.0f}')
    if total_sales > 0:
        print(f'  利润率: {total_profit / total_sales * 100:.1f}%')
    _show_visual_prompt(lambda cr: cr.render_sales_vs_costs_bar(data))
    press_enter()


# ==================== 商品库存分析 ====================

def inventory_analysis_menu():
    while True:
        clear_screen()
        print(SEP)
        print('  商品库存分析')
        print(SEP)
        print('  1. 库存预警')
        print('  2. 商品分类分布')
        print('  3. 库存价值分析')
        print('  V. 可视化图表')
        print('  0. 返回数据分析')
        print(SEP)
        choice = input('请选择: ').strip().upper()

        if choice == '1':
            do_low_stock_alert()
        elif choice == '2':
            do_category_distribution()
        elif choice == '3':
            do_inventory_value()
        elif choice == 'V':
            do_visual_inventory()
        elif choice == '0':
            break
        else:
            print('无效选择。')
            press_enter()


def do_low_stock_alert():
    clear_screen()
    print(SEP)
    print('  库存预警（库存 < 10）')
    print(SEP)
    low_stock = dh.get_low_stock_products(10)
    if not low_stock:
        print('  无库存预警商品，库存状态良好！')
        press_enter()
        return
    max_stock = max(int(p['stock']) for p in low_stock) if low_stock else 10
    max_stock = max(max_stock, 1)
    print(f'  {"名称":<12} {"分类":<10} {"当前库存":<10} {"价格":<10}  库存条')
    print('  ' + '-' * 60)
    for p in low_stock:
        bar_len = max(int(int(p['stock']) / max_stock * 15), 1)
        bar = '░' * bar_len
        label = '⚠' if int(p['stock']) == 0 else '  '
        print(f'  {label}{p["name"]:<10} {p["category"]:<10} {p["stock"]:<10} ¥{float(p["price"]):<8.2f} {bar}')
    print(f'\n  共 {len(low_stock)} 件商品库存不足，建议尽快补货！')
    _show_visual_prompt(lambda cr: cr.render_low_stock_bar(low_stock))
    press_enter()


def do_category_distribution():
    clear_screen()
    print(SEP)
    print('  商品分类分布')
    print(SEP)
    dist = dh.get_category_distribution()
    if not dist:
        print('暂无商品数据。')
        press_enter()
        return
    max_count = max(d['count'] for d in dist.values())
    max_stock = max(d['total_stock'] for d in dist.values())
    max_stock = max(max_stock, 1)
    print(f'  {"分类":<10} {"商品数":<8} {"总库存":<8}  商品数分布          库存分布')
    print('  ' + '-' * 65)
    for cat in sorted(dist.keys()):
        d = dist[cat]
        bar1 = '█' * int(d['count'] / max_count * 15) if max_count > 0 else ''
        bar2 = '▓' * int(d['total_stock'] / max_stock * 15) if max_stock > 0 else ''
        print(f'  {cat:<10} {d["count"]:<8} {d["total_stock"]:<8} {bar1:<15} {bar2}')
    total_products = sum(d['count'] for d in dist.values())
    total_stock = sum(d['total_stock'] for d in dist.values())
    print(f'\n  总分类数: {len(dist)}  总商品数: {total_products}  总库存量: {total_stock}')
    _show_visual_prompt(lambda cr: (
        cr.render_category_count_bar(dist),
        cr.render_category_stock_bar(dist)
    ))
    press_enter()


def do_inventory_value():
    clear_screen()
    print(SEP)
    print('  库存价值分析')
    print(SEP)
    dist = dh.get_category_distribution()
    if not dist:
        print('暂无商品数据。')
        press_enter()
        return
    max_value = max(d['total_value'] for d in dist.values())
    max_value = max(max_value, 1)
    total_value = 0
    print(f'  {"分类":<10} {"库存价值":>12}  占比')
    print('  ' + '-' * 50)
    for cat in sorted(dist.keys()):
        d = dist[cat]
        total_value += d['total_value']
        bar_len = int(d['total_value'] / max_value * 25) if max_value > 0 else 0
        bar = '█' * bar_len
        print(f'  {cat:<10} ¥{d["total_value"]:>10,.0f} | {bar}')
    for cat in sorted(dist.keys()):
        d = dist[cat]
        pct = d['total_value'] / total_value * 100 if total_value > 0 else 0
        pct_bar = '▓' * int(pct)
        print(f'  {cat:<10} {pct:>5.1f}% {pct_bar}')
    print(f'\n  库存总价值: ¥{total_value:,.0f}')
    _show_visual_prompt(lambda cr: cr.render_category_value_bar(dist))
    press_enter()


# ==================== 会员数据分析 ====================

def member_analysis_menu():
    while True:
        clear_screen()
        print(SEP)
        print('  会员数据分析')
        print(SEP)
        print('  1. 会员等级分布')
        print('  2. 会员积分排行')
        print('  3. 会员消费排行')
        print('  4. 礼品兑换统计')
        print('  V. 可视化图表')
        print('  0. 返回数据分析')
        print(SEP)
        choice = input('请选择: ').strip().upper()

        if choice == '1':
            do_member_level_dist()
        elif choice == '2':
            do_member_points_rank()
        elif choice == '3':
            do_member_spending_rank()
        elif choice == '4':
            do_gift_stats()
        elif choice == 'V':
            do_visual_member()
        elif choice == '0':
            break
        else:
            print('无效选择。')
            press_enter()


def do_member_level_dist():
    clear_screen()
    print(SEP)
    print('  会员等级分布')
    print(SEP)
    dist = dh.get_member_level_distribution()
    if not dist:
        print('暂无会员数据。')
        press_enter()
        return
    total = sum(dist.values())
    level_order = ['钻石会员', '金卡会员', '银卡会员', '普通会员']
    max_count = max(dist.values()) if dist else 1
    for level in level_order:
        count = dist.get(level, 0)
        pct = count / total * 100 if total > 0 else 0
        bar = '█' * int(count / max_count * 30) if max_count > 0 else ''
        print(f'  {level:<8} | {count:>3} 人 | {pct:>5.1f}% | {bar}')
    print(f'\n  会员总数: {total}')
    _show_visual_prompt(lambda cr: cr.render_member_level_pie(dist))
    press_enter()


def do_member_points_rank():
    clear_screen()
    print(SEP)
    print('  会员积分排行 (Top 10)')
    print(SEP)
    members = dh.get_member_top_points(10)
    if not members:
        print('暂无会员数据。')
        press_enter()
        return
    max_points = int(members[0]['points']) if members else 1
    max_points = max(max_points, 1)
    print(f'  {"排名":<6} {"会员号":<10} {"姓名":<8} {"等级":<10} {"积分":>10}  积分条')
    print('  ' + '-' * 65)
    for i, m in enumerate(members):
        rank = i + 1
        points = int(m['points'])
        bar_len = int(points / max_points * 30)
        bar = '█' * bar_len
        print(f'  {rank:<6} {m["member_id"]:<10} {m["name"]:<8} {m["level"]:<10} {points:>10,} | {bar}')
    _show_visual_prompt(lambda cr: cr.render_member_points_bar(members))
    press_enter()


def do_member_spending_rank():
    clear_screen()
    print(SEP)
    print('  会员消费排行 (Top 10)')
    print(SEP)
    top = dh.get_top_members_by_spending(10)
    if not top:
        print('暂无会员消费数据。')
        press_enter()
        return
    max_amount = top[0]['amount'] if top else 1
    max_amount = max(max_amount, 1)
    print(f'  {"排名":<6} {"会员号":<10} {"姓名":<8} {"累计消费":>12}  消费条')
    print('  ' + '-' * 60)
    for i, t in enumerate(top):
        rank = i + 1
        bar_len = int(t['amount'] / max_amount * 30)
        bar = '█' * bar_len
        print(f'  {rank:<6} {t["member_id"]:<10} {t["name"]:<8} ¥{t["amount"]:>10,.0f} | {bar}')
    total_spending = sum(t['amount'] for t in top)
    print(f'\n  Top 10 会员累计消费: ¥{total_spending:,.0f}')
    _show_visual_prompt(lambda cr: cr.render_member_spending_bar(top))
    press_enter()


def do_gift_stats():
    clear_screen()
    print(SEP)
    print('  礼品兑换统计')
    print(SEP)
    stats = dh.get_gift_redemption_stats()
    if not stats:
        print('暂无兑换记录。')
        press_enter()
        return
    max_count = max(s['count'] for s in stats.values()) if stats else 1
    total_count = 0
    total_points = 0
    print(f'  {"礼品名称":<16} {"兑换次数":<8} {"消耗积分":<10}  频次')
    print('  ' + '-' * 55)
    for name in sorted(stats.keys()):
        s = stats[name]
        total_count += s['count']
        total_points += s['total_points']
        bar = '█' * int(s['count'] / max_count * 20) if max_count > 0 else ''
        print(f'  {name:<16} {s["count"]:<8} {s["total_points"]:<10} | {bar}')
    print(f'\n  总兑换次数: {total_count}  总消耗积分: {total_points}')
    _show_visual_prompt(lambda cr: cr.render_gift_stats_bar(stats))
    press_enter()


# ==================== 员工数据分析 ====================

def employee_analysis_menu():
    while True:
        clear_screen()
        print(SEP)
        print('  员工数据分析')
        print(SEP)
        print('  1. 部门人数分布')
        print('  2. 薪资区间分布')
        print('  3. 在职状态分布')
        print('  V. 可视化图表')
        print('  0. 返回数据分析')
        print(SEP)
        choice = input('请选择: ').strip().upper()

        if choice == '1':
            do_department_dist()
        elif choice == '2':
            do_salary_dist()
        elif choice == '3':
            do_employee_status()
        elif choice == 'V':
            do_visual_employee()
        elif choice == '0':
            break
        else:
            print('无效选择。')
            press_enter()


def do_department_dist():
    clear_screen()
    print(SEP)
    print('  部门人数分布（在职员工）')
    print(SEP)
    dist = dh.get_department_distribution()
    if not dist:
        print('暂无员工数据。')
        press_enter()
        return
    total = sum(dist.values())
    max_count = max(dist.values()) if dist else 1
    sorted_depts = sorted(dist.items(), key=lambda x: x[1], reverse=True)
    for dept, count in sorted_depts:
        pct = count / total * 100 if total > 0 else 0
        bar = '█' * int(count / max_count * 30) if max_count > 0 else ''
        print(f'  {dept:<10} | {count:>3} 人 | {pct:>5.1f}% | {bar}')
    print(f'\n  在职总人数: {total}  部门数: {len(dist)}')
    _show_visual_prompt(lambda cr: cr.render_dept_pie(dist))
    press_enter()


def do_salary_dist():
    clear_screen()
    print(SEP)
    print('  薪资区间分布（在职员工）')
    print(SEP)
    ranges = dh.get_salary_range_distribution()
    total = sum(ranges.values())
    max_count = max(ranges.values()) if ranges else 1
    range_order = ['<3000', '3k-4k', '4k-5k', '5k-6k', '6k-8k', '>=8k']
    for r in range_order:
        count = ranges.get(r, 0)
        pct = count / total * 100 if total > 0 else 0
        bar = '█' * int(count / max_count * 30) if max_count > 0 else ''
        print(f'  {r:<8} | {count:>3} 人 | {pct:>5.1f}% | {bar}')
    print(f'\n  在职总人数: {total}')

    employees = dh.get_employees()
    active_emps = [e for e in employees if e['status'] == '在职']
    if active_emps:
        salaries = [float(e['salary']) for e in active_emps]
        print(f'  最高薪资: ¥{max(salaries):,.0f}')
        print(f'  最低薪资: ¥{min(salaries):,.0f}')
        print(f'  平均薪资: ¥{sum(salaries) / len(salaries):,.0f}')
    _show_visual_prompt(lambda cr: cr.render_salary_dist_bar(ranges))
    press_enter()


def do_employee_status():
    clear_screen()
    print(SEP)
    print('  员工在职状态分布')
    print(SEP)
    dist = dh.get_employee_status_distribution()
    if not dist:
        print('暂无员工数据。')
        press_enter()
        return
    total = sum(dist.values())
    for status, count in dist.items():
        pct = count / total * 100 if total > 0 else 0
        bar = '█' * int(pct)
        symbol = '●' if status == '在职' else '○'
        print(f'  {symbol} {status:<6} | {count:>3} 人 | {pct:>5.1f}% | {bar}')
    print(f'\n  员工总数: {total}')
    _show_visual_prompt(lambda cr: cr.render_employee_status_bar(dist))
    press_enter()


# ==================== 员工管理 ====================

def employees_menu():
    while True:
        clear_screen()
        print(SEP)
        print('  员工管理')
        print(SEP)
        print('  1. 查看所有员工')
        print('  2. 搜索员工')
        print('  3. 员工入职')
        print('  4. 编辑员工')
        print('  5. 员工升职')
        print('  6. 员工调岗')
        print('  7. 员工辞职')
        print('  8. 查看员工履历')
        print('  0. 返回主菜单')
        print(SEP)
        choice = input('请选择: ').strip()

        if choice == '1':
            do_view_employees()
        elif choice == '2':
            do_search_employees()
        elif choice == '3':
            do_add_employee()
        elif choice == '4':
            do_edit_employee()
        elif choice == '5':
            do_promote_employee()
        elif choice == '6':
            do_transfer_employee()
        elif choice == '7':
            do_resign_employee()
        elif choice == '8':
            do_view_employee_history()
        elif choice == '0':
            break
        else:
            print('无效选择。')
            press_enter()


def do_view_employees():
    clear_screen()
    print(SEP)
    print('  全部员工')
    print(SEP)
    employees = dh.get_employees()
    display_employees(employees)
    press_enter()


def do_search_employees():
    clear_screen()
    print(SEP)
    print('  搜索员工')
    print(SEP)
    keyword = input('请输入搜索关键词（姓名/部门/职位/门店）: ').strip()
    if not keyword:
        print('关键词不能为空。')
        press_enter()
        return
    employees = dh.search_employees(keyword)
    display_employees(employees)
    press_enter()


def do_add_employee():
    clear_screen()
    print(SEP)
    print('  员工入职')
    print(SEP)
    name = input('姓名: ').strip()
    if not name:
        print('姓名不能为空。')
        press_enter()
        return
    phone = input('电话: ').strip()
    email = input('邮箱: ').strip()
    department = input('部门: ').strip()
    position = input('职位: ').strip()
    salary = safe_float('薪资: ')
    if salary is None:
        press_enter()
        return
    hire_date = input('入职日期 (YYYY-MM-DD): ').strip()
    store_id = input('门店编号: ').strip()
    dh.add_employee(name, phone, email, department, position, salary, hire_date, store_id)
    print(f'\n员工 "{name}" 入职成功！')
    press_enter()


def do_edit_employee():
    clear_screen()
    print(SEP)
    print('  编辑员工')
    print(SEP)
    employees = dh.get_employees()
    display_employees(employees)
    eid = safe_int('\n请输入要编辑的员工ID（输入0取消）: ')
    if eid is None or eid == 0:
        return
    emp = dh.get_employee_by_id(eid)
    if not emp:
        print('员工不存在！')
        press_enter()
        return
    print(f'\n正在编辑: {emp["name"]}')
    name = input(f'姓名 ({emp["name"]}): ').strip() or emp['name']
    phone = input(f'电话 ({emp["phone"]}): ').strip() or emp['phone']
    email = input(f'邮箱 ({emp["email"]}): ').strip() or emp['email']
    department = input(f'部门 ({emp["department"]}): ').strip() or emp['department']
    position = input(f'职位 ({emp["position"]}): ').strip() or emp['position']
    salary_str = input(f'薪资 ({emp["salary"]}): ').strip()
    salary = float(salary_str) if salary_str else float(emp['salary'])
    store_id = input(f'门店 ({emp["store_id"]}): ').strip() or emp['store_id']
    dh.update_employee(eid, name, phone, email, department, position, salary, store_id)
    print(f'\n员工 "{name}" 更新成功！')
    press_enter()


def do_promote_employee():
    clear_screen()
    print(SEP)
    print('  员工升职')
    print(SEP)
    employees = dh.get_employees()
    display_employees(employees)
    eid = safe_int('\n请输入要升职的员工ID（输入0取消）: ')
    if eid is None or eid == 0:
        return
    emp = dh.get_employee_by_id(eid)
    if not emp:
        print('员工不存在！')
        press_enter()
        return
    if emp['status'] != '在职':
        print('只能对在职员工执行此操作。')
        press_enter()
        return
    print(f'\n当前: {emp["name"]} | {emp["position"]} | ¥{emp["salary"]}')
    new_position = input('新职位: ').strip()
    if not new_position:
        print('职位不能为空。')
        press_enter()
        return
    new_salary = safe_float('新薪资: ')
    if new_salary is None:
        press_enter()
        return
    remark = input('备注（可选）: ').strip()
    dh.employee_promote(eid, new_position, new_salary, remark)
    print(f'\n{emp["name"]} 升职成功！{emp["position"]} -> {new_position}')
    press_enter()


def do_transfer_employee():
    clear_screen()
    print(SEP)
    print('  员工调岗')
    print(SEP)
    employees = dh.get_employees()
    display_employees(employees)
    eid = safe_int('\n请输入要调岗的员工ID（输入0取消）: ')
    if eid is None or eid == 0:
        return
    emp = dh.get_employee_by_id(eid)
    if not emp:
        print('员工不存在！')
        press_enter()
        return
    if emp['status'] != '在职':
        print('只能对在职员工执行此操作。')
        press_enter()
        return
    print(f'\n当前: {emp["name"]} | {emp["department"]} - {emp["position"]}')
    new_department = input('新部门: ').strip()
    new_position = input('新职位: ').strip()
    if not new_department or not new_position:
        print('部门和职位不能为空。')
        press_enter()
        return
    remark = input('备注（可选）: ').strip()
    dh.employee_transfer(eid, new_department, new_position, remark)
    print(f'\n{emp["name"]} 调岗成功！{emp["department"]} -> {new_department}')
    press_enter()


def do_resign_employee():
    clear_screen()
    print(SEP)
    print('  员工辞职')
    print(SEP)
    employees = dh.get_employees()
    display_employees(employees)
    eid = safe_int('\n请输入要辞职的员工ID（输入0取消）: ')
    if eid is None or eid == 0:
        return
    emp = dh.get_employee_by_id(eid)
    if not emp:
        print('员工不存在！')
        press_enter()
        return
    if emp['status'] != '在职':
        print('该员工已不在职。')
        press_enter()
        return
    confirm = input(f'确认 {emp["name"]} 辞职？(y/n): ').strip().lower()
    if confirm != 'y':
        print('已取消。')
        press_enter()
        return
    remark = input('备注（可选）: ').strip()
    dh.employee_resign(eid, remark)
    print(f'\n{emp["name"]} 已办理辞职。')
    press_enter()


def do_view_employee_history():
    clear_screen()
    print(SEP)
    print('  员工履历')
    print(SEP)
    employees = dh.get_employees()
    display_employees(employees)
    eid = safe_int('\n请输入员工ID（输入0取消）: ')
    if eid is None or eid == 0:
        return
    emp = dh.get_employee_by_id(eid)
    if not emp:
        print('员工不存在！')
        press_enter()
        return
    history = dh.get_employee_history(eid)
    print(f'\n{emp["name"]} 的履历:')
    if not history:
        print('  暂无履历记录。')
    else:
        for h in history:
            print(f'  {h["action_date"]} | {h["action"]} | '
                  f'{h["old_department"]}->{h["new_department"]} | '
                  f'{h["old_position"]}->{h["new_position"]}')
    press_enter()


# ==================== 会员管理 ====================

def members_menu():
    while True:
        clear_screen()
        print(SEP)
        print('  会员管理')
        print(SEP)
        print('  1. 查看所有会员')
        print('  2. 添加会员')
        print('  3. 编辑会员')
        print('  4. 查看会员详情')
        print('  0. 返回主菜单')
        print(SEP)
        choice = input('请选择: ').strip()

        if choice == '1':
            do_view_members()
        elif choice == '2':
            do_add_member()
        elif choice == '3':
            do_edit_member()
        elif choice == '4':
            do_view_member_detail()
        elif choice == '0':
            break
        else:
            print('无效选择。')
            press_enter()


def do_view_members():
    clear_screen()
    print(SEP)
    print('  全部会员')
    print(SEP)
    members = dh.get_members()
    display_members(members)
    press_enter()


def do_add_member():
    clear_screen()
    print(SEP)
    print('  添加会员')
    print(SEP)
    member_id = input('会员编号: ').strip()
    if not member_id:
        print('会员编号不能为空。')
        press_enter()
        return
    existing = dh.get_member_by_id(member_id)
    if existing:
        print(f'会员编号 "{member_id}" 已存在！')
        press_enter()
        return
    name = input('姓名: ').strip()
    phone = input('电话: ').strip()
    email = input('邮箱: ').strip()
    birthday = input('生日 (YYYY-MM-DD): ').strip()
    join_date = input('入会日期 (YYYY-MM-DD): ').strip()
    dh.add_member(member_id, name, phone, email, birthday, join_date)
    print(f'\n会员 "{name}" 添加成功！')
    press_enter()


def do_edit_member():
    clear_screen()
    print(SEP)
    print('  编辑会员')
    print(SEP)
    members = dh.get_members()
    display_members(members)
    member_id = input('\n请输入会员编号（输入0取消）: ').strip()
    if member_id == '0' or not member_id:
        return
    member = dh.get_member_by_id(member_id)
    if not member:
        print('会员不存在！')
        press_enter()
        return
    print(f'\n正在编辑: {member["name"]} ({member["member_id"]})')
    name = input(f'姓名 ({member["name"]}): ').strip() or member['name']
    phone = input(f'电话 ({member["phone"]}): ').strip() or member['phone']
    email = input(f'邮箱 ({member["email"]}): ').strip() or member['email']
    birthday = input(f'生日 ({member["birthday"]}): ').strip() or member['birthday']
    level = input(f'等级 ({member["level"]}): ').strip() or member['level']
    dh.update_member(member_id, name, phone, email, birthday, level)
    print(f'\n会员 "{name}" 更新成功！')
    press_enter()


def do_view_member_detail():
    clear_screen()
    print(SEP)
    print('  会员详情')
    print(SEP)
    member_id = input('请输入会员编号: ').strip()
    if not member_id:
        print('会员编号不能为空。')
        press_enter()
        return
    member = dh.get_member_by_id(member_id)
    if not member:
        print('会员不存在！')
        press_enter()
        return
    print(f'\n会员详情:')
    print(f'  会员编号: {member["member_id"]}')
    print(f'  姓名: {member["name"]}')
    print(f'  电话: {member["phone"]}')
    print(f'  邮箱: {member["email"]}')
    print(f'  生日: {member["birthday"]}')
    print(f'  入会日期: {member["join_date"]}')
    print(f'  等级: {member["level"]}')
    print(f'  积分: {member["points"]}')

    from datetime import datetime
    try:
        birthday = datetime.strptime(member['birthday'], '%Y-%m-%d')
        today = datetime.now()
        if today.month == birthday.month and today.day == birthday.day:
            print(f'\n  🎂 今天是{member["name"]}的生日！购物可享额外折扣！')
    except Exception:
        pass
    press_enter()


# ==================== 礼品兑换 ====================

def redeem_menu():
    while True:
        clear_screen()
        print(SEP)
        print('  礼品兑换')
        print(SEP)
        print('  1. 查看所有礼品')
        print('  2. 兑换礼品')
        print('  0. 返回主菜单')
        print(SEP)
        choice = input('请选择: ').strip()

        if choice == '1':
            do_view_gifts()
        elif choice == '2':
            do_redeem_gift()
        elif choice == '0':
            break
        else:
            print('无效选择。')
            press_enter()


def do_view_gifts():
    clear_screen()
    print(SEP)
    print('  全部礼品')
    print(SEP)
    gifts = dh.get_gifts()
    display_gifts(gifts)
    press_enter()


def do_redeem_gift():
    clear_screen()
    print(SEP)
    print('  兑换礼品')
    print(SEP)
    member_id = input('请输入会员编号: ').strip()
    if not member_id:
        print('会员编号不能为空。')
        press_enter()
        return
    member = dh.get_member_by_id(member_id)
    if not member:
        print('会员不存在！')
        press_enter()
        return
    points = dh.get_member_points(member_id)
    print(f'\n{member["name"]}  当前积分: {points}')
    print()
    gifts = dh.get_gifts()
    display_gifts(gifts)
    gid = safe_int('\n请输入要兑换的礼品ID（输入0取消）: ')
    if gid is None or gid == 0:
        return
    gift = dh.get_gift_by_id(gid)
    if not gift:
        print('礼品不存在！')
        press_enter()
        return
    print(f'\n选择: {gift["name"]} (需要 {gift["points_required"]} 积分)')
    print(f'当前积分: {points}')
    confirm = input('确认兑换？(y/n): ').strip().lower()
    if confirm != 'y':
        print('已取消。')
        press_enter()
        return
    success, msg = dh.redeem_gift(member_id, gid)
    if success:
        new_points = dh.get_member_points(member_id)
        print(f'\n{msg}')
        print(f'剩余积分: {new_points}')
    else:
        print(f'\n兑换失败: {msg}')
    press_enter()


# ==================== 主菜单 ====================

def main_menu():
    while True:
        clear_screen()
        print(SEP)
        print('  超市管理系统')
        print(SEP)
        print('  1. 商品管理')
        print('  2. 商品结算')
        print('  3. 数据分析')
        print('  4. 员工管理')
        print('  5. 会员管理')
        print('  6. 礼品兑换')
        print('  0. 退出系统')
        print(SEP)
        choice = input('请选择: ').strip()

        if choice == '1':
            products_menu()
        elif choice == '2':
            checkout_menu()
        elif choice == '3':
            analytics_menu()
        elif choice == '4':
            employees_menu()
        elif choice == '5':
            members_menu()
        elif choice == '6':
            redeem_menu()
        elif choice == '0':
            print('\n感谢使用，再见！')
            break
        else:
            print('无效选择，请重试。')
            press_enter()


# ==================== matplotlib 可视化（懒加载） ====================

def _import_cr():
    try:
        import matplotlib
        matplotlib.use('TkAgg')
        import chart_renderer as cr
        return cr
    except ImportError:
        clear_screen()
        print(SEP)
        print('  matplotlib 未安装，无法生成图表')
        print(SEP)
        print('  请在 CMD 中运行以下命令安装:')
        print('    pip install matplotlib')
        print(SEP)
        press_enter()
        return None


def _show_visual_prompt(visual_fn):
    print('\n  V. 查看可视化图表  其他键. 返回')
    choice = input('请选择: ').strip().upper()
    if choice == 'V':
        cr = _import_cr()
        if cr is not None:
            visual_fn(cr)


def do_visual_dashboard():
    cr = _import_cr()
    if cr is None:
        return
    import matplotlib.pyplot as plt
    clear_screen()
    print(SEP)
    print('  正在生成可视化总览，请查看弹出的图表窗口...')
    print(SEP)
    print('  图表包含:')
    print('    1. 支付方式饼图')
    print('    2. 月度销售额柱状图')
    print('    3. 部门人数饼图')
    print('    4. 会员等级环形图')
    print(SEP)
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.patch.set_facecolor('#F5F6FA')
    fig.suptitle('超市数据可视化总览', fontsize=20, fontweight='bold', y=0.98)
    fig.subplots_adjust(hspace=0.35, wspace=0.3, top=0.92)
    for ax_row in axes:
        for ax in ax_row:
            ax.set_facecolor('#F5F6FA')

    stats = dh.get_payment_method_stats()
    labels = list(stats.keys())
    values = list(stats.values())
    axes[0, 0].pie(values, labels=labels, autopct='%1.1f%%', startangle=90,
                   colors=cr.COLORS10[:len(labels)], explode=[0.02] * len(labels))
    axes[0, 0].set_title('支付方式占比', fontsize=14, fontweight='bold')

    monthly = dh.get_monthly_sales_amount()
    sorted_items = sorted(monthly.items())
    mlabels = [x[0] for x in sorted_items]
    mvalues = [x[1] for x in sorted_items]
    axes[0, 1].bar(range(len(mlabels)), mvalues, color=cr.COLORS10[:len(mlabels)], edgecolor='white')
    axes[0, 1].set_xticks(range(len(mlabels)))
    axes[0, 1].set_xticklabels(mlabels, fontsize=9)
    axes[0, 1].set_title('月度销售额（元）', fontsize=14, fontweight='bold')

    dept_dist = dh.get_department_distribution()
    dlabels = list(dept_dist.keys())
    dvalues = list(dept_dist.values())
    axes[1, 0].pie(dvalues, labels=dlabels, autopct='%1.1f%%', startangle=90,
                   colors=cr.COLORS10[:len(dlabels)], explode=[0.02] * len(dlabels))
    axes[1, 0].set_title('部门人数分布（在职）', fontsize=14, fontweight='bold')

    level_dist = dh.get_member_level_distribution()
    order = ['钻石会员', '金卡会员', '银卡会员', '普通会员']
    llabels, lvalues = [], []
    for level in order:
        if level in level_dist:
            llabels.append(level)
            lvalues.append(level_dist[level])
    axes[1, 1].pie(lvalues, labels=llabels, autopct='%1.1f%%', startangle=90,
                   colors=cr.COLORS10[:len(llabels)], pctdistance=0.82,
                   wedgeprops=dict(width=0.35))
    axes[1, 1].set_title('会员等级分布', fontsize=14, fontweight='bold')

    fig.tight_layout()
    plt.show(block=False)
    print('  图表已打开，查看完毕后关闭窗口即可继续操作。')
    press_enter()


def do_visual_sales():
    cr = _import_cr()
    if cr is None:
        return
    clear_screen()
    print(SEP)
    print('  正在生成销售分析图表...')
    print(SEP)
    cr.render_payment_pie(dh.get_payment_method_stats())
    cr.render_sales_trend_line(dh.get_daily_sales_trend())
    cr.render_sales_vs_costs_bar(dh.get_monthly_sales_vs_costs())
    print('  已打开 3 个图表窗口，查看完毕后关闭窗口即可。')
    press_enter()


def do_visual_inventory():
    cr = _import_cr()
    if cr is None:
        return
    clear_screen()
    print(SEP)
    print('  正在生成库存分析图表...')
    print(SEP)
    dist = dh.get_category_distribution()
    cr.render_category_count_bar(dist)
    cr.render_category_stock_bar(dist)
    cr.render_low_stock_bar(dh.get_low_stock_products(10))
    print('  已打开 3 个图表窗口，查看完毕后关闭窗口即可。')
    press_enter()


def do_visual_member():
    cr = _import_cr()
    if cr is None:
        return
    clear_screen()
    print(SEP)
    print('  正在生成会员分析图表...')
    print(SEP)
    cr.render_member_level_pie(dh.get_member_level_distribution())
    cr.render_member_spending_bar(dh.get_top_members_by_spending(10))
    cr.render_gift_stats_bar(dh.get_gift_redemption_stats())
    print('  已打开 3 个图表窗口，查看完毕后关闭窗口即可。')
    press_enter()


def do_visual_employee():
    cr = _import_cr()
    if cr is None:
        return
    clear_screen()
    print(SEP)
    print('  正在生成员工分析图表...')
    print(SEP)
    cr.render_dept_pie(dh.get_department_distribution())
    cr.render_salary_dist_bar(dh.get_salary_range_distribution())
    cr.render_employee_status_bar(dh.get_employee_status_distribution())
    print('  已打开 3 个图表窗口，查看完毕后关闭窗口即可。')
    press_enter()


def main():
    dh.init_files()
    main_menu()


if __name__ == '__main__':
    main()
