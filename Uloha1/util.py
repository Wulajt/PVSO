import cv2
import math
import matplotlib.pyplot as plt

def showOpenCVImagesGrid(images, x, y, titles=None, axis="on"):
    fig = plt.figure()
    i = 1
    for image in images:
        copy = image.copy()
        channel = len(copy.shape)
        cmap = None
        if channel == 2:
            cmap = "gray"
        elif channel == 3:
            copy = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)
        elif channel == 4:
            copy = cv2.cvtColor(copy, cv2.COLOR_BGRA2RGBA)

        fig.add_subplot(x, y, i)
        if titles is not None:
            plt.title(titles[i-1])
        plt.axis(axis)
        plt.imshow(copy, cmap=cmap)
        i += 1
    plt.show()


def grayImage(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray


def drawLines(image, lines, thickness=1):
    for line in lines:
        # print("line="+str(line))
        cv2.line(image, (line[0], line[1]), (line[2], line[3]),
                (0, 0, 255), thickness)


def drawContours(image, contours, thickness=1):
    i = 0
    for contour in contours:
        cv2.drawContours(image, [contours[i]], i, (0, 255, 0), thickness)
        area = cv2.contourArea(contour)
        i += 1
