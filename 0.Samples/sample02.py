# -*- coding: utf-8 -*-
# 画像からカスケード分類器を用いて顔認識を行うサンプル

import cv2

# サンプル顔認識特徴量ファイル
cascade_path = "haarcascades/haarcascade_fullbody.xml"
image_path = "theta04.jpg"

# これは、BGRの順になっている気がする
color = (255, 255, 255) #白

# 画像の読み込み
image = cv2.imread(image_path)

# 分類器を作る?みたいな作業
cascade = cv2.CascadeClassifier(cascade_path)

# 顔認識の実行
facerect = cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

if len(facerect) > 0:
  # 検出した顔を囲む矩形の作成
  for rect in facerect:
    cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
else:
  print("no face")

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
