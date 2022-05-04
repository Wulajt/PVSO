from processImage import *
import cv2
import numpy as np


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c, accuracy, area_threshold, solidity_threshold):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, accuracy * peri, True)
        (x, y, w, h) = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        equi_diameter = np.sqrt(4*area/np.pi)
        hull = cv2.convexHull(c)
        hull_area = cv2.contourArea(hull)
        solidity = float(area)/hull_area

        if area < area_threshold or solidity < solidity_threshold:
            return shape, 0.0, 0.0

        if len(approx) == 3:
            shape = "triangle"
        elif len(approx) == 4:
            ar = w / float(h)
            shape = "square" if ar >= 0.90 and ar <= 1.10 else "rectangle"
        elif len(approx) == 5:
            shape = "pentagon"
        #elif 5 < len(approx) < 20:
        #  shape = "circle"
        elif 0.90*w < equi_diameter < 1.10*w and 0.90*h < equi_diameter < 1.10*h:
            shape = "circle"
        return shape, area, solidity