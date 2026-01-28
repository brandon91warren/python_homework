import sqlite3

def main():
    conn = sqlite3.connect("../db/lesson.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    # Task 1: First 5 line items with total price
    query_task1 = """
    SELECT
        line_items.line_item_id,
        products.price * line_items.quantity AS total_price
    FROM line_items
    JOIN products
        ON line_items.product_id = products.product_id
    ORDER BY line_items.line_item_id
    LIMIT 5;
    """
    cursor.execute(query_task1)
    results_task1 = cursor.fetchall()
    print("Task 1: Total Price per Line Item (First 5)")
    for line_item_id, total_price in results_task1:
        print(f"Line Item ID: {line_item_id}, Total Price: ${total_price:.2f}")

    print("\n")

    # Task 2: Average total price of line items
    query_task2 = """
    SELECT
        AVG(total_price) AS average_total_price
    FROM (
        SELECT
            products.price * line_items.quantity AS total_price
        FROM line_items
        JOIN products
            ON line_items.product_id = products.product_id
    );
    """
    cursor.execute(query_task2)
    result_task2 = cursor.fetchone()
    print("Task 2: Average Total Price of Line Items")
    print(f"Average Total Price: ${result_task2[0]:.2f}")

    print("\n")

    # Task 3: Insert transaction for 3 cheapest products
    print("Task 3: Insert Simulation")
    cursor.execute("SELECT product_id FROM products ORDER BY price LIMIT 3;")
    cheapest_products = [row[0] for row in cursor.fetchall()]

    try:
        # Insert 10 of each cheapest product
        for pid in cheapest_products:
            cursor.execute(
                "INSERT INTO line_items (product_id, quantity) VALUES (?, ?);",
                (pid, 10)
            )
        conn.commit()

        # Show inserted records
        cursor.execute(
            "SELECT line_item_id, product_id, quantity "
            "FROM line_items ORDER BY line_item_id DESC LIMIT 3;"
        )
        inserted = cursor.fetchall()
        for line_item_id, product_id, quantity in inserted:
            print(f"Line Item ID: {line_item_id}, Product ID: {product_id}, Quantity: {quantity}")

        # Cleanup: delete inserted records
        for line_item_id, _, _ in inserted:
            cursor.execute("DELETE FROM line_items WHERE line_item_id = ?;", (line_item_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Transaction failed:", e)

    print("\n")

    # Task 4: Simulated HAVING - products with more than 1 line item
    # NOTE: This is a simulation because there is no employees or orders table
    print("Task 4: Products with more than 1 line item (simulated HAVING)")
    query_task4 = """
    SELECT
        product_id,
        COUNT(line_item_id) AS item_count
    FROM line_items
    GROUP BY product_id
    HAVING COUNT(line_item_id) > 1
    ORDER BY product_id;
    """
    cursor.execute(query_task4)
    results_task4 = cursor.fetchall()
    for product_id, item_count in results_task4:
        print(f"Product ID: {product_id}, Line Item Count: {item_count}")

    conn.close()

if __name__ == "__main__":
    main()
