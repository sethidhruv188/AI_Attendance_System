import face_recognition 
import cv2
import numpy as np
import os
import csv 
from datetime import datetime 

path = 'Images_test'

images=[] # list of all images
names=[] # names of images

myList = os.listdir(path)

for img in myList:
    currentImg = cv2.imread(f'{path}/{img}') # used to load images
    images.append(currentImg) #appends current image to images list
    names.append(os.path.splitext(img[0])) # used to remove .jpg and append just the name to names list


def findEncodings(images): # function to find encodings from image
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # converts image to RGB
        encodeImg = face_recognition.face_encodings(img)[0] # finds encodings of image
        encodeList.append(encodeImg) # appends the encodings to list
    return encodeList

encodeListKnown=findEncodings(images) # calls the findEncodings function
print('ENCODING COMPLETE.')

video_capture = cv2.VideoCapture(0)

while True:
    success,img = video_capture.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25) # scales image to 0.25 of its original size
    imgS = cv2.cvtColor(cv2.COLOR_BGR2RGB)

    facesCurrFrame = face_recognition.face_locations(imgS) # finds locations of faces in current frame
    encodesCurrFrame = face_recognition.face_encodings(imgS,facesCurrFrame) # finds encodings of faces in current frame

    for encodeFace, faceLoc in zip(encodesCurrFrame,facesCurrFrame): # grabs one face location from facesCurrFrame and then it will grab the encoding from encodesCurrFrame
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace) # compares faces from encodeListKnown and encodeFace








