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

### 改良版HOG
def improvementHOG(image):

    # property
    CELL_SIZE = 5
    BLOCK_SIZE = 3

    # read image size
    HEIGHT = image.shape[0]
    WIDTH = image.shape[1]

    # branck result image
    result = np.zeros((WIDTH, HEIGHT, 3), np.uint8)

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
            #if grad_x == 0:
            #    grad_x = 1
            # 勾配方向の角度をtanで求めて後でセル比率を用いて計算する
            #gradient[x][y] = math.tan((grad_y/grad_x))
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
            # セル内の対応するピクセルを求める
            pixel_x = cell_x * CELL_SIZE
            pixel_y = cell_y * CELL_SIZE
            # セル内ヒストグラムの作成
            # セル拡張のための横幅と縦幅を２次関数に近似して求める
            cell_height = int(math.fabs((2*HEIGHT/WIDTH**2)*(pixel_x-WIDTH/2)**2)/CELL_SIZE/10)
            cell_width = int(math.fabs((2*WIDTH/HEIGHT**2)*(pixel_y-HEIGHT/2)**2)/CELL_SIZE/10)
            # 0の時(頂点付近はセル幅を1にして通常計算を行う)
            if cell_width == 0:
                cell_width = 1
            if cell_height == 0:
                cell_height = 1
            #print (str(pixel_x)+","+str(pixel_y)+",,"+str(cell_width) + "," + str(cell_height))
            new_cell_size_x = 0
            new_cell_size_y = 0
            # 右半分はセルを左に拡張する
            if pixel_x <= WIDTH/2:
                new_cell_size_x = -(CELL_SIZE*cell_width)
            # 左半分はセルを右に拡張する
            else:
                new_cell_size_x = CELL_SIZE*cell_width
            # 上半分はセルを上に拡張する
            if pixel_y <= HEIGHT/2:
                new_cell_size_y = -(CELL_SIZE*cell_height)
            # 下半分はセルを下に拡張する
            else:
                new_cell_size_y = CELL_SIZE*cell_height
            # 拡張したセルが画像のサイズを超えている場合、通常のHOGと同じように計算を行う(とりあえずの処置)
            if pixel_x+new_cell_size_x < 0 or pixel_y+new_cell_size_y < 0 or pixel_x+new_cell_size_x > WIDTH or pixel_y+new_cell_size_y > HEIGHT:
                for y in range(CELL_SIZE):
                    for x in range(CELL_SIZE):
                        for angle in range(9):
                            hist[cell_y][cell_x][angle] += magnitude[pixel_x+x][pixel_y+y]
            # 拡張したセルが画像のサイズ内に収まる場合、拡張を行って計算を行う
            else:
                #print (str(pixel_x)+","+str(pixel_y)+",,"+str(new_cell_size_x) + "," + str(new_cell_size_y))
                #if pixel_y < pixel_y+new_cell_size_y:
                #    if pixel_x < pixel_x+new_cell_size_x:
                #        window = image[pixel_y:pixel_y+new_cell_size_y,pixel_x:pixel_x+new_cell_size_x]
                #    else:
                #        window = image[pixel_y:pixel_y+new_cell_size_y,pixel_x+new_cell_size_x:pixel_x]
                #else:
                #    if pixel_x < pixel_x+new_cell_size_x:
                #        window = image[pixel_y+new_cell_size_y:pixel_y,pixel_x:pixel_x+new_cell_size_x]
                #    else:
                #        window = image[pixel_y+new_cell_size_y:pixel_y,pixel_x+new_cell_size_x:pixel_x]
                #while True:
                #    cv2.imshow("detected.jpg", window)
                #	#out.write(img_test)#動画
                #    k = cv2.waitKey(1) # 1msec待つ
                #    if k == 27: # ESCキーで終了
                #        break
                # 拡張セルのサイズないでヒストグラムを作成
                for y in range(CELL_SIZE*cell_height):
                    for x in range(CELL_SIZE*cell_width):
                        ratio = 0
                        # セルサイズの縦横比で角度を調整 ratio = 比率
                        if cell_width > cell_height:
                            ratio = cell_height/cell_width
                        else:
                            ratio = cell_width/cell_height
                        new_x = 0
                        new_y = 0
                        # 拡張セルを伸ばしていく方向をセル位置に応じて決める
                        if new_cell_size_x > 0:
                            new_x = x
                        else:
                            new_x = -x
                        if new_cell_size_y > 0:
                            new_y = y
                        else:
                            new_y = -y
                        # tan-1(tan()*セル比率)
                        #angle = math.atan(gradient[pixel_x+x][pixel_y+y]*ratio)
                        # ラジアン → 角度 変換 atanの値域が pi/2 ~ -pi/2 なので90度足すことで pi ~ 0にする
                        #angle = (angle*180.0)/math.pi + 90
                        # 角度を投票用に20度で割る
                        #angle = int(angle / 20)
                        angle = int(gradient[pixel_x+x][pixel_y+y]/20)
                        # 投票するときにセル数で割ることで正規化を行う
                        hist[cell_y][cell_x][angle] += magnitude[pixel_x+x][pixel_y+y]/((cell_height)*(cell_width))

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
        cv2.imshow("detected.jpg", gray)
    	#out.write(img_test)#動画
        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            cv2.imwrite("detected.jpg", gray)
            break
    return hog
