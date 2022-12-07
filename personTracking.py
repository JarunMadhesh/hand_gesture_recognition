import mediapipe as mp
import cv2
import face_recognition
from faceRecognition import FaceRecognition


class PersonTracking:

    def __init__(self):
        self.numberOfPerson = 1

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_holistics = mp.solutions.holistic
        self.mp_faceDetection = mp.solutions.face_detection

        self.modelComplexity = 1
        self.enableSegmentation = True
        self.refineFaceLandmarks = False

        self.faceRecognition = FaceRecognition()
        self.isRecognized = False

        self.holistics = self.mp_holistics.Holistic(refine_face_landmarks=self.refineFaceLandmarks,
                                                    enable_segmentation= self.enableSegmentation,
                                                    min_detection_confidence=0.8,
                                                    min_tracking_confidence=0.8)

        self.faceDetection = self.mp_faceDetection.FaceDetection(model_selection=1, min_detection_confidence=0.8)

    def detect(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.holistics.process(frame)
        # face_results = self.faceDetection.process(frame)

        # print(results.pose_landmarks.landmark[8], results.pose_landmarks.landmark[7])

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks and not self.isRecognized:
            height, width, channels = frame.shape

            face_width = round(width * results.pose_landmarks.landmark[7].x-width * results.pose_landmarks.landmark[8].x)
            face_center = round(height * results.pose_landmarks.landmark[0].y)

            face_position = (face_center - face_width,
                             round(width * results.pose_landmarks.landmark[7].x),
                             face_center + face_width,
                             round(width * results.pose_landmarks.landmark[8].x))

            self.isRecognized = self.faceRecognition.recognize(frame, [face_position])
        elif not results.pose_landmarks and self.isRecognized:
            self.isRecognized = False

        self.mp_drawing.draw_landmarks(
            frame,
            results.left_hand_landmarks,
            self.mp_holistics.HAND_CONNECTIONS,
            connection_drawing_spec=self.mp_drawing_styles.get_default_hand_connections_style())
        self.mp_drawing.draw_landmarks(
            frame,
            results.right_hand_landmarks,
            self.mp_holistics.HAND_CONNECTIONS,
            connection_drawing_spec=self.mp_drawing_styles
                .get_default_hand_connections_style())
        # self.mp_drawing.draw_landmarks(
        #     frame,
        #     results.pose_landmarks,
        #     self.mp_holistics.POSE_CONNECTIONS,
        #     landmark_drawing_spec=self.mp_drawing_styles
        #         .get_default_pose_landmarks_style())

        return frame


