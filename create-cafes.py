import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent

FREQUENTS_DATA = [
    ("Adamariz", "Starbucks"),
    ("Neko", "Esselon Cafe"),
    ("Keilan", "Tandem Bagel Company"),
    ("Makhi", "Haymarket Café"),
    ("Jimy", "Cafe Balagon"),
    ("Nianna", "Shelburne Falls Roastery"),
    ("Archer", "Woodstar Café"),
    ("Cherokee", "Haymarket Café"),
    ("Saliha", "Bread & Butter"),
    ("Dell", "Starbucks"),
    ("Abhishek", "Woodstar Café"),
    ("Kalese", "Tandem Bagel Company"),
    ("Helene", "Haymarket Café"),
    ("Breken", "Esselon Cafe"),
    ("Sydnei", "Woodstar Café"),
    ("Layne", "Woodstar Café"),
    ("Zyaria", "Woodstar Café"),
    ("Corde", "Bread & Butter"),
    ("Betel", "Esselon Cafe"),
    ("Sumit", "Shelburne Falls Roastery"),
    ("Yalixa", "Bread & Butter"),
    ("Lindzy", "Haymarket Café"),
    ("Jahia", "Starbucks"),
    ("Airi", "Shelburne Falls Roastery"),
    ("Nykera", "Woodstar Café"),
    ("Alacia", "Bread & Butter"),
    ("Adetayo", "Starbucks"),
    ("Chanah", "Starbucks"),
    ("Cera", "Bread & Butter"),
    ("Litsy", "Woodstar Café"),
    ("Mckenna", "Shelburne Falls Roastery"),
]

SELLS_DATA = [
    ("Bread & Butter", "Iced Coffee", 2.75),
    ("Bread & Butter", "Mocha", 4.50),
    ("Cafe Balagon", "Cappuccino", 3.75),
    ("Cafe Balagon", "Cortado", 4.25),
    ("Dunkin Donuts", "Americano", None),
    ("Dunkin Donuts", "Cappuccino", 3.50),
    ("Dunkin Donuts", "Latte", 4.00),
    ("Dunkin Donuts", "Espresso", 4.50),
    ("Dunkin Donuts", "Iced Coffee", 2.75),
    ("Esselon Cafe", "Espresso", 4.50),
    ("Esselon Cafe", "Latte", 4.25),
    ("Esselon Cafe", "Cortado", 4.50),
    ("Haymarket Café", "Americano", 3.00),
    ("Haymarket Café", "Cappuccino", 3.50),
    ("Haymarket Café", "Espresso", 4.25),
    ("Haymarket Café", "Iced Coffee", 2.75),
    ("Haymarket Café", "Macchiato", 3.50),
    ("Haymarket Café", "Mocha", 4.75),
    ("Shelburne Falls Roastery", "Macchiato", 3.75),
    ("Shelburne Falls Roastery", "Americano", 3.00),
    ("Shelburne Falls Roastery", "Cappuccino", 3.50),
    ("Shelburne Falls Roastery", "Latte", 4.25),
    ("Shelburne Falls Roastery", "Mocha", 4.75),
    ("Starbucks", "Americano", 3.25),
    ("Starbucks", "Cappuccino", 3.75),
    ("Starbucks", "Espresso", 4.75),
    ("Starbucks", "Iced Coffee", 2.50),
    ("Starbucks", "Macchiato", 3.50),
    ("Starbucks", "Latte", None),
    ("Starbucks", "Mocha", 4.50),
    ("Tandem Bagel Company", "Americano", 3.25),
    ("Tandem Bagel Company", "Macchiato", 3.75),
    ("Tandem Bagel Company", "Cortado", 4.25),
    ("Woodstar Café", "Cortado", 4.00),
    ("Woodstar Café", "Macchiato", 3.75),
    ("Woodstar Café", "Mocha", 4.75),
    ("Woodstar Café", "Espresso", 4.75),
    ("Woodstar Café", "Latte", 4.25),
]


def print_tables_and_schema(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()

    print("\nTables:")
    table_rows = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    ).fetchall()
    for row in table_rows:
        print(f" - {row[0]}")

    print("\nSchema:")
    schema_rows = cur.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' ORDER BY name;"
    ).fetchall()
    for row in schema_rows:
        print(row[0])
        print()


def main() -> None:
    db_path = HERE / "cafes.db"

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Easy to rerun in class without manual cleanup.
        cur.execute('DROP TABLE IF EXISTS "Frequents";')
        cur.execute('DROP TABLE IF EXISTS "Sells";')

        cur.execute("""
            CREATE TABLE "Frequents" (
                "regular" TEXT,
                "cafe" TEXT,
                PRIMARY KEY ("regular", "cafe")
            );
        """)

        cur.execute("""
            CREATE TABLE "Sells" (
                "cafe" TEXT,
                "drink" TEXT,
                "price" NUMERIC,
                PRIMARY KEY ("cafe", "drink")
            );
        """)

        cur.executemany(
            'INSERT INTO "Frequents" ("regular", "cafe") VALUES (?, ?);',
            FREQUENTS_DATA
        )

        cur.executemany(
            'INSERT INTO "Sells" ("cafe", "drink", "price") VALUES (?, ?, ?);',
            SELLS_DATA
        )

        conn.commit()

        print(f"\nDatabase '{db_path}' created and populated.")
        print_tables_and_schema(conn)

    except sqlite3.Error as err:
        print(f"SQLite error: {err}")

    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()