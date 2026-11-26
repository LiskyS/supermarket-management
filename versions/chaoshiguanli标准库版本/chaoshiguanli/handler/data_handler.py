# ========================================
# 数据处理模块 - 简化版
# 适合大一Python初学者学习
# 使用CSV文件存储数据
# ========================================

import os
import csv
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
os.makedirs(DATA_DIR, exist_ok=True)

PRODUCTS_FILE = os.path.join(DATA_DIR, 'data_products.csv')
SALES_FILE = os.path.join(DATA_DIR, 'data_sales.csv')
EMPLOYEES_FILE = os.path.join(DATA_DIR, 'data_employees.csv')
MEMBERS_FILE = os.path.join(DATA_DIR, 'data_members.csv')
COSTS_FILE = os.path.join(DATA_DIR, 'data_costs.csv')
GIFTS_FILE = os.path.join(DATA_DIR, 'data_gifts.csv')
REDEMPTIONS_FILE = os.path.join(DATA_DIR, 'data_redemptions.csv')

# ========================================
# 基础工具函数
# ========================================

def read_csv(filepath):
    rows = []
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
    return rows

def write_csv(filepath, headers, rows):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)

def append_csv(filepath, row):
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)

def get_next_id(filepath, id_col='id'):
    rows = read_csv(filepath)
    if not rows:
        return 1
    max_id = max(int(row[id_col]) for row in rows)
    return max_id + 1

# ========================================
# 初始化数据文件
# ========================================

def init_files():
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'price', 'stock', 'category', 'description'])
            writer.writerow([1, '苹果', 5.99, 100, '水果', '新鲜红苹果'])
            writer.writerow([2, '香蕉', 3.99, 150, '水果', '进口香蕉'])
            writer.writerow([3, '牛奶', 6.99, 80, '饮品', '纯牛奶'])
            writer.writerow([4, '面包', 4.50, 60, '烘焙', '全麦面包'])
            writer.writerow([5, '鸡蛋', 8.99, 120, '生鲜', '土鸡蛋'])

    if not os.path.exists(SALES_FILE):
        with open(SALES_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'customer_id', 'sale_date', 'total_amount', 'payment_method'])

    if not os.path.exists(EMPLOYEES_FILE):
        with open(EMPLOYEES_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'phone', 'email', 'department', 'position', 'salary', 'hire_date', 'status', 'store_id'])
            writer.writerow([1, '张志华', '1376069****', 'zhangzh@store.com', '管理部', '店长', 8000, '2023-01-15', '在职', '08001001'])
            writer.writerow([2, '刘思雨', '1376069****', 'liusy@store.com', '销售部', '销售主管', 5500, '2023-03-20', '在职', '08001002'])

    if not os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'member_id', 'name', 'phone', 'email', 'birthday', 'join_date', 'points', 'level'])
            writer.writerow([1, 'M001', '张三', '13800138001', 'zhangsan@example.com', '1990-01-01', '2024-01-01', 100, '普通会员'])
            writer.writerow([2, 'M002', '李四', '13800138002', 'lisi@example.com', '1992-02-02', '2024-02-01', 200, '银卡会员'])

    if not os.path.exists(COSTS_FILE):
        with open(COSTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'month', 'rent', 'utilities', 'salaries', 'supplies', 'maintenance', 'other', 'total'])
            writer.writerow([1, '2024-01', 15000, 2500, 45000, 3000, 1500, 2000, 69000])
            writer.writerow([2, '2024-02', 15000, 2200, 45000, 2800, 1200, 1800, 67000])

    if not os.path.exists(GIFTS_FILE):
        with open(GIFTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'points_required', 'description', 'stock'])
            writer.writerow([1, '定制购物袋', 50, '环保可重复使用购物袋', 30])
            writer.writerow([2, '精美马克杯', 80, '定制Logo陶瓷马克杯', 25])
            writer.writerow([3, '雨伞', 120, '防风防雨折叠雨伞', 20])
            writer.writerow([4, '保温饭盒', 200, '304不锈钢保温饭盒', 15])
            writer.writerow([5, '蓝牙耳机', 500, '无线蓝牙耳机', 10])

    if not os.path.exists(REDEMPTIONS_FILE):
        with open(REDEMPTIONS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'member_id', 'gift_id', 'gift_name', 'points_spent', 'redeem_date'])

# ========================================
# 商品管理函数
# ========================================

def get_products():
    return read_csv(PRODUCTS_FILE)

