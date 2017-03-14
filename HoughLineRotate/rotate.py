# import
import cv2
import math
import numpy as np

# Make inverse rotation matrix
def rotate(lon, lat, ang):
    # around the x axis
    x_rotate = np.matrix( [[1, 0,             0             ], \
                           [0, math.cos(ang), -math.sin(ang)], \
                           [0, math.sin(ang), math.cos(ang)]] )
    # around the y axis
    y_rotate = np.matrix( [[math.cos(lat),  0, math.sin(lat)], \
                           [0,              1, 0            ], \
                           [-math.sin(lat), 0, math.cos(lat)]] )
    # around the z axis
    z_rotate = np.matrix( [[math.cos(lon), -math.sin(lon), 0], \
                           [math.sin(lon), math.cos(lon),  0], \
                           [0,             0,              1]] )
    # matrix product
    matrix = z_rotate.dot(y_rotate) # z * y
    matrix = matrix.dot(x_rotate)   # z * y * x

    return matrix


# Make inverse rotation matrix
def rerotate(lon, lat, ang):
    # around the z axis
    z_rotate = np.matrix( [[math.cos(lon), -math.sin(lon), 0], \
                           [math.sin(lon), math.cos(lon),  0], \
                           [0,              0,             1]] )
    # around the y axis
    y_rotate = np.matrix( [[math.cos(lat),  0, math.sin(lat) ], \
                           [0,              1, 0             ], \
                           [-math.sin(lat), 0, math.cos(lat) ]] )
    # around the x axis
    x_rotate = np.matrix( [[1, 0,             0             ], \
                           [0, math.cos(ang), -math.sin(ang)], \
                           [0, math.sin(ang), math.cos(ang)]] )
    # matrix product
    matrix = x_rotate.dot(y_rotate) # x * y
    matrix = matrix.dot(z_rotate)   # x * y * z

    return matrix

# Make inverse rotation matrix
def double_rerotate(lon, lat, ang):
    # around the z axis
    z_rotate = np.matrix( [[math.cos(lon), -math.sin(lon), 0], \
                           [math.sin(lon), math.cos(lon),  0], \
                           [0,              0,             1]] )
    # around the y axis
    y_rotate = np.matrix( [[math.cos(lat),  0, math.sin(lat) ], \
                           [0,              1, 0             ], \
                           [-math.sin(lat), 0, math.cos(lat) ]] )
    # around the x axis
    x_rotate = np.matrix( [[1, 0,             0             ], \
                           [0, math.cos(ang), -math.sin(ang)], \
                           [0, math.sin(ang), math.cos(ang)]] )

    return x_rotate, y_rotate, z_rotate

# theta zenith rotate
def zenith_rotate(zX, zY, compass):
    matrix = np.matrix( [[math.cos(zY), -math.sin(zY)*math.cos(zX),         -math.sin(zY)*math.sin(zX)], \
                         [math.sin(zY), math.cos(zY)*math.cos(zX),  math.cos(zY)*math.sin(zX) ], \
                         [0,            math.sin(zX),               math.cos(zX)              ]] )

    return matrix
