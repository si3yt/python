# -*- coding: utf-8 -*-
# 画像からカスケード分類器を用いて顔認識を行うサンプル

import cv2

# サンプル顔認識特徴量ファイル
cascade_path = "haarcascades/haarcascade_fullbody.xml"

video = cv2.VideoCapture("video02.MP4")

while(1):
    ret, image = video.read()#画像取得 [ret,image]

    # HoG特徴量の計算
    hog = cv2.HOGDescriptor()

    # SVMによる人検出
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    hogParams = {'hitThreshold': 0, 'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.05, 'finalThreshold': 1}

    # 人を検出した座標
    human, r = hog.detectMultiScale(image, **hogParams)
    # 長方形で人を囲う
    for (x, y, w, h) in human:
        cv2.rectangle(image, (x, y),(x+w, y+h),(0,50,255), 3)

    height = image.shape[0]
    width = image.shape[1]
    half_size = cv2.resize(image,(int(width/2),int(height/2)))

    # 認識結果の表示
    cv2.imshow("detected.jpg", half_size)
    if cv2.waitKey(10) > 0:
        break
