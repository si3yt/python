import cv2
import numpy as np
import math

img = cv2.imread('../image/square_theta.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10

lines = cv2.HoughLinesP(edges,1,math.pi/360,100,minLineLength,maxLineGap)
# 第二引数：画素単位
# 第三引数：radian単位

for i in range(0,len(lines)):
    for x1,y1,x2,y2 in lines[i]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

while(1):
    cv2.imshow("sphere_rotate", img)
    k = cv2.waitKey(1)
    if k == 27: # ESCキーで終了
        cv2.imwrite("detected.jpg", img)
        break