def get_product_by_id(product_id):
    products = read_csv(PRODUCTS_FILE)
    for p in products:
        if int(p['id']) == product_id:
            return p
    return None

def add_product(name, price, stock, category, description):
    product_id = get_next_id(PRODUCTS_FILE)
    append_csv(PRODUCTS_FILE, [product_id, name, price, stock, category, description])
    return product_id

def delete_product(product_id):
    rows = read_csv(PRODUCTS_FILE)
    rows = [row for row in rows if int(row['id']) != product_id]
    write_csv(PRODUCTS_FILE, ['id', 'name', 'price', 'stock', 'category', 'description'],
              [[r['id'], r['name'], r['price'], r['stock'], r['category'], r['description']] for r in rows])

def update_product(product_id, name, price, stock, category, description):
    rows = read_csv(PRODUCTS_FILE)
    for row in rows:
        if int(row['id']) == product_id:
            row['name'] = name
            row['price'] = price
            row['stock'] = stock
            row['category'] = category
            row['description'] = description
            break
    write_csv(PRODUCTS_FILE, ['id', 'name', 'price', 'stock', 'category', 'description'],
              [[r['id'], r['name'], r['price'], r['stock'], r['category'], r['description']] for r in rows])

def search_products(keyword):
    products = read_csv(PRODUCTS_FILE)
    keyword = keyword.lower()
    return [p for p in products if keyword in p['name'].lower() or keyword in p['category'].lower()]

# ========================================
# 销售管理函数
# ========================================

def add_sale(customer_id, total_amount, payment_method, items):
    sale_id = get_next_id(SALES_FILE)
    sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    append_csv(SALES_FILE, [sale_id, customer_id or '', sale_date, total_amount, payment_method])
    
    for item in items:
        update_product_stock(item['product_id'], item['quantity'])
    
    if customer_id:
        add_member_points(customer_id, total_amount)
    
    return sale_id

def update_product_stock(product_id, quantity):
    rows = read_csv(PRODUCTS_FILE)
    for row in rows:
        if int(row['id']) == product_id:
            row['stock'] = str(int(row['stock']) - quantity)
            break
    write_csv(PRODUCTS_FILE, ['id', 'name', 'price', 'stock', 'category', 'description'],
              [[r['id'], r['name'], r['price'], r['stock'], r['category'], r['description']] for r in rows])

def get_sales_count_by_date():
    sales = read_csv(SALES_FILE)
    date_counts = {}
    for sale in sales:
        date = sale['sale_date'].split(' ')[0]
        date_counts[date] = date_counts.get(date, 0) + 1
    return date_counts

def get_sales_amount_by_date():
    sales = read_csv(SALES_FILE)
    date_data = {}
    for sale in sales:
        date = sale['sale_date'].split(' ')[0]
        if date not in date_data:
            date_data[date] = {'total': 0, 'count': 0}
        date_data[date]['total'] += float(sale['total_amount'])
        date_data[date]['count'] += 1
    return date_data

# ========================================
# 员工管理函数
# ========================================

def get_employees():
    return read_csv(EMPLOYEES_FILE)

def get_employee_by_id(employee_id):
    employees = read_csv(EMPLOYEES_FILE)
    for emp in employees:
        if int(emp['id']) == employee_id:
            return emp
    return None

def add_employee(name, phone, email, department, position, salary, hire_date, store_id):
    employee_id = get_next_id(EMPLOYEES_FILE)
    append_csv(EMPLOYEES_FILE, [employee_id, name, phone, email, department, position, salary, hire_date, '在职', store_id])
    return employee_id

def update_employee(employee_id, name, phone, email, department, position, salary, store_id):
    employee = get_employee_by_id(employee_id)
    if not employee:
        return False
    
    rows = read_csv(EMPLOYEES_FILE)
    for row in rows:
        if int(row['id']) == employee_id:
            row['name'] = name
            row['phone'] = phone
            row['email'] = email
            row['department'] = department
            row['position'] = position
            row['salary'] = salary
            row['store_id'] = store_id
            break
    
    headers = ['id', 'name', 'phone', 'email', 'department', 'position', 'salary', 'hire_date', 'status', 'store_id']
    write_csv(EMPLOYEES_FILE, headers, [[r['id'], r['name'], r['phone'], r['email'], r['department'], r['position'], r['salary'], r['hire_date'], r['status'], r['store_id']] for r in rows])
    return True

