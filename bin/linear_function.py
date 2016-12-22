# import library
import cv2
import math
import numpy as np

def ab(x1, y1, x2, y2):
    a = 0
    if x2 - x1 != 0:
        a = (y2 - y1)/(x2 - x1)
    b = a * (-x1) + y1

    return a, b

def center_slice(a, b, height, x):
    if a != 0:
        return (height/2 - b) / a
    else:
        return x

def two_slice(a, b, top, bottom, x):
    if a != 0:
        cross1_x = (top    - b) / a
        cross2_x = (bottom - b) / a
    else:
        cross1_x = cross2_x = x

    return cross1_x, cross2_x
