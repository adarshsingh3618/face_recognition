import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ------------------------
# Database Configuration
# ------------------------
DB_USER = "attendance_user"      # your MySQL user
DB_PASSWORD = "Admin@123"        # your MySQL password
DB_HOST = "localhost"
DB_NAME = "face_attendance"


# ------------------------
# Create Database Connection
# ------------------------
def create_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if conn.is_connected():
            return conn
    except Error as e:
        messagebox.showerror("DB Error", f"Database Connection Failed:\n{e}")
    return None


# ----------------------------------------------------
# Initialize Database (Run once)
# ----------------------------------------------------
def init_db():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()

        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                roll_no VARCHAR(50) UNIQUE NOT NULL,
                image_path VARCHAR(255)
            )
        """)

        # Attendance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                status VARCHAR(20) NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id)
                ON DELETE CASCADE
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()


# ----------------------------------------------------
# Student Functions
# ----------------------------------------------------
def add_student(name, roll_no, image_path):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO students (name, roll_no, image_path)
                VALUES (%s, %s, %s)
            """, (name, roll_no, image_path))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
        except Error as e:
            messagebox.showerror("Error", f"Student Insert Error: {e}")
        finally:
            cursor.close()
            conn.close()


def get_student_by_name(name):
    conn = create_connection()
    student = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE name = %s", (name,))
        student = cursor.fetchone()
        cursor.close()
        conn.close()
    return student


# ----------------------------------------------------
# Attendance Functions
# ----------------------------------------------------
def insert_attendance(student_id, status="Present"):
    """
    Adds attendance with CURRENT date & time
    """
    date = datetime.now().date()
    time = datetime.now().time()

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO attendance (student_id, date, time, status)
                VALUES (%s, %s, %s, %s)
            """, (student_id, date, time, status))
            conn.commit()
        except Error as e:
            messagebox.showerror("Error", f"Attendance Insert Error: {e}")
        finally:
            cursor.close()
            conn.close()


def get_attendance_records():
    conn = create_connection()
    records = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.id, s.name, s.roll_no, a.date, a.time, a.status
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            ORDER BY a.id DESC
        """)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
    return records


# ----------------------------------------------------
# View all students in Tkinter window
# ----------------------------------------------------
def show_all_students():
    conn = create_connection()
    if not conn:
        return

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    win = tk.Toplevel()
    win.title("Students List")
    win.geometry("600x400")

    table = ttk.Treeview(win, columns=("ID", "Name", "Roll", "Image"), show="headings")
    table.heading("ID", text="ID")
    table.heading("Name", text="Name")
    table.heading("Roll", text="Roll No")
    table.heading("Image", text="Image Path")

    for col in ("ID", "Name", "Roll", "Image"):
        table.column(col, width=150)

    table.pack(fill=tk.BOTH, expand=True)

    for row in rows:
        table.insert("", tk.END, values=(row["id"], row["name"], row["roll_no"], row["image_path"]))


# ----------------------------------------------------
# View attendance table in Tkinter window
# ----------------------------------------------------
def show_attendance():
    records = get_attendance_records()

    win = tk.Toplevel()
    win.title("Attendance Records")
    win.geometry("750x450")

    table = ttk.Treeview(win, columns=("ID", "Name", "Roll", "Date", "Time", "Status"), show="headings")
    table.heading("ID", text="ID")
    table.heading("Name", text="Student Name")
    table.heading("Roll", text="Roll No")
    table.heading("Date", text="Date")
    table.heading("Time", text="Time")
    table.heading("Status", text="Status")

    for col in ("ID", "Name", "Roll", "Date", "Time", "Status"):
        table.column(col, width=120)

    table.pack(fill=tk.BOTH, expand=True)

    for r in records:
        table.insert("", tk.END, values=(r["id"], r["name"], r["roll_no"], r["date"], r["time"], r["status"]))


# ----------------------------------------------------
# Run once to initialize the DB tables
# ----------------------------------------------------
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
