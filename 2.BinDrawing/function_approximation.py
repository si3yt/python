# import library
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from PIL import Image
# import files
import list_operation as list_opr
import linear_function as linear

def newton(a, b, center_x, width, height, amplitude, phase, newton_count, newton_threshold):
    x = center_x
    for j in range(0,newton_count):
        fx = a * x + b + amplitude * math.sin(2*math.pi * x/width + phase) - height/2
        dx = a + amplitude * 2*math.pi/width * math.cos(2*math.pi * x/width + phase)

        x2 = x - fx / dx

        if abs(x2 - x) < newton_threshold:
            break

        x = x2

    return x

def tangent_angle(trapezoid_line, i, width, height, amplitude, phase, newton_count, newton_threshold, orthogonal_threshold):
    x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i)

    a, b = linear.ab(x1, y1, x2, y2)

    center_x = linear.center_slice(a, b, height, x1)

    # y = - amplitude * sin(2π * x/W + phase) + H/2
    # y = ax + b

    # ax + b + 振幅(amplitude) * sin(2*pi * (x/w) + 位相(phase)) - H/2
    # 微分
    # a + amplitude * 2π/W * cos(2π * (x/w) + phase)

    # ニュートン法
    nt_x = newton(a, b, center_x, width, height, amplitude, phase, newton_count, newton_threshold)

    # 接線
    # y = f'(nt_x)*x + (-nt_x*f'(nt_x) + f(nt_x))
    fx = -amplitude * math.sin(2*math.pi * nt_x/width + phase) + height/2
    dx = -amplitude * 2*math.pi/width * math.cos(2*math.pi * nt_x/width + phase)

    tangent_a = dx
    tangent_b = -nt_x*dx + fx

    # 接線と直線との角度
    theta = math.atan((tangent_a-a)/(1+a*tangent_a))
    theta = theta * 180 / math.pi

    if theta >= (90 - orthogonal_threshold) or (theta >= -orthogonal_threshold and theta <= 0):
        return True
    else:
        return False

def make_sin_bin(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold):
    # sin用bin
    # 1度ずつ360度ずらす
    phs_trans = 360
    amp_trans = 360
    sin_bin = [[0 for i in range(phs_trans)] for j in range(amp_trans)]

    voting = np.zeros((amp_trans * 4, phs_trans * 4,3), np.uint8)
    color_interval = 255 / len(trapezoid_line)

    plot_img = np.zeros((height, width,3), np.uint8)

    default_img = cv2.imread('../image/theta04_cor.jpg')
    BGR_img = default_img
    RGB_img = default_img
    for h in range(0,height):
        for w in range(0,width):
            R = BGR_img[h][w][2]
            B = BGR_img[h][w][0]
            RGB_img[h][w][2] = B
            RGB_img[h][w][0] = R

    plot_img = RGB_img

    for phs in range(0,phs_trans):
        phase = phs
        # 角度 → ラジアン
        phase = phase * math.pi / 180
        for amp in range(0,amp_trans):
            for i in range(0,len(trapezoid_line)):
                tangent_bool = tangent_angle(trapezoid_line, i, width, height, amp, phase, newton_count, newton_threshold, orthogonal_threshold)
                if tangent_bool:
                    sin_bin[amp][phs] += 1
                    for color_h in range(0,4):
                        for color_w in range(0,4):
                            voting[phs*4+color_h][amp*4+color_w][2] += color_interval
                    if phs == 100 and amp == 100:
                        x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i);
                        cv2.line(plot_img,(x1,y1),(x2,y2),(255,0,0),2)

            if phs == 100 and amp == 100:
                plt.figure(figsize=(25,10))
                plt.subplot2grid((1,3), (0,0), colspan=2)
                x = np.linspace(0, width, width)
                plt.imshow(plot_img)
                plt.plot(x, amp * np.sin(2 * math.pi * x/width + phs) + height/2)
                plt.xlim(0,width)
                plt.ylim(height, 0)

                plt.subplot2grid((1,3), (0,2))
                plt.imshow(voting)
                #plt.show()
                plt.savefig('binline.png')

    cv2.imwrite("voting.jpg", voting)

    bin_max_index = np.argmax(sin_bin)
    phs_i = bin_max_index % phs_trans
    amp_i = bin_max_index / phs_trans

    phs_ask = phs_i * math.pi / 180
    amp_ask = amp_i

    return phs_ask, amp_ask

def approximation_draw(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold):
    # 出力配列
    draw_line = []

    # 求まった関数の位相
    phase, amplitude = make_sin_bin(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold)

    for i in range(0,len(trapezoid_line)):
        tangent_bool = tangent_angle(trapezoid_line, i, width, height, amplitude, phase, newton_count, newton_threshold, orthogonal_threshold)
        if tangent_bool:
            x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i)
            draw_line.append((x1,y1,x2,y2))

    return draw_line

def approximation_vertex(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold):
    # 求まった関数の位相
    phase, amplitude = make_sin_bin(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold)

    sin_vertex_x = width * (3/4 - phase/(2*math.pi))
    sin_vettex_y = height/2 + amplitude

    return sin_vertex_x, sin_vettex_y
