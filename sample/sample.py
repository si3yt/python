import cv2

img = cv2.imread('sample.jpg')
# アルゴリズム名を引数で渡す
detector = cv2.FastFeatureDetector_create()
keypoints = detector.detect(img)
# 画像への特徴点の書き込み
out = cv2.drawKeypoints(img, keypoints, None)
# 表示
cv2.imshow("a", out)
cv2.waitKey(0)
