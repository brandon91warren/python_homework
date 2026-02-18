import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

SQL = """
SELECT
  last_name,
  SUM(price * quantity) AS revenue
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY e.employee_id;
"""

conn = sqlite3.connect("db/lesson.db")
employee_results = pd.read_sql_query(SQL, conn)
conn.close()

employee_results["revenue"] = pd.to_numeric(employee_results["revenue"], errors="coerce").fillna(0)
employee_results = employee_results.sort_values("revenue", ascending=False)

ax = employee_results.plot(
    kind="bar",
    x="last_name",
    y="revenue",
    legend=False,
    color="steelblue"
)

ax.set_title("Revenue by Employee")
ax.set_xlabel("Employee Last Name")
ax.set_ylabel("Revenue ($)")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
