# import library
import cv2
import math
import numpy as np

# create files
import bicubic as bicubic
import conversion as conv
import constant as const


def adaptation_value(result, rgb, h, w):
    result[h][w][0] = rgb[0]
    result[h][w][1] = rgb[1]
    result[h][w][2] = rgb[2]

    return result

def adaptation_pixel(matrix):
    # result image array
    filename = const.get_filename()
    img    = cv2.imread(filename, 1)
    height = const.get_img_height()
    width  = const.get_img_width()
    result = np.zeros((height, width, 3), np.uint8)

    r = height / math.pi

    for h in range(height):
        for w in range(width):
            # cylinder → polar
            sphere_lat_rad = h / r
            sphere_lon_rad = w / r
            # polar → xyz
            x, y, z = conv.get_xyz(r, sphere_lat_rad, sphere_lon_rad)
            # xyz → rotated xyz
            new_x, new_y, new_z = conv.get_after_xyz(x, y, z, matrix)
            # rotated xyz → polar
            distance, theta, phi = conv.get_polar(new_x, new_y, new_z)
            if phi < 0:
                phi = 2 * math.pi + phi #range:0~2pi

            # cylinder expansion
            cylinder_x, cylinder_y = conv.cylinder_expansion(phi, theta, r, width, height)

            # bicubic interpolation
            rgb = bicubic.bicubic(cylinder_x, cylinder_y, img, height, width)
            # adaptation value of rgb
            adaptation_value(result, rgb, h, w)

        print ('|>  Now image height : %4d / %d' % (h ,height))

    return result
