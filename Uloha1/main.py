# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Camera.Camera import Camera
import cv2
import numpy as np
import time
import util

if __name__ == '__main__':
    camera = Camera()
    while True:
        image = camera.getGrayFrame()
        output = image.copy()
        #cv2.imshow('frame', image)
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.2, 100)

        edges = cv2.Canny(image, 50, 200)
        lines = cv2.HoughLinesP(edges, 1, 3.14159/180, 50, minLineLength=50, maxLineGap=10)[0]
        linesImage = image.copy()
        util.drawLines(linesImage, lines, thickness=10)

        contoursImage = image.copy()
        (contours, hierarchy) = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        util.drawContours(contoursImage, contours, thickness=10)

        cv2.imshow('edges', edges)
        cv2.imshow('lines', linesImage)
        cv2.imshow('contoursImage', contoursImage)

        blur = cv2.medianBlur(image, 5)
        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

        thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        min_area = 100
        max_area = 10000
        image_number = 0
        for c in cnts:
            area = cv2.contourArea(c)
            if area > min_area:
                x, y, w, h = cv2.boundingRect(c)
                ROI = image[y:y + h, x:x + w]
                # cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
                cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
                image_number += 1

        # cv2.imshow('sharpen', sharpen)
        # cv2.imshow('close', close)
        # cv2.imshow('thresh', thresh)
        cv2.imshow('image', image)


        # triangles = cv2.HoughLines();
        squares = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.2, 100)

        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            # show the output image
        # cv2.imshow("output", np.hstack([image, output]))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    del camera
    cv2.destroyAllWindows()
