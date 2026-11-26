# ========================================
# 超市管理系统 - 简化版
# 适合大一Python初学者学习
# ========================================

# 1. 导入必要的库
from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime, timedelta

# 2. 导入数据处理模块
import data_handler as dh

# 3. 创建Flask应用
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), '../frontend_templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '../static'))

# ========================================
# 页面路由 - 返回HTML页面
# ========================================

# 首页
@app.route('/')
def index():
    return render_template('page_index.html')

# 商品管理页面
@app.route('/products')
def products():
    return render_template('page_products.html')

# 结算页面
@app.route('/checkout')
def checkout():
    return render_template('page_checkout.html')

# 会员确认页面
@app.route('/checkout/confirm')
def checkout_confirm():
    return render_template('page_checkout_confirm.html')

# 数据分析页面
@app.route('/analytics')
def analytics():
    return render_template('page_analytics.html')

# 员工管理页面
@app.route('/employees')
def employees():
    return render_template('page_employees.html')

# 会员管理页面
@app.route('/members')
def members():
    return render_template('page_members.html')

# ========================================
# API接口 - 处理数据请求
# ========================================

# 获取所有商品
@app.route('/api/products', methods=['GET'])
def get_products():
    products = dh.get_products()
    for p in products:
        p['price'] = float(p['price'])
        p['stock'] = int(p['stock'])
        p['id'] = int(p['id'])
    return jsonify(products)

# 添加商品
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    dh.add_product(
        data['name'],
        data['price'],
        data['stock'],
        data['category'],
        data['description']
    )
    return jsonify({'message': '商品添加成功！'})

# 删除商品
@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    dh.delete_product(id)
    return jsonify({'message': '商品删除成功！'})

# 更新商品
@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    dh.update_product(id, data['name'], data['price'], data['stock'], data['category'], data['description'])
    return jsonify({'message': '商品更新成功！'})

# 搜索商品
@app.route('/api/products/search', methods=['GET'])
def search_products():
    keyword = request.args.get('keyword', '')
    products = dh.search_products(keyword)
    for p in products:
        p['price'] = float(p['price'])
        p['stock'] = int(p['stock'])
        p['id'] = int(p['id'])
    return jsonify(products)

# 结算下单
@app.route('/api/checkout', methods=['POST'])
def process_checkout():
    data = request.get_json()
    
    try:
        for item in data['items']:
            product = dh.get_product_by_id(item['product_id'])
            if not product or int(product['stock']) < item['quantity']:
                return jsonify({'error': '商品库存不足！'}), 400
        
        sale_id = dh.add_sale(
            data.get('customer_id'),
            data['total_amount'],
            data['payment_method'],
            data['items']
        )
        
        message = '结算成功！'
        if data.get('is_member'):
            original_amount = data.get('original_amount', data['total_amount'])
            discount = original_amount - data['total_amount']
            discount_percent = int((1 - data['total_amount'] / original_amount) * 100)
            if data.get('is_birthday'):
                message = f'结算成功！🎂 生日会员享受{100 - discount_percent}折优惠，已优惠 ¥{discount:.2f}'
            else:
                message = f'结算成功！会员享受{100 - discount_percent}折优惠，已优惠 ¥{discount:.2f}'
        
        return jsonify({'message': message, 'sale_id': sale_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# 获取每日销售统计
@app.route('/api/analytics/daily_customers')
def daily_customers():
    date_counts = dh.get_sales_count_by_date()
    
    dates = []
    counts = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
        dates.append(date)
        counts.append(date_counts.get(date, 0))
    
    return jsonify({'dates': dates, 'counts': counts})

# 获取客单价统计
@app.route('/api/analytics/average_transaction')
def average_transaction():
    date_data = dh.get_sales_amount_by_date()
    
    dates = []
    average_prices = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
        dates.append(date)
        data = date_data.get(date, {'total': 0, 'count': 0})
        avg = round(data['total'] / data['count'], 2) if data['count'] > 0 else 0
        average_prices.append(avg)
    
    return jsonify({'dates': dates, 'average_prices': average_prices})

# 获取所有员工
@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = dh.get_employees()
    for emp in employees:
        emp['id'] = int(emp['id'])
        emp['salary'] = float(emp['salary'])
    return jsonify(employees)

# 添加员工
@app.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    dh.add_employee(
        data['name'],
        data['phone'],
        data['email'],
        data['department'],
        data['position'],
        data['salary'],
        data['hire_date'],
        data['store_id']
    )
    return jsonify({'message': '员工入职成功！'})

# 获取单个员工
@app.route('/api/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = dh.get_employee_by_id(id)
    if employee:
        employee['id'] = int(employee['id'])
        employee['salary'] = float(employee['salary'])
        return jsonify(employee)
    return jsonify({'error': '员工不存在'}), 404

# 更新员工信息
@app.route('/api/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    success = dh.update_employee(
        id,
        data['name'],
        data['phone'],
        data['email'],
        data['department'],
        data['position'],
        data['salary'],
        data['store_id']
    )
    if success:
        return jsonify({'message': '员工信息更新成功！'})
    return jsonify({'error': '员工不存在'}), 404

# 员工辞职
@app.route('/api/employees/<int:id>/resign', methods=['POST'])
def employee_resign(id):
    data = request.get_json()
    success = dh.employee_resign(id, data.get('remark', ''))
    if success:
        return jsonify({'message': '员工已办理辞职！'})
    return jsonify({'error': '员工不存在'}), 404

# 获取成本数据
@app.route('/api/analytics/costs')
def get_costs():
    months, totals = dh.get_costs_by_month()
    return jsonify({'months': months, 'totals': totals})

# 获取成本构成
@app.route('/api/analytics/cost_breakdown')
def get_cost_breakdown():
    breakdown = dh.get_cost_breakdown()
    return jsonify({'breakdown': breakdown})

# 获取所有会员
@app.route('/api/members', methods=['GET'])
def get_members():
    members = dh.get_members()
    for member in members:
        member['id'] = int(member['id'])
        member['points'] = int(member['points'])
    return jsonify(members)

# 添加会员
@app.route('/api/members', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member = dh.add_member(
        data['member_id'],
        data['name'],
        data['phone'],
        data['email'],
        data['birthday'],
        data['join_date']
    )
    return jsonify({'message': '会员添加成功！', 'member': new_member})

# 获取单个会员
@app.route('/api/members/<member_id>', methods=['GET'])
def get_member(member_id):
    member = dh.get_member_by_id(member_id)
    if member:
        member['id'] = int(member['id'])
        member['points'] = int(member['points'])
        return jsonify(member)
    return jsonify({'error': '会员不存在！'}), 404

# 添加评价
@app.route('/api/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    new_review = dh.add_review(
        data['member_id'],
        data['member_name'],
        data['sale_id'],
        data['rating'],
        data['comment']
    )
    return jsonify({'message': '评价添加成功！', 'review': new_review})

# 获取所有评价
@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    reviews = dh.get_all_reviews()
    for review in reviews:
        review['id'] = int(review['id'])
        review['rating'] = int(review['rating'])
    return jsonify(reviews)

# ========================================
# 启动应用
# ========================================

if __name__ == '__main__':
    dh.init_files()
    app.run(host='0.0.0.0', port=5000, debug=True)