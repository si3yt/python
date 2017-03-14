# import library
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

# import files
import constant as const
import list_operation as list_opr
import linear_function as linear
import conversion as conv
import horizon as horizon

# newton method
def newton(a, b, center_x, amplitude, phase, h, w):
    x = center_x
    count = const.get_newton_count()
    threshold = const.get_newton_threshold()
    for j in range(0, count):
        fx = horizon.get_fx0(a, b, x, amplitude, phase, h, w)
        dx = horizon.get_dx0(a, x, amplitude, phase, h, w)
        x2 = 0
        if dx != 0:
            x2 = x - fx / dx

        if abs(x2 - x) < threshold:
            break

        x = x2

    return x

# bool angle at tangent line
def tangent_angle(trapezoid_line, i, amplitude, phase, h, w):
    x1, y1, x2, y2 = list_opr.adaptation_value(trapezoid_line, i)
    a, b = linear.get_ab(x1, y1, x2, y2)
    center_x = linear.slice_center_x(a, b, h, x1)

    # newton method
    nt_x = newton(a, b, center_x, amplitude, phase, h, w)

    # ask tangent line
    # horizon
    fx = horizon.get_fx(nt_x, amplitude, phase, h, w)
    # differential
    dx = horizon.get_dx(nt_x, amplitude, phase, h, w)

    tangent_a = dx
    tangent_b = -nt_x*dx + fx

    # angle of line and tangent line
    theta = 0
    if (1 + a * tangent_a) != 0:
        theta = math.atan((tangent_a-a)/(1+a*tangent_a))
    theta = theta * 180 / math.pi

    threshold = const.get_orthogonal_threshold()
    if theta >= (90 - threshold) or (theta >= -threshold and theta <= 0):
        return True
    else:
        return False

# get orthogonal a
def get_line_orthogonal(a):
    return -1 / a
# get intersection x
def get_intersection_x(a, b, y):
    x = (y - b) / a
    return x
# get phase
def get_phs(x, y, a, h, w):
    phs = math.atan2((math.pi * (y - h/2)), a * h) - (2*math.pi*x) / w

    return phs
# get amplitude
def get_amp(x, y, phs, h, w):
    amp = 0
    if h *math.sin((2*math.pi*x) / w + phs) != 0:
        amp = ((y - h/2) * math.pi) / (h * math.sin((2*math.pi*x) / w + phs))

    return amp

# show midstream img
def show_midstream_img(x1, y1, x2, y2, oy1, oy2, amp, phs, filename):
    img = cv2.imread(filename, 1)
    h = img.shape[0]
    w = img.shape[1]

    cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)
    cv2.line(img, (0,int(oy1)), (w,int(oy2)), (0,0,255), 2)
    amp_rad = conv.get_rad(amp - 90)
    phs_rad = conv.get_rad(phs - 180)
    for x in range(0,w):
        fx = h/math.pi * amp_rad * math.sin((2*math.pi*x / w + phs_rad)) + h/2
        cv2.line(img, (x,int(fx-5)), (x,int(fx+5)), (0,255,00), 2)
    while(1):
        img = cv2.resize(img, (int(w/4), int(h/4)))
        cv2.imshow("tangent line", img)
        k = cv2.waitKey(1)
        if k == 27: # ESC key finish while
            break

    return 0

# get phase and amplitude
def get_phsamp(trapezoid_line, i, y, h, w, filename):
    x1, y1, x2, y2 = list_opr.adaptation_value(trapezoid_line, i)
    a, b = linear.get_ab(x1, y1, x2, y2)
    # find tangent line (ort = tangent line)
    if a != 0:
        ort_a = get_line_orthogonal(a)
        x = get_intersection_x(a, b, y)
        ort_b = linear.get_b(ort_a, x, y)
    else:
        ort_a = 0
        ort_b = y
        x = x1
    phs = get_phs(x, y, ort_a, h, w)
    amp = get_amp(x, y, phs, h, w)
    phs = round(conv.get_degree(phs) + 180)
    amp = round(conv.get_degree(amp) + 90)
    oy1, oy2 = linear.slice_two_x(ort_a, ort_b, 0, w)

    # show midstream image
    #show_midstream_img(x1, y1, x2, y2, oy1, oy2, amp, phs, filename)

    return phs, amp

