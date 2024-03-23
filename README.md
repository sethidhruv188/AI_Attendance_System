# **AI Attendance System**
The AI Attendance System is a facial recognition-based attendance tracking application designed to streamline the process of recording attendance for individuals. Leveraging computer vision and facial recognition technology, this system allows for efficient and accurate attendance tracking without the need for manual input.

## **Features**
- Facial Recognition: Utilizes face recognition algorithms to identify individuals from webcam footage.

- Database Integration: Stores facial encodings in a MySQL database for efficient retrieval and recognition.

- Automatic Encoding: Automatically adds new individuals to the database by extracting and storing facial encodings from images in a specified folder.

- Attendance Logging: Marks attendance in a CSV file, recording timestamps under the respective date for each recognized individual.

- Multi-Day Support: Capable of storing attendance data for multiple days in the same CSV file, ensuring that previous data is preserved and not overridden.

## **How It Works**
- Database Initialization: The system initializes a MySQL database to store facial encodings and individual identities.

- Encoding Complete: Facial encodings are extracted from images stored in a designated folder and stored in the database.

- Webcam Recognition: Upon completion of encoding, the webcam is activated to recognize individuals in real-time.

- Attendance Marking: Recognized individuals are marked as present in an attendance CSV file, with timestamps recorded under the respective date.

## **Usage**
To use the AI Attendance System:

- Ensure that the required libraries (OpenCV, face_recognition, pymysql) are installed.

- Place images of individuals in a designated folder, ensuring that each image is labeled with the individual's name.

- Run the program to initialize the database and perform facial encoding.

- Once encoding is complete, the webcam will activate, and attendance tracking will commence automatically.

- View attendance records in the generated CSV file, which will contain names in column A and dates with timestamps in subsequent columns.

## **Installation**
To install the required libraries, run the following commands:

![image](https://github.com/sethidhruv188/AI_Attendance_System/assets/140970083/23511f5b-7f1f-476d-a305-0d84522a4630)


# **Contributors**
- Dhruv Sethi

# **License**
- This project is licensed under the GNU General Public License v3.0 (GPL-3.0). You can find a copy of the license in the LICENSE file.
