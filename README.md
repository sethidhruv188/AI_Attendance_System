# **AI Attendance System**
The AI Attendance System is a facial recognition-based attendance tracking application designed to streamline the process of recording attendance for individuals. Leveraging computer vision and facial recognition technology, this system allows for efficient and accurate attendance tracking without the need for manual input.

## **Features**
- <ins>Facial Recognition:</ins> Utilizes face recognition algorithms to identify individuals from webcam footage.

- <ins>Database Integration:</ins> Stores facial encodings in a MySQL database for efficient retrieval and recognition.

- <ins>Automatic Encoding:</ins> Automatically adds new individuals to the database by extracting and storing facial encodings from images in a specified folder.

- <ins>Attendance Logging:</ins> Marks attendance in a CSV file, recording timestamps under the respective date for each recognized individual.

- <ins>Multi-Day Support:</ins> Capable of storing attendance data for multiple days in the same CSV file, ensuring that previous data is preserved and not overridden.

## **How It Works**
- <ins> Database Initialization </ins>: The system initializes a MySQL database to store facial encodings and individual identities.

- <ins> Encoding Complete </ins>: Facial encodings are extracted from images stored in a designated folder and stored in the database.

- <ins> Webcam Recognition </ins>: Upon completion of encoding, the webcam is activated to recognize individuals in real-time.

- <ins> Attendance Marking </ins>: Recognized individuals are marked as present in an attendance CSV file, with timestamps recorded under the respective date.


## **Usage**
To use the AI Attendance System:

- Ensure that the required libraries (OpenCV, face_recognition, pymysql) are installed.

- Place images of individuals in a designated folder, ensuring that each image is labeled with the individual's name.

- Run the program to initialize the database and perform facial encoding.

- Once encoding is complete, the webcam will activate, and attendance tracking will commence automatically.

- View attendance records in the generated CSV file, which will contain names in column A and dates with timestamps in subsequent columns.

## **Installation**
1. Clone the repository:
git clone https://github.com/sethidhruv188/AI-attendance-system.git

2. Install dependencies:
pip install -r requirements.txt


# **Contributors**
- Dhruv Sethi

# **License**
- This project is licensed under the [GNU General Public License v3.0 (GPL-3.0)](https://opensource.org/licenses/GPL-3.0). You can find a copy of the license in the [LICENSE](LICENSE) file.

# **Acknowledgements**
- This project utilizes the [face_recognition](https://github.com/ageitgey/face_recognition) library for face recognition.
- Special thanks to [OpenCV](https://opencv.org/) for webcam integration.

