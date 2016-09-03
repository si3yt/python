# import
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from sklearn import svm
from skimage import data, color, exposure
from sklearn.externals import joblib
from sklearn import cross_validation
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from skimage.transform import resize

### HOG表示処理(HOG処理の関数)
def printHOG(image):

    # property
    CELL_SIZE = 5
    BLOCK_SIZE = 3

    # read image size
    HEIGHT = image.shape[0]
    WIDTH = image.shape[1]

    # branck result image
    result = np.zeros((HEIGHT, WIDTH, 3), np.uint8)

    ## 画像のグレースケール化(色バリエーションの最小化)
    GRAY = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ## 各画素のエッジ情報の算出(輝度から勾配強度と勾配方向を求める)
    # 輝度値の取得
    # 勾配強度配列
    magnitude = [[0 for i in range(HEIGHT)] for j in range(WIDTH)]
    # 勾配方向配列
    gradient = [[0 for i in range(HEIGHT)] for j in range(WIDTH)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # brightness = 輝度
            brightness = GRAY[y,x]
            mx = px = my = py = 1
            if x == 0:
                mx = 0
            elif x == WIDTH-1:
                px = 0
            if y == 0:
                my = 0
            elif y == HEIGHT-1:
                py = 0
            grad_x = int(GRAY[y,x+px]) - int(GRAY[y,x-mx])
            grad_y = int(GRAY[y+py,x]) - int(GRAY[y-my,x])
            # 勾配強度計算式
            magnitude[x][y] = math.sqrt(grad_x**2 + grad_y**2)
            # 勾配方向計算式(ラジアン)
            gradient[x][y] = math.atan2(grad_y,grad_x)
            # ラジアン → 角度 変換
            gradient[x][y] = (gradient[x][y]*180.0)/math.pi
            # 負符号の反転
            if gradient[x][y] < 0.0:
                gradient[x][y] += 360.0
            if gradient[x][y] > 180.0:
                gradient[x][y] -= 180.0
            if gradient[x][y] == 180.0:
                gradient[x][y] = 179

    ## セル領域分割 (5 x 5)
    ## ヒストグラム構築(方向20度毎の9次元ベクトル)
    # ヒストグラム配列
    BINS = 9
    CELL_NAMBER_Y= int(HEIGHT/CELL_SIZE)
    CELL_NAMBER_X= int(WIDTH/CELL_SIZE)
    hist = [[[0 for i in range(BINS)] for j in range(CELL_NAMBER_X)] for k in range(CELL_NAMBER_Y)]
    for cell_y in range(CELL_NAMBER_Y):
        for cell_x in range(CELL_NAMBER_X):
            pixel_x = cell_x * CELL_SIZE
            pixel_y = cell_y * CELL_SIZE
            # セル内ヒストグラムの作成
            for y in range(CELL_SIZE):
                for x in range(CELL_SIZE):
                    angle = int(gradient[pixel_x+x][pixel_y+y]/20)
                    hist[cell_y][cell_x][angle] += magnitude[pixel_x+x][pixel_y+y]

    # ヒストグラム正規化
    hog = [0]*(int((CELL_NAMBER_X-BLOCK_SIZE+1)*(CELL_NAMBER_Y-BLOCK_SIZE+1)*BLOCK_SIZE*BLOCK_SIZE*BINS))
    count = 0;
    hist_sum = 0
    COLOR_STRENGTH = 10
    for block_y in range(CELL_NAMBER_Y-BLOCK_SIZE+1):
        for block_x in range(CELL_NAMBER_X-BLOCK_SIZE+1):
            # ブロック内総和
            hist_sum = 0
            for y in range(BLOCK_SIZE):
                for x in range(BLOCK_SIZE):
                    for bins in range(BINS):
                        hist_sum += hist[block_y+y][block_x+x][bins]
            # 正規化
            for y in range(BLOCK_SIZE):
                for x in range(BLOCK_SIZE):
                    for bins in range(BINS):
                        if hist_sum == 0:
                            hog[count] = 0
                        else:
                            hog[count] = float(hist[block_y+y][block_x+x][bins]/hist_sum)
                            ## 表示処理
                            center_x = (block_x*CELL_SIZE)+CELL_SIZE+(int(CELL_SIZE/2)+1)
                            center_y = (block_y*CELL_SIZE)+CELL_SIZE+(int(CELL_SIZE/2)+1)
                            theta = (bins * 20 + 90) * math.pi / 180
                            rd_x = CELL_SIZE*0.5*math.cos(theta)
                            rd_y = CELL_SIZE*0.5*math.sin(theta)
                            rp = (int(center_x - rd_x), int(center_y - rd_y))
                            lp = (int(center_x + rd_x), int(center_y + rd_y))
                            cv2.line(result, rp,lp,(hog[count]*COLOR_STRENGTH*255,hog[count]*COLOR_STRENGTH*255,hog[count]*COLOR_STRENGTH*255), 1)
                        #print (hog[count])
                        count += 1

    while True:
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        cv2.imshow("detectedNormal.jpg", gray)
    	#out.write(img_test)#動画
        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            cv2.imwrite("detectedNormal.jpg", gray)
            break
    return hog
