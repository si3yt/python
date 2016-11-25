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

def dense_judge(trapezoid, trapezoid_threshold, dense_threshold):
    dense_count = 0
    for k in range(0,len(trapezoid)):
        if trapezoid[k] <= trapezoid_threshold:
            dense_count += 1

    if dense_count < dense_threshold:
        return True
    else:
        return False

def trapezoidal_comparison(degree_line, slice_line_top, slice_line_bottom, trapezoid_threshold, dense_threshold):
    # 絞り込み後格納配列
    trapezoid_line = []

    # 注目直線
    for i in range(0,len(degree_line)):
        # 値の取り出し
        x11, y11, x12, y12 = list_opr.value_take_out(degree_line, i)

        # 台形配列の初期化
        trapezoid = []

        # 注目直線 y = ax + b
        a1, b1 = linear.ab(x11, y11, x12, y12)

        # 注目直線と横線との交点
        cross11_x, cross12_x = linear.two_slice(a1, b1, slice_line_top, slice_line_bottom, x11)

        # 比較対象直線
        for j in range(0,len(degree_line)):
            if j != i:
                # 値の取り出し
                x21, y21, x22, y22 = list_opr.value_take_out(degree_line, j)

                # 比較対象直線 y = ax + b
                a2, b2 = linear.ab(x21, y21, x22, y22)

                # 比較直線と横線との交点
                cross21_x, cross22_x = linear.two_slice(a2, b2, slice_line_top, slice_line_bottom, x21)

                # 台形
                trapezoid.append(trapezoid_area(cross11_x, cross12_x, cross21_x, cross22_x, slice_line_top, slice_line_bottom))

        # 台形面積による絞り込み
        if dense_judge(trapezoid, trapezoid_threshold, dense_threshold):
            trapezoid_line.append((x11,y11,x12,y12))

    return trapezoid_line
