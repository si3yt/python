# import library
import cv2
import math
import numpy as np

#import files
import list_operation as list_opr
import hough_conversion as hough
import trapezoid as trapezoidal#al_comparison as trapezoidal
import function_approximation as f_approximation

# make output image
def output_img(line, filename):
    img_temp = cv2.imread(filename, 1)
    for i in range(0,len(line)):
        x1, y1, x2, y2 = list_opr.adaptation_value(line, i)
        cv2.line(img_temp,(x1,y1),(x2,y2),(0,0,255),10)
    return img_temp

# line function
def line_detection(img, filename, txt):
    height = img.shape[0]
    width = img.shape[1]

    print ('-- Start hough conversion --')
    # hough conversion
    # angle narrowing down
    lines, degree_line = hough.hough_lines(img)
    print ("degreeline:" + str(len(degree_line)))
    txt.write("hough line: " + str(lines) + '\n')
    txt.write("degree line: " + str(len(degree_line)) + '\n')
    # output degree line
    #img_temp = output_img(degree_line, filename)
    #cv2.imwrite("degree.jpg", img_temp)
    print ('== End hough conversion ==')

    print ('-- Start trapezoid area comparison --')
    # trapezoid area comparison
    trapezoid_line = trapezoidal.trapezoidal_comparison(degree_line, height, width)
    print ("trapezoidline:" + str(len(trapezoid_line)))
    txt.write("trapezoid line: " + str(len(trapezoid_line)) + '\n')
    # output trapezoid line
    img_temp = output_img(trapezoid_line, filename)
    cv2.imwrite("trapezoid.jpg", img_temp)
    print ('== End trapezoid area comparison ==')

    print ('-- Start approximation function --')
    # approximation function
    vertex_x, vertex_y = f_approximation.approximation_func(trapezoid_line, height, width, filename)
    print ("方位角:" + str(vertex_x) + "、仰角:" + str(vertex_y))
    txt.write("orientation angle: " + str(vertex_x) + '\n')
    txt.write("elevation angle: " + str(vertex_y) + '\n')
    print ('== End approximation function ==')

    return vertex_x, vertex_y
