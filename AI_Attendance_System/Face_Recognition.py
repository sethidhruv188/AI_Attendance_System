import face_recognition 
import cv2
import numpy as np
import os
import csv 
from datetime import datetime 

path = 'Images_test'

images=[] # list of all images
classNames=[] # names of images

myList = os.listdir(path)

for img in myList:
    currentImg = cv2.imread(f'{path}/{img}') # used to load images
    images.append(currentImg) #appends current image to images list
    classNames.append(os.path.splitext(img)[0]) # used to remove .jpg and append just the name to classNames list


def findEncodings(images): # function to find encodings from image
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # converts image to RGB
        encodeImg = face_recognition.face_encodings(img)[0] # finds encodings of image
        encodeList.append(encodeImg) # appends the encodings to list
    return encodeList

def markAttendance(name): # function to mark attendance in .csv file
    with open('Attendance.csv','r+') as f: # opens attendance.csv file
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',') # splits the entry based on comma
            nameList.append(entry[0]) # appends the name to nameList

        if name not in nameList:
            now = datetime.now() 
            dateString = now.strftime('%H:%M:%S') # formats the dateString into HH:MM:SS format
            f.writelines(f'\n{name},{dateString}')


encodeListKnown=findEncodings(images) # calls the findEncodings function
print('ENCODING COMPLETE.')

video_capture = cv2.VideoCapture(0)

while True:
    success,img = video_capture.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25) # scales image to 0.25 of its original size
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    facesCurrFrame = face_recognition.face_locations(imgS) # finds locations of faces in current frame
    encodesCurrFrame = face_recognition.face_encodings(imgS,facesCurrFrame) # finds encodings of faces in current frame

    for encodeFace, faceLoc in zip(encodesCurrFrame,facesCurrFrame): # grabs one face location from facesCurrFrame and then it will grab the encoding from encodesCurrFrame
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace) # compares faces from encodeListKnown and encodeFace
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace) # gives us the face distance in the form of a list - lowest distance is best match
        matchIndex = np.argmin(faceDis) # gives us the minimum value

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # code to draw a rectangle around the face and display the name of the person
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,255,255),2)
            markAttendance(name) # calls the function to mark attendance
       
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)
         
            









