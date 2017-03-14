# import
import cv2
import math
import numpy as np

# create files
import bicubic as bicubic
import exif as exif
import rotate as rotate
import conversion as conv
import constant as const
import rgb_operation as rgb_opr

# exif zenith rotate
def exif_rotate(filename):
    # read image
    img    = cv2.imread(filename, 1)
    height = img.shape[0]
    width  = img.shape[1]

    zenith_x, zenith_y, compass = exif.get_angles(filename)
    zenith_x_rad = conv.get_rad(zenith_x)
    zenith_y_rad = conv.get_rad(zenith_y)
    compass_rad  = conv.get_rad(compass)
    matrix = rotate.rerotate(0, -zenith_y_rad, -zenith_x_rad)

    # result image array
    result = adaptation_pixel(matrix, filename)

    # save result image
    result_filename = "exif_correction.jpg"
    cv2.imwrite(result_filename, result)

    return result_filename

def adaptation_pixel(matrix, filename):
    # result image array
    img    = cv2.imread(filename, 1)
    height = img.shape[0]
    width  = img.shape[1]
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
            rresult = rgb_opr.adaptation_value(result, rgb, h, w)

        print ('|>  Now image height : %4d / %d' % (h ,height))

    return result
