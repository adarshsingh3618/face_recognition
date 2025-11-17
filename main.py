import tkinter as tk
from tkinter import messagebox
import multiprocessing
import logging
import os
import add_student_gui


logging.basicConfig(filename="app.log", level=logging.ERROR,
                    format="%(asctime)s %(levelname)s: %(message)s")

def run_recognition_process():
    """
    Run recognition completely isolated from Tkinter (macOS fix).
    """
    import recognition
    import cv2
    import face_recognition
    import time

    encodings, names = recognition.load_known_faces()
    if not encodings:
        print("No faces found.")
        return

    cap = cv2.VideoCapture(0)
    marked = set()
    status_messages = ["System ready..."]

    detected_name = None
    detection_time = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if detected_name is None:
            small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

            locations = face_recognition.face_locations(rgb_small)
            encs = face_recognition.face_encodings(rgb_small, locations)

            for enc, loc in zip(encs, locations):
                matches = face_recognition.compare_faces(encodings, enc)
                distances = face_recognition.face_distance(encodings, enc)

                name = "Unknown"
                if len(distances) > 0:
                    best = distances.argmin()
                    if matches[best]:
                        name = names[best]

                top, right, bottom, left = [v * 4 for v in loc]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                if name != "Unknown":
                    detected_name = name
                    detection_time = time.time()
                    status_messages.append(f"Detected {name}. Confirming...")
                    break

        else:
            status_messages.append(f"Confirming {detected_name}...")

            if time.time() - detection_time >= 2:
                from attendance import mark_attendance
                if detected_name not in marked:
                    mark_attendance(detected_name, detected_name)
                    marked.add(detected_name)
                    status_messages.append(f"Attendance marked for {detected_name} ✅")
                else:
                    status_messages.append(f"Attendance already marked for {detected_name} ⚠️")

                final = recognition.draw_status_panel(frame, status_messages)
                cv2.imshow("Face Recognition Attendance", final)
                cv2.waitKey(3000)
                break

        display = recognition.draw_status_panel(frame, status_messages)
        cv2.imshow("Face Recognition Attendance", display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


class FaceAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        tk.Label(root, text="Face Recognition Attendance System",
                 font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(root, text="Start Recognition", width=20, height=2,
                  command=self.start_recognition_process).pack(pady=10)

        tk.Button(root, text="Manage Database", width=20, height=2,
                  command=self.manage_database).pack(pady=10)
        

        tk.Button(root, text="Add Student", width=20, height=2,
          command=self.open_add_student).pack(pady=10)
        

        tk.Button(root, text="Exit", width=20, height=2,
                  command=self.exit_app).pack(pady=10)

        multiprocessing.set_start_method("spawn", force=True)

    def start_recognition_process(self):
        try:
            p = multiprocessing.Process(target=run_recognition_process)
            p.start()
        except Exception as e:
            logging.error(f"Recognition failed: {e}")
            messagebox.showerror("Error", f"Recognition failed: {e}")

    def manage_database(self):
        try:
            import db
            db.show_all_students()
        except Exception as e:
            logging.error(f"DB error: {e}")
            messagebox.showerror("Error", f"Database error: {e}")

    def open_add_student(self):
        add_student_gui.AddStudentWindow(self.root)


    def exit_app(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    FaceAttendanceApp(root)
    root.mainloop()
