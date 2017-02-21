# import
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# create files
import constant as const
import conversion as conv
import bicubic as bicubic
import exif as exif
import rotate as rotate
import exif_rotate as exif_rotate
import line_detection as line
import rgb_operation as rgb_opr

### main
if __name__ == "__main__":
    # read image
    print ('--- Program start ---')
    filename = './image/R0010211_xmp.jpg'
    img    = cv2.imread(filename, 1)
    height = img.shape[0]
    width  = img.shape[1]

    for angle in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
        angle_rad = conv.get_rad(angle)
        x_matrix, y_matrix, z_matrix = rotate.double_rerotate(0, 0, angle_rad)

        # result image array
        result = rgb_opr.adaptation_pixel(x_matrix, y_matrix, z_matrix, filename)

        cv2.imwrite("detected"+str(angle)+".jpg", result)
