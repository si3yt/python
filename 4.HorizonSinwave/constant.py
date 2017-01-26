# import
import cv2
import math
import numpy as np

# constant
filename = '../image/theta04_cor.jpg'
image = cv2.imread(filename, 1)
height = image.shape[0]
width  = image.shape[1]
hough_line_extend = width
hough_line_len = 100
degree_threshold = 10
slice_line_top = 100
slice_line_bottom = 1700
trapezoid_threshold = 100000
dense_threshold = 2
newton_count = 1000
newton_threshold = 0.00001
orthogonal_threshold = 3

def get_filename():
    return filename

def set_filename(name):
    filename = name
    image = cv2.imread(filename, 1)
    height = image.shape[0]
    width  = image.shape[1]

def get_img_height():
    return height

def get_img_width():
    return width

def get_hough_line_extend():
    return hough_line_extend

def get_hough_line_len():
    return hough_line_len

def get_degree_threshold():
    return degree_threshold

def get_slice_line_top():
    return slice_line_top

def get_slice_line_bottom():
    return slice_line_bottom

def get_trapezoid_threshold():
    return trapezoid_threshold

def get_dense_threshold():
    return dense_threshold

def get_newton_count():
    return newton_count

def get_newton_threshold():
    return newton_threshold

def get_orthogonal_threshold():
    return orthogonal_threshold
