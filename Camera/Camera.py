import cv2
import threading


class Camera(threading.Thread):
    def __init__(self):
        super().__init__()
        self._cameraPort = 0
        self._frame = None
        self._ret = None

        self._video = cv2.VideoCapture(self._cameraPort)

    def run(self) -> None:
        self._startCamera()

    def _startCamera(self):
        while True:
            self._ret, self._frame = self._video.read()

            cv2.imshow('frame', self._frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self._video.release()
        cv2.destroyAllWindows()

    def getFrame(self):
        return self._frame

    def getRet(self):
        return self._ret
