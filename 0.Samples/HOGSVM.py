import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if cap.isOpened() is False:
	raise("IO Error")
fret,fimage = cap.read()
#fourcc = cv2.VideoWriter_fourcc(*'XVID') #動画
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))#動画

while True:
    ret, image = cap.read()#画像取得 [ret,image]

    # これは、BGRの順になっている気がする
    color = (255, 255, 255)#白

    # HoG特徴量の計算
    hog = cv2.HOGDescriptor()

    # SVMによる人検出
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    hogParams = {'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.05}

    # 人を検出した座標
    human, r = hog.detectMultiScale(image, **hogParams)
    # 長方形で人を囲う
    for (x, y, w, h) in human:
        cv2.rectangle(image, (x, y),(x+w, y+h),(0,50,255), 3)

    cv2.imshow("detected.jpg", image)
	#out.write(img_test)#動画
    k = cv2.waitKey(1) # 1msec待つ
    if k == 27: # ESCキーで終了
        break
    elif k == 32:
        fret,fimage = cap.read()
cap.release()

#out.release()#動画
cv2.destroyAllWindows()
