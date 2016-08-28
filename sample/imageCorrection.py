# import
import cv2
import numpy as np
import math
# read image file
image = cv2.imread('../image/theta04.jpg')
# read image size
height = image.shape[0]
width = image.shape[1]
#　one side fish eye radius
fish_radius = int(width / 4)
# one side fish eye image
one_side_image = image[0:height, fish_radius:fish_radius*3]
# other side fish eye image
other1 = image[0:height, fish_radius*3:fish_radius*4]
other2 = image[0:height, 0:fish_radius]
other_side_image = cv2.hconcat([other1, other2])

# output image create
output = np.zeros((height, fish_radius*2, 3), np.uint8)

# output resize
one_half = cv2.resize(one_side_image,(int(fish_radius),int(height/2)))
other_half = cv2.resize(other_side_image,(int(fish_radius),int(height/2)))

# output image
#while(1):
    # HoG特徴量の計算
hog = cv2.HOGDescriptor()

    # SVMによる人検出
#    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
#    hogParams = {'hitThreshold': 0, 'winStride': (8, 8), 'padding': (32, 32), 'scale': 1.05, 'finalThreshold': 1}

    # 人を検出した座標
#    human, r = hog.detectMultiScale(other_half, **hogParams)
    # 長方形で人を囲う
#    for (x, y, w, h) in human:
#        cv2.rectangle(other_half, (x, y),(x+w, y+h),(0,50,255), 3)

cv2.imwrite("output.jpg", one_half)

#res = hog.compute(other_half)
#print (res)
#print (len(res))
#    if cv2.waitKey(10) > 0:
#        break
