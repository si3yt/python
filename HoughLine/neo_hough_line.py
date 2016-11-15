import cv2
import numpy as np
import math
from operator import itemgetter, attrgetter

img = cv2.imread('../image/theta04_cor.jpg')
height = img.shape[0]
width = img.shape[1]
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

line_len = 100

lines = cv2.HoughLines(edges,1,math.pi/360,line_len)

degree_range = 10

line_xyd = []

range_line = width

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

        degree = theta * 180 / math.pi

        if degree < degree_range:
            degree = degree + 10
            line_xyd.append((x1,y1,x2,y2,degree,x0))
        elif degree > 180-degree_range:
            if degree == 180:
                degree = 10
            else:
                degree = degree - 170
            line_xyd.append((x1,y1,x2,y2,degree,x0))

sorted(line_xyd, key=itemgetter(5))

print (line_xyd)

for i in range(0,len(line_xyd)):
    x1 = line_xyd[i][0]
    y1 = line_xyd[i][1]
    x2 = line_xyd[i][2]
    y2 = line_xyd[i][3]
    degree = line_xyd[i][4]
    x0 = line_xyd[i][5]
    diff_deg = 0
    diff_x0 = 0
    diff_flag = False
    if (i+1 < len(line_xyd) and i-1 >= 0):
        diff_deg = abs(degree - line_xyd[i+1][4])
        diff_deg += abs(degree - line_xyd[i-1][4])
        diff_x0 = abs(x0 - line_xyd[i+1][5])
        diff_x0 += abs(x0 - line_xyd[i-1][5])
    if diff_deg < 10 and diff_x0 < 500:
        diff_flag = True

    if (i+2 < len(line_xyd)):
        diff_deg = abs(degree - line_xyd[i+1][4])
        diff_deg += abs(degree - line_xyd[i+2][4])
        diff_x0 = abs(x0 - line_xyd[i+1][5])
        diff_x0 += abs(x0 - line_xyd[i+2][5])
    if diff_deg < 10 and diff_x0 < 500:
        diff_flag = True

    if (i-2 >= 0):
        diff_deg = abs(degree - line_xyd[i-1][4])
        diff_deg += abs(degree - line_xyd[i-2][4])
        diff_x0 = abs(x0 - line_xyd[i-1][5])
        diff_x0 += abs(x0 - line_xyd[i-2][5])
    if diff_deg < 10 and diff_x0 < 500:
        diff_flag = True

    if diff_flag == False:
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)



while(1):
    img = cv2.resize(img, (int(width/4), int(height/4)))
    cv2.imshow("sphere_rotate", img)
    k = cv2.waitKey(1)
    if k == 27: # ESCキーで終了
        cv2.imwrite("detected.jpg", img)
        #img = cv2.imread('../image/square_theta.jpg')
        break
