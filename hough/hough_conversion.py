# import library
import cv2
import math
import numpy as np

def hough_lines(img, line_extend, line_len, degree_threshold):
    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # エッジ抽出
    edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
    # ハフ変換
    # 第一引数：image
    # 第二引数：rhoの精度
    # 第三引数：thetaの精度
    # 第四引数：最小の直線の長さ
    lines = cv2.HoughLines(edges, 1, math.pi/360, line_len)

    # 絞り込み後の直線格納リスト
    degree_line = []

    # 直線の端点を求める
    for i in range(0,len(lines)):
        # rho：直線までの距離
        # theta：直線の角度
        for rho,theta in lines[i]:
            # 端点取得
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + line_extend*(-b))
            y1 = int(y0 + line_extend*(a))
            x2 = int(x0 - line_extend*(-b))
            y2 = int(y0 - line_extend*(a))

            if angle_refine(theta, degree_threshold):
                degree_line.append((x1,y1,x2,y2))

    return degree_line

# 直線の絞り込み
def angle_refine(degree, degree_threshold):
    # theta：ラジアン → 度
    degree = degree * 180 / math.pi

    # 直線の絞り込み
    if degree < degree_threshold or degree > 180-degree_threshold: # 負の角度
        return True
    else:
        return False
