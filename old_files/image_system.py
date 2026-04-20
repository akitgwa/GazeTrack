from deepface import DeepFace
import cv2
import os
from student_data import student_data
from datetime import datetime

# Load known faces
path = 'students'
known_faces = []
known_names = []

for file in os.listdir(path):
    known_faces.append(os.path.join(path, file))
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

# Load group image
img = cv2.imread('ThisMe.jpg')

# Detect faces
faces = DeepFace.extract_faces(
    img,
    detector_backend='retinaface',
    enforce_detection=False
)

print("Faces detected:", len(faces))   # 👈 YAHAN add kiya hai

# Loop through faces
for face in faces:
    area = face['facial_area']
    x, y, w, h = area['x'], area['y'], area['w'], area['h']

    face_img = img[y:y+h, x:x+w]

    temp_path = "temp.jpg"
    cv2.imwrite(temp_path, face_img)

    # Compare with known faces
    for i, known_img in enumerate(known_faces):
        result = DeepFace.verify(
            temp_path,
            known_img,
            model_name="Facenet",
            distance_metric="cosine",
            enforce_detection=False
        )

        print("Checking with:", known_names[i],
              "→", result['verified'], "Distance:", result['distance'])

        if result['verified']:
            name = known_names[i]

            mark_attendance(name)

            cv2.putText(img, name, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

            break

    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

# Show result
cv2.imshow("Group Image Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()