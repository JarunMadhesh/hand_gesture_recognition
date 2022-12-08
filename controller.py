from threading import Thread
import time


class Hand():

    def positions(self, imgshape, my_hand):
        pt_list = []
        for i, lm in enumerate(my_hand.landmark):
            h, w, c = imgshape
            cx, cy = int(lm.x * w), int(lm.y * h)
            pt_list.append([i, cx, cy])
        return pt_list

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


class LeftHand(Hand):

    def __init__(self):

        pass

    def control(self):

        pt_list = Hand.positions()

    def run(self):
        for i in range(10):
            time.sleep(1)
            print("Left hand")


class RightHand(Hand):
    def __init__(self):
        pass

    def run(self, number):
        for j in range(10):
            time.sleep(1)
            print("Right hand " + number)


if __name__ == "__main__":
    L = LeftHand()
    a = Thread(target=L.run)
    R = RightHand()
    b = Thread(target=R.run, args=("4",))
    a.start()
    b.start()
