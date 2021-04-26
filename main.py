import cv2
import time
from handTracking import HandDetection
from menu import Menu
from ui import *


def camera():
    cam = cv2.VideoCapture(0)
    cam.set(3, 1270)
    cam.set(4, 720)

    # hand_detection = HandDetection()
    menu = Menu()
    start = time.time()

    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        frame = menu.menu(frame)

        cv2.putText(frame, f"fps: {round(1 / (time.time() - start))}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 1.5,
                    (255, 0, 0), 2)
        start = time.time()
        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # camera()
    ui()