🧑‍🏫 Face Recognition Attendance System
A Python-based real-time face recognition project that automatically marks attendance and stores it with timestamps.
This project uses OpenCV, face_recognition, and MySQL to detect faces, save attendance logs, and manage a database of registered students.
Useful for colleges, classrooms, labs, offices, and automated attendance systems.
🚀 Features
🎥 Real-time face recognition using webcam
🧠 Uses the powerful face_recognition Python library
🗂 Automatically marks attendance with name, ID, time, and date
💾 Stores student data in MySQL database
🏷 Loads face images from ImagesAttendance/ folder
🖼 GUI to add a new student with image
📁 Saves attendance logs in the attendance/ folder
🐍 Easy to run on any system with Python and MySQL installed
🧩 Project Structure
face_attendance/
│── main.py                    # Main script to run face recognition
│── attendance.py              # Handles attendance logic
│── recognition.py             # Face recognition logic
│── db.py                      # Database connection & queries
│── add_student_gui.py         # GUI to add students
│── ImagesAttendance/          # Folder containing student images
│── attendance/                # Attendance log files
│── app.log                    # Logs for debugging
│── test_student.py            # Testing add_student function
│── .gitignore                 # Ignored files
🔧 Technologies Used
Backend & Recognition
Python 3
OpenCV
face_recognition
NumPy
Database
MySQL (CRUD operations using mysql-connector-python)
Interface
Tkinter (for student registration GUI)
DevOps Tools (Optional for Deployment)
Docker (containerize the app)
GitHub Actions
AWS EC2 (deploy your server)
🛠 Installation Guide
1️⃣ Clone the repository
git clone git@github.com:adarshsingh3618/face_recognition.git
cd face_recognition
2️⃣ Create a Python virtual environment
python3 -m vvenv venv
source venv/bin/activate
3️⃣ Install required packages
pip install -r requirements.txt
🗄 MySQL Database Setup
1. Start MySQL server
2. Create a database:
CREATE DATABASE attendance_system;
3. Update your DB credentials in db.py
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_NAME = "attendance_system"
4. Run the student registration test
python3 test_student.py
▶️ Running the Application
Start face recognition attendance:
python3 main.py
Add a new student:
python3 add_student_gui.py
📸 Adding Student Images
Place a clear image of the student's face inside:
ImagesAttendance/Name.jpg
Example:
ImagesAttendance/Adarsh.jpg
📤 Attendance Export
Attendance files will be saved in:
attendance/attendance_YYYY-MM-DD.csv
Each row contains:
Student name
Student ID
Time
Date
🚀 Future Improvements
Integrate with AWS Rekognition
Create a web interface (Flask/Django)
Add QR code backup attendance
Add role-based access (Admin/Teacher)
Build Docker support
Host on EC2 with NGINX
🤝 Contributions
Pull requests are welcome!
If you find bugs or want improvements, feel free to open an issue.
👨‍💻 Author
Adarsh Singh
📧 Email: adarshsingh3618@gmail.com
🔗 GitHub: https://github.com/adarshsingh3618
🔗 LinkedIn: https://www.linkedin.com/in/adarshsingh3618
⭐ Support
If you like this project, please ⭐ the repo — it motivates continued development!
