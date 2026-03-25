from flask import Flask, render_template, request, send_from_directory
from deepface import DeepFace
import cv2
import os
from datetime import datetime
from student_data import student_data
import pandas as pd


app = Flask(__name__)

# Ensure attendance_records folder exists
if not os.path.exists('attendance_records'):
    os.mkdir('attendance_records')

# Load known faces
path = 'students'
known_faces = []
known_names = []

for file in os.listdir(path):
    known_faces.append(os.path.join(path, file))
    known_names.append(os.path.splitext(file)[0])

# Attendance function
def mark_attendance(face_img):
    for i, known_img in enumerate(known_faces):
        temp_path = "known_Faces/temp_face.jpg"
        cv2.imwrite(temp_path, face_img)
        result = DeepFace.verify(
            temp_path,
            known_img,
            model_name="Facenet",
            distance_metric="cosine",
            enforce_detection=False
        )
        if result['verified']:
            return known_names[i]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    teacher = request.form['teacher']
    subject = request.form['subject']
    photo = request.files['photo']

    if not photo:
        return "No photo uploaded!"

    filename = "known_Faces/temp_upload.png"
    photo.save(filename)
    img = cv2.imread(filename)

    faces = DeepFace.extract_faces(img, detector_backend='retinaface', enforce_detection=False)

    attendance_list = []
    for face in faces:
        area = face['facial_area']
        x, y, w, h = area['x'], area['y'], area['w'], area['h']
        face_img = img[y:y+h, x:x+w]

        name = mark_attendance(face_img)
        if name and name not in [x['Name'] for x in attendance_list]:
            roll = student_data.get(name, "Unknown")
            now = datetime.now()
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M:%S')
            attendance_list.append({"Name": name, "Roll": roll, "Time": time})

            # Draw rectangle and name on image
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    # Save CSV
    if attendance_list:
        date_str = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H%M%S")
        out_file = f"attendance_records/{teacher}_{subject}_{date_str}_{timestamp}.csv"
        df = pd.DataFrame(attendance_list)
        df.to_csv(out_file, index=False)
        file_link = os.path.basename(out_file)
        return render_template('index.html', file_link=file_link)

    else:
        file_link = None

    # Optional: show image for 2 seconds
    cv2.imshow("Attendance Result", img)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()

    return render_template('index.html', file_link=file_link)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory('attendance_records', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)