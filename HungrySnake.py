import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)


class SnakeGameClass:
    def __init__(self, pathFoods):
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point

        self.foodImages = [cv2.imread(f"Food Images/{path}", cv2.IMREAD_UNCHANGED) for path in pathFoods]
        self.currentFood = random.choice(self.foodImages)
        self.hFood, self.wFood, _ = self.currentFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

        self.score = 0
        self.bestScore = 0  # Track best score
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)
        self.currentFood = random.choice(self.foodImages)
        self.hFood, self.wFood, _ = self.currentFood.shape

    def update(self, imgMain, currentHead):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400],
                               scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550],
                               scale=7, thickness=5, offset=20)
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Check if snake ate the Food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                self.bestScore = max(self.bestScore, self.score)
                print(self.score)

            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, tuple(self.points[i - 1]), tuple(self.points[i]), (0, 0, 255), 20)
                cv2.circle(imgMain, tuple(self.points[-1]), 20, (0, 255, 0), cv2.FILLED)

            # Draw Food
            imgMain = cvzone.overlayPNG(imgMain, self.currentFood,
                                        (rx - self.wFood // 2, ry - self.hFood // 2))

            cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80],
                               scale=3, thickness=3, offset=10)
            cvzone.putTextRect(imgMain, f'Best Score: {self.bestScore}', [870, 80],
                               scale=3, thickness=3, offset=10)

            # Check for Collision
            if len(self.points) > 10:  # Check collision only if the snake has more than 10 points
                pts = np.array(self.points[:-int(len(self.points) / 3)], np.int32)  # Ignore first 1/3 of the body
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
                minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

                if -1 <= minDist <= 1:
                    print("Hit")
                    self.gameOver = True
                    self.points = []  # all points of the snake
                    self.lengths = []  # distance between each point
                    self.currentLength = 0  # total length of the snake
                    self.allowedLength = 150  # total allowed Length
                    self.previousHead = 0, 0  # previous head point
                    self.randomFoodLocation()

        return imgMain


game = SnakeGameClass(["donut.png", "muffin.png", "onion-rings.png", "pizza-slice.png", "sausage.png", "spaghetti.png"])

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
        game.score = 0  # Reset score on restart
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()