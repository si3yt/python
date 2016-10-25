# import
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# create files
import by_cubec as by_cubec
import EXIF_rotate as exif

# 画像の読み込み
img    = cv2.imread("image/sample00.jpg", 1)
height = img.shape[0]
width  = img.shape[1]
# 結果画像配列作成
result = np.zeros((height, width, 3), np.uint8)

latitude  = 40
longitude = 0
angle     = 0

latitude_rad  = -latitude  * math.pi / 180   # y軸周り
longitude_rad = -longitude * math.pi / 180   # z軸周り
angle_rad     = -angle     * math.pi / 180   # z軸周り

def rotate():
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

    return matrix

def theta_rotate():
    zenith_x, zenith_y, compass = exif.get_angles("image/theta04.jpg")

    zenith_x = zenith_x * math.pi / 180   # y軸周り
    zenith_y = zenith_y * math.pi / 180   # z軸周り

    matrix = np.matrix( [[math.cos(zenith_y), -math.sin(zenith_y)*math.cos(zenith_x), -math.sin(zenith_y)*math.sin(zenith_x)], \
                         [math.sin(zenith_y), math.cos(zenith_y)*math.cos(zenith_x), math.cos(zenith_y)*math.sin(zenith_x)], \
                         [0, math.sin(zenith_x), math.cos(zenith_x)]] )

    return matrix

### main
if __name__ == "__main__":

    matrix = theta_rotate()

    r = height / math.pi

    for h in range(height):
        for w in range(width):
            # 円筒平面 → 球(極座標)
            sphere_lat_rad = h / r
            sphere_lon_rad = w / r

            x = r * math.sin(sphere_lat_rad) * math.cos(sphere_lon_rad)
            y = r * math.sin(sphere_lat_rad) * math.sin(sphere_lon_rad)
            z = r * math.cos(sphere_lat_rad)

            new_x = x * matrix[0,0] + y * matrix[0,1] + z * matrix[0,2]
            new_y = x * matrix[1,0] + y * matrix[1,1] + z * matrix[1,2]
            new_z = x * matrix[2,0] + y * matrix[2,1] + z * matrix[2,2]

            distance = math.sqrt(new_x**2 + new_y**2 + new_z**2)
            theta    = math.acos(new_z/distance)                 # 値域:0~pi   # 緯度
            phi      = math.atan2(new_y,new_x)                   # 値域:-pi~pi # 経度

            if phi < 0:
                phi = 2 * math.pi + phi

            ## 円筒展開
            cylinder_x = (phi   * r) / width  * (width  - 1) # 経度 * 球体半径
            cylinder_y = (theta * r) / height * (height - 1) # 経度 * 球体半径

            rgb = by_cubec.byCubec(cylinder_x, cylinder_y, img, height, width)

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
