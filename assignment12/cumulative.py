import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

SQL = """
SELECT o.order_id, SUM(p.price * l.quantity) AS total_price
FROM orders o
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id;
"""

conn = sqlite3.connect("db/lesson.db")
df = pd.read_sql_query(SQL, conn)
conn.close()

df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce").fillna(0)

def cumulative(row):
    totals_above = df["total_price"][0:row.name+1]
    return totals_above.sum()

df["cumulative"] = df.apply(cumulative, axis=1)

ax = df.plot(kind="line", x="order_id", y="cumulative", legend=False)
ax.set_title("Cumulative Revenue by Order")
ax.set_xlabel("Order ID")
ax.set_ylabel("Cumulative Revenue ($)")
plt.tight_layout()
plt.show()
