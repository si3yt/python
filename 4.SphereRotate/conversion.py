# import
import math
import numpy as np

# degree　→　radian
def get_rad(degree):
    rad = degree * math.pi / 180
    return rad

# radian → degree
def get_degree(radian):
    degree = radian * 180 / math.pi
    return degree

# polar → xyz
def get_xyz(r, latitude, longitude):
    x = r * math.sin(latitude) * math.cos(longitude)
    y = r * math.sin(latitude) * math.sin(longitude)
    z = r * math.cos(latitude)

    return x, y, z

# xyz → polar
def get_polar(x, y, z):
    distance = math.sqrt(x**2 + y**2 + z**2)
    theta    = math.acos(z / distance)   # range:0~pi   # latitude
    phi      = math.atan2(y, x)          # range:-pi~pi # longitude

    return distance, theta, phi

# after rotate xyz
def get_after_xyz(x, y, z, matrix):
    after_x = x * matrix[0,0] + y * matrix[0,1] + z * matrix[0,2]
    after_y = x * matrix[1,0] + y * matrix[1,1] + z * matrix[1,2]
    after_z = x * matrix[2,0] + y * matrix[2,1] + z * matrix[2,2]

    return after_x, after_y, after_z

# cylinder expansion
def cylinder_expansion(phi, theta, r, width, height):
    cylinder_x = (phi   * r) / width  * (width  - 1) # latitude * r
    cylinder_y = (theta * r) / height * (height - 1) # longitude * r

    return cylinder_x, cylinder_y
