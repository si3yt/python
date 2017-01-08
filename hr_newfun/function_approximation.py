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

def newton(a, b, center_x, width, height, amplitude, phase, newton_count, newton_threshold):
    x = center_x
    amp_rad = rad_conv(amplitude)
    for j in range(0,newton_count):
        fx = a * x + b + width/(2*math.pi) * math.asin( math.sin(amp_rad) * math.sin(math.atan2(math.sin(2*math.pi * x/width+phase), math.cos(amp_rad)*math.cos(2*math.pi * x/width+phase)))) - height/2
        dx = a + (math.sin(amp_rad)*math.cos(amp_rad)*math.cos(math.atan2(math.sin(2*math.pi * x/width+phase),math.cos(amp_rad)*math.cos(2*math.pi * x/width+phase)))) / ((((math.cos(2*math.pi * x/width+phase))**2)*((math.cos(amp_rad))**2)+((math.sin(2*math.pi * x/width+phase))**2))*math.sqrt(1-((math.sin(amp_rad))**2)*((math.sin(math.atan2(math.sin(2*math.pi * x/width+phase),math.cos(amp_rad)*math.cos(2*math.pi * x/width+phase))))**2)))
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
    fx = - width/(2*math.pi) * math.asin( math.sin(amp_rad) * math.sin(math.atan2(math.sin(2*math.pi *nt_x/width+phase), math.cos(amp_rad)*math.cos(2*math.pi *nt_x/width+phase)))) + height/2
    dx = - (math.sin(amp_rad)*math.cos(amp_rad)*math.cos(math.atan2(math.sin(2*math.pi *nt_x/width+phase),math.cos(amp_rad)*math.cos(2*math.pi *nt_x/width+phase)))) / ((((math.cos(2*math.pi *nt_x/width+phase))**2)*((math.cos(amp_rad))**2)+((math.sin(2*math.pi *nt_x/width+phase))**2))*math.sqrt(1-((math.sin(amp_rad))**2)*((math.sin(math.atan2(math.sin(2*math.pi *nt_x/width+phase),math.cos(amp_rad)*math.cos(2*math.pi *nt_x/width+phase))))**2)))

    tangent_a = dx
    tangent_b = -nt_x*dx + fx

    '''
    filename = '../image/theta04_cor.jpg'
    img    = cv2.imread(filename, 1)

    for fxi in range(0, width):
        fxx = - width/(2*math.pi) * math.asin( math.sin(amp_rad) * math.sin(math.atan2(math.sin(2*math.pi *fxi/width+phase), math.cos(amp_rad)*math.cos(2*math.pi *fxi/width+phase)))) + height/2
        cv2.line(img,(int(width/2),int(height/2)),(int(fxi),int(fxx)),(255,0,0),2)

    x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i)
    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    fxx = - width/(2*math.pi) * math.asin( math.sin(amp_rad) * math.sin(math.atan2(math.sin(2*math.pi *nt_x/width+phase), math.cos(amp_rad)*math.cos(2*math.pi *nt_x/width+phase)))) + height/2
    cv2.line(img,(int(width/2),int(height/2)),(int(nt_x),int(fxx)),(0,255,0),2)

    tx1, tx2 = linear.two_slice(tangent_a, tangent_b, -2000, 2000, center_x)
    ty1 = tangent_a * tx1 + tangent_b
    ty2 = tangent_a * tx2 + tangent_b
    cv2.line(img,(int(tx1),int(ty1)),(int(tx2),int(ty2)),(0,255,0),2)

    print (tangent_a, tx1, ty1, tx2, ty2)

    while(1):
        img = cv2.resize(img, (int(width/4), int(height/4)))
        cv2.imshow("sphere_rotate", img)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            break
    '''

    # 接線と直線との角度
    theta = 0
    if (1+a*tangent_a) != 0:
        theta = math.atan((tangent_a-a)/(1+a*tangent_a))
    theta = theta * 180 / math.pi

    if theta >= (90 - orthogonal_threshold) or (theta >= -orthogonal_threshold and theta <= 0):
        return True
    else:
        return False

def make_sin_bin(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold, amplitude_lim):
    # sin用bin
    # 1度ずつ360度ずらす
    phs_trans = 360
    amp_trans = amplitude_lim
    sin_bin = [[0 for i in range(phs_trans)] for j in range(amp_trans)]

    for phs in range(0,phs_trans):
        phase = phs
        # 角度 → ラジアン
        phase = rad_conv(phase)
        for amp in range(0,amp_trans):#range(0,amp_trans):
            for i in range(0,len(trapezoid_line)):
                tangent_bool = tangent_angle(trapezoid_line, i, width, height, amp, phase, newton_count, newton_threshold, orthogonal_threshold)
                if tangent_bool:
                    sin_bin[amp][phs] += 1

    sin_bin_max = np.max(sin_bin)
    index_phs = np.array([])
    index_amp = np.array([])
    for phs_i in range(0, phs_trans):
        for amp_i in range(0, amp_trans):
            if sin_bin_max == sin_bin[amp_i][phs_i]:
                index_phs = np.append(index_phs, phs_i)
                index_amp = np.append(index_amp, amp_i)
                print (amp_i, phs_i)

    phs_i = index_phs.mean()
    amp_i = index_amp.mean()

    phs_ask = phs_i
    amp_ask = amp_i

    return phs_ask, amp_ask

def approximation_draw(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold):
    # 出力配列
    draw_line = []

    # 求まった関数の位相
    phase, amplitude = make_sin_bin(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold)

    filename = '../image/theta04_cor.jpg'
    img    = cv2.imread(filename, 1)

    for i in range(0,len(trapezoid_line)):
        tangent_bool = tangent_angle(trapezoid_line, i, width, height, amplitude, phase, newton_count, newton_threshold, orthogonal_threshold)
        if tangent_bool:
            x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i)
            draw_line.append((x1,y1,x2,y2))
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    while(1):
        img = cv2.resize(img, (int(width/4), int(height/4)))
        cv2.imshow("sphere_rotate", img)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            break

    return draw_line

def approximation_vertex(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold, amplitude_lim):
    # 求まった関数の位相
    phase, amplitude = make_sin_bin(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold, amplitude_lim)

    '''
    filename = '../image/theta04_cor.jpg'
    img    = cv2.imread(filename, 1)

    for i in range(0,len(trapezoid_line)):
        tangent_bool = tangent_angle(trapezoid_line, i, width, height, amplitude, phase, newton_count, newton_threshold, orthogonal_threshold)
        if tangent_bool:
            x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i)
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    while(1):
        img = cv2.resize(img, (int(width/4), int(height/4)))
        cv2.imshow("sphere_rotate", img)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            break
    '''

    sin_vertex_x = phase
    sin_vettex_y = amplitude

    return sin_vertex_x, sin_vettex_y
