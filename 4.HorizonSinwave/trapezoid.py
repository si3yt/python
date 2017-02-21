# import library
import cv2
import math
import numpy as np

# import files
import constant as const
import list_operation as list_opr
import linear_function as linear

def trapezoid_area(c11, c12, c21, c22, top, bottom):
    # length of trapezoid top
    t_top = abs(c11 - c21)
    # length of trapezoid bottom
    t_bottom = abs(c12 - c22)
    # trapezoid height
    t_height = abs(bottom - top)
    # trapezoidal area
    return (t_top + t_bottom) * t_height / 2

def dense_judge(trapezoid):
    threshold = const.get_trapezoid_threshold()
    if trapezoid <= threshold:
        return True
    else:
        return False

def cross_point(line, i, top, bottom):
    x1, y1, x2, y2 = list_opr.adaptation_value(line, i)
    a, b = linear.get_ab(x1, y1, x2, y2)
    # cross
    if a != 0:
        cross1_x, cross2_x = linear.slice_two_y(a, b, top, bottom)
    else:
        cross1_x = cross2_x = x1

    return cross1_x, cross2_x


def search_dense_area(a_line, rem_line):
    top = const.get_slice_line_top()
    bottom = const.get_slice_line_bottom()

    append_line = []
    # line of interst
    for i in range(0, len(a_line)):
        cross11_x, cross12_x = cross_point(a_line, i, top, bottom)
        # comparison
        j = 0
        while(True):
            if len(rem_line) == 0:
                break
            cross21_x, cross22_x = cross_point(rem_line, j, top, bottom)
            # trapezoidal area
            trapezoid = (trapezoid_area(cross11_x, cross12_x, cross21_x, cross22_x, top, bottom))
            # refine by
            if dense_judge(trapezoid):
                x1, y1, x2, y2 = list_opr.adaptation_value(rem_line, j)
                append_line.append((x1,y1,x2,y2,j))
                rem_line.pop(j)
            else:
                j += 1
            if j == len(rem_line):
                break

    return rem_line, a_line

# search other dense line
def search_more_line(t_line, rem_line, lines, h, w):
    x1, y1, x2, y2 = list_opr.adaptation_value_pop(t_line)
    a, b = linear.get_ab(x1, y1, x2, y2)
    if a != 0:
        ox1, ox2 = linear.slice_two_y(a, b, 0, h)
    else:
        ox1 = ox2 = x1
    count = 1
    append_line = lines
    # search dense area
    while(True):
        for j in range(0, len(lines)):
            x1, y1, x2, y2 = list_opr.adaptation_value(lines, j)
            a, b = linear.get_ab(x1, y1, x2, y2)
            if a != 0:
                cx1, cx2 = linear.slice_two_y(a, b, 0, h)
            else:
                cx1 = cx2 = x1
            ox1 += cx1
            ox2 += cx2
            count += 1
        if len(rem_line) != 0:
            rem_line, append_line = search_dense_area(append_line, rem_line)
        else:
            append_line = []
        lines = append_line
        if len(append_line) == 0:
            break

    ox1 = int(ox1 / count)
    ox2 = int(ox2 / count)

    return rem_line, ox1, ox2


# first dense judgment
def search_dense_line(line, i):
    # dense const
    top = const.get_slice_line_top()
    bottom = const.get_slice_line_bottom()
    # dense array
    dense_line = []
    # line of interest
    cross11_x, cross12_x = cross_point(line, i, top, bottom)
    target_line = line.pop(i)
    # comparison
    j = 0
    if len(line) != 0:
        while(True):
            cross21_x, cross22_x = cross_point(line, j, top, bottom)
            # trapezoidal area
            trapezoid = trapezoid_area(cross11_x, cross12_x, cross21_x, cross22_x, top, bottom)
            # refine by
            if dense_judge(trapezoid):
                x1, y1, x2, y2 = list_opr.adaptation_value(line, j)
                line.pop(j)
                dense_line.append((x1,y1,x2,y2))
            else:
                j += 1
            if len(line) == j:
                break

    return line, target_line, dense_line

# main
def trapezoidal_comparison(degree_line, height, width):
    # output array
    trapezoid_line = []
    # afeter removal line
    rem_line = degree_line

    # dense judgment
    while(True):
        # dense array
        rem_line, target_line, dense_line = search_dense_line(rem_line, 0)

        if len(dense_line) != 0 and len(rem_line) != 0:
            rem_line, ox1, ox2 = search_more_line(target_line, rem_line, dense_line, height, width)
            trapezoid_line.append((ox1, 0, ox2, height))
        # line of interest is not dense line
        elif len(dense_line) == 0:
            x1, y1, x2, y2 = list_opr.adaptation_value_pop(target_line)
            trapezoid_line.append((x1,y1,x2,y2))

        print (len(rem_line))

        if len(rem_line) == 0:
            break

    return trapezoid_line