def employee_resign(employee_id, remark=''):
    employee = get_employee_by_id(employee_id)
    if not employee:
        return False
    
    rows = read_csv(EMPLOYEES_FILE)
    for row in rows:
        if int(row['id']) == employee_id:
            row['status'] = '离职'
            break
    
    headers = ['id', 'name', 'phone', 'email', 'department', 'position', 'salary', 'hire_date', 'status', 'store_id']
    write_csv(EMPLOYEES_FILE, headers, [[r['id'], r['name'], r['phone'], r['email'], r['department'], r['position'], r['salary'], r['hire_date'], r['status'], r['store_id']] for r in rows])
    
    add_employee_history(employee_id, '辞职', 
                        employee['department'], '', 
                        employee['position'], '', 
                        employee['salary'], '', remark)
    
    return True

def employee_promote(employee_id, new_position, new_salary, remark=''):
    employee = get_employee_by_id(employee_id)
    if not employee:
        return False
    
    rows = read_csv(EMPLOYEES_FILE)
    for row in rows:
        if int(row['id']) == employee_id:
            row['position'] = new_position
            row['salary'] = str(new_salary)
            break
    
    headers = ['id', 'name', 'phone', 'email', 'department', 'position', 'salary', 'hire_date', 'status', 'store_id']
    write_csv(EMPLOYEES_FILE, headers, [[r['id'], r['name'], r['phone'], r['email'], r['department'], r['position'], r['salary'], r['hire_date'], r['status'], r['store_id']] for r in rows])
    
    add_employee_history(employee_id, '升职', 
                        employee['department'], employee['department'], 
                        employee['position'], new_position, 
                        employee['salary'], str(new_salary), remark)
    
    return True

def employee_transfer(employee_id, new_department, new_position, remark=''):
    employee = get_employee_by_id(employee_id)
    if not employee:
        return False
    
    rows = read_csv(EMPLOYEES_FILE)
    for row in rows:
        if int(row['id']) == employee_id:
            row['department'] = new_department
            row['position'] = new_position
            break
    
    headers = ['id', 'name', 'phone', 'email', 'department', 'position', 'salary', 'hire_date', 'status', 'store_id']
    write_csv(EMPLOYEES_FILE, headers, [[r['id'], r['name'], r['phone'], r['email'], r['department'], r['position'], r['salary'], r['hire_date'], r['status'], r['store_id']] for r in rows])
    
    add_employee_history(employee_id, '调岗', 
                        employee['department'], new_department, 
                        employee['position'], new_position, 
                        employee['salary'], employee['salary'], remark)
    
    return True

def search_employees(keyword):
    employees = read_csv(EMPLOYEES_FILE)
    keyword = keyword.lower()
    return [emp for emp in employees if keyword in emp['name'].lower() or 
                                          keyword in emp['department'].lower() or 
                                          keyword in emp['position'].lower() or 
                                          keyword in emp['store_id'].lower()]

