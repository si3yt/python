# import library
import cv2
import math
import numpy as np

# import files
import list_operation as list_opr
import linear_function as linear

def rad_conv(a):
    a = a * math.pi / 180
    return a

def degree_conv(a):
    a = a * 180 / math.pi
    return a

def newton(a, b, center_x, width, height, amplitude, phase, newton_count, newton_threshold):
    x = center_x
    amp_rad = rad_conv(amplitude)
    for j in range(0,newton_count):
        fx = a * x + b - width/(2*math.pi) * math.asin( math.sin(amp_rad) * math.sin(math.atan2(math.sin(2*math.pi * x/width+phase), math.cos(amp_rad)*math.cos(2*math.pi * x/width+phase)))) + height/2
        dx = a - (math.sin(amp_rad)*math.cos(amp_rad)*math.cos(math.atan2(math.sin(2*math.pi * x/width+phase),math.cos(amp_rad)*math.cos(2*math.pi * x/width+phase)))) / ((((math.cos(2*math.pi * x/width+phase))**2)*((math.cos(amp_rad))**2)+((math.sin(2*math.pi * x/width+phase))**2))*math.sqrt(1-((math.sin(amp_rad))**2)*((math.sin(math.atan2(math.sin(2*math.pi * x/width+phase),math.cos(amp_rad)*math.cos(2*math.pi * x/width+phase))))**2)))
        x2 = 0
        if dx != 0:
            x2 = x - fx / dx

        if abs(x2 - x) < newton_threshold:
            break

        x = x2

    return x

def tangent_angle(trapezoid_line, i, width, height, amplitude, phase, newton_count, newton_threshold, orthogonal_threshold):
    x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i)

    a, b = linear.ab(x1, y1, x2, y2)

    center_x = linear.center_slice(a, b, height, x1)

    # y = - W/2π * asin(sin(amp)*sin(atan(tan(x+phs)*cos(amp)))) + H/2
    # y = ax + b

    # ax + b + 振幅(amplitude) * sin(2*pi * (x/w) + 位相(phase)) - H/2
    # 微分
    # a + amplitude * 2π/W * cos(2π * (x/w) + phase)

    # ニュートン法
    nt_x = newton(a, b, center_x, width, height, amplitude, phase, newton_count, newton_threshold)

    # 接線
    # y = f'(nt_x)*x + (-nt_x*f'(nt_x) + f(nt_x))
    amp_rad = rad_conv(amplitude)
    fx = width/(2*math.pi) * math.asin( math.sin(amp_rad) * math.sin(math.atan2(math.sin(2*math.pi *nt_x/width+phase), math.cos(amp_rad)*math.cos(2*math.pi *nt_x/width+phase)))) + height/2
    dx = (math.sin(amp_rad)*math.cos(amp_rad)*math.cos(math.atan2(math.sin(2*math.pi *nt_x/width+phase),math.cos(amp_rad)*math.cos(2*math.pi *nt_x/width+phase)))) / ((((math.cos(2*math.pi *nt_x/width+phase))**2)*((math.cos(amp_rad))**2)+((math.sin(2*math.pi *nt_x/width+phase))**2))*math.sqrt(1-((math.sin(amp_rad))**2)*((math.sin(math.atan2(math.sin(2*math.pi *nt_x/width+phase),math.cos(amp_rad)*math.cos(2*math.pi *nt_x/width+phase))))**2)))

    tangent_a = dx
    tangent_b = -nt_x*dx + fx

    # 接線と直線との角度
    theta = 0
    if (1+a*tangent_a) != 0:
        theta = math.atan((tangent_a-a)/(1+a*tangent_a))
    theta = theta * 180 / math.pi

    if theta >= (90 - orthogonal_threshold) or (theta >= -orthogonal_threshold and theta <= 0):
        return True
    else:
        return False

def line_orthogonal(a):
    ort_a = -1 / a
    return ort_a

def line_orthogonal_intersection(a, b, ort_a, inter_y):
    inter_x = (inter_y - b) / a
    ort_b = inter_x * (a - ort_a) + b
    return inter_x , ort_b

