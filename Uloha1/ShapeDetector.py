from processImage import *
import cv2


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c, accuracy, area_thresh):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, accuracy * peri, True)

        if cv2.contourArea(c) < area_thresh:
            return shape

        if len(approx) == 3:
            shape = "triangle"
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        # elif len(approx) == 5:
        #     shape = "pentagon"
        return shape