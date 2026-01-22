import sqlite3

def create_tables(conn):
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS publishers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                publisher_id INTEGER NOT NULL,
                FOREIGN KEY (publisher_id) REFERENCES publishers(id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                UNIQUE (name, address)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                UNIQUE (subscriber_id, magazine_id),
                FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
                FOREIGN KEY (magazine_id) REFERENCES magazines(id)
            )
        """)
    except sqlite3.Error as e:
        print("Error creating tables:", e)


def add_publisher(conn, name):
    try:
        conn.execute(
            "INSERT OR IGNORE INTO publishers (name) VALUES (?)",
            (name,)
        )
    except sqlite3.Error as e:
        print(e)


def add_magazine(conn, name, publisher_id):
    try:
        conn.execute(
            "INSERT OR IGNORE INTO magazines (name, publisher_id) VALUES (?, ?)",
            (name, publisher_id)
        )
    except sqlite3.Error as e:
        print(e)


def add_subscriber(conn, name, address):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id FROM subscribers
            WHERE name = ? AND address = ?
            """,
            (name, address)
        )
        if cursor.fetchone() is None:
            conn.execute(
                "INSERT INTO subscribers (name, address) VALUES (?, ?)",
                (name, address)
            )
    except sqlite3.Error as e:
        print(e)


def add_subscription(conn, subscriber_id, magazine_id, expiration_date):
    try:
        conn.execute(
            """
            INSERT OR IGNORE INTO subscriptions
            (subscriber_id, magazine_id, expiration_date)
            VALUES (?, ?, ?)
            """,
            (subscriber_id, magazine_id, expiration_date)
        )
    except sqlite3.Error as e:
        print(e)


try:
    conn = sqlite3.connect("../db/magazines.db")
    conn.execute("PRAGMA foreign_keys = 1")
    cursor = conn.cursor()

    print("Database connection successful.")

    # 🔹 CREATE TABLES FIRST
    create_tables(conn)

    # 🔹 INSERT DATA
    add_publisher(conn, "Tech Media")
    add_publisher(conn, "Health Weekly")
    add_publisher(conn, "Global News")

    add_magazine(conn, "Python Monthly", 1)
    add_magazine(conn, "AI Today", 1)
    add_magazine(conn, "Wellness Digest", 2)

    add_subscriber(conn, "Alice Smith", "123 Main St")
    add_subscriber(conn, "Bob Jones", "456 Oak Ave")
    add_subscriber(conn, "Alice Smith", "123 Main St")  # duplicate ignored

    add_subscription(conn, 1, 1, "2026-12-31")
    add_subscription(conn, 1, 2, "2026-06-30")
    add_subscription(conn, 2, 3, "2025-09-01")

    conn.commit()
    print("Data inserted successfully.")

    # 🔹 QUERIES
    print("\nAll Subscribers:")
    for row in cursor.execute("SELECT * FROM subscribers"):
        print(row)

    print("\nAll Magazines (sorted by name):")
    for row in cursor.execute("SELECT * FROM magazines ORDER BY name"):
        print(row)

    print("\nMagazines published by 'Tech Media':")
    for row in cursor.execute("""
        SELECT magazines.name
        FROM magazines
        JOIN publishers
        ON magazines.publisher_id = publishers.id
        WHERE publishers.name = 'Tech Media'
    """):
        print(row)

except sqlite3.Error as error:
    print("SQLite error:", error)

finally:
    if 'conn' in locals():
        conn.close()
        print("\nDatabase connection closed.")
