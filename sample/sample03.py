# -*- coding: utf-8 -*-
# 画像からカスケード分類器を用いて顔認識を行うサンプル

import cv2

# サンプル顔認識特徴量ファイル
cascade_path = "haarcascades/haarcascade_fullbody.xml"
image_path = "theta04.jpg"

# 画像の読み込み
image = cv2.imread(image_path)

# HoG特徴量の計算
hog = cv2.HOGDescriptor()

# SVMによる人検出
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
hogParams = {'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.05}

# 人を検出した座標
human, r = hog.detectMultiScale(image, **hogParams)
# 長方形で人を囲う
for (x, y, w, h) in human:
    cv2.rectangle(image, (x, y),(x+w, y+h),(255,255,255), 3)

height = image.shape[0]
width = image.shape[1]
half_size = cv2.resize(image,(int(width/4),int(height/4)))

# 認識結果の表示
cv2.imshow("detected.jpg", half_size)
cv2.imwrite("sample00.jpg", half_size)

# 何かキーが押されたら終了
while(1):
  if cv2.waitKey(10) > 0:
    break