# operation bin
def operation_bin(v_bin, c_bin, temp_bin, len1, len2, color_interval):
    for i in range(0, len1):
        for j in range(0, len2):
            if temp_bin[i][j] == 1:
                v_bin[i][j] += 1
                for ch in range(0,4):
                    for cw in range(0,4):
                        c_bin[i*4+ch][j*4+cw][0] += color_interval
                        c_bin[i*4+ch][j*4+cw][1] += color_interval
                        c_bin[i*4+ch][j*4+cw][2] += color_interval

    return v_bin, c_bin

# get max value in voting bin
def get_bin_max(voting_bin):
    voting_max_value = np.max(voting_bin)
    voting_max = []
    for i in range(0, len(voting_bin)):
        for j in range(0, len(voting_bin[0])):
            if voting_max_value == voting_bin[i][j]:
                voting_max.append((i, j))
    voting_dispersion = np.array([])
    for i in range(0, len(voting_max)):
        mean_i = voting_max[i][0]
        mean_j = voting_max[i][1]
        dispersion_sum = 0
        for j in range(0, len(voting_max)):
            a = (voting_max[j][0] - mean_i)
            b = (voting_max[j][1] - mean_j)
            dispersion_sum += a**2 + b**2
        dispersion = dispersion_sum / len(voting_max)
        voting_dispersion = np.append(voting_dispersion, dispersion)
    dispersion_max_index = np.nanargmax(voting_dispersion)

    max_i = voting_max[dispersion_max_index][0]
    max_j = voting_max[dispersion_max_index][1]

    return max_i, max_j

# make voting space bin
def make_voting_bin(trapezoid_line, h, w, filename):
    # voting bin
    # one degree move
    phs_trans = 360
    amp_trans = 180
    voting_bin = [[0 for i in range(phs_trans+1)] for j in range(amp_trans+1)]

    # votin image array
    voting_img = np.zeros((amp_trans * 4, phs_trans * 4,3), np.uint8)
    color_interval = 255 / len(trapezoid_line)

    for i in range(0, len(trapezoid_line)):
        temp_voting_bin = [[0 for i in range(phs_trans+1)] for j in range(amp_trans+1)]
        for y in range(int(h * 2/5), int(h * 3/5)):
            phs, amp = get_phsamp(trapezoid_line, i, y, h, w, filename)
            temp_voting_bin[amp][phs] = 1

        voting_bin, voting_img = operation_bin(voting_bin, voting_img, temp_voting_bin, amp_trans, phs_trans, color_interval)

    # show and save voting bin
    plt.figure(figsize=(25,10))
    plt.imshow(voting_img)
    #plt.show()
    plt.savefig('voting_bin.png')

    # get max value in voting bin
    amp_i, phs_i = get_bin_max(voting_bin)

    # degree correction
    phs_ask = phs_i - 180
    amp_ask = amp_i - 90

    return phs_ask, amp_ask

# draw approximation horizon in image
def draw_horizon(trapezoid_line, amp, phs, filename):
    # output array
    approximation_line = []

    amp_rad = conv.get_rad(amp)
    phs_rad = conv.get_rad(phs)
    # make output image
    img = cv2.imread(filename, 1)
    h = img.shape[0]
    w = img.shape[1]
    # approximation horizon
    #for i in range(0,len(trapezoid_line)):
        #tangent_bool = tangent_angle(trapezoid_line, i, amp_rad, phs_rad, h, w)
        #if tangent_bool:
            #x1, y1, x2, y2 = list_opr.adaptation_value(trapezoid_line, i)
            #approximation_line.append((x1, y1, x2, y2))
            #cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)

    for nt_x in range(0, w):
        fx = horizon.get_fx(nt_x, amp_rad, phs_rad, h, w)
        cv2.line(img, (nt_x,int(fx-20)), (nt_x,int(fx+20)), (0,255,0), 2)

    cv2.imwrite("func.jpg", img)

# approximation function
def approximation_func(trapezoid_line, height, width, filename):
    # phase and rotation angle of function
    phase, amplitude = make_voting_bin(trapezoid_line, height, width, filename)

    # approximation horizon
    draw_horizon(trapezoid_line, amplitude, phase, filename)

    return phase, amplitude
