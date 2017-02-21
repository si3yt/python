# import
import cv2
import math
import numpy as np

# constant

def get_hough_line_len():
    hough_line_len = 100
    return hough_line_len

def get_degree_threshold():
    degree_threshold = 10
    return degree_threshold

def get_slice_line_top():
    slice_line_top = 100
    return slice_line_top

def get_slice_line_bottom():
    slice_line_bottom = 1700
    return slice_line_bottom

def get_trapezoid_threshold():
    trapezoid_threshold = 50000
    return trapezoid_threshold

def get_dense_threshold():
    dense_threshold = 2
    return dense_threshold

def get_newton_count():
    newton_count = 1000
    return newton_count

def get_newton_threshold():
    newton_threshold = 0.00001
    return newton_threshold

def get_orthogonal_threshold():
    orthogonal_threshold = 3
    return orthogonal_threshold
