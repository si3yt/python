import cv2
import numpy as np
import math

img = cv2.imread('../image/square_theta.jpg')
height = img.shape[0]
width = img.shape[1]
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10

lines = cv2.HoughLines(edges,1,math.pi/360,200)

range_line = 7000

for i in range(0,len(lines)):
    for rho,theta in lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + range_line*(-b))
        y1 = int(y0 + range_line*(a))
        x2 = int(x0 - range_line*(-b))
        y2 = int(y0 - range_line*(a))

        if x0 > 1000 and x0 < 2700 and y0 > 600 and y0 < 1800:
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

while(1):
    img = cv2.resize(img, (int(width/4), int(height/4)))
    cv2.imshow("sphere_rotate", img)
    k = cv2.waitKey(1)
    if k == 27: # ESCキーで終了
        cv2.imwrite("detected.jpg", img)
        #img = cv2.imread('../image/square_theta.jpg')
        break
