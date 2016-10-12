# import
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# 画像の読み込み
img = cv2.imread("image/sample00.jpg", 1)
height = img.shape[0]
width = img.shape[1]
# 結果画像配列作成
result = np.zeros((height * 2, width * 2, 3), np.uint8)

def onTrackbarChanged(x):
    pass


### main
if __name__ == "__main__":
    # ウィンドウの表示形式の設定
     # 第一引数：ウィンドウを識別するための名前
     # 第二引数：ウィンドウの表示形式
      # cv2.WINDOW_AUTOSIZE：デフォルト。ウィンドウ固定表示
      # cv2.WINDOW_NORMAL：ウィンドウのサイズを変更可能にする
    cv2.namedWindow("sphere_rotate")

    # トラックバーの作成
     # latiude = 緯度
     # longitude = 経度
      # マイナスの値が使えないため初期値を中間とする
    cv2.createTrackbar('latitude','sphere_rotate',90,180,onTrackbarChanged)
    cv2.createTrackbar('longitude','sphere_rotate',180,360,onTrackbarChanged)
    cv2.createTrackbar('angle','sphere_rotate',180,360,onTrackbarChanged)

    # get current positions of four trackbars
    latitude = 90#cv2.getTrackbarPos('latitude','sphere_rotate')
    longitude = 180#cv2.getTrackbarPos('longitde','sphere_rotate')
    angle = 180#cv2.getTrackbarPos('angle','sphere_rotate')

    latitude_rad = (latitude - 90) * math.pi / 180      # y軸周り
    longitude_rad = (longitude - 180) * math.pi / 180   # z軸周り
    angle_rad = (angle - 180) * math.pi / 180           # z軸周り

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
            z_rotate = np.matrix([[math.cos(longitude_rad),math.sin(longitude_rad),0],[- math.sin(longitude_rad), math.cos(longitude_rad),0],[0,0,1]])
            # y軸周り
            y_rotate = np.matrix([[math.cos(latitude_rad),0,- math.sin(latitude_rad)],[0,1,0],[math.sin(latitude_rad),0,math.cos(latitude_rad)]])
            # x軸周り
            x_rotate = np.matrix([[1,0,0],[0,math.cos(angle_rad),math.sin(angle_rad)],[0,- math.sin(angle_rad),math.cos(angle_rad)]])
            # 行列の積
            matrix = z_rotate.dot(y_rotate)
            matrix = matrix.dot(x_rotate)

            new_x = x * matrix[0,0] + y * matrix[1,0] + z * matrix[2,0]
            new_y = x * matrix[0,1] + y * matrix[1,1] + z * matrix[2,1]
            new_z = x * matrix[0,2] + y * matrix[1,2] + z * matrix[2,2]

            distance = math.sqrt(new_x**2 + new_y**2 + new_z**2)
            theta = math.acos(new_z/distance) # 値域:0~pi # 緯度
            phi = math.atan2(new_y,new_x) # 値域:-pi~pi # 経度

            if phi < 0:
                phi = 2 * math.pi + phi

            ## 円筒展開
            cylinder_x = int(phi * r) # 経度 * 球体半径
            cylinder_y = int(theta * r) # 経度 * 球体半径

            result[cylinder_y][cylinder_x][0] = img[h][w][0]
            result[cylinder_y][cylinder_x][1] = img[h][w][1]
            result[cylinder_y][cylinder_x][2] = img[h][w][2]



    while(1):
        cv2.imshow("sphere_rotate", result)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            break

    cv2.destroyAllWindows()
