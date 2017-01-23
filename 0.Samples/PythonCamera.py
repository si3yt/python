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

	image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)#HSVに変換

	lower_yellow = np.array([40, 25, 10])#下限
	upper_yellow = np.array([80, 255, 190])#上限
	img_mask = cv2.inRange(image, lower_yellow, upper_yellow)#範囲内を１、それ以外を０とするマスクを作成
	
	fmimage = cv2.bitwise_and(fimage, fimage, mask=img_mask)#マスクを背景に適用
	img_mask=~img_mask#マスク反転
	mimage = cv2.bitwise_and(image, image, mask=img_mask)#反転したマスクを現在フレームに適用
	
	mimage = cv2.cvtColor(mimage, cv2.COLOR_HSV2BGR)#現在フレームはHSVなのでRGBに戻す

	img_test = fmimage + mimage#背景と現在フレームを足し合わせる
	cv2.imshow("cap",img_test)
	#out.write(img_test)#動画
	k = cv2.waitKey(1) # 1msec待つ
	if k == 27: # ESCキーで終了
		break
	elif k == 32:
		fret,fimage = cap.read()
cap.release()

#out.release()#動画
cv2.destroyAllWindows()