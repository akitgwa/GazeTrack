from deepface import DeepFace
import cv2
import os
from datetime import datetime

path = 'students'
known_faces = []
known_names = []

for file in os.listdir(path):
    img_path = os.path.join(path, file)
    known_faces.append(img_path)
    known_names.append(os.path.splitext(file)[0])

# Attendance file
def mark_attendance(name):
    with open('attendance.csv', 'a+') as f:
        f.seek(0)
        data = f.readlines()
        names = [line.split(',')[0] for line in data]

        if name not in names:
            now = datetime.now()
            time = now.strftime('%H:%M:%S')
            f.write(f"{name},{time}\n")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    try:
        temp_path = "temp.jpg"
        cv2.imwrite(temp_path, frame)

        for i, known_img in enumerate(known_faces):
            result = DeepFace.verify(temp_path, known_img, enforce_detection=False)

            if result['verified']:
                name = known_names[i]

                mark_attendance(name)

                cv2.putText(frame, f"{name}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                break

    except:
        pass

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()