# ========================================
# 超市管理系统 - 简化版
# 适合大一Python初学者学习
# ========================================

# 1. 导入必要的库
from flask import Flask, render_template, request, jsonify, Response
import os
from datetime import datetime, timedelta
import io
import base64
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

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

# 员工升职
@app.route('/api/employees/<int:id>/promote', methods=['POST'])
def employee_promote(id):
    data = request.get_json()
    success = dh.employee_promote(id, data.get('new_position'), data.get('new_salary'), data.get('remark', ''))
    if success:
        return jsonify({'message': '员工升职成功！'})
    return jsonify({'error': '员工不存在'}), 404

# 员工调岗
@app.route('/api/employees/<int:id>/transfer', methods=['POST'])
def employee_transfer(id):
    data = request.get_json()
    success = dh.employee_transfer(id, data.get('new_department'), data.get('new_position'), data.get('remark', ''))
    if success:
        return jsonify({'message': '员工调岗成功！'})
    return jsonify({'error': '员工不存在'}), 404

# 搜索员工
@app.route('/api/employees/search', methods=['GET'])
def search_employees():
    keyword = request.args.get('keyword', '')
    employees = dh.search_employees(keyword)
    for emp in employees:
        emp['id'] = int(emp['id'])
        emp['salary'] = float(emp['salary'])
    return jsonify(employees)

# 获取员工履历
@app.route('/api/employees/<int:id>/history', methods=['GET'])
def get_employee_history(id):
    history = dh.get_employee_history(id)
    return jsonify(history)

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

# ========================================
# 图表生成API - 使用matplotlib
# ========================================

def generate_chart_image(fig):
    """将matplotlib图表转换为PNG图片"""
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
    img_buffer.seek(0)
    return Response(img_buffer.getvalue(), mimetype='image/png')

@app.route('/api/analytics/daily_customers_data')
def daily_customers_data():
    """每日顾客数量数据（用于统计卡片）"""
    date_counts = dh.get_sales_count_by_date()
    
    dates = []
    counts = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
        dates.append(date)
        counts.append(date_counts.get(date, 0))
    
    return jsonify({'dates': dates, 'counts': counts})

@app.route('/api/analytics/chart/daily_customers')
def chart_daily_customers():
    """每日顾客数量趋势图"""
    date_counts = dh.get_sales_count_by_date()
    
    dates = []
    counts = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
        dates.append(date)
        counts.append(date_counts.get(date, 0))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, counts, marker='o', linestyle='-', color='#3498db', linewidth=2, markersize=8)
    ax.fill_between(dates, counts, alpha=0.1, color='#3498db')
    
    ax.set_title('每日顾客数量趋势', fontsize=14, fontweight='bold', color='#2c3e50')
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('顾客数量', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xticklabels(dates, rotation=45, ha='right')
    
    for i, count in enumerate(counts):
        ax.annotate(str(count), xy=(dates[i], count), xytext=(0, 5), 
                    textcoords='offset points', fontsize=10, color='#3498db')
    
    plt.tight_layout()
    return generate_chart_image(fig)

@app.route('/api/analytics/chart/average_transaction')
def chart_average_transaction():
    """客单价趋势图"""
    date_data = dh.get_sales_amount_by_date()
    
    dates = []
    average_prices = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).strftime('%Y-%m-%d')
        dates.append(date)
        data = date_data.get(date, {'total': 0, 'count': 0})
        avg = round(data['total'] / data['count'], 2) if data['count'] > 0 else 0
        average_prices.append(avg)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, average_prices, marker='s', linestyle='-', color='#2ecc71', linewidth=2, markersize=8)
    ax.fill_between(dates, average_prices, alpha=0.1, color='#2ecc71')
    
    ax.set_title('客单价趋势', fontsize=14, fontweight='bold', color='#2c3e50')
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('客单价 (¥)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_xticklabels(dates, rotation=45, ha='right')
    
    for i, price in enumerate(average_prices):
        ax.annotate(f'¥{price:.2f}', xy=(dates[i], price), xytext=(0, 5), 
                    textcoords='offset points', fontsize=10, color='#2ecc71')
    
    plt.tight_layout()
    return generate_chart_image(fig)

@app.route('/api/analytics/chart/costs')
def chart_costs():
    """每月固定成本柱状图"""
    months, totals = dh.get_costs_by_month()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(months, totals, color='#e74c3c', edgecolor='white', width=0.6)
    
    ax.set_title('每月固定成本', fontsize=14, fontweight='bold', color='#2c3e50')
    ax.set_xlabel('月份', fontsize=12)
    ax.set_ylabel('成本金额 (¥)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'¥{height:,.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5), textcoords='offset points', ha='center', fontsize=10, color='#e74c3c')
    
    plt.tight_layout()
    return generate_chart_image(fig)

@app.route('/api/analytics/chart/cost_breakdown')
def chart_cost_breakdown():
    """成本构成饼图"""
    breakdown = dh.get_cost_breakdown()
    labels = list(breakdown.keys())
    values = list(breakdown.values())
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']
    
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors,
                                       autopct='%1.1f%%', startangle=90,
                                       textprops={'fontsize': 12})
    
    ax.set_title('成本构成分析', fontsize=14, fontweight='bold', color='#2c3e50')
    ax.legend(wedges, labels, loc='upper right', bbox_to_anchor=(1.3, 0.9))
    
    plt.tight_layout()
    return generate_chart_image(fig)

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

# 更新会员信息
@app.route('/api/members/<member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.get_json()
    success = dh.update_member(
        member_id,
        data['name'],
        data['phone'],
        data['email'],
        data['birthday'],
        data['level']
    )
    if success:
        return jsonify({'message': '会员信息更新成功！'})
    return jsonify({'error': '会员不存在！'}), 404

# ========================================
# 礼品兑换
# ========================================

# 礼品兑换页面
@app.route('/redeem')
def redeem():
    return render_template('page_redeem.html')

# 获取所有礼品
@app.route('/api/gifts', methods=['GET'])
def get_gifts():
    gifts = dh.get_gifts()
    for g in gifts:
        g['id'] = int(g['id'])
        g['points_required'] = int(g['points_required'])
        g['stock'] = int(g['stock'])
    return jsonify(gifts)

# 获取会员积分
@app.route('/api/members/<member_id>/points', methods=['GET'])
def get_member_points(member_id):
    points = dh.get_member_points(member_id)
    return jsonify({'points': points})

# 处理礼品兑换
@app.route('/api/redeem', methods=['POST'])
def process_redeem():
    data = request.get_json()
    member_id = data.get('member_id')
    gift_id = data.get('gift_id')

    if not member_id or not gift_id:
        return jsonify({'error': '请填写完整信息'}), 400

    success, message = dh.redeem_gift(member_id, int(gift_id))
    if success:
        return jsonify({'message': message})
    return jsonify({'error': message}), 400

# ========================================
# 启动应用
# ========================================

if __name__ == '__main__':
    dh.init_files()
    app.run(host='0.0.0.0', port=5000, debug=True)