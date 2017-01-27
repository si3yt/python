# import
import cv2
import math
import numpy as np

# import files
import bicubic_correspondence as cor

# sinc function
def sinc_h(t):
    t = math.fabs(t)
    if t <= 1:
        return t**3 - 2 * t**2 + 1
    elif 1 < t <= 2:
        return -t**3 + 5 * t**2 - 8 * t + 4
    elif 2 < t: # else
        return 0

# bicubic interpolation
def bicubic(x, y, img, height, width):
    result_rgb = np.array([0,0,0])

    if x < 0 or x >= width-1 or y < 0 or y >= height-1: # not in image
        return [ 0, 0, 0 ]
    x1 = 1 + x - int(x)
    x2 = x - int(x)
    x3 = 1 - x + int(x)
    x4 = 2 - x + int(x)
    y1 = 1 + y - int(y)
    y2 = y - int(y)
    y3 = 1 - y + int(y)
    y4 = 2 - y + int(y)

    f22 = img[int(y+y2)][int(x-x2)]
    f23 = img[int(y-y3)][int(x-x2)]
    f32 = img[int(y+y2)][int(x+x3)]
    f33 = img[int(y-y3)][int(x+x3)]

    f11, f12, f13, f14, f21, f24, f31, f34, f41, f42, f43, f44 = cor.correspondence(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width)

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
