# import library
import cv2
import math
import numpy as np

# import files
import constant as const

def adaptation_value(list_object, i):
    x1 = list_object[i][0]
    y1 = list_object[i][1]
    x2 = list_object[i][2]
    y2 = list_object[i][3]

    return x1, y1, x2, y2

def draw_one_line(img, line, i, color):
    height = const.get_img_height()
    width = const.get_img_width()

    x1, y1, x2, y2 = adaptation_value(line, i)
    cv2.line(img,(x1,y1),(x2,y2),color,2)

    img_resize = cv2.resize(img, (int(width/4), int(height/4)))
    while(1):
        cv2.imshow("draw line array", img_resize)
        k = cv2.waitKey(1)
        if k == 27: # ESC key finish while
            break

    return img

def draw_line_array(img, line, color):
    height = const.get_img_height()
    width = const.get_img_width()
    for i in range(0, len(line)):
        x1, y1, x2, y2 = adaptation_value(line, i)
        cv2.line(img,(x1,y1),(x2,y2),color,2)

    img_resize = cv2.resize(img, (int(width/4), int(height/4)))
    while(1):
        cv2.imshow("draw line array", img_resize)
        k = cv2.waitKey(1)
        if k == 27: # ESC key finish while
            break

    return img
