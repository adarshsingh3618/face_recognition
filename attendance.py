"""
Attendance marking logic for Face Recognition Attendance System
"""

import csv
import os
from datetime import datetime
from db import insert_attendance  # function from db.py

# Path for fallback CSV logging inside attendance folder
ATTENDANCE_CSV = os.path.join("attendance", "attendance_log.csv")


def mark_attendance(student_id: str, student_name: str):
    """
    Marks attendance for a student.
    - First logs into database using db.py
    - Also appends to a CSV file as backup
    - Skips if already marked today
    """

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Step 0: Check if already marked today
    if has_already_marked(student_id, date_str):
        print(f"[INFO] {student_name} already marked on {date_str}. Skipping.")
        return

    # Step 1: Insert into database
    try:
        insert_attendance(student_id, date_str, time_str)
        print(f"[DB] Attendance marked for {student_name} ({student_id}) at {time_str}")
    except Exception as e:
        print(f"[DB ERROR] Could not insert attendance: {e}")
        raise

    # Step 2: Append into CSV as backup
    try:
        os.makedirs("attendance", exist_ok=True)  # ensure folder exists
        with open(ATTENDANCE_CSV, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([student_id, student_name, date_str, time_str])
        print(f"[CSV] Attendance logged for {student_name}")
    except Exception as e:
        print(f"[CSV ERROR] Could not write attendance: {e}")
        raise


def has_already_marked(student_id: str, date: str) -> bool:
    """
    Checks if student has already marked attendance for the given date.
    This can query DB or fallback CSV.

    Args:
        student_id (str): Unique ID of student
        date (str): Date in format YYYY-MM-DD

    Returns:
        bool: True if attendance already exists
    """
    try:
        with open(ATTENDANCE_CSV, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[0] == student_id and row[2] == date:
                    return True
    except FileNotFoundError:
        return False

    return False
