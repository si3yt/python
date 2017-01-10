# import library
import cv2
import math
import numpy as np

#import files
import list_operation as list_opr
import hough_conversion as hough
import trapezoidal_comparison as trapezoidal
import function_approximation as f_approximation

def line_detection(img, amp, filename):
    height = img.shape[0]
    width = img.shape[1]

    # ハフ変換、角度の絞り込み
    degree_line = hough.hough_lines(img, width, 100, 10)

    img_temp = cv2.imread(filename, 1)
    for i in range(0,len(degree_line)):
        x1, y1, x2, y2 = list_opr.value_take_out(degree_line, i)
        cv2.line(img_temp,(x1,y1),(x2,y2),(0,0,255),2)
    cv2.imwrite("degree.jpg", img_temp)

    print ('end degree_line')

    # 台形の面積比較による絞り込み
    trapezoid_line = trapezoidal.trapezoidal_comparison(degree_line, 100, 1700, 40000, 2)
    img_temp = cv2.imread(filename, 1)
    for i in range(0,len(trapezoid_line)):
        x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i)
        cv2.line(img_temp,(x1,y1),(x2,y2),(0,0,255),2)
    cv2.imwrite("trapezoid.jpg", img_temp)

    print ('end trapezoid_line')

    draw_line, vertex_x, vertex_y = f_approximation.approximation_dv(trapezoid_line, width, height, 1000, 0.00001, 3, amp)

    img_temp = cv2.imread(filename, 1)
    for i in range(0,len(draw_line)):
        x1, y1, x2, y2 = list_opr.value_take_out(draw_line, i)
        cv2.line(img_temp,(x1,y1),(x2,y2),(0,0,255),2)
    cv2.imwrite("draw.jpg", img_temp)

    print ('end draw_line')

    return vertex_x, vertex_y
