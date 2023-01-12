# התכנה

import cv2
import os

# הגדרת המשתנים החיוניים לתהליך
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

# הגדרת התיקיות שבהן ממתינים התמונות שבהן מזהים את הפנים
base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, "images")


# אתחול התהליכים הנדרשים
def start_training():
    # הפעלת המצלמה
    cap = cv2.VideoCapture(0)

    # יצירת משתנים המכילים את התמונות של הפנים שזוהו
    faces = []
    ids = []

    # קבלת התמונות מהתיקייה שלהן
    for image in os.listdir(image_dir):
        img = cv2.imread(os.path.join(image_dir, image))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # זיהוי הפנים בתמונה
        faces_detected = face_cascade.detectMultiScale(gray, 1.3, 5)
        # הוספת הפנים שזוהו לרשימה
        for (x, y, w, h) in faces_detected:
            faces.append(gray[y:y + h, x:x + w])
            ids.append(int(os.path.split(image)[-1].split(".")[1]))

    # הצבעת הפנים שזוהו בתמונה
    for face in faces:
        cv2.imshow('Face', face)
        cv2.waitKey(1000)
    cv2.destroyAllWindows()

    # הגדרת האלגוריתם של הזיהוי
    recognizer.train(faces, np.array(ids))

    # שמירת התוצאות
    recognizer.save('trainer/trainer.yml')


# פונקציה לזיהוי הפנים
def detect_faces():
    # הפעלת המצלמה
    cap = cv2.VideoCapture(0)

    # הפעלת האלגוריתם של הזיהוי
    recognizer.read('trainer/trainer.yml')
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # הצבעת הפנים שזוהו בתמונה
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            # מופעלת כשהסבלנות היא גבוהה
            if (confidence < 100):
                # שאלת המשתמש את השם של הפנים שזוהו
                name = input("What is the name of the person? ")
                # שמירת השם של הפנים שזוהו בקובץ
                with open("names.txt", "a") as file:
                    file.write(name + "\n")
                cv2.putText(img, name, (x, y + h), font, 1, (255, 255, 255), 2)

            else:
                cv2.putText(img, 'No Match', (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('img', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


# הפעלת התהליכים של התוכנה
start_training()
detect_faces()