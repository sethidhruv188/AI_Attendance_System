import pymysql
import face_recognition
import cv2
import numpy as np
import pickle
from datetime import datetime
import os
import glob
import threading
import csv

# MySQL Database Configuration
db_host = '127.0.0.1'  # Database host address
db_user = 'root'  # Database username
db_password = 'sethidhruv188'  # Database password
db_name = 'faces'  # Database name

# Establish MySQL connection
connection = pymysql.connect(host=db_host, user=db_user, passwd=db_password, database=db_name, charset='utf8',
                             use_unicode=True)
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


def is_name_present(name):
    """
    Check if the provided name is already present in the 'Attendance.csv' file.
    """
    if not os.path.isfile('Attendance.csv'):
        return False

    with open('Attendance.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == name:
                return True
    return False

def mark_attendance(name, present=True):
    """
    Mark attendance in the 'Attendance.csv' file.
    """
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d')
    time_string = now.strftime('%H:%M:%S')

    # Create or append to the CSV file
    attendance_data = []

    # If the file exists, read existing data
    if os.path.isfile('Attendance.csv'):
        with open('Attendance.csv', 'r') as f:
            reader = csv.reader(f)
            attendance_data = list(reader)

    # Ensure that the attendance data has consistent number of columns
    max_columns = max(len(row) for row in attendance_data)
    for row in attendance_data:
        while len(row) < max_columns:
            row.append(None)  # Fill missing cells with None

    # Find the index of the name in the first column
    name_index = -1
    for i, row in enumerate(attendance_data):
        if len(row) > 0 and row[0] == name:
            name_index = i
            break

    if name_index == -1:
        # Name not found, add a new row for the name
        new_row = [name] + [None] * (len(attendance_data[0]) - 1 if attendance_data else 0)  # -1 to exclude the name column
        attendance_data.append(new_row)
        name_index = len(attendance_data) - 1

    # Find the index of the current date column or insert it
    current_date_index = None
    for i, date in enumerate(attendance_data[0][1:], start=1):  # Start from index 1 to skip the name column
        if date == date_string:
            current_date_index = i
            break

    if current_date_index is None:
        # Shift existing data one column to the right
        for row in attendance_data:
            row.insert(1, '')

        # Update the first row with the current date in column B
        if len(attendance_data) == 0 or len(attendance_data[0]) < 2 or attendance_data[0][1] != date_string:
            for row in attendance_data:
                row[1] = date_string
        current_date_index = 1

    # Create a variable to hold the value to be written to the CSV file
    value_to_write = time_string if present else ''

    # Write the updated attendance record to the CSV file
    attendance_data[name_index][current_date_index] = value_to_write

    # Write the updated data back to the CSV file
    with open('Attendance.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(attendance_data)

    remove_datestamps()

def remove_datestamps():
    """
    Remove datestamps from cells (excluding the first row) in the 'Attendance.csv' file.
    """
    attendance_data = []

    # Read existing attendance data from the CSV file
    if os.path.isfile('Attendance.csv'):
        with open('Attendance.csv', 'r') as f:
            reader = csv.reader(f)
            attendance_data = list(reader)

    # Remove datestamps from cells (excluding the first row)
    for row in attendance_data[1:]:
        for i, cell in enumerate(row):
            if i != 0:  # Skip the first column (name column)
                if cell and ':' in cell:  # Check if the cell contains a timestamp
                    continue  # Skip cells containing timestamps
                row[i] = ''  # Clear datestamps from all columns except the first column

    # Write the updated data back to the CSV file
    with open('Attendance.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(attendance_data)





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
            encodes_curr_frame = face_recognition.face_encodings(img_s,
                                                                 faces_curr_frame)  # Find face encodings in the current frame

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
                    cv2.putText(img, name, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, font_scale,
                                (255, 255, 255), 2)

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


def get_image_files(folder_path):
    return glob.glob(os.path.join(folder_path, "*.jpg")) + glob.glob(os.path.join(folder_path, "*.png"))


def add_new_faces_to_database(image_folder_path):
    image_files = get_image_files(image_folder_path)
    known_names = get_class_names()  # Retrieve names already in the database
    for image_file in image_files:
        image_name = os.path.splitext(os.path.basename(image_file))[0]
        if image_name not in known_names:  # Check if the name is not already in the database
            img = face_recognition.load_image_file(image_file)
            face_encodings = face_recognition.face_encodings(img)
            if len(face_encodings) > 0:
                face_encoding = face_encodings[0]  # Assuming only one face per image
                store_encoding_to_db(image_name, face_encoding)
                known_names.append(image_name)  # Update the known names list


def main():
    initialize_database()

    # Add new faces to the database from the 'Images


    # Add new faces to the database from the 'Images_test' folder
    add_new_faces_to_database("Images_test")

    webcam_thread_instance = threading.Thread(target=webcam_thread)
    webcam_thread_instance.start()
    webcam_thread_instance.join()

    connection.close()
  
