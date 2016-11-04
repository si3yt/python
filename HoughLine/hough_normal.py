import cv2
import numpy as np

img = cv2.imread('../image/squareW.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10

lines = cv2.HoughLines(edges,1,np.pi/180,200)

for i in range(0,len(lines)-1):
    for rho,theta in lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

while(1):
    cv2.imshow("sphere_rotate", edges)
    k = cv2.waitKey(1)
    if k == 27: # ESCキーで終了
        cv2.imwrite("detected.jpg", edges)
        break
