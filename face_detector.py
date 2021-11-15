import numpy as np
from cv2 import cv2
import face_recognition
import os


#   itialiazing images
images_file = []
images_name = []
images_path = "images"
images_list = os.listdir(images_path)

for image_class in images_list:
    image = cv2.imread(f'{images_path}/{image_class}')
    images_file.append(image)
    images_name.append(os.path.splitext(image_class)[0])


#   image encoding
def get_encodings(images_file):
    encoded_image = []

    for image in images_file:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encoded_image.append(face_recognition.face_encodings(image)[0])

    return encoded_image


known_encoded_image = get_encodings(images_file)


#   capturing data from webcam
def detect_face():
    camera = cv2.VideoCapture(0)

    match = False
    while match == False:
        success, image = camera.read()

        if success == True:

            resized_image = cv2.resize(image, (0, 0), None, 0.25, 0.25)
            resized_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            face_location = face_recognition.face_locations(resized_image)
            encoded_resized_image = face_recognition.face_encodings(
                resized_image, face_location)

            for encoded_face, face_location in zip(encoded_resized_image, face_location):
                cv2.rectangle(image, (face_location[3], face_location[0]), (
                    face_location[1], face_location[2]), (0, 0, 255), 3)

                differece = face_recognition.face_distance(
                    known_encoded_image, encoded_face)
                matchIndex = np.argmin(differece)

                if differece[matchIndex] < 0.5:
                    camera.release()
                    cv2.destroyAllWindows()

                    match = True
                    name = images_name[matchIndex]

                    cv2.rectangle(image, (face_location[3], face_location[0]), (
                        face_location[1], face_location[2]), (0, 205, 0), 3)

                    cv2.rectangle(image, (face_location[3], face_location[2]), (
                        face_location[1], face_location[2]+30), (0, 255, 0), cv2.FILLED)

                    
                    cv2.putText(
                        image, name, (face_location[3]+5, face_location[2]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    cv2.imshow(name, image)
                    return name

            if (cv2.waitKey(1) & 0xFF == 27) or match == True:
                break
            else:
                cv2.imshow("WebCam (Press Esc to Close)", image)

        else:
            break

    camera.release()
    cv2.destroyAllWindows()
