import sqlite3
import pandas as pd

conn = sqlite3.connect('../db/lesson.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    price REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS line_items (
    line_item_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

cursor.execute("SELECT COUNT(*) FROM products")
if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO products (product_id, product_name, price) VALUES (?, ?, ?)
    """, [
        (1, 'Widget', 10.0),
        (2, 'Gadget', 15.0),
        (3, 'Thingamajig', 7.5),
        (4, 'Doodad', 12.0),
        (5, 'Whatchamacallit', 20.0)
    ])

cursor.execute("SELECT COUNT(*) FROM line_items")
if cursor.fetchone()[0] == 0:
    cursor.executemany("""
    INSERT INTO line_items (line_item_id, product_id, quantity) VALUES (?, ?, ?)
    """, [
        (1, 1, 3),
        (2, 2, 2),
        (3, 1, 1),
        (4, 3, 5),
        (5, 2, 4),
        (6, 4, 2),
        (7, 5, 1)
    ])

conn.commit()

query = """
SELECT
    line_items.line_item_id,
    line_items.quantity,
    products.product_id,
    products.product_name,
    products.price
FROM line_items
JOIN products
ON line_items.product_id = products.product_id
"""

df = pd.read_sql_query(query, conn)

print(df.head())

df['total'] = df['quantity'] * df['price']
print(df.head())

summary = df.groupby('product_id').agg(
    line_item_count=('line_item_id', 'count'),
    total=('total', 'sum'),
    product_name=('product_name', 'first')
).reset_index()

summary = summary.sort_values('product_name')

print(summary.head())

summary.to_csv('order_summary.csv', index=False)

conn.close()
