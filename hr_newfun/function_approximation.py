# import library
import cv2
import math
import numpy as np

# import files
import list_operation as list_opr
import linear_function as linear

def newton(a, b, center_x, width, height, amplitude, phase, newton_count, newton_threshold):
    x = center_x
    for j in range(0,newton_count):
        fx = a * x + b + amplitude * math.sin(2*math.pi * x/width + phase) - height/2
        dx = a + amplitude * 2*math.pi/width * math.cos(2*math.pi * x/width + phase)

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
        phase = phase * math.pi / 180
        for amp in range(0,amp_trans):#range(0,amp_trans):
            for i in range(0,len(trapezoid_line)):
                tangent_bool = tangent_angle(trapezoid_line, i, width, height, amp, phase, newton_count, newton_threshold, orthogonal_threshold)
                if tangent_bool:
                    sin_bin[amp][phs] += 1

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

def approximation_vertex(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold, amplitude_lim):
    # 求まった関数の位相
    phase, amplitude = make_sin_bin(trapezoid_line, width, height, newton_count, newton_threshold, orthogonal_threshold, amplitude_lim)

    sin_vertex_x = width * (3/4 - phase/(2*math.pi))
    sin_vettex_y = height/2 + amplitude

    return sin_vertex_x, sin_vettex_y
