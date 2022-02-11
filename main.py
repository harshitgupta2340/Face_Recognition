import cv2 
import numpy as np
import face_recognition
import os
from datetime import datetime


path='images'
images=[]
personName=[]
mylist=os.listdir(path)
print(mylist)
for cv_img in mylist:
    current_Img=cv2.imread(f'{path}/{cv_img}')
    images.append(current_Img)
    personName.append(os.path.splitext(cv_img)[0])
print(personName)


def faceEncodings(images):

    encodelist=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

encodeListKnown=faceEncodings(images)
print("All Encodings Complete!!!!!")

# Function for Marking the Attendence
def attendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList=f.readlines()
        nameList=[]
        for line in myDataList:
            entry=line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            time_now=datetime.now()
            tStr=time_now.strftime('%H:%M:%S')
            dStr=time_now.strftime('%d/%m/%Y')
            f.writelines(f'{name},{tStr},{dStr}')








cap=cv2.VideoCapture(0)


while True:
    ret,frame=cap.read()
    faces=cv2.resize(frame,(0,0),None,0.25,0.25)
    faces=cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)

    facesCurrentFrame=face_recognition.face_locations(faces)
    encodesCurrentFrame=face_recognition.face_encodings(faces,facesCurrentFrame)


    for encodeFace,faceloc in zip(encodesCurrentFrame,facesCurrentFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)\

        matchIndex=np.argmin(faceDis)

        if matches[matchIndex]:
            name=personName[matchIndex].upper()
            # print(name)  
            y1,x2,y2,x1=faceloc 
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2) 
            cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            attendance(name)



    cv2.imshow("Camera",frame)
    if cv2.waitKey(10)==13:
        break
cap.release()
cv2.destroyAllWindows()










# import cv2                           # Package Imported

# cam=cv2.VideoCapture(0)              #For web cam
# cam.set(3,640)                       #For width of Web cam
# cam.set(4,480)                       #For height of Web cam
# cam.set(10,100)                      #For brightness 


# while True:
#     success,img=cam.read()
#     cv2.imshow("Video",img)
#     if cv2.waitKey(1000) :
#         break

# img=cv2.imread("Resources/Gaurav.jpg")
# cv2.imshow("Output",img)
# cv2.waitKey(0)