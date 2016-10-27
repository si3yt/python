# import
import cv2
import numpy as np
import math
import os

def rerotate(lon, lat, ang):
    # z軸周り
    z_rotate = np.matrix( [[math.cos(lon),  math.sin(lon), 0], \
                           [-math.sin(lon), math.cos(lon), 0], \
                           [0,              0,             1]] )
    # y軸周り
    y_rotate = np.matrix( [[math.cos(lat), 0, -math.sin(lat)], \
                           [0,             1, 0             ], \
                           [math.sin(lat), 0, math.cos(lat) ]] )
    # x軸周り
    x_rotate = np.matrix( [[1, 0,              0            ], \
                           [0, math.cos(ang),  math.sin(ang)], \
                           [0, -math.sin(ang), math.cos(ang)]] )
    # 行列の積
    matrix = x_rotate.dot(y_rotate) # x軸回転 * y軸回転
    matrix = matrix.dot(z_rotate)   # x軸回転 * y軸回転 * z軸回転

    return matrix

def zenith_rotate(zX, zY, compass):
    matrix = np.matrix( [[math.cos(zY), -math.sin(zY)*math.cos(zX), -math.sin(zY)*math.sin(zX)], \
                         [math.sin(zY), math.cos(zY)*math.cos(zX),  math.cos(zY)*math.sin(zX) ], \
                         [0,            math.sin(zX),               math.cos(zX)              ]] )

    return matrix
