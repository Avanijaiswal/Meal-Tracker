import sqlite3
from datetime import datetime
DB_FILE = "meal_tracker.db"

def get_connection():
    # Opens (or creates) the database file
    return sqlite3.connect(DB_FILE)

def init_db():
    # Creates the meals table if it doesn't exist yet
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                dish_name TEXT NOT NULL,
                calories REAL,
                protein_g REAL,
                carbs_g REAL,
                fat_g REAL,
                sodium_mg REAL,
                flags TEXT
            )
        """)
        conn.commit()
    finally:
        conn.close()


def log_meal(dish_name, nutrients_dict, calories, flags):
    init_db()  # make sure the table exists

    def get_qty(key):
        return nutrients_dict.get(key, {}).get("quantity", 0)

    now = datetime.now()

    conn = get_connection()
    try:
        # The ? marks are placeholders: sqlite fills them safely
        conn.execute(
            """
            INSERT INTO meals
            (date, time, dish_name, calories, protein_g, carbs_g, fat_g, sodium_mg, flags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                dish_name.title(),
                round(calories, 1) if calories is not None else None,
                round(get_qty("PROCNT"), 1),
                round(get_qty("CHOCDF"), 1),
                round(get_qty("FAT"), 1),
                round(get_qty("NA"), 1),
                "; ".join(flags),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_all_meals():
    init_db()
    conn = get_connection()
    try:
        cursor = conn.execute("SELECT * FROM meals ORDER BY id")
        return cursor.fetchall()
    finally:
        conn.close()
