# ========================================
# 数据处理模块 - 简化版
# 适合大一Python初学者学习
# 使用CSV文件存储数据
# ========================================

import os
import csv
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '../data_files')
os.makedirs(DATA_DIR, exist_ok=True)

PRODUCTS_FILE = os.path.join(DATA_DIR, 'data_products.csv')
SALES_FILE = os.path.join(DATA_DIR, 'data_sales.csv')
EMPLOYEES_FILE = os.path.join(DATA_DIR, 'data_employees.csv')
MEMBERS_FILE = os.path.join(DATA_DIR, 'data_members.csv')
COSTS_FILE = os.path.join(DATA_DIR, 'data_costs.csv')
REVIEWS_FILE = os.path.join(DATA_DIR, 'data_reviews.csv')

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

    if not os.path.exists(REVIEWS_FILE):
        with open(REVIEWS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'member_id', 'member_name', 'sale_id', 'rating', 'comment', 'review_date'])

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
    return True

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
# 评价管理函数
# ========================================

def add_review(member_id, member_name, sale_id, rating, comment):
    reviews = read_csv(REVIEWS_FILE)
    new_id = len(reviews) + 1
    review_date = datetime.now().strftime('%Y-%m-%d')
    
    new_review = [new_id, member_id, member_name, sale_id, rating, comment, review_date]
    
    with open(REVIEWS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(new_review)
    return new_review

def get_all_reviews():
    return read_csv(REVIEWS_FILE)