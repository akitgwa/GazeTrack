import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load image (Side view photos it cannot detect which are group4.png and group5.png)
img = cv2.imread('groupPhotos/group2.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# Draw boxes
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

# Count
count = len(faces)
cv2.putText(img, f"Count: {count}", (20,50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

cv2.imshow("Group Image Test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()