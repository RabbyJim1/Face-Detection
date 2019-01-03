import numpy as np
import cv2
import sqlite3

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


def insertOrUpdate(Id,Name,Age,Gender,Phone):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM people Where ID="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="Update people SET Name="+str(Name)+",Age="+str(Age)+",Gender="+str(Gender)+",phone="+str(Phone)+" Where ID="+str(Id)
    else:
        cmd="Insert into people(ID,Name,Age,Gender,phone) values("+str(Id)+","+str(Name)+","+str(Age)+","+str(Gender)+","+str(phone)+")"
    conn.execute(cmd)
    conn.commit()
    conn.close()


cap = cv2.VideoCapture(0)
id=input('enter your id: ')
name=input('enter your name: ')
age=input('enter your age: ')
gender=input('enter your gender: ')
phone=input('enter your phone number: ')
insertOrUpdate(id,name,age,gender,phone)
sampleNum=0
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        sampleNum=sampleNum+1
        cv2.imwrite("dataSet/User."+str(id)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        cv2.waitKey(500)

    cv2.imshow('img',img)
    cv2.waitKey(1)
    if(sampleNum>100):
        break

cap.release()
cv2.destroyAllWindows()
