import cv2
import numpy as np

cascade_path = "haarcascades/haarcascade_frontalface_alt.xml"

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

    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 分類器を作る?みたいな作業
    cascade = cv2.CascadeClassifier(cascade_path)

    # 顔認識の実行
    facerect = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(1, 1))

    if len(facerect) > 0:
        # 検出した顔を囲む矩形の作成
        for rect in facerect:
            cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)

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
