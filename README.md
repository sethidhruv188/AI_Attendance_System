Facial Attendance System
The Facial Attendance System is a project aimed at automating attendance marking using facial recognition technology. It leverages various libraries such as OpenCV and face_recognition to achieve its functionality.

Features
Image Storage: Images of individuals are stored in a designated folder on the local machine, with each image file named after the respective individual.

SQL Database: An SQL database is utilized to store the facial encodings of individuals. This enables efficient retrieval and comparison during the recognition process.

Automatic Encoding: When a new individual's image is detected in the folder but not present in the database, the system automatically extracts and stores their facial encodings in the SQL database.

Recognition: Once the encoding process is complete, the system initializes the webcam to recognize faces in real-time.

Attendance Marking: Upon recognizing a face, the system marks the attendance of the individual in a CSV file. The CSV file contains columns for names (Column A) and dates (Column B), with timestamps recorded under the respective date for each individual.

Multi-Day Attendance: The system is capable of storing attendance data for multiple days within the same CSV file, ensuring that previous data is not overridden.

Getting Started
To use the Facial Attendance System, follow these steps:

Set up Image Folder: Store images of individuals in a designated folder on your local machine.

Initialize Database: Run the system to initialize the SQL database and store facial encodings of individuals.

Run the System: Launch the system, which will begin webcam-based facial recognition and attendance marking.

Review Attendance: Check the generated CSV file to review the attendance data captured by the system.

Dependencies
Python 3.x
OpenCV
face_recognition
pymysql
Contributors
[Your Name]
License
This project is licensed under the [License Name] License - see the LICENSE file for details.This project is a basic prototype of an AI_Attendance System which works through facial recognition
- Uses python libraries face_recognition, os, numpy, datetime, opencv and csv
- Face_Recognition.py is the python file where all the logic is present, Attendance.csv is the file in which the program marks attendance and Images_test folder has images in it for testing the program
- This project takes images from the Images_test folder and creates encodings for the images
- After this, input is taken from the webcam and image is detected through previously saved encodings
- User's name is displayed on screen and they are marked present in the Attendance.csv file

  # Upcoming changes:
  - To create a firebase database which can load and encode images faster
  - Create a better front-end and user-friendly interface
  - Try to store attendance in the same .csv file for multiple days without overriding previous data