def rotation_angle(a, x, y, width, height):
    phs = math.atan2((math.pi*(y-height/2)),a * height) - (2*math.pi*x)/width
    amp = 0
    if height*math.sin((2*math.pi*x)/width + phs) != 0:
        amp = ((y-height/2)*math.pi)/(height*math.sin((2*math.pi*x)/width + phs))
    phs = degree_conv(phs) + 180
    amp = degree_conv(amp) + 90
    print (phs, amp)
    return round(phs), round(amp)

def get_phs(trapezoid_line, i, width, height, y, filename):
    x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i)
    a, b = linear.ab(x1, y1, x2, y2)
    ort_a = line_orthogonal(a)
    x, ort_b = line_orthogonal_intersection(a, b, ort_a, y)
    phs, amp = rotation_angle(ort_a, x, y, width, height)
    ox1, ox2 = linear.two_slice(ort_a, ort_b, int(ort_b-500), int(ort_b+500), int(width/2))
    # y座標軸は上が0、下に伸びる
    img_temp = cv2.imread(filename, 1)
    cv2.line(img_temp,(x1,y1),(x2,y2),(0,0,255),2)
    cv2.line(img_temp,(int(ox1),int(ort_b-500)),(int(ox2),int(ort_b+500)),(0,0,255),2)
    print (y, x, ort_b)
    print (amp, phs)
    for x in range(0,width):
        fx = - height/math.pi * rad_conv(amp-90) * math.sin((2*math.pi *x/width+rad_conv(phs-180))) + height/2
        cv2.line(img_temp,(x,int(fx-5)),(x,int(fx+5)),(0,255,00),2)
    while(1):
        img_temp = cv2.resize(img_temp, (int(width/4), int(height/4)))
        cv2.imshow("sessen", img_temp)
        k = cv2.waitKey(1)
        if k == 27:
            break
    return phs, amp

def make_sin_bin(trapezoid_line, width, height, filename):
    # sin用bin
    # 1度ずつ360度ずらす
    phs_trans = 360
    amp_trans = 180
    sin_bin = [[0 for i in range(phs_trans)] for j in range(amp_trans)]

    for i in range(0,len(trapezoid_line)):
        for y in range(int(height/4), int(height*3/4)):
            phs, amp = get_phs(trapezoid_line, i, width, height, y, filename)
            sin_bin[amp][phs] += 1

    sin_bin_max = np.max(sin_bin)
    index_phs = np.array([])
    index_amp = np.array([])
    for phs_i in range(0, phs_trans):
        for amp_i in range(0, amp_trans):
            if sin_bin_max == sin_bin[amp_i][phs_i]:
                index_phs = np.append(index_phs, phs_i)
                index_amp = np.append(index_amp, amp_i)
                #print (amp_i, phs_i)

    phs_i = index_phs.mean()
    amp_i = index_amp.mean()

    phs_ask = phs_i - 180
    amp_ask = amp_i - 90

    return phs_ask, amp_ask

def approximation_dv(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold, filename):
    # 出力配列
    draw_line = []

    # 求まった関数の位相
    phase, amplitude = make_sin_bin(trapezoid_line, width, height, filename)

    amp_rad = rad_conv(amplitude)
    phs_rad = rad_conv(phase)
    img_temp = cv2.imread(filename, 1)
    for i in range(0,len(trapezoid_line)):
        tangent_bool = tangent_angle(trapezoid_line, i, width, height, amplitude, phs_rad, newton_count, newton_threshold, orthogonal_threshold)
        if tangent_bool:
            x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i)
            draw_line.append((x1,y1,x2,y2))
            cv2.line(img_temp,(x1,y1),(x2,y2),(0,0,255),2)

    for nt_x in range(0,width):
        fx = - width/(2*math.pi) * math.asin( math.sin(amp_rad) * math.sin(math.atan2(math.sin(2*math.pi *nt_x/width+phs_rad), math.cos(amp_rad)*math.cos(2*math.pi *nt_x/width+phs_rad)))) + height/2
        cv2.line(img_temp,(nt_x,int(fx-5)),(nt_x,int(fx+5)),(0,255,00),2)

    cv2.imwrite("func.jpg", img_temp)

    return draw_line, phase, amplitude
