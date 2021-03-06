import cv2
import time
import numpy
import HandTrackingModule as htm
import math
import osascript

############################

cap = cv2.VideoCapture(0)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)
minVol = 0
maxVol = 100
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        # hand range 50 - 300
        # vol range 0 - 100
        vol = numpy.interp(length, [50, 300], [minVol, maxVol])
        volumeScript = f'set volume output volume {int(math.floor(vol))}'
        print(volumeScript)
        osascript.osascript(volumeScript)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)