import face_recognition
import cv2
import numpy as np


class FaceRecognition:

    def __init__(self):

        jarun = face_recognition.load_image_file("jarun.jpg")
        jarun_face_encoding = face_recognition.face_encodings(jarun)[0]

        obama = face_recognition.load_image_file("obama.jfif")
        obama_face_encoding = face_recognition.face_encodings(obama)[0]

        self.known_face_encodings = [
            jarun_face_encoding,
            obama_face_encoding
        ]

        self.known_face_names = [
            "Jarun",
            "Obama"
        ]

    def recognize(self, frame, face_locations):
        # face_locations = []
        face_encodings = []
        face_names = []

        # face_locations = face_recognition.face_locations(frame)

        face_encodings = face_recognition.face_encodings(frame, face_locations)

        matches = face_recognition.compare_faces(self.known_face_encodings, face_encodings[0])

        name = ""
        if True in matches:
            first_match_index = matches.index(True)
            name = self.known_face_names[first_match_index]
            face_names.append(name)

            (top, right, bottom, left) = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

            return True

        return False


        # face_names = []
        # for face_encoding in face_encodings:
        #     # See if the face is a match for the known face(s)
        #     matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
        #     name = "Unknown"
        #
        #     # If a match was found in known_face_encodings, just use the first one.
        #     # if True in matches:
        #     #     first_match_index = matches.index(True)
        #     #     name = self.known_face_names[first_match_index]
        #     #     face_names.append(name)
        #
        #     # Or instead, use the known face with the smallest distance to the new face
        #     face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        #     best_match_index = np.argmin(face_distances)
        #     if matches[best_match_index]:
        #         name = self.known_face_names[best_match_index]
        #
        #     face_names.append(name)

            # Display the results
            # for (top, right, bottom, left), name in zip(face_locations, face_names):
            #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            #     top *= 4
            #     right *= 4
            #     bottom *= 4
            #     left *= 4
            #
            #     # Draw a box around the face
            #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            #
            #     # Draw a label with a name below the face
            #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            #     font = cv2.FONT_HERSHEY_DUPLEX
            #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # return frame