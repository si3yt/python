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

# create files
import process_HOG as normalHOG
import print_HOG as printHOG
import learning_SVM as SVM
import improvement_HOG as impHOG
import improvement_HOG_second as impHOGsnd

### main
if __name__ == "__main__":

    imgSample = cv2.imread('./image/sample2.jpg')

    impHOGsnd.improvementHOG(imgSample)

    #printHOG.printHOG(imgSample)
    #impHOG.improvementHOG(imgSample)
    #SVM.createSVM()

    #SVM
    '''
    # SVMの学習結果を読み込む
    print ('start loading SVM.')
    detector = joblib.load('Best_human_detector.pkl')
    print ('finish loading SVM.')

    # 検出器の大きさの指定
    PERSON_WIDTH = 100
    PERSON_HEIGHT = 100
    PERSON_SIZE = (PERSON_WIDTH, PERSON_HEIGHT)

    # 検出対象画像の指定
    read_img_path = './image/testSample.jpg'
    read_img = cv2.imread(read_img_path)

    # read image size
    img_h = read_img.shape[0]
    img_w = read_img.shape[1]
    img_size = (img_w, img_h)

    # 探索の細かさ
    step_w = 5
    step_h = 5

    # リサイズ用変数
    RESIZE_VALUE = 10
    resize_count = RESIZE_VALUE + 1
    slide_value_h = img_h
    slide_value_w = img_w
    slide_value = (slide_value_w, slide_value_h)
    resize_img = read_img

    # 画像をスキャンして，各領域の人らしさを計算
    likelihood_list = []
    while  (slide_value > PERSON_SIZE) and (resize_count > 0):
        # 画像のサイズ変更
        resize_count = resize_count - 1
        slide_value_h = int(slide_value_h * (resize_count / RESIZE_VALUE))
        slide_value_w = int(slide_value_w * (resize_count / RESIZE_VALUE))
        slide_value = (slide_value_w, slide_value_h)
        resize_img = cv2.resize(resize_img, slide_value)
        for x in range(0,slide_value_w-step_w-PERSON_WIDTH,step_w):
            for y in range(0,slide_value_h-step_h-PERSON_HEIGHT,step_h):
                window = resize_img[y:y+PERSON_HEIGHT,x:x+PERSON_WIDTH]
                fd = normalHOG.processHOG(window) ## 領域内のHOG特徴量を取り出し、SVMに入力して学習データと比較
                fd = np.array(fd).reshape(1, -1)
                print ('Now Play SVM : y=' + str(y) + ' x=' + str(x) + ' i=' + str(resize_count))
                estimated_class = 1/(1+(math.exp(-1*detector.decision_function(fd)))) ##SVMの出力値をシグモイド関数で0~1に正規化
                if estimated_class >= 0.6: ## 領域内の人らしさが...割を超えた場合のみ座標を保持
                    multi = RESIZE_VALUE / resize_count
                    likelihood_list.append([int(x*multi),int(y*multi),int(x*multi)+int(PERSON_WIDTH*multi),int(y*multi)+int(PERSON_HEIGHT*multi)])

    if len(likelihood_list) > 0:
        for rect in likelihood_list:
            cv2.rectangle(read_img, tuple(rect[0:2]), tuple(rect[2:4]), (0,0,0), 2)

    # 人らしさの表示
    while True:
        cv2.imshow("result.jpg", read_img)
    	#out.write(img_test)#動画
        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            break

    '''
