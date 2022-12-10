import time
from os import path

import cv2
import numpy as np
from pygame import error
from pygame import mixer  # Load the popular external library

import Utils
from PoseModule import PoseDetector

detector = PoseDetector(False, True, 0.5, 0.5)

# For webcam input:
cap = cv2.VideoCapture(0)

# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 1280
height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

frameWidth = 1920
frameHeight = 1080
ptime = 0
ctime = 0
color = (0, 0, 255)
direction = 0
push_ups = 0
TIMER = 20
currentTimer = 20
prev = time.time()

basepath = path.dirname(__file__)
#mixer.init()
#mixer.music.load(path.abspath(basepath + "/audio/" + str(1) + ".ogg"))
#mixer.music.play()
while cap.isOpened():
    success, image = cap.read()
    # image = cv2.resize(image, (frameWidth, frameHeight))
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
    # overlay = image.copy()

    img = detector.findPose(image, False)

    lmlst, bbox = detector.findPosition(img, False, False)

    plm = detector.mpPose.PoseLandmark

    if lmlst:

        rightArmAngle = detector.findAngle(img, plm.RIGHT_SHOULDER, plm.RIGHT_ELBOW, plm.RIGHT_WRIST, False)

        # a2 = detector.findAngle(img, plm.LEFT_SHOULDER, plm.LEFT_ELBOW, plm.LEFT_WRIST, True)
        leftArmAngle = detector.findAngle(img, plm.LEFT_WRIST, plm.LEFT_ELBOW, plm.LEFT_SHOULDER, False)

        per_val1 = int(np.interp(rightArmAngle, (85, 165), (100, 0)))
        per_val2 = int(np.interp(leftArmAngle, (85, 165), (100, 0)))

        if per_val1 == 100 and per_val2 == 100:
            if direction == 0:
                push_ups += 0.5
                direction = 1
                color = (0, 255, 0)
        elif per_val1 == 0 and per_val2 == 0:
            if direction == 1:
                push_ups += 0.5
                direction = 0
                color = (0, 255, 0)
                print(str(int(push_ups)))

                filepath = path.abspath(basepath + "/audio/" + str(int(push_ups)) + ".ogg")

                try:

                    #mixer.init()
                    #mixer.music.load(filepath)
                    #mixer.music.play()
                    print("test")
                except error as message:
                    print(message)
                # p = vlc.MediaPlayer(filepath)
                # p.play()
                # p.play()
        else:
            color = (0, 0, 255)

        Utils.putTextRect(img, f'Push Ups : {int(push_ups)}', (218, 30), 2, 2, colorT=(0, 0, 0),
                          colorR=(255, 255, 255), colorB=(), border=2)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # print(f"{fps} frames per second")

        cur = time.time()

        currentTimer = TIMER + (prev - cur)
        # print(prev - cur)
        # Update and keep track of Countdown
        # if time elapsed is one second
        # then decrease the counter

        print(currentTimer)
        if currentTimer > 0:
            Utils.drawArcCv2((0, 0, 255), (100, 100), 90, 10, 360 * currentTimer / 20, img)

    # Flip the image horizontally for a selfie-view display.
    # cv2.imshow('MediaPipe Pose', cv2.flip(img, 1))
    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
