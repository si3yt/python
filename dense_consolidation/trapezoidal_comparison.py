# import library
import cv2
import math
import numpy as np

# import files
import list_operation as list_opr
import linear_function as linear

def trapezoid_area(c11, c12, c21, c22, top, bottom):
    # 台形上辺長さ
    t_top = abs(c11 - c21)
    # 台形下辺長さ
    t_bottom = abs(c12 - c22)
    # 台形高さ
    t_height = bottom - top
    # 台形面積
    return (t_top + t_bottom) * t_height / 2

def dense_judge(trapezoid, trapezoid_threshold):
    if trapezoid <= trapezoid_threshold:
        return True
    else:
        return False

def cross_make(line, i, top, bottom):
    # 値の取り出し
    x1, y1, x2, y2 = list_opr.value_take_out(line, i)

    # 注目直線 y = ax + b
    a, b = linear.ab(x1, y1, x2, y2)

    # 注目直線と横線との交点
    cross1_x, cross2_x = linear.two_slice(a, b, top, bottom, x1)

    return cross1_x, cross2_x

def trapezoidal_make(dense, line1, line2, label, top, bottom, t_threshold):
    # 注目直線
    for i in range(0,len(line1)):
        if label[i] == 0:
            # 注目直線と横線との交点
            cross11_x, cross12_x = cross_make(line1, i, top, bottom)

            # 比較対象直線
            for j in range(0,len(line2)):
                if j != i and label[j] == 0:
                    # 比較直線と横線との交点
                    cross21_x, cross22_x = cross_make(line2, j, top, bottom)

                    # 台形面積
                    trapezoid = (trapezoid_area(cross11_x, cross12_x, cross21_x, cross22_x, top, bottom))

                    # 台形面積による絞り込み
                    if dense_judge(trapezoid, t_threshold):
                        # 値の取り出し
                        x21, y21, x22, y22 = list_opr.value_take_out(line2, j)
                        dense_line.append((x11,y11,x12,y12,j))


def trapezoidal_comparison(degree_line, slice_line_top, slice_line_bottom, trapezoid_threshold, dense_threshold):
    # 絞り込み後格納配列
    trapezoid_line = []
    # 密集判定ラベル
    dense_label = np.zeros(len(degree_line))
    # 密集配列
    dense_line = []

    for i in range(0,len(degree_line)):
        if dense_label[i] == 0:
            # 注目直線と横線との交点
            cross11_x, cross12_x = cross_make(degree_line, i, slice_line_top, slice_line_bottom)

            # 比較対象直線
            for j in range(0,len(degree_line)):
                if j != i and dense_label[j] == 0:
                    # 比較直線と横線との交点
                    cross21_x, cross22_x = cross_make(degree_line, j, slice_line_top, slice_line_bottom)

                    # 台形面積
                    trapezoid = (trapezoid_area(cross11_x, cross12_x, cross21_x, cross22_x, slice_line_top, slice_line_bottom))

                    # 台形面積による絞り込み
                    if dense_judge(trapezoid, trapezoid_threshold):
                        # 値の取り出し
                        x21, y21, x22, y22 = list_opr.value_take_out(degree_line, j)
                        dense_line.append((x11,y11,x12,y12,j))

            if len(dense_line) != 0:
                while(1):




        if len(dense_line) != 0:
            dense_label[i] = 1
            for k in range(0,len(dense_line)):
                for l in range(0,len(degree_line)):
                    if k != l and dense_label[l] == 0:




    return trapezoid_line
