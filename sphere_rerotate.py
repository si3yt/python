# import
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# 画像の読み込み
img    = cv2.imread("image/sample00.jpg", 1)
height = img.shape[0]
width  = img.shape[1]
# 結果画像配列作成
result = np.zeros((height, width, 3), np.uint8)

def sinc_h(t): #sinc関数
    t = math.fabs(t)
    if t <= 1:
        return t**3 - 2 * t**2 + 1
    elif 1 < t <= 2:
        return -t**3 + 5 * t**2 - 8 * t + 4
    elif 2 < t: #else
        return 0

def byCubec(x, y):
    if x < 0 or x >= width-1 or y < 0 or y >= height-1: #参照先が画像内でない
        return [ 0, 0, 0 ]
    x1 = 1 + x - int(x)
    x2 = x - int(x)
    x3 = 1 - x + int(x)
    x4 = 2 - x + int(x)
    y1 = 1 + y - int(y)
    y2 = y - int(y)
    y3 = 1 - y + int(y)
    y4 = 2 - y + int(y)

    black = [0, 0, 0]
    f_flag = [False]*4

    if x-x1 < 0:
        f11 = f12 = f13 = f14 = black
        f_flag[0] = True
    if x+x4 >= width:
        f41 = f42 = f43 = f44 = black
        f_flag[1] = True
    if y+y1 >= height:
        f11 = f21 = f31 = f41 = black
        f_flag[2] = True
    if y-y4 < 0:
        f14 = f24 = f34 = f44 = black
        f_flag[3] = True

    if f_flag[0] == False:
        if f_flag[2] == False:
            f11 = img[y+y1][x-x1]
        if f_flag[3] == False:
            f14 = img[y-y4][x-x1]
        f12 = img[y+y2][x-x1]
        f13 = img[y-y3][x-x1]
    if f_flag[1] == False:
        if f_flag[2] == False:
            f41 = img[y+y1][x+x4]
        if f_flag[3] == False:
            f44 = img[y-y4][x+x4]
        f42 = img[y+y2][x+x4]
        f43 = img[y-y3][x+x4]
    if f_flag[2] == False:
        f21 = img[y+y1][x-x2]
        f31 = img[y+y1][x+x3]
    if f_flag[3] == False:
        f34 = img[y-y4][x+x3]
        f24 = img[y-y4][x-x2]
    f22 = img[y+y2][x-x2]
    f23 = img[y-y3][x-x2]
    f32 = img[y+y2][x+x3]
    f33 = img[y-y3][x+x3]


    result_rgb = np.array([0,0,0])

    for i in range(3):
        matrix_hx = np.array([ sinc_h(x1), sinc_h(x2), sinc_h(x3), sinc_h(x4) ])
        matrix_f  = np.array([ [f11[i], f12[i], f13[i], f14[i]], \
                      [f21[i], f22[i], f23[i], f24[i]], \
                      [f31[i], f32[i], f33[i], f34[i]], \
                      [f41[i], f42[i], f43[i], f44[i]] ])
        matrix_hy = np.array([ [sinc_h(y1)], \
                      [sinc_h(y2)], \
                      [sinc_h(y3)], \
                      [sinc_h(y4)] ])

        matrix_cube = matrix_hx.dot(matrix_f)
        matrix_cube = matrix_cube.dot(matrix_hy)
        if matrix_cube > 255:
            matrix_cube = 255
        elif matrix_cube < 0:
            matrix_cube = 0
        result_rgb[i] = matrix_cube

    return result_rgb


### main
if __name__ == "__main__":
    # get current positions of four trackbars
    latitude  = -40
    longitude = 0
    angle     = 0

    latitude_rad  = -latitude  * math.pi / 180   # y軸周り
    longitude_rad = -longitude * math.pi / 180   # z軸周り
    angle_rad     = -angle     * math.pi / 180   # z軸周り

    r = height / math.pi

    for h in range(height):
        for w in range(width):
            # 円筒平面 → 球(極座標)
            sphere_lat_rad = h / r
            sphere_lon_rad = w / r

            x = r * math.sin(sphere_lat_rad) * math.cos(sphere_lon_rad)
            y = r * math.sin(sphere_lat_rad) * math.sin(sphere_lon_rad)
            z = r * math.cos(sphere_lat_rad)

            # z軸周り
            z_rotate = np.matrix( [[math.cos(longitude_rad)  , math.sin(longitude_rad), 0], \
                                   [- math.sin(longitude_rad), math.cos(longitude_rad), 0], \
                                   [0                        , 0                      , 1]] )
            # y軸周り
            y_rotate = np.matrix( [[math.cos(latitude_rad), 0, -math.sin(latitude_rad)], \
                                   [0                     , 1, 0                      ], \
                                   [math.sin(latitude_rad), 0, math.cos(latitude_rad) ]] )
            # x軸周り
            x_rotate = np.matrix( [[1, 0                   , 0                  ], \
                                   [0, math.cos(angle_rad) , math.sin(angle_rad)], \
                                   [0, -math.sin(angle_rad), math.cos(angle_rad)]] )
            # 行列の積
            matrix = x_rotate.dot(y_rotate) # x軸回転 * y軸回転
            matrix = matrix.dot(z_rotate)   # x軸回転 * y軸回転 * z軸回転

            new_x = x * matrix[0,0] + y * matrix[1,0] + z * matrix[2,0]
            new_y = x * matrix[0,1] + y * matrix[1,1] + z * matrix[2,1]
            new_z = x * matrix[0,2] + y * matrix[1,2] + z * matrix[2,2]

            distance = math.sqrt(new_x**2 + new_y**2 + new_z**2)
            theta    = math.acos(new_z/distance)                 # 値域:0~pi   # 緯度
            phi      = math.atan2(new_y,new_x)                   # 値域:-pi~pi # 経度

            if phi < 0:
                phi = 2 * math.pi + phi

            ## 円筒展開
            cylinder_x = phi   * r # 経度 * 球体半径
            cylinder_y = theta * r # 経度 * 球体半径

            rgb = byCubec(cylinder_x, cylinder_y)

            result[h][w][0] = rgb[0]
            result[h][w][1] = rgb[1]
            result[h][w][2] = rgb[2]

    # ウィンドウの表示形式の設定
     # 第一引数：ウィンドウを識別するための名前
     # 第二引数：ウィンドウの表示形式
      # cv2.WINDOW_AUTOSIZE：デフォルト。ウィンドウ固定表示
      # cv2.WINDOW_NORMAL：ウィンドウのサイズを変更可能にする
    cv2.namedWindow("sphere_rotate")

    while(1):
        cv2.imshow("sphere_rotate", result)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            cv2.imwrite("detected.jpg", result)
            break

    cv2.destroyAllWindows()
