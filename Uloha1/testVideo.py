# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Camera.Camera import Camera
import cv2
import numpy as np
import time
import util
import processImage as pimg
import imutils
from ShapeDetector import *
import datetime as dt
import math

def nothing(x):
    pass

def createTrackbars():
    cv2.namedWindow("Trackbars")

    cv2.createTrackbar("Canny Low", "Trackbars", 30, 255, nothing)
    cv2.createTrackbar("Canny High", "Trackbars", 40, 255, nothing)
    cv2.createTrackbar("Weight 1", "Trackbars", 30, 100, nothing)
    cv2.createTrackbar("Weight 2", "Trackbars", 0, 100, nothing)
    cv2.createTrackbar("Weight gamma", "Trackbars", 70, 100, nothing)
    cv2.createTrackbar("Detect accuracy", "Trackbars", 2, 10, nothing)
    cv2.createTrackbar("Detect thresh", "Trackbars", 5000, 30000, nothing)
    return

if __name__ == '__main__':
    camera = Camera()
    sd = ShapeDetector()

    idx = 0

    # img_queue = [camera.getGrayFrame() for i in range(4)]
    createTrackbars()
    while True:
        image = camera.getFrame()
        # gray = camera.getGrayFrame()
        imgBlur = cv2.GaussianBlur(image, (7, 7), 1)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

        canny_l = cv2.getTrackbarPos('Canny Low', 'Trackbars')
        canny_h = cv2.getTrackbarPos('Canny High', 'Trackbars')

        detect_accuracy = cv2.getTrackbarPos('Detect accuracy', 'Trackbars') /100
        detect_thresh = cv2.getTrackbarPos('Detect thresh', 'Trackbars')

        imgCanny = cv2.Canny(imgGray, canny_l, canny_h)
        kernel = np.ones((3, 3))
        imgErr = cv2.erode(imgCanny, np.ones((1, 1)), iterations=1)
        imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # np.concatenate((image, imgGray, imgCanny, imgDil))
        cv2.imshow('Images', cv2.hconcat([imgGray, imgCanny, imgDil, imgErr]))

        # cnt = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # contours = imutils.grab_contours(cnt)

        #
        # circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, 1.5, 50)

        i = 0
        for c in contours:
            if i == 0:
                i = 1
                continue

            area = cv2.contourArea(c)

            if area > detect_thresh:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                if len(approx) == 4 or len(approx) == 3:
                    cv2.drawContours(image, c, -1, (255, 0, 255), 7)
                    x_, y_, w, h = cv2.boundingRect(approx)
                    cv2.rectangle(image, (x_, y_), (x_ + w, y_ + h), (0, 255, 0), 5)


            # M = cv2.moments(c)
            # if M["m00"] is None or M["m00"] == 0:
            #     continue
            # rect = cv2.boundingRect(c)
            # # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            # # cv2.rectangle(image, re)
            # cX = int(M["m10"] / M["m00"])
            # cY = int(M["m01"] / M["m00"])
            #
            # shape = sd.detect(c, detect_accuracy, detect_thresh)
            # if shape == "unidentified":
            #     continue
            # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            # # cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
            # cv2.putText(image, str(shape), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)
            #
            # area = cv2.contourArea(c)
            # cv2.putText(image, "Area: " + str(area), (cX, cY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 2)

        # i = 0
        # for c in contours:
        #     if i == 0:
        #         i = 1
        #         continue
        #
        #     M = cv2.moments(c)
        #     if M["m00"] is None or M["m00"] == 0:
        #         continue
        #     rect = cv2.boundingRect(c)
        #     # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        #     # cv2.rectangle(image, re)
        #     cX = int(M["m10"] / M["m00"])
        #     cY = int(M["m01"] / M["m00"])
        #
        #     shape = sd.detect(c, detect_accuracy, detect_thresh)
        #     if shape == "unidentified":
        #         continue
        #     cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        #     # cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
        #     cv2.putText(image, str(shape), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)
        #
        #     area = cv2.contourArea(c)
        #     cv2.putText(image, "Area: " + str(area), (cX, cY + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 2)
        #
        # if circles is not None:
        #     circles = np.round(circles[0, :]).astype("int")
        #     for (x, y, r) in circles:
        #         cv2.circle(image, (x, y), r, (0, 255, 0), 4)
        #         cv2.putText(image, "circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow("Image", image)
        # cv2.imshow("canny", canny)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        idx = idx + 1

    del camera
    cv2.destroyAllWindows()
