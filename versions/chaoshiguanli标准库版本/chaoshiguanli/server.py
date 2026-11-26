# ========================================
# 超市管理系统 - 简易 Python HTTP 服务器
# 使用 Python 内置 http.server，不依赖 Flask/Django
# ========================================

import http.server
import json
import urllib.parse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'handler'))
import data_handler as dh

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'template')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

HTML_ROUTES = {
    '/': 'page_index.html',
    '/products': 'page_products.html',
    '/checkout': 'page_checkout.html',
    '/checkout/confirm': 'page_checkout_confirm.html',
    '/analytics': 'page_analytics.html',
    '/employees': 'page_employees.html',
    '/members': 'page_members.html',
    '/redeem': 'page_redeem.html',
}


def json_response(handler, data, status=200):
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.end_headers()
    handler.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))


def read_body(handler):
    length = int(handler.headers.get('Content-Length', 0))
    if length == 0:
        return {}
    body = handler.rfile.read(length)
    return json.loads(body.decode('utf-8'))


class StoreHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path in HTML_ROUTES:
            self._serve_html(HTML_ROUTES[path])
            return

        try:
            if path == '/api/products':
                self._handle_get_products()
            elif path == '/api/products/search':
                self._handle_search_products(query)
            elif path == '/api/employees':
                self._handle_get_employees()
            elif path == '/api/employees/search':
                self._handle_search_employees(query)
            elif path == '/api/members':
                self._handle_get_members()
            elif path == '/api/gifts':
                self._handle_get_gifts()
            elif path == '/api/analytics/daily_customers':
                self._handle_daily_customers()
            elif path == '/api/analytics/daily_customers_data':
                self._handle_daily_customers_data()
            elif path == '/api/analytics/average_transaction':
                self._handle_average_transaction()
            elif path == '/api/analytics/costs':
                self._handle_costs()
            elif path == '/api/analytics/cost_breakdown':
                self._handle_cost_breakdown()
            elif path.startswith('/api/products/'):
                self._handle_get_product_by_id(path)
            elif path.startswith('/api/employees/') and '/history' in path:
                self._handle_get_employee_history(path)
            elif path.startswith('/api/employees/'):
                self._handle_get_employee_by_id(path)
            elif path.startswith('/api/members/') and '/birthday-discount' in path:
                self._handle_member_birthday_discount(path)
            elif path.startswith('/api/members/') and '/points' in path:
                self._handle_get_member_points(path)
            elif path.startswith('/api/members/'):
                self._handle_get_member_by_id(path)
            else:
                self._serve_404()
        except Exception as e:
            json_response(self, {'error': str(e)}, 500)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = read_body(self)

        try:
            if path == '/api/products':
                self._handle_add_product(body)
            elif path == '/api/checkout':
                self._handle_checkout(body)
            elif path == '/api/employees':
                self._handle_add_employee(body)
            elif path == '/api/members':
                self._handle_add_member(body)
            elif path == '/api/redeem':
                self._handle_redeem(body)
            elif path.startswith('/api/employees/') and '/resign' in path:
                self._handle_employee_resign(path, body)
            elif path.startswith('/api/employees/') and '/promote' in path:
                self._handle_employee_promote(path, body)
            elif path.startswith('/api/employees/') and '/transfer' in path:
                self._handle_employee_transfer(path, body)
            else:
                self._serve_404()
        except Exception as e:
            json_response(self, {'error': str(e)}, 500)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = read_body(self)

        try:
            if path.startswith('/api/products/'):
                self._handle_update_product(path, body)
            elif path.startswith('/api/employees/'):
                self._handle_update_employee(path, body)
            elif path.startswith('/api/members/'):
                self._handle_update_member(path, body)
            else:
                self._serve_404()
        except Exception as e:
            json_response(self, {'error': str(e)}, 500)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            if path.startswith('/api/products/'):
                self._handle_delete_product(path)
            else:
                self._serve_404()
        except Exception as e:
            json_response(self, {'error': str(e)}, 500)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")

    def _serve_html(self, filename):
        filepath = os.path.join(TEMPLATE_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self._serve_404()

    def _serve_404(self):
        self.send_response(404)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Not Found'}).encode('utf-8'))

    # ============ Products API ============

    def _handle_get_products(self):
        products = dh.get_products()
        for p in products:
            p['price'] = float(p['price'])
            p['stock'] = int(p['stock'])
            p['id'] = int(p['id'])
        json_response(self, products)

    def _handle_get_product_by_id(self, path):
        pid = int(path.split('/')[-1])
        p = dh.get_product_by_id(pid)
        if p:
            p['price'] = float(p['price'])
            p['stock'] = int(p['stock'])
            p['id'] = int(p['id'])
            json_response(self, p)
        else:
            json_response(self, {'error': '商品不存在'}, 404)

    def _handle_search_products(self, query):
        keyword = query.get('keyword', [''])[0]
        products = dh.search_products(keyword)
        for p in products:
            p['price'] = float(p['price'])
            p['stock'] = int(p['stock'])
            p['id'] = int(p['id'])
        json_response(self, products)

    def _handle_add_product(self, body):
        dh.add_product(body['name'], body['price'], body['stock'],
                       body['category'], body['description'])
        json_response(self, {'message': '商品添加成功！'})

    def _handle_update_product(self, path, body):
        pid = int(path.split('/')[-1])
        dh.update_product(pid, body['name'], body['price'], body['stock'],
                          body['category'], body['description'])
        json_response(self, {'message': '商品更新成功！'})

    def _handle_delete_product(self, path):
        pid = int(path.split('/')[-1])
        dh.delete_product(pid)
        json_response(self, {'message': '商品删除成功！'})

    # ============ Checkout API ============

    def _handle_checkout(self, body):
        try:
            for item in body['items']:
                product = dh.get_product_by_id(item['product_id'])
                if not product or int(product['stock']) < item['quantity']:
                    json_response(self, {'error': '商品库存不足！'}, 400)
                    return

            sale_id = dh.add_sale(body.get('customer_id'), body['total_amount'],
                                  body['payment_method'], body['items'])

            message = '结算成功！'
            if body.get('is_member'):
                original_amount = body.get('original_amount', body['total_amount'])
                discount = original_amount - body['total_amount']
                discount_percent = int((1 - body['total_amount'] / original_amount) * 100)
                if body.get('is_birthday'):
                    message = f'结算成功！🎂 生日会员享受{100 - discount_percent}折优惠，已优惠 ¥{discount:.2f}'
                else:
                    message = f'结算成功！会员享受{100 - discount_percent}折优惠，已优惠 ¥{discount:.2f}'

            json_response(self, {'message': message, 'sale_id': sale_id})
        except Exception as e:
            json_response(self, {'error': str(e)}, 400)

    # ============ Employee API ============

    def _handle_get_employees(self):
        employees = dh.get_employees()
        for emp in employees:
            emp['id'] = int(emp['id'])
            emp['salary'] = float(emp['salary'])
        json_response(self, employees)

    def _handle_get_employee_by_id(self, path):
        eid = int(path.split('/')[-1])
        emp = dh.get_employee_by_id(eid)
        if emp:
            emp['id'] = int(emp['id'])
            emp['salary'] = float(emp['salary'])
            json_response(self, emp)
        else:
            json_response(self, {'error': '员工不存在'}, 404)

    def _handle_search_employees(self, query):
        keyword = query.get('keyword', [''])[0]
        employees = dh.search_employees(keyword)
        for emp in employees:
            emp['id'] = int(emp['id'])
            emp['salary'] = float(emp['salary'])
        json_response(self, employees)

    def _handle_add_employee(self, body):
        dh.add_employee(body['name'], body['phone'], body['email'],
                        body['department'], body['position'], body['salary'],
                        body['hire_date'], body['store_id'])
        json_response(self, {'message': '员工入职成功！'})

    def _handle_update_employee(self, path, body):
        eid = int(path.split('/')[-1])
        success = dh.update_employee(eid, body['name'], body['phone'], body['email'],
                                     body['department'], body['position'], body['salary'],
                                     body['store_id'])
        if success:
            json_response(self, {'message': '员工信息更新成功！'})
        else:
            json_response(self, {'error': '员工不存在'}, 404)

    def _handle_employee_resign(self, path, body):
        parts = path.split('/')
        eid = int(parts[-2]) if parts[-1] == 'resign' else int(parts[-1])
        success = dh.employee_resign(eid, body.get('remark', ''))
        if success:
            json_response(self, {'message': '员工已办理辞职！'})
        else:
            json_response(self, {'error': '员工不存在'}, 404)

    def _handle_employee_promote(self, path, body):
        parts = path.split('/')
        eid = int(parts[-2]) if parts[-1] == 'promote' else int(parts[-1])
        success = dh.employee_promote(eid, body.get('new_position'),
                                      body.get('new_salary'), body.get('remark', ''))
        if success:
            json_response(self, {'message': '员工升职成功！'})
        else:
            json_response(self, {'error': '员工不存在'}, 404)

    def _handle_employee_transfer(self, path, body):
        parts = path.split('/')
        eid = int(parts[-2]) if parts[-1] == 'transfer' else int(parts[-1])
        success = dh.employee_transfer(eid, body.get('new_department'),
                                       body.get('new_position'), body.get('remark', ''))
        if success:
            json_response(self, {'message': '员工调岗成功！'})
        else:
            json_response(self, {'error': '员工不存在'}, 404)

    def _handle_get_employee_history(self, path):
        parts = path.split('/')
        eid = int(parts[-2]) if parts[-1] == 'history' else int(parts[-1])
        history = dh.get_employee_history(eid)
        json_response(self, history)

    # ============ Member API ============

    def _handle_get_members(self):
        members = dh.get_members()
        for m in members:
            m['id'] = int(m['id'])
            m['points'] = int(m['points'])
        json_response(self, members)

    def _handle_add_member(self, body):
        dh.add_member(body['member_id'], body['name'], body['phone'],
                      body['email'], body['birthday'], body['join_date'])
        json_response(self, {'message': '会员添加成功！'})

    def _handle_get_member_by_id(self, path):
        member_id = path.split('/')[-1]
        member = dh.get_member_by_id(member_id)
        if member:
            member['id'] = int(member['id'])
            member['points'] = int(member['points'])
            json_response(self, member)
        else:
            json_response(self, {'error': '会员不存在！'}, 404)

    def _handle_get_member_points(self, path):
        parts = path.split('/')
        member_id = parts[-2] if parts[-1] == 'points' else parts[-1]
        points = dh.get_member_points(member_id)
        json_response(self, {'points': points})

    def _handle_member_birthday_discount(self, path):
        from datetime import datetime
        parts = path.split('/')
        member_id = parts[-2] if parts[-1] == 'birthday-discount' else parts[-1]
        member = dh.get_member_by_id(member_id)
        if not member:
            json_response(self, {'is_birthday': False}, 200)
            return
        try:
            birthday = datetime.strptime(member['birthday'], '%Y-%m-%d')
            today = datetime.now()
            is_birthday = (today.month == birthday.month and today.day == birthday.day)
            json_response(self, {'is_birthday': is_birthday})
        except Exception:
            json_response(self, {'is_birthday': False})

    def _handle_update_member(self, path, body):
        member_id = path.split('/')[-1]
        success = dh.update_member(member_id, body['name'], body['phone'],
                                   body['email'], body['birthday'], body['level'])
        if success:
            json_response(self, {'message': '会员信息更新成功！'})
        else:
            json_response(self, {'error': '会员不存在！'}, 404)

    # ============ Gifts & Redeem API ============

    def _handle_get_gifts(self):
        gifts = dh.get_gifts()
        for g in gifts:
            g['id'] = int(g['id'])
            g['points_required'] = int(g['points_required'])
            g['stock'] = int(g['stock'])
        json_response(self, gifts)

    def _handle_redeem(self, body):
        member_id = body.get('member_id')
        gift_id = body.get('gift_id')
        if not member_id or not gift_id:
            json_response(self, {'error': '请填写完整信息'}, 400)
            return
        success, message = dh.redeem_gift(member_id, int(gift_id))
        if success:
            json_response(self, {'message': message})
        else:
            json_response(self, {'error': message}, 400)

    # ============ Analytics API ============

    def _handle_daily_customers(self):
        self._handle_daily_customers_data()

    def _handle_daily_customers_data(self):
        from datetime import datetime, timedelta
        date_counts = dh.get_sales_count_by_date()
        dates, counts = [], []
        for i in range(7):
            date = (datetime.now() - timedelta(days=6 - i)).strftime('%Y-%m-%d')
            dates.append(date)
            counts.append(date_counts.get(date, 0))
        json_response(self, {'dates': dates, 'counts': counts})

    def _handle_average_transaction(self):
        from datetime import datetime, timedelta
        date_data = dh.get_sales_amount_by_date()
        dates, average_prices = [], []
        for i in range(7):
            date = (datetime.now() - timedelta(days=6 - i)).strftime('%Y-%m-%d')
            dates.append(date)
            data = date_data.get(date, {'total': 0, 'count': 0})
            avg = round(data['total'] / data['count'], 2) if data['count'] > 0 else 0
            average_prices.append(avg)
        json_response(self, {'dates': dates, 'average_prices': average_prices})

    def _handle_costs(self):
        months, totals = dh.get_costs_by_month()
        json_response(self, {'months': months, 'totals': totals})

    def _handle_cost_breakdown(self):
        breakdown = dh.get_cost_breakdown()
        json_response(self, {'breakdown': breakdown})


def main():
    dh.init_files()
    port = 5000
    server = http.server.HTTPServer(('0.0.0.0', port), StoreHandler)
    print(f'========================================')
    print(f'  超市管理系统已启动！')
    print(f'  请在浏览器中打开: http://localhost:{port}')
    print(f'========================================')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n服务器已关闭。')
        server.server_close()


if __name__ == '__main__':
    main()
