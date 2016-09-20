# import
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

### main
if __name__ == "__main__":

    # read image file
    image = cv2.imread('./image/sample00.jpg')
    # read image size
    height = image.shape[0]
    width = image.shape[1]
    #　one side fish eye radius
    fish_radius = int(width / 4)

    # 球体の方程式
    # x^2 + y^2 + z^2 = r^2
    r = fish_radius

    # 直線の公式
    # 媒介変数形式 (x,y,z) = (x1,y1,z1) + t(x2-x1,y2-y1,z-z1)
    # 変形 (x-x1)/(x2-x1) = (y-y1)/(y2-y1)=(z-z1)/(z2-z1)
    # 原点を通る3次元直線の公式
    # x/x2 = y/y2 = z/z2
