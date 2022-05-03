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

if __name__ == '__main__':
    camera = Camera()
    sd = ShapeDetector()
    while True:
        image = camera.getFrame()
        image_gray = camera.getGrayFrame()

        cnt_gray = pimg.getContours(image_gray)
        cnt = pimg.getContours(image)

        contours = imutils.grab_contours(cnt)

        circles = cv2.HoughCircles(image_gray, cv2.HOUGH_GRADIENT, 1.25, 100)

        for c in contours:
            M = cv2.moments(c)
            if M["m00"] is None or M["m00"] == 0:
                continue
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            shape = sd.detect(c)
            if shape == "unidentified":
                continue
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(image, shape, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(image, (x, y), r, (0, 255, 0), 4)
                cv2.putText(image, "circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow("Image", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    del camera
    cv2.destroyAllWindows()
