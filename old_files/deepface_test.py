from deepface import DeepFace
import cv2

# Start camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera error")
        break

    try:
        # Analyze face
        result = DeepFace.analyze(frame, actions=['age', 'gender'], enforce_detection=False)

        # Get gender
        gender = result[0]['dominant_gender']

        # Show text
        cv2.putText(frame, f"Gender: {gender}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    except:
        pass

    cv2.imshow("DeepFace Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()