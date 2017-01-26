# import library
import cv2
import math
import numpy as np

# Find a line from 2 points
def get_ab(x1, y1, x2, y2):
    if y1 == y2: # horizon line
        return 0, y1
    if x1 == x2: # vertical line
        return 0, -1 # line in image
    # not horizon or vertical
    a = (y2 - y1)/(x2 - x1)
    b = -a * x1 + y1
    return a, b

# Coordinate of the intersection at height/2
def slice_center_x(a, b, height, x):
    if a != 0:
        return (height/2 - b) / a
    else:
        return x

# Coordinate of the intersection at two y's
def slice_two_y(a, b, line1, line2):
    cross1_x = (line1 - b) / a
    cross2_x = (line2 - b) / a

    return cross1_x, cross2_x

# Coordinate of the intersection at two x's
def slice_two_x(a, b, line1, line2):
    cross1_y = a * line1 + b
    cross2_y = a * line2 + b

    return cross1_y, cross2_y

# y = ax + b
def get_y(a, b, x):
    y = a * x + b
    return y

def get_b(a, x, y):
    b = y - a * x
    return b
