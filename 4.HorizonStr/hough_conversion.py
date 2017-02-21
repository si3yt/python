# import library
import cv2
import math
import numpy as np

# import files
import constant as const
import conversion as conv

# hough transform and degree
def hough_lines(img):
    # grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # edge extraction
    edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
    # hough transform
    # first  argument：image
    # second argument：rho accuracy
    # third  argument：theta accuracy
    # fourth argument：minimum straight line length
    line_len = const.get_hough_line_len()
    lines = cv2.HoughLines(edges, 1, math.pi/360, line_len)

    print ("houghline:" + str(len(lines)))

    # output array
    degree_line = []

    line_extend = width = img.shape[1]
    # end points of straight line
    for i in range(0,len(lines)):
        # rho  ：distandce to line
        # theta：angle of line
        for rho,theta in lines[i]:
            # get end points
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + line_extend*(-b))
            y1 = int(y0 + line_extend*(a))
            x2 = int(x0 - line_extend*(-b))
            y2 = int(y0 - line_extend*(a))

            if angle_refine(theta):
                degree_line.append((x1,y1,x2,y2))

    return len(lines), degree_line

# angle narrowing down
def angle_refine(degree):
    degree = conv.get_degree(degree)

    threshold = const.get_degree_threshold()
    if degree < threshold or degree > 180 - threshold:
        return True
    else:
        return False
