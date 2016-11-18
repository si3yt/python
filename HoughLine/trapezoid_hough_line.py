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

trapezoid = []
draw_line = []

slice_line1 = 100
slice_line2 = 1700

for i in range(0,len(line_xyd)):
    x11 = line_xyd[i][0]
    y11 = line_xyd[i][1]
    x12 = line_xyd[i][2]
    y12 = line_xyd[i][3]
    degree = line_xyd[i][4]
    x0 = line_xyd[i][5]
    trapezoid = []

    a1 = 0
    if x12 - x11 != 0:
        a1 = (y12 - y11)/(x12 - x11)
    b1 = a * (-x11) + y11

    if a1 != 0:
        cross11_x = (slice_line1 - b1) / a1
        cross12_x = (slice_line2 - b1) / a1
    else:
        cross11_x = slice_line1
        cross12_x = slice_line2

    cv2.line(img,(x11,y11),(x12,y12),(0,0,255),2)

    while(1):
        re_img = cv2.resize(img, (int(width/4), int(height/4)))
        cv2.imshow("sphere_rotate", re_img)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            #img = cv2.imread('../image/theta04_cor.jpg')
            break

    for j in range(0,len(line_xyd)):
        if j != i:
            x21 = line_xyd[j][0]
            y21 = line_xyd[j][1]
            x22 = line_xyd[j][2]
            y22 = line_xyd[j][3]
            degree = line_xyd[j][4]
            x0 = line_xyd[j][5]

            a2 = 0
            if x22 - x21 != 0:
                a2 = (y22 - y21)/(x22 - x21)
            b2 = a * (-x21) + y21

            if a2 != 0:
                cross21_x = (slice_line1 - b2) / a2
                cross22_x = (slice_line2 - b2) / a2
            else:
                cross21_x = slice_line1
                cross22_x = slice_line2

            t_top = abs(cross11_x - cross21_x)
            t_bottom = abs(cross12_x - cross22_x)
            t_height = slice_line2 - slice_line1
            trapezoid_area = (t_top + t_bottom) * t_height / 2

            trapezoid.append(trapezoid_area)

            cv2.line(img,(x21,y21),(x22,y22),(0,255,),2)

            print (cross11_x, cross21_x, cross12_x, cross22_x)
            print (trapezoid_area, t_top, t_bottom)

            while(1):
                re_img = cv2.resize(img, (int(width/4), int(height/4)))
                cv2.imshow("sphere_rotate", re_img)
                k = cv2.waitKey(1)
                if k == 27: # ESCキーで終了
                    img = cv2.imread('../image/theta04_cor.jpg')
                    cv2.line(img,(x11,y11),(x12,y12),(0,0,255),2)
                    break


    dense_count = 0

    for k in range(0,len(trapezoid)):
        if trapezoid[k] <= 50000:
            dense_count += 1

    if dense_count < 2:
        draw_line.append((x11,y11,x12,y12,degree,x0))
        #cv2.line(img,(x11,y11),(x12,y12),(0,0,255),2)

    img = cv2.imread('../image/theta04_cor.jpg')

while(1):
    img = cv2.resize(img, (int(width/4), int(height/4)))
    cv2.imshow("sphere_rotate", img)
    k = cv2.waitKey(1)
    if k == 27: # ESCキーで終了
        cv2.imwrite("detected.jpg", img)
        #img = cv2.imread('../image/square_theta.jpg')
        break
