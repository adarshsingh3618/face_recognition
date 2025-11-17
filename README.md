# 📘 Face Recognition Attendance System
A complete attendance management system using **Python**, **OpenCV**, **Face Recognition**, and **MySQL** with a GUI built in **Tkinter**.

## 🚀 Features
- Face Recognition with 2‑second verification  
- Automatic attendance marking  
- Add Students with webcam capture  
- Real-time status panel  
- MySQL database integration  
- Tkinter GUI dashboard

## 📂 Project Structure
```
face_attendance/
│── main.py
│── recognition.py
│── attendance.py
│── add_student_gui.py
│── db.py
│── images/
│── test_student.py
│── README.md
```

## 🛠 Installation

### 1. Install Python (Recommended: Python 3.10)

### 2. Install required packages
Create requirements.txt:
```
opencv-python
face_recognition
numpy
mysql-connector-python
pillow
```

Install using:
```
pip install -r requirements.txt
```

### 3. Install MySQL and create database
Run:
```
CREATE DATABASE face_attendance;
CREATE USER 'attendance_user'@'localhost' IDENTIFIED BY 'Admin@123';
GRANT ALL PRIVILEGES ON face_attendance.* TO 'attendance_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Initialize the database
```
python db.py
```

### 5. Start the application
```
python main.py
```

## 📸 Adding Students
Photos must be saved in:
```
images/StudentName/photo.jpg
```

The folder name must match the student's name exactly.

## 🎥 How Recognition Works
1. System detects face  
2. Confirms for 2 seconds  
3. Marks attendance  
4. Shows confirmation  
5. Exits smoothly  

## 📦 Running on Another PC
- Install Python  
- Install dependencies  
- Install CMake (if needed)  
- Install MySQL server  
- Copy entire project folder  
- Run:
```
python main.py
```

## 🧠 Notes
- Use Python 3.8–3.11  
- Ensure MySQL credentials match `db.py`  
- Camera is required  
- Folder structure must not change

## ✅ Enjoy your Face Recognition Attendance System!
