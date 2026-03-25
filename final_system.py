from deepface import DeepFace
import cv2
import os
from datetime import datetime
from student_data import student_data

# Load student images
path = 'students'
known_faces = []
known_names = []

for file in os.listdir(path):
    img_path = os.path.join(path, file)
    known_faces.append(img_path)
    known_names.append(os.path.splitext(file)[0])

# Attendance function
def mark_attendance(name):
    roll = student_data.get(name, "Unknown")

    with open('attendance.csv', 'a+') as f:
        f.seek(0)
        data = f.readlines()
        names = [line.split(',')[0] for line in data]

        if name not in names:
            now = datetime.now()
            time = now.strftime('%H:%M:%S')
            f.write(f"{name},{roll},{time}\n")

cap = cv2.VideoCapture(0)

# Resolution improve
cap.set(3, 1280)
cap.set(4, 720)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    try:
        # Detect multiple faces
        faces = DeepFace.extract_faces(
            frame,
            detector_backend='retinaface',
            enforce_detection=False
        )

        for face in faces:
            x, y, w, h = face['facial_area'].values()

            # Crop face
            face_img = frame[y:y+h, x:x+w]

            temp_path = "temp.jpg"
            cv2.imwrite(temp_path, face_img)

            # Compare with known faces
            for i, known_img in enumerate(known_faces):
                result = DeepFace.verify(temp_path, known_img, enforce_detection=False)

                if result['verified']:
                    name = known_names[i]

                    mark_attendance(name)

                    cv2.putText(frame, f"{name}", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

                    break

            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    except:
        pass

    cv2.imshow("Smart Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()