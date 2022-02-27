# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Camera.Camera import Camera
import cv2
import numpy as np
import time

if __name__ == '__main__':
    camera = Camera()
    while True:
        image = camera.getGrayFrame()
        output = image.copy()
        #cv2.imshow('frame', image)
        circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.2, 100)

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
        cv2.imshow("output", np.hstack([image, output]))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    del camera
    cv2.destroyAllWindows()
