import cv2
import pickle
import sqlite3

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainner/trainner.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="Select * from people where ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile


cam = cv2.VideoCapture(0)
#font =(FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
fontColor = (255, 255, 255)
while True:
    ret, im =cam.read()
    if ret is True:
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    else :
        continue
    faces=faceCascade.detectMultiScale(gray, 1.2,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
        Id, conf = recognizer.predict(gray[y:y+h,x:x+w])

        profile=getProfile(Id)
        if(profile!=None):
            cv2.putText(im, str("Name: ")+str(profile[1]), ( x, y+h+30), fontFace, fontScale, fontColor)
            cv2.putText(im, str("Age: ")+str(profile[2]), ( x, y+h+60), fontFace, fontScale, fontColor)
            cv2.putText(im, str("Gender: ")+str(profile[3]), ( x, y+h+90), fontFace, fontScale, fontColor)
            cv2.putText(im, str("Phone: ")+str(profile[4]), ( x, y+h+120), fontFace, fontScale, fontColor)
        else:
            cv2.putText(im, str("Unknown Person"), ( x, y+h+30), fontFace, fontScale, fontColor)


    cv2.imshow('im',im)
    if cv2.waitKey(10) & 0xFF == ord('q') :
        break
cam.release()
cv2.destroyAllWindows()
