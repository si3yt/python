# import
import cv2
import math
import numpy as np

# create files
import bicubic as bicubic
import exif as exif
import rotate as rotate
import conversion as conv
import rgb_operation as rgb_opr
import constant as const

# exif zenith rotate
def exif_rotate():
    # read image
    filename = const.get_filename()
    img    = cv2.imread(filename, 1)
    height = img.shape[0]
    width  = img.shape[1]

    zenith_x, zenith_y, compass = exif.get_angles(filename)
    zenith_x_rad = conv.get_rad(zenith_x)
    zenith_y_rad = conv.get_rad(zenith_y)
    compass_rad  = conv.get_rad(compass)
    matrix = rotate.rerotate(0, zenith_y_rad, zenith_x_rad)

    # result image array
    result = rgb_opr.adaptation_pixel(matrix)
    
    # save result image
    result_filename = "exif_correction.jpg"
    cv2.imwrite(result_filename, result)

    return result_filename
