# import library
import cv2
import math
import numpy as np

#import files
import list_operation as list_opr
import hough_conversion as hough
import trapezoidal_comparison as trapezoidal
import function_approximation as f_approximation

# main
if __name__ == "__main__":
    img = cv2.imread('../image/theta04_cor.jpg')
    height = img.shape[0]
    width = img.shape[1]

    # ハフ変換、角度の絞り込み
    degree_line = hough.hough_lines(img, width, 100, 10)

    '''
    for i in range(0,len(degree_line)):
        x1, y1, x2, y2 = list_opr.value_take_out(degree_line, i);

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    while(1):
        img = cv2.resize(img, (int(width/4), int(height/4)))
        cv2.imshow("sphere_rotate", img)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            cv2.imwrite("degree.jpg", img)
            img = cv2.imread('../image/theta04_cor.jpg')
            break
    '''

    # 台形の面積比較による絞り込み
    trapezoid_line = trapezoidal.trapezoidal_comparison(degree_line, 100, 1700, 40000, 2)

    '''
    for i in range(0,len(trapezoid_line)):
        x1, y1, x2, y2 = list_opr.value_take_out(trapezoid_line, i);

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    while(1):
        img = cv2.resize(img, (int(width/4), int(height/4)))
        cv2.imshow("sphere_rotate", img)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            cv2.imwrite("trapezoid.jpg", img)
            img = cv2.imread('../image/theta04_cor.jpg')
            break
    '''
    
    draw_line = f_approximation.approximation_draw(trapezoid_line, width, height, 1000, 0.00001, 3)


    for i in range(0,len(draw_line)):
        x1, y1, x2, y2 = list_opr.value_take_out(draw_line, i)

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    while(1):
        img = cv2.resize(img, (int(width/4), int(height/4)))
        cv2.imshow("sphere_rotate", img)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            cv2.imwrite("draw.jpg", img)
            img = cv2.imread('../image/theta04_cor.jpg')
            break
