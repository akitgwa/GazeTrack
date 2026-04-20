# 📸 Smart Attendance System (GazeTrack)

## 📌 Overview
Smart Attendance System is a prototype application that automates attendance marking using image processing and face recognition.

Instead of manually calling out names, a teacher can simply upload a classroom photo. The system detects faces, matches them with registered students, and generates attendance automatically.

---

## 🎯 Problem Statement

Traditional attendance systems:
- Are time-consuming ⏳  
- Allow proxy attendance ❌  
- Are not scalable for large classrooms  

This project aims to provide a **faster, automated, and more reliable attendance solution**.

---

## 💡 Solution

This system:
1. Takes a classroom image as input  
2. Detects faces in the image  
3. Matches them with stored student images  
4. Marks attendance automatically  
5. Exports attendance into a CSV file  

---

## 🚀 Features

- 📷 Upload classroom image  
- 🧠 Face detection and recognition  
- 🧾 Automatic attendance marking  
- 📊 CSV export of attendance  
- 🔍 Unknown face handling  

---

## 🛠️ Tech Stack

- Python  
- Flask  
- OpenCV  
- DeepFace  
- HTML/CSS  

---

## 📂 Project Structure

```
SmartAttendenceSystem/
│
├── app.py                  # Main Flask application
├── student_data.py         # Student name & roll mapping
├── requirements.txt
├── README.md
│
├── templates/              # HTML files
├── static/                 # CSS / JS
│
├── students/               # Known student images
├── groupPhotos/            # Classroom images
├── known_Faces/            # Unknown detected faces
├── attendance_records/     # Generated CSV files
│
├── old_files/              # Experimental files
```

## ⚙️ Project Workflow

### Step 1: Add Student Data
- Add student images in `students/` folder  
- Image name = Student name (e.g., `Ganga.jpg`)  

### Step 2: Update Student Records
- Open `student_data.py`  
- Add entry in dictionary:
```python
"Ganga": 240204922
```

### Step 3: Run Application

```bash
pip install -r requirements.txt
python app.py
```

### Step 4: Use the System

- Open browser  
- Go to:  
  http://127.0.0.1:10000
  
- Upload classroom image  
- Attendance will be generated automatically 
