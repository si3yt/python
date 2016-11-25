# import library
import cv2
import math
import numpy as np

def value_take_out(list_object, i):
    x1 = list_object[i][0]
    y1 = list_object[i][1]
    x2 = list_object[i][2]
    y2 = list_object[i][3]

    return x1, y1, x2, y2
