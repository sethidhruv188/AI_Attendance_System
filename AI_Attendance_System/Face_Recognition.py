import pymysql  # Used for connecting to MySQL database
import face_recognition  # Provides face recognition functionality
import cv2  # Used for webcam access and image processing
import numpy as np  # Provides support for numerical arrays and operations
import pickle # Used for serializing and deserializing Python objects
from datetime import datetime  # Provides functionality to work with dates and timestamps
import os  # Used for interacting with the operating system
import threading  # Provides support for multithreading

# MySQL Database Configuration
db_host = '127.0.0.1'  # Database host address
db_user = 'root'  # Database username
db_password = 'sethidhruv188'  # Database password
db_name = 'faces'  # Database name

# Establish MySQL connection
connection = pymysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name, charset='utf8', use_unicode=True)
cursor = connection.cursor()

def initialize_database():
    """
    Initialize the MySQL database by creating the 'testFace' table if it doesn't exist.
    """
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS testFace (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            face_encoding BLOB
        )
    """)
    connection.commit()

def get_known_encodings():
    """
    Retrieve known face encodings from the database.
    """
    cursor.execute("SELECT face_encoding FROM testFace")
    return [pickle.loads(row[0]) for row in cursor.fetchall()]

def get_class_names():
    """
    Retrieve known class names from the database.
    """
    cursor.execute("SELECT name FROM testFace")
    return [row[0] for row in cursor.fetchall()]

def store_encoding_to_db(name, encoding):
    """
    Store face encoding and name in the 'testFace' table.
    """
    encoding_bytes = pickle.dumps(encoding)
    cursor.execute("INSERT INTO testFace (name, face_encoding) VALUES (%s, %s)", (name, encoding_bytes))
    connection.commit()

def mark_attendance(name):
    """
    Mark attendance in the 'Attendance.csv' file.
    """
    with open('Attendance.csv', 'r+') as f:
        my_data_list = f.readlines()
        name_list = [line.split(',')[0] for line in my_data_list]

        if name not in name_list:  # Check if the name is not already in the attendance list
            now = datetime.now()
            date_string = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{date_string}')  # Append the name and timestamp to the attendance file

def webcam_thread():
    """
    Separate thread for capturing frames from the webcam.
    """
    video_capture = cv2.VideoCapture(0)  # Initialize video capture from webcam

    # Initialize face recognition
    known_encodings = get_known_encodings()
    class_names = get_class_names()

    print('ENCODING COMPLETE.')  # Print message after retrieving known face encodings

    try:
        while True:
            success, img = video_capture.read()  # Read a frame from the webcam
            img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # Resize the frame for faster processing
            img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

            faces_curr_frame = face_recognition.face_locations(img_s)  # Find face locations in the current frame
            encodes_curr_frame = face_recognition.face_encodings(img_s, faces_curr_frame)  # Find face encodings in the current frame

            for encode_face, face_loc in zip(encodes_curr_frame, faces_curr_frame):
                matches = face_recognition.compare_faces(known_encodings, encode_face)
                face_dis = face_recognition.face_distance(known_encodings, encode_face)
                match_index = np.argmin(face_dis)

                if matches[match_index]:  # Check if the face matches a known face
                    name = class_names[match_index].upper()

                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                    # Calculate the optimal text position
                    text_width, text_height = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 2)[0]
                    max_text_width = x2 - x1 - 12  # Maximum width for text within the rectangle
                    font_scale = min(1, max_text_width / text_width)
                    text_x = x1 + 6
                    text_y = max(y1 + text_height + 6, y2 - 6)

                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale, (255, 255, 255), 2)

                    if name not in class_names:
                        store_encoding_to_db(name, encode_face)
                        class_names.append(name)

                    mark_attendance(name)

            cv2.imshow('Webcam', img)  # Display the frame with face recognition

            key = cv2.waitKey(1)
            if key == 27 or key == 113:  # Break the loop if 'esc' or 'q' is pressed
                break

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        video_capture.release()  # Release the video capture
        cv2.destroyAllWindows()  # Close OpenCV windows

def main():
    initialize_database()

    webcam_thread_instance = threading.Thread(target=webcam_thread)  # Create a thread for the webcam
    webcam_thread_instance.start()  # Start the webcam thread

    webcam_thread_instance.join()  # Wait for the webcam thread to finish

    connection.close()  # Close the MySQL connection

if __name__ == "__main__":
    main()  # Execute the main function when the script is run
