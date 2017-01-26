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

def search_dense_area(line1, line2, label, top, bottom):
    dense_count = 0

    append_line = []
    # line of interst
    for i in range(0,len(line1)):
        cross11_x, cross12_x = cross_point(line1, i, top, bottom)

        # comparison
        for j in range(0,len(line2)):
            if j != line1[i][4] and label[j] == 0:
                cross21_x, cross22_x = cross_point(line2, j, top, bottom)

                # trapezoidal area
                trapezoid = (trapezoid_area(cross11_x, cross12_x, cross21_x, cross22_x, top, bottom))

                # refine by
                if dense_judge(trapezoid):
                    x1, y1, x2, y2 = list_opr.adaptation_value(line2, j)
                    append_line.append((x1,y1,x2,y2,j))
                    label[j] = 1
                    dense_count += 1
    return append_line, label, dense_count

def trapezoidal_comparison(degree_line):
    width  = const.get_img_width()
    height = const.get_img_height()
    # output array
    trapezoid_line = []
    # dense judgment label
    dense_label = np.zeros(len(degree_line))
    top = const.get_slice_line_top()
    bottom = const.get_slice_line_bottom()

    # dense judgment
    for i in range(0,len(degree_line)):
        #filename = const.get_filename()
        #img = cv2.imread(filename, 1)
        if dense_label[i] == 0:
            # dense array
            dense_line = []
            # line of interest
            cross11_x, cross12_x = cross_point(degree_line, i, top, bottom)

            #img = list_opr.draw_one_line(img, degree_line, i, (0,255,0))

            # comparison
            for j in range(0,len(degree_line)):
                # not dense line
                if j != i and dense_label[j] == 0:
                    cross21_x, cross22_x = cross_point(degree_line, j, top, bottom)

                    # trapezoidal area
                    trapezoid = trapezoid_area(cross11_x, cross12_x, cross21_x, cross22_x, top, bottom)

                    # refine by
                    if dense_judge(trapezoid):
                        x1, y1, x2, y2 = list_opr.adaptation_value(degree_line, j)
                        dense_line.append((x1,y1,x2,y2,j))
                        dense_label[j] = 1

            #img = list_opr.draw_line_array(img, dense_line, (0,0,255))

            # line of interest is dense parts
            if len(dense_line) != 0:
                dense_label[i] = 1
                x1, y1, x2, y2 = list_opr.adaptation_value(degree_line, i)
                a, b = linear.get_ab(x1, y1, x2, y2)
                if a != 0:
                    ox1, ox2 = linear.slice_two_y(a, b, 0, height)
                else:
                    ox1 = ox2 = x1
                count = 1
                append_line = dense_line
                # search dense area
                while(1):
                    for j in range(0,len(dense_line)):
                        x1, y1, x2, y2 = list_opr.adaptation_value(dense_line, j)
                        a, b = linear.get_ab(x1, y1, x2, y2)
                        if a != 0:
                            cx1, cx2 = linear.slice_two_y(a, b, 0, height)
                        else:
                            cx1 = cx2 = x1
                        ox1 += cx1
                        ox2 += cx2
                        count += 1
                    append_line, dense_label, dense_count = search_dense_area(append_line, degree_line, dense_label, top, bottom)

                    dense_line = append_line

                    #img = list_opr.draw_line_array(img, append_line, (255,0,0))

                    if dense_count == 0:
                        break

                ox1 = int(ox1 / count)
                oy1 = 0
                ox2 = int(ox2 / count)
                oy2 = height
                trapezoid_line.append((ox1,oy1,ox2,oy2))

                #img = list_opr.draw_one_line(img, trapezoid_line, len(trapezoid_line)-1, (0,255,0))
            # line of interest is not dense line
            else:
                x1, y1, x2, y2 = list_opr.adaptation_value(degree_line, i)
                trapezoid_line.append((x1,y1,x2,y2))

    return trapezoid_line
