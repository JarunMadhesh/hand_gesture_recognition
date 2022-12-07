import mediapipe as mp
import cv2


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

        self.holistics = self.mp_holistics.Holistic(refine_face_landmarks=self.refineFaceLandmarks,
                                                    enable_segmentation= self.enableSegmentation,
                                                    min_detection_confidence=0.8,
                                                    min_tracking_confidence=0.8)

        self.faceDetection = self.mp_faceDetection.FaceDetection(model_selection=1, min_detection_confidence=0.8)

    def detect(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.holistics.process(frame)
        face_results = self.faceDetection.process(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if face_results.detections:
            for detection in face_results.detections:
                self.mp_drawing.draw_detection(frame, detection)
                print(detection)

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


