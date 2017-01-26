# import library
import cv2
import math
import numpy as np

# import files
import constant as const
import list_operation as list_opr
import linear_function as linear
import conversion as conv
import horizon as horizon

# newton method
def newton(a, b, center_x, amplitude, phase):
    x = center_x
    count = const.get_newton_count()
    threshold = const.get_newton_threshold()
    for j in range(0, count):
        fx = horizon.get_fx0(a, b, x, amplitude, phase)
        dx = horizon.get_dx0(a, x, amplitude, phase)
        x2 = 0
        if dx != 0:
            x2 = x - fx / dx

        if abs(x2 - x) < threshold:
            break

        x = x2

    return x

# bool angle at tangent line
def tangent_angle(trapezoid_line, i, amplitude, phase):
    width  = const.get_img_width()
    height = const.get_img_height()
    x1, y1, x2, y2 = list_opr.adaptation_value(trapezoid_line, i)
    a, b = linear.get_ab(x1, y1, x2, y2)
    center_x = linear.slice_center_x(a, b, height, x1)

    # newton method
    nt_x = newton(a, b, center_x, amplitude, phase)

    # ask tangent line
    # horizon
    fx = horizon.get_fx(nt_x, amplitude, phase)
    # differential
    dx = horizon.get_dx(nt_x, amplitude, phase)

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
def get_phs(x, y, a):
    width  = const.get_img_width()
    height = const.get_img_height()
    phs = math.atan2((math.pi*(y-height/2)),a * height) - (2*math.pi*x)/width

    return phs
# get amplitude
def get_amp(x, y, phs):
    width  = const.get_img_width()
    height = const.get_img_height()
    amp = 0
    if height*math.sin((2*math.pi*x)/width + phs) != 0:
        amp = ((y-height/2)*math.pi)/(height*math.sin((2*math.pi*x)/width + phs))

    return amp
# get phase and amplitude
def get_phsamp(trapezoid_line, i, y):
    width  = const.get_img_width()
    height = const.get_img_height()

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
    phs = get_phs(x, y, ort_a)
    amp = get_amp(x, y, phs)
    phs = round(conv.get_degree(phs) + 180)
    amp = round(conv.get_degree(amp) + 90)
    oy1, oy2 = linear.slice_two_x(ort_a, ort_b, 0, width)

    '''
    # show halfway image
    filename = const.get_filename()
    img_temp = cv2.imread(filename, 1)
    cv2.line(img_temp,(x1,y1),(x2,y2),(0,0,255),2)
    cv2.line(img_temp,(0,int(oy1)),(width,int(oy2)),(0,0,255),2)
    for x in range(0,width):
        fx = height/math.pi * conv.get_rad(amp-90) * math.sin((2*math.pi *x/width+conv.get_rad(phs-180))) + height/2
        cv2.line(img_temp,(x,int(fx-5)),(x,int(fx+5)),(0,255,00),2)
    while(1):
        img_temp = cv2.resize(img_temp, (int(width/4), int(height/4)))
        cv2.imshow("sessen", img_temp)
        k = cv2.waitKey(1)
        if k == 27: # ESC key finish while
            break
    '''

    return phs, amp
# make voting space bin
def make_voting_bin(trapezoid_line):
    # voting bin
    # one degree move
    phs_trans = 360
    amp_trans = 180
    voting_bin = [[0 for i in range(phs_trans)] for j in range(amp_trans)]

    width  = const.get_img_width()
    height = const.get_img_height()

    for i in range(0, len(trapezoid_line)):
        for y in range(int(height*2/5), int(height*3/5)):
            phs, amp = get_phsamp(trapezoid_line, i, y)
            voting_bin[amp][phs] += 1

    # get max value in voting bin
    voting_bin_max = np.max(voting_bin)
    index_phs = np.array([])
    index_amp = np.array([])
    # find max value index
    for phs_i in range(0, phs_trans):
        for amp_i in range(0, amp_trans):
            if voting_bin_max == voting_bin[amp_i][phs_i]:
                index_phs = np.append(index_phs, phs_i)
                index_amp = np.append(index_amp, amp_i)
    # average of max value index
    phs_i = index_phs.mean()
    amp_i = index_amp.mean()
    # degree correction
    phs_ask = phs_i - 180
    amp_ask = amp_i - 90

    return phs_ask, amp_ask

# approximation function
def approximation_func(trapezoid_line):
    width  = const.get_img_width()
    height = const.get_img_height()
    # output array
    approximation_line = []

    # phase and rotation angle of function
    phase, amplitude = make_voting_bin(trapezoid_line)
    amp_rad = conv.get_rad(amplitude)
    phs_rad = conv.get_rad(phase)

    # make output image
    filename = const.get_filename()
    img_temp = cv2.imread(filename, 1)
    # approximation horizon
    for i in range(0,len(trapezoid_line)):
        tangent_bool = tangent_angle(trapezoid_line, i, amp_rad, phs_rad)
        if tangent_bool:
            x1, y1, x2, y2 = list_opr.adaptation_value(trapezoid_line, i)
            approximation_line.append((x1,y1,x2,y2))
            cv2.line(img_temp,(x1,y1),(x2,y2),(0,0,255),2)

    for nt_x in range(0,width):
        fx = horizon.get_fx(nt_x, amp_rad, phs_rad)
        cv2.line(img_temp,(nt_x,int(fx-5)),(nt_x,int(fx+5)),(0,255,00),2)

    cv2.imwrite("func.jpg", img_temp)

    return phase, amplitude
