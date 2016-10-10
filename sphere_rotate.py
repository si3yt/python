# import
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# 画像の読み込み
img = cv2.imread("image/sample.jpg", 1)
height = img.shape[0]
width = img.shape[1]
# 結果画像配列作成
result = np.zeros((height, width, 3), np.uint8)

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


    while(1):
        cv2.imshow("sphere_rotate", result)
        k = cv2.waitKey(1)
        if k == 27: # ESCキーで終了
            break
        # get current positions of four trackbars
        latitude = cv2.getTrackbarPos('latitude','sphere_rotate')
        longitude = cv2.getTrackbarPos('longitude','sphere_rotate')

        latitude_rad = (latitude - 90) * math.pi / 180
        longitude_rad = (longitude - 180) * math.pi / 180

        r = height / math.pi

        for h in range(height):
            for w in range(width):
                # 円筒平面 → 球
                #sphere_lat_rad = h / r
                #sphere_lon_rad = w / r
                # トラックバー分足す
                #sphere_lat_rad = sphere_lat_rad + latitude_rad
                #sphere_lon_rad = sphere_lon_rad + longitude_rad

                cylinder_x = int(w + (longitude_rad * r))
                cylinder_y = int(h + (latitude_rad * r))
                result[cylinder_y][cylinder_x][0] = img[h][w][0]
                result[cylinder_y][cylinder_x][1] = img[h][w][1]
                result[cylinder_y][cylinder_x][2] = img[h][w][2]

    cv2.destroyAllWindows()
