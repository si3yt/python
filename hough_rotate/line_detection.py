# import library
import cv2
import math
import numpy as np

#import files
import list_operation as list_opr
import hough_conversion as hough
import trapezoidal_comparison as trapezoidal
import function_approximation as f_approximation

def line_detection(img, orthogonal_threshold):
    height = img.shape[0]
    width = img.shape[1]

    # ハフ変換、角度の絞り込み
    degree_line = hough.hough_lines(img, width, 100, 10)

    # 台形の面積比較による絞り込み
    trapezoid_line = trapezoidal.trapezoidal_comparison(degree_line, 100, 1700, 40000, 2)

    vertex_x, vertex_y = f_approximation.approximation_vertex(trapezoid_line, width, height, 1000, 0.00001, orthogonal_threshold)

    return vertex_x, vertex_y
