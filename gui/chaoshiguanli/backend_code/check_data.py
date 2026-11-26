import sqlite3
import os

# 获取数据库文件路径
db_path = os.path.join(os.path.dirname(__file__), '../data/supermarket.db')

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查看销售表数据
print("=== 销售表数据 ===")
cursor.execute('SELECT * FROM sales')
sales_data = cursor.fetchall()
print(f"销售记录数量: {len(sales_data)}")
for sale in sales_data:
    print(sale)

# 查看销售商品详情表数据
print("\n=== 销售商品详情表数据 ===")
cursor.execute('SELECT * FROM sales_items')
sales_items_data = cursor.fetchall()
print(f"销售商品详情记录数量: {len(sales_items_data)}")

# 查看商品表数据
print("\n=== 商品表数据 ===")
cursor.execute('SELECT * FROM products')
products_data = cursor.fetchall()
print(f"商品记录数量: {len(products_data)}")
for product in products_data:
    print(product)

# 关闭连接
conn.close()