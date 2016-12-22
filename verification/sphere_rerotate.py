# import
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# create files
import bicubic as bicubic
import rotate as rotate

# 画像の読み込み
filename = '../image/horizon.png'
img    = cv2.imread(filename, 1)
height = img.shape[0]
width  = img.shape[1]
# 結果画像配列作成
result = np.zeros((height, width, 3), np.uint8)
# 回転角度
latitude  = 50   #緯度
longitude = 50   #経度
angle     = 00   #角度
# 度　→　ラジアン
def rad_conv(a):
    a = a * math.pi / 180
    return a
# 回転角ラジアン
latitude_rad  = rad_conv(-latitude)  # y軸周り
longitude_rad = rad_conv(-longitude) # x軸周り
angle_rad     = rad_conv(-angle)     # z軸周り
### main
def horizon_rotate(rot_angle):

    matrix = rotate.rerotate(0, rot_angle, 0)

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

            rgb = bicubic.bicubic(cylinder_x, cylinder_y, img, height, width)

            result[h][w][0] = rgb[0]
            result[h][w][1] = rgb[1]
            result[h][w][2] = rgb[2]

    return r, result
