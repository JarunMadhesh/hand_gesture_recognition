from handTracking import HandDetection
import cv2
import numpy as np
import winsound
from firebase import firebase
import mysqlDb


class Menu:
    def __init__(self):
        self.number = 0
        self.menu_opened = False
        self.started = False
        self.prevent_repetition = False
        self.point = None
        self.hand_detection = HandDetection()

        self.volume = 0
        self.channel = 0

        self.firebase = firebase.FirebaseApplication(
            "https://hand-gesture-recognition-cfec6-default-rtdb.asia-southeast1.firebasedatabase.app/", None)

        self.db = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="root@123",
            db="trial"
        )

        self.curr = db.cursor()

    @staticmethod
    def calculate(num, dx):
        if num < 0 and dx < 0:
            return 0
        if num > 100 and dx > 0:
            return 100
        return num + 0.002 * dx

    def menu(self, frame):
        frame = self.hand_detection.detect(frame=frame)
        pts_list = self.hand_detection.positions(frame)

        if len(pts_list) == 0:
            return frame

        fingers = self.count(pts_list)
        count = fingers.count(1)

        cv2.putText(frame, f"number: {count}", (np.shape(frame)[1] - 250, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 0), 1)

        if (not self.started) and count == 2 and fingers[0] == 1 and fingers[-1] == 1:
            self.started = True
            self.point = (pts_list[9][1], pts_list[9][2])
            winsound.Beep(1250, 300)

        elif self.started:

            # Force eject
            if count == 1 and fingers[1] == 3:
                self.point = None
                self.menu_opened = False
                self.started = False
                winsound.Beep(1250, 300)

            # Gateway.. enters only with 5
            elif (not self.menu_opened) and count == 5:
                self.point = (pts_list[9][1], pts_list[9][2])
                self.prevent_repetition = True
                self.menu_opened = True

            # Menu opens
            elif self.menu_opened:


                # return if 0, 3, 4
                if count == 0 or count == 3 or count == 4:
                    return frame

                # to set things up
                if self.prevent_repetition and count == 5:
                    current_point = (pts_list[9][1], pts_list[9][2])
                    self.point = current_point
                    cv2.circle(frame, current_point, 5, (255, 255, 0), 10)
                    cv2.putText(frame, f"1: Channel", (np.shape(frame)[1] - 250, np.shape(frame)[0] - 200),
                                cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 0, 0), 2)
                    cv2.putText(frame, f"2: Volume", (np.shape(frame)[1] - 250, np.shape(frame)[0] - 170),
                                cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 0, 0), 2)

                # Channel
                elif count == 1 and fingers[1] == 1:
                    current_point = (pts_list[9][1], pts_list[9][2])
                    channel = self.calculate(self.channel, current_point[0] - self.point[0])
                    if channel > self.channel:
                        # Sending to DB
                        self.curr.execute("INSERT INTO movement (direction, time) VALUES ('channel_up', NOW())")
                        self.db.commit()
                        cv2.putText(frame, f"Channel up", (np.shape(frame)[1] - 250,
                                                          np.shape(frame)[0] - 200),
                                    cv2.FONT_HERSHEY_PLAIN, 2,
                                    (255, 0, 0), 2)
                    else:
                        # Sending to DB
                        self.curr.execute("INSERT INTO movement (direction, time) VALUES ('channel_down', NOW())")
                        self.db.commit()
                        cv2.putText(frame, f"Channel Down", (np.shape(frame)[1] - 250,
                                                            np.shape(frame)[0] - 200),
                                    cv2.FONT_HERSHEY_PLAIN, 2,
                                    (255, 0, 0), 2)
                    self.channel = channel
                    cv2.circle(frame, current_point, 5, (255, 0, 0), 10)
                    cv2.circle(frame, self.point, 5, (255, 255, 0), 10)
                    self.prevent_repetition = False

                # Volume
                elif count == 2 and fingers[1] == 1 and fingers[2] == 1:
                    current_point = (pts_list[9][1], pts_list[9][2])
                    volume = self.calculate(self.volume, current_point[0] - self.point[0])
                    if volume > self.volume:
                        self.curr.execute("INSERT INTO movement (direction, time) VALUES ('vol_up', NOW())")
                        self.db.commit()
                        cv2.putText(frame, f"Volume up", (np.shape(frame)[1] - 250,
                                                                          np.shape(frame)[0] - 200),
                                    cv2.FONT_HERSHEY_PLAIN, 2,
                                    (255, 0, 0), 2)
                    else:
                        self.curr.execute("INSERT INTO movement (direction, time) VALUES ('vol_down', NOW())")
                        self.db.commit()
                        cv2.putText(frame, f"Volume Down", (np.shape(frame)[1] - 250,
                                                                          np.shape(frame)[0] - 200),
                                    cv2.FONT_HERSHEY_PLAIN, 2,
                                    (255, 0, 0), 2)
                    self.volume = volume

                    cv2.circle(frame, current_point, 5, (255, 0, 0), 10)
                    cv2.circle(frame, self.point, 5, (255, 255, 0), 10)
                    self.prevent_repetition = False

                # If 5 again, stop
                elif (not self.prevent_repetition) and count == 5:
                    self.point = None
                    self.menu_opened = False
                    self.started = False

                    winsound.Beep(1250, 300)

        return frame

    def count(self, pts_list):
        tips = [4, 8, 12, 16, 20]
        # base = [5, 9, 13, 17]

        fingers = []
        if len(pts_list):

            # To check whether the hand is upright
            if pts_list[0][2] < pts_list[9][2]:
                return []

            # Check for thumb open and close
            if pts_list[5][1] > pts_list[17][1]:
                if pts_list[tips[0]][1] > pts_list[tips[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if pts_list[tips[0]][1] < pts_list[tips[0] - 1][1]:
                    self.number = self.number + 1
                    fingers.append(1)
                else:
                    fingers.append(0)

            # check for other fingers open and close
            for i in range(1, len(tips)):
                if pts_list[tips[i]][2] < pts_list[tips[i] - 3][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers
