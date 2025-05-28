import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import os

# Optional: Import init_db if you want to ensure DB is initialized on startup
# from models import init_db

app = Flask(__name__)

# Define the path to the database file
# It's good practice to use an absolute path or a path relative to the app instance
DATABASE_DIR = os.path.join(os.path.dirname(__file__), 'database')
DATABASE = os.path.join(DATABASE_DIR, 'schedule.db')

# Optional: Initialize the database if it hasn't been already
# This could be done here, or via app.before_request_funcs
# For this subtask, we assume models.py was run and schedule.db exists.
# if not os.path.exists(DATABASE):
#     print(f"Database not found at {DATABASE}, attempting to initialize.")
#     try:
#         init_db() # This would require models.py to be structured to allow this call
#         print("Database initialized.")
#     except Exception as e:
#         print(f"Error initializing database: {e}")
# else:
#     print(f"Database found at {DATABASE}")


def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

@app.route('/')
def index():
    """Displays existing bookings."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, renter_name, booking_date, start_time, end_time, created_at FROM bookings ORDER BY booking_date ASC, start_time ASC")
        bookings_data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        bookings_data = [] # Return empty list on error
    finally:
        if conn:
            conn.close()
    
    # The actual index.html will be created in a later step
    return render_template('index.html', bookings=bookings_data)

@app.route('/add_booking', methods=['POST'])
def add_booking():
    """Adds a new booking to the database."""
    renter_name = request.form.get('renter_name')
    booking_date = request.form.get('booking_date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    # Basic backend validation
    if not all([renter_name, booking_date, start_time, end_time]):
        # For MVP, we'll just redirect without a flash message
        # In a full app, you'd typically flash an error message to the user
        print("Form validation failed: One or more fields are empty.")
        return redirect(url_for('index'))

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (renter_name, booking_date, start_time, end_time) VALUES (?, ?, ?, ?)",
            (renter_name, booking_date, start_time, end_time)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error on insert: {e}")
        # Optionally, handle the error more gracefully (e.g., flash message)
    finally:
        if conn:
            conn.close()
            
    return redirect(url_for('index'))

@app.route('/delete_booking/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    """Deletes a booking from the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error on delete: {e}")
        # Optionally, handle the error more gracefully (e.g., flash message)
    finally:
        if conn:
            conn.close()
            
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Note: The host '0.0.0.0' makes the app accessible from any IP on the network.
    # For development, '127.0.0.1' (localhost) is often used.
    # The sandbox environment might require 0.0.0.0 to be accessible.
    app.run(debug=True, host='0.0.0.0', port=5000)
