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
import process_HOG as HOG

### SVM
def createSVM():
    ## 学習データ
    # ポジティブ画像
    POS_IMG_DIR = './HumanData/PosImages/'
    POS_IMG_FILES = os.listdir(POS_IMG_DIR)
    # ネガティブ画像
    NEG_IMG_DIR = './HumanData/NegImages/'
    NEG_IMG_FILES = os.listdir(NEG_IMG_DIR)

    PERSON_WIDTH = 100
    PERSON_HEIGHT = 40
    leftop = [0,0]
    rightbottom =  [0+PERSON_WIDTH,0+PERSON_HEIGHT]

    X = []
    y = []

    ## ポジティブ画像からのHOG特徴量の取り出し
    print ('start loading ' + str(len(POS_IMG_FILES)) + ' positive files')
    for pos_img_file in POS_IMG_FILES:
        pos_filepath = POS_IMG_DIR + pos_img_file
        print (pos_filepath)
        pos_img = cv2.imread(pos_filepath)
        fd = HOG.processHOG(pos_img)
        X.append(fd)
        y.append(1)

    ## ネガティブ画像からのHOG特徴量の取り出し
    print ('start loading ' + str(len(NEG_IMG_FILES)) + ' negative files')
    for neg_img_file in NEG_IMG_FILES:
        neg_filepath = NEG_IMG_DIR + neg_img_file
        print (neg_filepath)
        neg_img = cv2.imread(neg_filepath)
        fd = HOG.processHOG(neg_img)
        X.append(fd)
        y.append(0)

    ## リストをnp.array型に変換
    X = np.array(X)
    y = np.array(y)

    ## 特徴量の書き出し
    np.savetxt("HOG_human_data.csv", X, fmt="%f", delimiter=",")
    np.savetxt("HOG_human_target.csv", y, fmt="%.0f", delimiter=",")

    # 特徴量の読み込み
    X = np.loadtxt("HOG_human_data.csv", delimiter=",")
    y = np.loadtxt("HOG_human_target.csv", delimiter=",")

    ## 線形SVMの学習パラメータを格子点探索で求める
    # Cパラメータを調整する
    tuned_parameters = [{'C': [0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]}]

    print ('start Grid Search')
    gscv = GridSearchCV(svm.LinearSVC(), tuned_parameters, cv=3) #cv = 折り返し値？
    gscv.fit(X, y)
    svm_best = gscv.best_estimator_

    print ('searched result of  C =', svm_best.C)

    # 最適なパラメータを用いたSVMの再学習
    print ('start re-learning SVM with best parameter set.')
    svm_best.fit(X, y)

    # 学習結果の保存
    print ('finish learning SVM　with Grid-search.')
    joblib.dump(svm_best, 'Best_human_detector.pkl', compress=9)
