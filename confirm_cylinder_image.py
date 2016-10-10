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
    # image = cv2.imread('./image/sample00.jpg')
    # read image size
    # height = image.shape[0]
    # width = image.shape[1]
    #　one side fish eye radius
    # fish_radius = int(width / 4)

    ## 球と人物点と原点を結んだ直線の交点を求める

    # 球体の方程式
    # x^2 + y^2 + z^2 = r^2
    r = 200 #fish_radius
    # グリッドの奥行き
    depth = -1000
    depth_type = 2 # 1 is y=depth , 2 is x=depth
    # 直線の公式
    # 媒介変数形式 (x,y,z) = (x1,y1,z1) + t(x2-x1,y2-y1,z-z1)
    # 変形 (x-x1)/(x2-x1) = (y-y1)/(y2-y1)=(z-z1)/(z2-z1)
    # 原点を通る3次元直線の公式
    # x/x2 = y/y2 = z/z2

    # 二次方程式の解を求める
    # ax^2 + bx + c
    # t^2(x^2+y^2+z^2) = r^2
    # x = y = z = 2 # x,y,z = 実態の三次元座標
    # grid search xyz配列
    # read image
    image = cv2.imread('./image/grid.jpg')
    height = image.shape[0]
    width = image.shape[1]
    grid_size = height * width # pixel数
    grid = [[0 for i in range(3)] for j in range(grid_size)]
    print ('Play make grid')
    for h in range(height):
        for w in range(width):
            size_i = w + width * h
            if depth_type == 1:
                grid[size_i][0] = width  / 2 - w # x
                grid[size_i][1] = depth          # y
                grid[size_i][2] = height / 2 - h # z
            else:
                grid[size_i][0] = depth          # x
                grid[size_i][1] = width  / 2 - w # y
                grid[size_i][2] = height / 2 - h # z
    #xy軸に対して垂直に立っている人
    #grid = [[200,200,250],[200,250,200],[200,210,150],[200,250,-200],[200,150,-200],[200,190,150],[200,150,200],[200,200,250]] # →xyz ↓index
    #カメラ(球体)に対して垂直に立っている人
    #grid = [[200,200,250],[200-25*math.sqrt(2),200+25*math.sqrt(2),200],[200-5*math.sqrt(2),200+5*math.sqrt(2),150],[200-25*math.sqrt(2),200+25*math.sqrt(2),-200],[200+25*math.sqrt(2),200-25*math.sqrt(2),-200],[200+5*math.sqrt(2),200-5*math.sqrt(2),150],[200+25*math.sqrt(2),200-25*math.sqrt(2),200],[200,200,250]] # →xyz ↓index
    #xy軸に対して垂直に立っている人の顔が前のめりになっている
    #grid = [[150,200,250],[150,250,200],[200,210,150],[200,250,-200],[200,150,-200],[200,190,150],[150,150,200],[150,200,250]] # →xyz ↓index
    #カメラ(球体)に対して垂直に立っている人の顔が前のめりになっている
    #grid = [[150,150,250],[150-25*math.sqrt(2),150+25*math.sqrt(2),200],[200-5*math.sqrt(2),200+5*math.sqrt(2),150],[200-25*math.sqrt(2),200+25*math.sqrt(2),-200],[200+25*math.sqrt(2),200-25*math.sqrt(2),-200],[200+5*math.sqrt(2),200-5*math.sqrt(2),150],[150+25*math.sqrt(2),150-25*math.sqrt(2),200],[150,150,250]] # →xyz ↓index
    #xy軸に対して垂直に立っている人の顔が後ろのめりになっている
    #grid = [[250,200,250],[250,250,200],[200,210,150],[200,250,-200],[200,150,-200],[200,190,150],[250,150,200],[250,200,250]] # →xyz ↓index
    #カメラ(球体)に対して垂直に立っている人の顔が後ろのめりになっている
    #grid = [[250,250,250],[250-25*math.sqrt(2),250+25*math.sqrt(2),200],[200-5*math.sqrt(2),200+5*math.sqrt(2),150],[200-25*math.sqrt(2),200+25*math.sqrt(2),-200],[200+25*math.sqrt(2),200-25*math.sqrt(2),-200],[200+5*math.sqrt(2),200-5*math.sqrt(2),150],[250+25*math.sqrt(2),250-25*math.sqrt(2),200],[250,250,250]] # →xyz ↓index

    cylinder = [[0 for i in range(2)] for j in range(len(grid))] # →xy ↓index

    print ('Now play for grid')
    # grid search for
    for grid_i in range(len(grid)): # grid配列に入れられた要素をすべて検証
        #print ('Now play is for grid NO.' + str(grid_i))
        h = int(grid_i / width)
        w = int(grid_i % width)
        if image[h][w][0] < 50:
            # 検索対象座標
            x = grid[grid_i][0]
            y = grid[grid_i][1]
            z = grid[grid_i][2]

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
            cross_x = [0]*2
            cross_y = [0]*2
            cross_z = [0]*2
            for i in range(len(t)):
                cross_x[i] = x * t[i]
                cross_y[i] = y * t[i]
                cross_z[i] = z * t[i]

            # 注目点に近い点を採用する
            # x,y,zのどれかが近い(差が少ない)場合、他の二つも近いと言える
            cross_index = 0
            if math.fabs(x - cross_x[0]) > math.fabs(x - cross_x[1]):
                cross_index = 1

            x = cross_x[cross_index]
            y = cross_y[cross_index]
            z = cross_z[cross_index]

            ## xyz座標から緯度経度を求める
            # xyz座標　→ 極座標　変換
            # 原点からの距離 r(distance) = sqrt(x^2+y^2+z^2)
            # z軸からの変換 θ = acos(z/sqrt(x^2+y^2+z^2))
            # x軸からの変換 φ = atan(y/x)
            distance = math.sqrt(x**2 + y**2 + z**2)
            theta = math.acos(z/distance) # 値域:0~pi # 緯度
            phi = math.atan2(y,x) # 値域:-pi~pi # 経度

            if phi < 0:
                phi = 2 * math.pi + phi
            ## 円筒展開
            cylinder_x = phi * r # 経度 * 球体半径
            cylinder_y = theta * r # 経度 * 球体半径

            cylinder[grid_i][0] = cylinder_x
            cylinder[grid_i][1] = cylinder_y
        else:
            cylinder[grid_i][0] = -1
            cylinder[grid_i][1] = -1

    # branck result image
    cylinder_height = int(math.pi * r)     # 緯度MAX = 180度 = pi
    cylinder_width  = int(math.pi * r * 2) # 経度MAX = 360度 = 2pi
    result = np.zeros((cylinder_height+1, cylinder_width+1, 3), np.uint8)

    print ('Play make result image')
    for i in range(len(cylinder)):
        if cylinder[i][1] > 0:
            result[int(cylinder[i][1])][int(cylinder[i][0])][0] = 255
            result[int(cylinder[i][1])][int(cylinder[i][0])][1] = 255
            result[int(cylinder[i][1])][int(cylinder[i][0])][2] = 255


    print ('Now play show')
    while True:
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        cv2.imshow("detected.jpg", gray)
        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            cv2.imwrite("detected.jpg", gray)
            break
