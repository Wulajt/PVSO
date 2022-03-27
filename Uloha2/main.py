import numpy as np
import matplotlib.pyplot as plt
import math
import cv2

def hough_line(image):
    #Get image dimensions
    # y for rows and x for columns 
    n_y, n_x = image.shape

    #Max diatance is diagonal one 
    Maxdist = int(np.round(np.sqrt(n_x**2 + n_y ** 2)))
    # Theta in range from -90 to 90 degrees
    thetas = np.deg2rad(np.arange(-90, 90))
    #Range of radius
    rs = np.linspace(-Maxdist, Maxdist, 2*Maxdist)
    accumulator = np.zeros((2 * Maxdist, len(thetas)))
    for y in range(n_y):
     for x in range(n_x):
         # Check if it is an edge pixel
         #  NB: y -> rows , x -> columns
          if image[y,x] > 0:
              # Map edge pixel to hough space
              for k in range(len(thetas)):
                # Calculate space parameter
                r = x*np.cos(thetas[k]) + y * np.sin(thetas[k])
                # Update the accumulator
                # N.B: r has value -max to max
                # map r to its idx 0 : 2*max
                accumulator[int(r) + Maxdist,k] += 1
    return accumulator, thetas, rs

def draw_line(rho,theta, colored_image):
    a=math.cos(theta)
    b=math.sin(theta)
    x0=rho*a
    y0=rho*b
    x1=int(x0+ 1000 * (-b))
    y1=int(y0+ 1000 * (a))
    x2=int(x0- 1000 * (-b))
    y2=int(y0- 1000 * (a))
    cv2.line(colored_image,(x1,y1),(x2,y2),(0,0,255),2)
    return colored_image

img = cv2.imread(r'C:\Users\janik\Desktop\FEI_STU\Ing\2.semester\PVSO\projekty\PVSO\Uloha2\sudoka.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

nase_rieseni_img = img.copy()
threshold = 200
accumulator, thetas, rhos = hough_line(edges)
indexs = np.argwhere(accumulator > threshold)
for indx in indexs:
    rho = int(rhos[indx[0]])
    theta = thetas[indx[1]]
    nase_rieseni_img = draw_line(rho,theta, nase_rieseni_img)


opencv_img = img.copy()
lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
for line in lines:
    rho,theta = line[0]
    opencv_img = draw_line(rho,theta, opencv_img)

cv2.imshow('edges', edges)
cv2.imshow('naseriesenie', nase_rieseni_img)
cv2.imshow('opencv', opencv_img)
k = cv2.waitKey(0)
cv2.destroyAllWindows()