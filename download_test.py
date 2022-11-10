#Face Detection

import cv2
import numpy as np

haarcascade = "models/haarcascade_frontalface_default.xml"

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

while True:
    success, img = cap.read()
    faceCascade = cv2.CascadeClassifier(haarcascade)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(img_gray, 1.1, 4)
    if len(faces) != 0:
        print(faces)
    else:
        print("done")
    # for (x,y,w,h) in faces:
    #     cv2.rectangle(img,(x,y), (x+w,y+h), (0,255,0), 2)

    # cv2.imshow("face",img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break