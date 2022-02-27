# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Camera.Camera import Camera
import time

if __name__ == '__main__':
    camera = Camera()
    camera.start()
    time.sleep(5)
    print(camera.getFrame())
    camera.join()
