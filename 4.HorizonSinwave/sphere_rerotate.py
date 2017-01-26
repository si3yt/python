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
    filename = const.get_filename()

    print ('Play exif rotate? Y or N')
    input_bool = input('>> ')
    if input_bool == 'Y':
        print ('--- Start exif rotate ---')
        filename = exif_rotate.exif_rotate()
        const.set_filename(filename)
        print ('=== End exif rotate ===')

    img    = cv2.imread(filename, 1)
    height = img.shape[0]
    width  = img.shape[1]

    print ('--- Start line detection ---')
    vertex_x, vertex_y = line.line_detection(img)
    transverse = conv.get_rad(vertex_x)
    longitudinal = conv.get_rad(-vertex_y)
    print ('=== End line detection ===')

    print ('--- Start make rotate matrix ---')
    #matrix = rotate.rotate(transverse, 0, -longitudinal)
    matrix = rotate.rerotate(transverse, longitudinal, 0)
    print ('=== End make rotate matrix ===')

    print ('--- Start matrix rotate image ---')
    # result image array
    result = rgb_opr.adaptation_pixel(matrix)
    print ('=== End matrix rotate image ===')

    print ('|>  Show result image ')
    print ('!- Push esc key for exit')
    result_resize = cv2.resize(result, (int(width/4), int(height/4)))
    while(1):
        cv2.imshow("sphere_rotate", result_resize)
        k = cv2.waitKey(1)
        if k == 27: # ESC key finish while
            cv2.imwrite("detected.jpg", result)
            break

    cv2.destroyAllWindows()

    print ('=== Program end ===')
