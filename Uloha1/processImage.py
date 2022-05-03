import cv2
import util
from Camera.Camera import Camera
import imutils


def getContours(gray_image):
    gray_copy = gray_image.copy()
    image = gray_image.copy()


    blurred = cv2.GaussianBlur(gray_copy, (5, 5), 0)
    canny = cv2.Canny(blurred, 50, 200)

    cv2.imshow("canny", canny)
    return cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
