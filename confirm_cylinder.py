# import
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

### main
if __name__ == "__main__":

    # read image file
    image = cv2.imread('./image/sample00.jpg')
    # read image size
    height = image.shape[0]
    width = image.shape[1]
    #　one side fish eye radius
    fish_radius = int(width / 4)

    ## 球と人物点と原点を結んだ直線の交点を求める

    # 球体の方程式
    # x^2 + y^2 + z^2 = r^2
    r = 1#fish_radius

    # 直線の公式
    # 媒介変数形式 (x,y,z) = (x1,y1,z1) + t(x2-x1,y2-y1,z-z1)
    # 変形 (x-x1)/(x2-x1) = (y-y1)/(y2-y1)=(z-z1)/(z2-z1)
    # 原点を通る3次元直線の公式
    # x/x2 = y/y2 = z/z2

    # 二次方程式の解を求める
    # ax^2 + bx + c
    # t^2(x^2+y^2+z^2) = r^2
    x = y = z = 2 # x,y,z = 実態の三次元座標
    a = (x**2 + y**2 + z**2)
    b = 0
    c = -(r**2)
    t = [0]*2
    real = imag = 0 # 虚部と実部の変数

    # 判別式 D
    d = b * b - 4 * a * c

    # 判別式による条件分岐
    if d > 0: # 球と直線(原点)の交点はこの計算のみが使われる
        t[0] = (-b + math.sqrt(d)) / (2*a)
        t[1] = (-b - math.sqrt(d)) / (2*a)
    ## 以下は二次方程式用の式
    elif d == 0:
        t[0] = t[1] = -b / (2*a)
    else: # bが0,cがマイナスの値をとるため入ることはない
        real = -b / (2*a)
        imag - math.sqrt(-d) / (2*a)
        t[0].real = real
        t[0].imag = imag
        t[1].real = real
        t[0].imag = -imag

    # x,y,zを求める
    cross_x = cross_y = cross_z = [0]*2
    for i in range(0,len(t)):
        cross_x[i] = x * t[i]
        cross_y[i] = y * t[i]
        cross_z[i] = z * t[i]

    # 注目点に近い点を採用する
    # x,y,zのどれかが近い(差が少ない)場合、他の二つも近いと言える
    cross_index = 0
    if x - cross_x[0] > x - cross_x[1]:
        cross_index = 1

    print ("x = " + str(cross_x[cross_index]) + ", y = " + str(cross_y[cross_index]) + ", z = " + str(cross_z[cross_index]))

    ## xyz座標から緯度経度を求める
