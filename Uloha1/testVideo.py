# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from xml_python import NoneType
from Camera.Camera import Camera
import cv2
import numpy as np
from ShapeDetector import *

def nothing(x):
    pass

def createTrackbars():
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("Canny Low", "Trackbars", 90, 255, nothing)
    cv2.createTrackbar("Canny High", "Trackbars", 100, 255, nothing)
    cv2.createTrackbar("Area of object", "Trackbars", 300, 30000, nothing)
    cv2.createTrackbar("Solidity of object", "Trackbars", 90, 100, nothing)
    return

if __name__ == '__main__':
    detect_accuracy = 0.02
    camera = Camera()
    sd = ShapeDetector()

    createTrackbars()
    while True:
        image = camera.getFrame()
        #bilateral = cv2.bilateralFilter(image, 15, 75, 75)
        imgBlur = cv2.GaussianBlur(image, (7, 7), 1)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

        canny_l = cv2.getTrackbarPos('Canny Low', 'Trackbars')
        canny_h = cv2.getTrackbarPos('Canny High', 'Trackbars')

        area_threshold = cv2.getTrackbarPos('Area of object', 'Trackbars')
        solidity_threshold = cv2.getTrackbarPos('Solidity of object', 'Trackbars')/100.0

        imgCanny = cv2.Canny(imgGray, canny_l, canny_h)
        kernel = np.ones((3, 3))
        imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        if hierarchy is not None:
            hierarchy = hierarchy[0]
            for c, h in zip(contours, hierarchy):
                
                M = cv2.moments(c)
                if M["m00"] is None or M["m00"] == 0:
                    continue
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            
                shape, area, solidity = sd.detect(c, detect_accuracy, area_threshold, solidity_threshold)
                if shape == "unidentified":
                    continue

                #if h[2] != -1:
                #    shape = shape +' (hollow)'
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.putText(image, str(shape), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)
                cv2.putText(image, "Area: " + str(area), (cX-20, cY + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
                cv2.putText(image, "Solidity: " + str(round(solidity,2)), (cX-20, cY + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
                #x_, y_, w, h = cv2.boundingRect(c)
                #cv2.rectangle(image, (x_, y_), (x_ + w, y_ + h), (0, 255, 0), 5)

            # if circles is not None:
            #     circles = np.round(circles[0, :]).astype("int")
            #     for (x, y, r) in circles:
            #         cv2.circle(image, (x, y), r, (0, 255, 0), 4)
            #         cv2.putText(image, "circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.imshow('Images', cv2.hconcat([imgGray, imgCanny, imgDil]))
        cv2.imshow("Image", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    del camera
    cv2.destroyAllWindows()
