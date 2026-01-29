import sqlite3

def main():
    conn = sqlite3.connect("../db/lesson.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    query_task1 = """
    SELECT
        o.order_id,
        SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
    """
    cursor.execute(query_task1)
    print("Task 1: Total price of first 5 orders")
    for order_id, total_price in cursor.fetchall():
        print(f"Order ID: {order_id}, Total Price: ${total_price:.2f}")

    print("\n")

    query_task2 = """
    SELECT
        c.customer_name,
        AVG(sub.total_price) AS average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT
            o.customer_id AS customer_id_b,
            SUM(p.price * li.quantity) AS total_price
        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.order_id
    ) sub
        ON c.customer_id = sub.customer_id_b
    GROUP BY c.customer_id;
    """
    cursor.execute(query_task2)
    print("Task 2: Average order price per customer")
    for name, avg_price in cursor.fetchall():
        if avg_price is not None:
            print(f"{name}: ${avg_price:.2f}")
        else:
            print(f"{name}: No orders")

    print("\n")

    try:
        conn.execute("BEGIN")

        cursor.execute(
            "SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons';"
        )
        customer_id = cursor.fetchone()[0]

        cursor.execute(
            "SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris';"
        )
        employee_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO orders (customer_id, employee_id)
            VALUES (?, ?)
            RETURNING order_id;
            """,
            (customer_id, employee_id)
        )
        order_id = cursor.fetchone()[0]

        cursor.execute(
            "SELECT product_id FROM products ORDER BY price ASC LIMIT 5;"
        )
        product_ids = [row[0] for row in cursor.fetchall()]

        for product_id in product_ids:
            cursor.execute(
                """
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, 10);
                """,
                (order_id, product_id)
            )

        conn.commit()

        cursor.execute(
            """
            SELECT
                li.line_item_id,
                li.quantity,
                p.product_name
            FROM line_items li
            JOIN products p ON li.product_id = p.product_id
            WHERE li.order_id = ?;
            """,
            (order_id,)
        )

        print("Task 3: Line items for new order")
        for li_id, qty, name in cursor.fetchall():
            print(f"Line Item ID: {li_id}, Product: {name}, Quantity: {qty}")

        cursor.execute("DELETE FROM line_items WHERE order_id = ?;", (order_id,))
        cursor.execute("DELETE FROM orders WHERE order_id = ?;", (order_id,))
        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Task 3 failed:", e)

    print("\n")

    query_task4 = """
    SELECT
        e.employee_id,
        e.first_name,
        e.last_name,
        COUNT(o.order_id) AS order_count
    FROM employees e
    JOIN orders o ON e.employee_id = o.employee_id
    GROUP BY e.employee_id
    HAVING COUNT(o.order_id) > 5;
    """
    cursor.execute(query_task4)
    print("Task 4: Employees with more than 5 orders")
    for emp_id, first, last, count in cursor.fetchall():
        print(f"{emp_id}: {first} {last} — Orders: {count}")

    conn.close()

if __name__ == "__main__":
    main()
