import sqlite3
import os

DATABASE_DIR = os.path.join(os.path.dirname(__file__), 'database')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'schedule.db')

def init_db():
    # Ensure the database directory exists
    os.makedirs(DATABASE_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        renter_name TEXT NOT NULL,
        booking_date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # This allows us to run this script directly to initialize the database
    init_db()
    print(f"Database initialized at {DATABASE_PATH}")
    # Verify table creation (optional)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bookings';")
    table_exists = cursor.fetchone()
    conn.close()
    if table_exists:
        print("Table 'bookings' verified.")
    else:
        print("Error: Table 'bookings' not found after initialization.")
