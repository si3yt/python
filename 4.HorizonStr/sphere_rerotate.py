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

    top_d = "image/"
    directory = ["R212/", "R292/", "R304/"]
    bottom_d = ["5_trans/", "10_trans/", "15_trans/", "20_trans/"]
    filename = ["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100", "110", "120", "130", "140", "150", "160", "170", "180", "-10", "-20", "-30", "-40", "-50", "-60", "-70", "-80", "-90", "-100", "-110", "-120", "-130", "-140", "-150", "-160", "-170"]
    filetype = ".JPG"

    txt = open("output.txt", 'w')

    for d in directory:
        txt.write("--- Image Name: " + d + ' ---\n')
        for bd in bottom_d:
            txt.write("-- Trans Angle: " + bd + ' --\n')
            for fn in filename:
                txt.write("- File Angle: " + fn + ' -\n')
                # read image
                print ('--- Program start ---')
                filename = top_d + d + bd + fn + filetype
                print (filename)

                img    = cv2.imread(filename, 1)
                height = img.shape[0]
                width  = img.shape[1]

                #print ('--- Start line detection ---')
                vertex_x, vertex_y = line.line_detection(img, filename, txt)

    '''
    transverse = conv.get_rad(180 - vertex_x)
    longitudinal = conv.get_rad(vertex_y)
    print ('=== End line detection ===')

    print ('--- Start make rotate matrix ---')
    x_matrix, y_matrix, z_matrix = rotate.double_rerotate(transverse, 0, longitudinal)
    print ('=== End make rotate matrix ===')

    print ('--- Start matrix rotate image ---')
    # result image array
    result = rgb_opr.adaptation_pixel(x_matrix, y_matrix, z_matrix, filename)
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
    '''
    txt.close()

    print ('=== Program end ===')
