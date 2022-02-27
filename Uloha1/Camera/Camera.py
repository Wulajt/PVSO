import cv2
import threading


class Camera:
    def __init__(self):
        self._cameraPort = 0
        self._frame = None
        self._ret = None

        self._video = cv2.VideoCapture(self._cameraPort)

    def __del__(self):
        self._video.release()

    def getFrame(self):
        self._ret, self._frame = self._video.read()
        return self._frame

    def getRet(self):
        return self._ret

    def getGrayFrame(self):
        return cv2.cvtColor(self.getFrame(), cv2.COLOR_BGR2GRAY)

