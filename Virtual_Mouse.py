import cv2
import numpy as np
import mediapipe
from HandsGestureDetector import HandDetector as hd
import time
import pyautogui
import math

wCam, hCam = 1300, 1300

prevX = prevY = curX = curY = 0
smoothing = 10
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

cTime = pTime = 0

detector = hd()

wScr, hScr = pyautogui.size()

while True:

    success, img = cap.read()

    img = cv2.flip(img, 1)
    img = detector.findHands(img)

    lmList = detector.findPosition(img)

    if len(lmList):
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[12][1], lmList[12][2]

        fingers = detector.fingersUp()

        cv2.rectangle(img, (100, 100), (wCam-50, hCam-50), (255, 255, 0), 3)

        if fingers[1] and not fingers[2]:
            x3, y3 = np.interp(x1, (100, wCam - 100), (0, wScr)), np.interp(y1, (100, hCam - 100), (0, hScr))

            # curX = prevX + (x3 - prevX) // smoothing
            # curY = prevY + (x3 - prevY) // smoothing

            pyautogui.moveTo(x3, y3)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)

            # prevX, prevY = curX, curY

        if fingers[1] and fingers[2]:
            x1, y1 = lmList[8][1], lmList[8][2]
            x2, y2 = lmList[12][1], lmList[12][2]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            length = math.hypot(x2 - x1, y2 - y1)

            if length < 60:
                pyautogui.click()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow('img', img)
    cv2.waitKey(1)

