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
    b1 = a1 * (-x11) + y11

    if a1 != 0:
        cross11_x = (slice_line1 - b1) / a1
        cross12_x = (slice_line2 - b1) / a1
    else:
        cross11_x = x11
        cross12_x = x12

    for j in range(0,len(line_xyd)):
        if j != i:
            x21 = line_xyd[j][0]
            y21 = line_xyd[j][1]
            x22 = line_xyd[j][2]
            y22 = line_xyd[j][3]

            a2 = 0
            if x22 - x21 != 0:
                a2 = (y22 - y21)/(x22 - x21)
            b2 = a2 * (-x21) + y21

            if a2 != 0:
                cross21_x = (slice_line1 - b2) / a2
                cross22_x = (slice_line2 - b2) / a2
            else:
                cross21_x = x21
                cross22_x = x22

            t_top = abs(cross11_x - cross21_x)
            t_bottom = abs(cross12_x - cross22_x)
            t_height = slice_line2 - slice_line1
            trapezoid_area = (t_top + t_bottom) * t_height / 2

            trapezoid.append(trapezoid_area)

    dense_count = 0

    for k in range(0,len(trapezoid)):
        if trapezoid[k] <= 40000:
            dense_count += 1

    if dense_count < 2:
        draw_line.append((x11,y11,x12,y12,degree,x0))
        cv2.line(img,(x11,y11),(x12,y12),(0,0,255),2)

amplitude = 100
newton_threshold = 0.00001

sin_bin = [0]*int(360/5)

phase = 0

img = cv2.imread('../image/theta04_cor.jpg')
for p in range(0,len(sin_bin)):
    phase = p * 5
    phase = phase * math.pi / 180
    img = cv2.imread('../image/theta04_cor.jpg')
    for i in range(0,width):
        x1 = i
        y1 = int(-amplitude * math.sin(2*math.pi * i/width + phase) + height/2)
        x2 = int(width/2)
        y2 = 500
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    while(1):
        img = cv2.resize(img, (int(width/4), int(height/4)))
        cv2.imshow("sphere_rotate", img)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            break


for p in range(0,len(sin_bin)):
    phase = p
    phase = phase * math.pi / 180
    for i in range(0,len(draw_line)):
        x1 = draw_line[i][0]
        y1 = draw_line[i][1]
        x2 = draw_line[i][2]
        y2 = draw_line[i][3]
        degree = draw_line[i][4]
        x0 = draw_line[i][5]

        a = 0
        if x2 - x1 != 0:
            a = (y2 - y1)/(x2 - x1)
        b = a * (-x1) + y1

        if a != 0:
            center_x = (height/2 - b) / a
        else:
            center_x = x1

        # y = - amplitude * sin(2π * x/W + phase) + H/2
        # y = ax + b

        # ax + b + 振幅(amplitude) * sin(2*pi * (x/w) + 位相(phase)) - H/2
        # 微分
        # a + amplitude * 2π/W * cos(2π * (x/w) + phase)

        nt_x = center_x
        for j in range(0,1000):
            print (nt_x)
            fx = a * nt_x + b + amplitude * math.sin(2*math.pi * nt_x/width + phase) - height/2
            dx = a + amplitude * 2*math.pi/width * math.cos(2*math.pi * nt_x/width + phase)

            nt_x2 = nt_x - fx / dx

            if abs(nt_x2 - nt_x) < newton_threshold:
                break

            nt_x = nt_x2

        # 接線
        # y = f'(nt_x)*x + (-nt_x*f'(nt_x) + f(nt_x))
        # 法線
        # y = - 1/f'(nt_x)*x + (nt_x*1/f'(nt_x) + f(nt_x))
        fx = -amplitude * math.sin(2*math.pi * nt_x/width + phase) + height/2
        dx = -amplitude * 2*math.pi/width * math.cos(2*math.pi * nt_x/width + phase)

        tangent_a = dx
        tangent_b = -nt_x*dx + fx

        tx1 = 10
        ty1 = int(tangent_a * tx1 + tangent_b)
        tx2 = width - 10
        ty2 = int(tangent_a * tx2 + tangent_b)

        print (tangent_a, tangent_b, ty1, ty2)


        theta = math.atan((tangent_a-a)/(1+a*tangent_a))
        print (theta)
        theta = theta * 180 / math.pi

        print (theta)

        if theta >= 80 and theta <= 100:
            sin_bin[p] += 1

print (sin_bin)

while(1):
    img = cv2.resize(img, (int(width/4), int(height/4)))
    cv2.imshow("sphere_rotate", img)
    k = cv2.waitKey(1)
    if k == 27: # ESCキーで終了
        cv2.imwrite("detected.jpg", img)
        #img = cv2.imread('../image/square_theta.jpg')
        break
