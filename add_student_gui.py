import tkinter as tk
from tkinter import messagebox
import cv2
import os

from db import add_student

IMAGE_SAVE_PATH = "images/"  


class AddStudentWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Add Student")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        tk.Label(self.window, text="Add New Student",
                 font=("Arial", 18, "bold")).pack(pady=20)

        # Name entry
        tk.Label(self.window, text="Student Name:", font=("Arial", 12)).pack()
        self.name_entry = tk.Entry(self.window, width=30)
        self.name_entry.pack(pady=5)

        # Roll no
        tk.Label(self.window, text="Roll Number:", font=("Arial", 12)).pack()
        self.roll_entry = tk.Entry(self.window, width=30)
        self.roll_entry.pack(pady=5)

        # Capture button
        tk.Button(self.window, text="Capture Image", width=20,
                  command=self.capture_image).pack(pady=20)

        # Save student
        tk.Button(self.window, text="Save Student", width=20,
                  command=self.save_student_data).pack(pady=20)

        self.captured_image_path = None

    def capture_image(self):
        name = self.name_entry.get()

        if not name:
            messagebox.showwarning("Input required", "Enter student name first.")
            return

        # Create folder for student
        student_folder = os.path.join(IMAGE_SAVE_PATH, name)
        os.makedirs(student_folder, exist_ok=True)

        cap = cv2.VideoCapture(0)
        messagebox.showinfo("Info", "Press SPACE to capture photo.\nPress ESC to cancel.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Capture Student Photo", frame)

            key = cv2.waitKey(1)

            if key == 32:  # SPACE = capture
                image_path = os.path.join(student_folder, f"{name}.jpg")
                cv2.imwrite(image_path, frame)
                self.captured_image_path = image_path
                messagebox.showinfo("Success", f"Photo saved at {image_path}")
                break

            elif key == 27:  # ESC = cancel
                break

        cap.release()
        cv2.destroyAllWindows()

    def save_student_data(self):
        name = self.name_entry.get()
        roll_no = self.roll_entry.get()

        if not name or not roll_no:
            messagebox.showwarning("Missing Info", "Name and Roll number are required.")
            return

        if not self.captured_image_path:
            messagebox.showwarning("Missing Image", "Please capture an image first.")
            return

        # Save to database
        add_student(name, roll_no, self.captured_image_path)
        messagebox.showinfo("Success", f"Student {name} added successfully!")
        self.window.destroy()
