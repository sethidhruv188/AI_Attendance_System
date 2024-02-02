This project is a basic prototype of an AI_Attendance System which works through facial recognition
- Uses python libraries face_recognition, os, numpy, datetime, opencv and csv
- Face_Recognition.py is the python file where all the logic is present, Attendance.csv is the file in which the program marks attendance and Images_test folder has images in it for testing the program
- This project takes images from the Images_test folder and creates encodings for the images
- After this, input is taken from the webcam and image is detected through previously saved encodings
- User's name is displayed on screen and they are marked present in the Attendance.csv file

  # Upcoming changes:
  - To create a firebase database which can load and encode images faster
  - Create a better front-end and user-friendly interface
  - Try to store attendance in the same .csv file for multiple days without overriding previous data
