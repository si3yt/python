# import
import os
import cv2
import math
import numpy as np

def sinc_h(t): #sinc関数
    t = math.fabs(t)
    if t <= 1:
        return t**3 - 2 * t**2 + 1
    elif 1 < t <= 2:
        return -t**3 + 5 * t**2 - 8 * t + 4
    elif 2 < t: #else
        return 0

def bicubic(x, y, img, height, width):
    result_rgb = np.array([0,0,0])

    if x < 0 or x >= width-1 or y < 0 or y >= height-1: #参照先が画像内でない
        return [ 0, 0, 0 ]
    x1 = 1 + x - int(x)
    x2 = x - int(x)
    x3 = 1 - x + int(x)
    x4 = 2 - x + int(x)
    y1 = 1 + y - int(y)
    y2 = y - int(y)
    y3 = 1 - y + int(y)
    y4 = 2 - y + int(y)

    left_flag         = False
    left_top_flag     = False
    left_bottom_flag  = False
    right_flag        = False
    right_top_flag    = False
    right_bottom_flag = False
    top_flag          = False
    bottom_flag       = False

    if x-x1 < 0:                    #左
        if y+y1 >= height:          #左下
            left_bottom_flag = True
        elif y-y4 < 0:              #左上
            left_top_flag = True
        else:
            left_flag = True
    elif x+x4 >= width:             #右
        if y+y1 >= height:          #右下
            right_bottom_flag = True
        elif y-y4 < 0:              #右上
            right_top_flag = True
        else:
            right_flag = True
    elif y+y1 >= height:
        bottom_flag = True          #下
    elif y-y4 < 0:
        top_flag = True             #上

    f22 = img[int(y+y2)][int(x-x2)]
    f23 = img[int(y-y3)][int(x-x2)]
    f32 = img[int(y+y2)][int(x+x3)]
    f33 = img[int(y-y3)][int(x+x3)]

    if left_flag == True:
        f11 = img[int(y+y1)][int(width-1)]
        f12 = img[int(y+y2)][int(width-1)]
        f13 = img[int(y-y3)][int(width-1)]
        f14 = img[int(y-y4)][int(width-1)]
        f21 = img[int(y+y1)][int(x-x2)]
        f24 = img[int(y-y4)][int(x-x2)]
        f31 = img[int(y+y1)][int(x+x3)]
        f34 = img[int(y-y4)][int(x+x3)]
        f41 = img[int(y+y1)][int(x+x4)]
        f42 = img[int(y+y2)][int(x+x4)]
        f43 = img[int(y-y3)][int(x+x4)]
        f44 = img[int(y-y4)][int(x+x4)]
    elif right_flag == True:
        f11 = img[int(y+y1)][int(x-x1)]
        f12 = img[int(y+y2)][int(x-x1)]
        f13 = img[int(y-y3)][int(x-x1)]
        f14 = img[int(y-y4)][int(x-x1)]
        f21 = img[int(y+y1)][int(x-x2)]
        f24 = img[int(y-y4)][int(x-x2)]
        f31 = img[int(y+y1)][int(x+x3)]
        f34 = img[int(y-y4)][int(x+x3)]
        f41 = img[int(y+y1)][int(0)]
        f42 = img[int(y+y2)][int(0)]
        f43 = img[int(y-y3)][int(0)]
        f44 = img[int(y-y4)][int(0)]
    elif bottom_flag == True:
        f11 = img[int(y-y1)][int(math.fabs(x-x1-width)-1)]
        f12 = img[int(y+y2)][int(x-x1)]
        f13 = img[int(y-y3)][int(x-x1)]
        f14 = img[int(y-y4)][int(x-x1)]
        f21 = img[int(y-y1)][int(math.fabs(x-x2-width)-1)]
        f24 = img[int(y-y4)][int(x-x2)]
        f31 = img[int(y-y1)][int(math.fabs(x+x3-width)-1)]
        f34 = img[int(y-y4)][int(x+x3)]
        f41 = img[int(y-y1)][int(math.fabs(x+x4-width)-1)]
        f42 = img[int(y+y2)][int(x+x4)]
        f43 = img[int(y-y3)][int(x+x4)]
        f44 = img[int(y-y4)][int(x+x4)]
    elif top_flag == True:
        f11 = img[int(y+y1)][int(x-x1)]
        f12 = img[int(y+y2)][int(x-x1)]
        f13 = img[int(y-y3)][int(x-x1)]
        f14 = img[int(y+y4)][int(math.fabs(x-x1-width)-1)]
        f21 = img[int(y+y1)][int(x-x2)]
        f24 = img[int(y+y4)][int(math.fabs(x-x2-width)-1)]
        f31 = img[int(y+y1)][int(x+x3)]
        f34 = img[int(y+y4)][int(math.fabs(x+x3-width)-1)]
        f41 = img[int(y+y1)][int(x+x4)]
        f42 = img[int(y+y2)][int(x+x4)]
        f43 = img[int(y-y3)][int(x+x4)]
        f44 = img[int(y+y4)][int(math.fabs(x+x4-width)-1)]
    elif left_bottom_flag == True:
        f11 = img[int(y-y1)][int(width-1)]
        f12 = img[int(y+y2)][int(width-1)]
        f13 = img[int(y-y3)][int(width-1)]
        f14 = img[int(y-y4)][int(width-1)]
        f21 = img[int(y-y1)][int(math.fabs(x-x2-width)-1)]
        f24 = img[int(y-y4)][int(x-x2)]
        f31 = img[int(y-y1)][int(math.fabs(x+x3-width)-1)]
        f34 = img[int(y-y4)][int(x+x3)]
        f41 = img[int(y-y1)][int(math.fabs(x+x4-width)-1)]
        f42 = img[int(y+y2)][int(x+x4)]
        f43 = img[int(y-y3)][int(x+x4)]
        f44 = img[int(y-y4)][int(x+x4)]
    elif left_top_flag == True:
        f11 = img[int(y+y1)][int(width-1)]
        f12 = img[int(y+y2)][int(width-1)]
        f13 = img[int(y-y3)][int(width-1)]
        f14 = img[int(y+y4)][int(width-1)]
        f21 = img[int(y+y1)][int(x-x2)]
        f24 = img[int(y+y4)][int(math.fabs(x-x2-width)-1)]
        f31 = img[int(y+y1)][int(x+x3)]
        f34 = img[int(y+y4)][int(math.fabs(x+x3-width)-1)]
        f41 = img[int(y+y1)][int(x+x4)]
        f42 = img[int(y+y2)][int(x+x4)]
        f43 = img[int(y-y3)][int(x+x4)]
        f44 = img[int(y+y4)][int(math.fabs(x+x4-width)-1)]
    elif right_bottom_flag == True:
        f11 = img[int(y-y1)][int(math.fabs(x-x1-width)-1)]
        f12 = img[int(y+y2)][int(x-x1)]
        f13 = img[int(y-y3)][int(x-x1)]
        f14 = img[int(y-y4)][int(x-x1)]
        f21 = img[int(y-y1)][int(math.fabs(x-x2-width)-1)]
        f24 = img[int(y-y4)][int(x-x2)]
        f31 = img[int(y-y1)][int(math.fabs(x+x3-width))]
        f34 = img[int(y-y4)][int(x+x3)]
        f41 = img[int(y-y1)][int(0)]
        f42 = img[int(y+y2)][int(0)]
        f43 = img[int(y-y3)][int(0)]
        f44 = img[int(y-y4)][int(0)]
    elif right_top_flag == True:
        f11 = img[int(y+y1)][int(x-x1)]
        f12 = img[int(y+y2)][int(x-x2)]
        f13 = img[int(y-y3)][int(x+x3)]
        f14 = img[int(y+y4)][int(math.fabs(x-x1-width)-1)]
        f21 = img[int(y+y1)][int(x-x2)]
        f24 = img[int(y+y4)][int(math.fabs(x-x2-width)-1)]
        f31 = img[int(y+y1)][int(x+x3)]
        f34 = img[int(y+y4)][int(math.fabs(x+x3-width)-1)]
        f41 = img[int(y+y1)][int(0)]
        f42 = img[int(y+y2)][int(0)]
        f43 = img[int(y-y3)][int(0)]
        f44 = img[int(y+y4)][int(0)]
    else:
        f11 = img[int(y+y1)][int(x-x1)]
        f12 = img[int(y+y2)][int(x-x1)]
        f13 = img[int(y-y3)][int(x-x1)]
        f14 = img[int(y-y4)][int(x-x1)]
        f21 = img[int(y+y1)][int(x-x2)]
        f24 = img[int(y-y4)][int(x-x2)]
        f31 = img[int(y+y1)][int(x+x3)]
        f34 = img[int(y-y4)][int(x+x3)]
        f41 = img[int(y+y1)][int(x+x4)]
        f42 = img[int(y+y2)][int(x+x4)]
        f43 = img[int(y-y3)][int(x+x4)]
        f44 = img[int(y-y4)][int(x+x4)]

    matrix_hx = np.array([ sinc_h(x1), sinc_h(x2), sinc_h(x3), sinc_h(x4) ])
    matrix_hy = np.array([ [sinc_h(y1)], [sinc_h(y2)], [sinc_h(y3)], [sinc_h(y4)] ])

    for i in range(3):
        matrix_f  = np.array([ [f11[i], f12[i], f13[i], f14[i]], \
                               [f21[i], f22[i], f23[i], f24[i]], \
                               [f31[i], f32[i], f33[i], f34[i]], \
                               [f41[i], f42[i], f43[i], f44[i]] ])
        matrix_cube = matrix_hx.dot(matrix_f)
        matrix_cube = matrix_cube.dot(matrix_hy)
        if matrix_cube > 255:
            matrix_cube = 255
        elif matrix_cube < 0:
            matrix_cube = 0
        result_rgb[i] = matrix_cube

    return result_rgb