def add_employee_history(employee_id, action, old_department, new_department, 
                        old_position, new_position, old_salary, new_salary, remark):
    history_file = os.path.join(DATA_DIR, 'data_employee_history.csv')
    rows = read_csv(history_file)
    new_id = len(rows) + 1
    action_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    employee = get_employee_by_id(employee_id)
    employee_name = employee['name'] if employee else ''
    
    new_history = [new_id, employee_id, employee_name, action, old_department, new_department, 
                   old_position, new_position, old_salary, new_salary, action_date, remark]
    
    with open(history_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if os.path.exists(history_file) and os.path.getsize(history_file) == 0:
            writer.writerow(['id', 'employee_id', 'employee_name', 'action', 'old_department', 'new_department', 
                           'old_position', 'new_position', 'old_salary', 'new_salary', 'action_date', 'remark'])
        writer.writerow(new_history)

def get_employee_history(employee_id):
    history_file = os.path.join(DATA_DIR, 'data_employee_history.csv')
    history = read_csv(history_file)
    return [h for h in history if int(h['employee_id']) == employee_id]

# ========================================
# 会员管理函数
# ========================================

def get_members():
    return read_csv(MEMBERS_FILE)

def get_member_by_id(member_id):
    members = read_csv(MEMBERS_FILE)
    for member in members:
        if member['member_id'] == member_id:
            return member
    return None

def add_member(member_id, name, phone, email, birthday, join_date):
    members = read_csv(MEMBERS_FILE)
    new_id = len(members) + 1
    new_member = [new_id, member_id, name, phone, email, birthday, join_date, 0, '普通会员']
    
    with open(MEMBERS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(new_member)
    return new_member

def update_member(member_id, name, phone, email, birthday, level):
    members = read_csv(MEMBERS_FILE)
    headers = ['id', 'member_id', 'name', 'phone', 'email', 'birthday', 'join_date', 'points', 'level']
    
    for member in members:
        if member['member_id'] == member_id:
            member['name'] = name
            member['phone'] = phone
            member['email'] = email
            member['birthday'] = birthday
            member['level'] = level
            break
    
    with open(MEMBERS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for member in members:
            writer.writerow([member['id'], member['member_id'], member['name'], member['phone'], member['email'], 
                           member['birthday'], member['join_date'], member['points'], member['level']])
    return True

def add_member_points(member_id, amount):
    members = read_csv(MEMBERS_FILE)
    headers = ['id', 'member_id', 'name', 'phone', 'email', 'birthday', 'join_date', 'points', 'level']
    
    for member in members:
        if member['member_id'] == member_id:
            points = int(member['points'])
            points += int(amount)
            member['points'] = str(points)
            
            if points >= 1000 and member['level'] != '钻石会员':
                member['level'] = '钻石会员'
            elif points >= 500 and member['level'] != '金卡会员' and member['level'] != '钻石会员':
                member['level'] = '金卡会员'
            elif points >= 200 and member['level'] == '普通会员':
                member['level'] = '银卡会员'
            break
    
    with open(MEMBERS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for member in members:
            writer.writerow([member['id'], member['member_id'], member['name'], member['phone'], member['email'], 
                           member['birthday'], member['join_date'], member['points'], member['level']])

# ========================================
# 成本分析函数
# ========================================

def get_costs_by_month():
    costs = read_csv(COSTS_FILE)
    months = []
    totals = []
    for cost in costs:
        months.append(cost['month'])
        totals.append(float(cost['total']))
    return months, totals

def get_cost_breakdown():
    costs = read_csv(COSTS_FILE)
    if not costs:
        return {}
    latest_cost = costs[-1]
    return {
        '房租': float(latest_cost['rent']),
        '水电费': float(latest_cost['utilities']),
        '工资': float(latest_cost['salaries']),
        '办公用品': float(latest_cost['supplies']),
        '维修费': float(latest_cost['maintenance']),
        '其他': float(latest_cost['other'])
    }

# ========================================
# 礼品兑换函数
# ========================================

def get_gifts():
    return read_csv(GIFTS_FILE)

def get_gift_by_id(gift_id):
    gifts = read_csv(GIFTS_FILE)
    for g in gifts:
        if int(g['id']) == gift_id:
            return g
    return None

def get_member_points(member_id):
    member = get_member_by_id(member_id)
    if member:
        return int(member['points'])
    return 0

def redeem_gift(member_id, gift_id):
    """会员兑换礼品，成功返回True，积分不够返回False"""
    member = get_member_by_id(member_id)
    gift = get_gift_by_id(gift_id)

    if not member or not gift:
        return False, '会员或礼品不存在'

    points = int(member['points'])
    points_required = int(gift['points_required'])
    stock = int(gift['stock'])

    if stock <= 0:
        return False, '礼品库存不足'

    if points < points_required:
        return False, '积分不够'

    # 扣除会员积分
    members = read_csv(MEMBERS_FILE)
    headers = ['id', 'member_id', 'name', 'phone', 'email', 'birthday', 'join_date', 'points', 'level']
    for m in members:
        if m['member_id'] == member_id:
            new_points = points - points_required
            m['points'] = str(new_points)
            break

    with open(MEMBERS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for m in members:
            writer.writerow([m['id'], m['member_id'], m['name'], m['phone'], m['email'],
                           m['birthday'], m['join_date'], m['points'], m['level']])

    # 减少礼品库存
    gifts = read_csv(GIFTS_FILE)
    for g in gifts:
        if int(g['id']) == gift_id:
            g['stock'] = str(stock - 1)
            break

    with open(GIFTS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'points_required', 'description', 'stock'])
        for g in gifts:
            writer.writerow([g['id'], g['name'], g['points_required'], g['description'], g['stock']])

    # 记录兑换记录
    redemptions = read_csv(REDEMPTIONS_FILE)
    new_id = len(redemptions) + 1
    redeem_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(REDEMPTIONS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([new_id, member_id, gift_id, gift['name'], points_required, redeem_date])

    return True, f'兑换成功！已扣除 {points_required} 积分'