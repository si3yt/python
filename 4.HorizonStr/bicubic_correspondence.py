# import
import math
import numpy as np

def left(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width):
    f11 = img[int(y+y1)][int(width-1)]
    f12 = img[int(y+y2)][int(width-1)]
    f13 = img[int(y-y3)][int(width-1)]
    f14 = img[int(y-y4)][int(width-1)]
    f21 = img[int(y+y1)][int(x-x2)]
    f24 = img[int(y-y4)][int(x-x2)]
    f31 = img[int(y+y1)][int(x+x3)]
    f34 = img[int(y-y4)][int(x+x3)]
    f41 = img[int(y+y1)][int(x+x4)]
    f42 = img[int(y+y2)][int(x+x4)]
    f43 = img[int(y-y3)][int(x+x4)]
    f44 = img[int(y-y4)][int(x+x4)]

    return f11, f12, f13, f14, f21, f24, f31, f34, f41, f42, f43, f44

def right(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width):
    f11 = img[int(y+y1)][int(x-x1)]
    f12 = img[int(y+y2)][int(x-x1)]
    f13 = img[int(y-y3)][int(x-x1)]
    f14 = img[int(y-y4)][int(x-x1)]
    f21 = img[int(y+y1)][int(x-x2)]
    f24 = img[int(y-y4)][int(x-x2)]
    f31 = img[int(y+y1)][int(x+x3)]
    f34 = img[int(y-y4)][int(x+x3)]
    f41 = img[int(y+y1)][int(0)]
    f42 = img[int(y+y2)][int(0)]
    f43 = img[int(y-y3)][int(0)]
    f44 = img[int(y-y4)][int(0)]

    return f11, f12, f13, f14, f21, f24, f31, f34, f41, f42, f43, f44

def bottom(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width):
    f11 = img[int(y-y1)][int(math.fabs(x-x1-width)-1)]
    f12 = img[int(y+y2)][int(x-x1)]
    f13 = img[int(y-y3)][int(x-x1)]
    f14 = img[int(y-y4)][int(x-x1)]
    f21 = img[int(y-y1)][int(math.fabs(x-x2-width)-1)]
    f24 = img[int(y-y4)][int(x-x2)]
    f31 = img[int(y-y1)][int(math.fabs(x+x3-width)-1)]
    f34 = img[int(y-y4)][int(x+x3)]
    f41 = img[int(y-y1)][int(math.fabs(x+x4-width)-1)]
    f42 = img[int(y+y2)][int(x+x4)]
    f43 = img[int(y-y3)][int(x+x4)]
    f44 = img[int(y-y4)][int(x+x4)]

    return f11, f12, f13, f14, f21, f24, f31, f34, f41, f42, f43, f44

def top(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width):
    f11 = img[int(y+y1)][int(x-x1)]
    f12 = img[int(y+y2)][int(x-x1)]
    f13 = img[int(y-y3)][int(x-x1)]
    f14 = img[int(y+y4)][int(math.fabs(x-x1-width)-1)]
    f21 = img[int(y+y1)][int(x-x2)]
    f24 = img[int(y+y4)][int(math.fabs(x-x2-width)-1)]
    f31 = img[int(y+y1)][int(x+x3)]
    f34 = img[int(y+y4)][int(math.fabs(x+x3-width)-1)]
    f41 = img[int(y+y1)][int(x+x4)]
    f42 = img[int(y+y2)][int(x+x4)]
    f43 = img[int(y-y3)][int(x+x4)]
    f44 = img[int(y+y4)][int(math.fabs(x+x4-width)-1)]

    return f11, f12, f13, f14, f21, f24, f31, f34, f41, f42, f43, f44

def left_bottom(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width):
    f11 = img[int(y-y1)][int(width-1)]
    f12 = img[int(y+y2)][int(width-1)]
    f13 = img[int(y-y3)][int(width-1)]
    f14 = img[int(y-y4)][int(width-1)]
    f21 = img[int(y-y1)][int(math.fabs(x-x2-width)-1)]
    f24 = img[int(y-y4)][int(x-x2)]
    f31 = img[int(y-y1)][int(math.fabs(x+x3-width)-1)]
    f34 = img[int(y-y4)][int(x+x3)]
    f41 = img[int(y-y1)][int(math.fabs(x+x4-width)-1)]
    f42 = img[int(y+y2)][int(x+x4)]
    f43 = img[int(y-y3)][int(x+x4)]
    f44 = img[int(y-y4)][int(x+x4)]

    return f11, f12, f13, f14, f21, f24, f31, f34, f41, f42, f43, f44

def left_top(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width):
    f11 = img[int(y+y1)][int(width-1)]
    f12 = img[int(y+y2)][int(width-1)]
    f13 = img[int(y-y3)][int(width-1)]
    f14 = img[int(y+y4)][int(width-1)]
    f21 = img[int(y+y1)][int(x-x2)]
    f24 = img[int(y+y4)][int(math.fabs(x-x2-width)-1)]
    f31 = img[int(y+y1)][int(x+x3)]
    f34 = img[int(y+y4)][int(math.fabs(x+x3-width)-1)]
    f41 = img[int(y+y1)][int(x+x4)]
    f42 = img[int(y+y2)][int(x+x4)]
    f43 = img[int(y-y3)][int(x+x4)]
    f44 = img[int(y+y4)][int(math.fabs(x+x4-width)-1)]

    return f11, f12, f13, f14, f21, f24, f31, f34, f41, f42, f43, f44

def right_bottom(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width):
    f11 = img[int(y-y1)][int(math.fabs(x-x1-width)-1)]
    f12 = img[int(y+y2)][int(x-x1)]
    f13 = img[int(y-y3)][int(x-x1)]
    f14 = img[int(y-y4)][int(x-x1)]
    f21 = img[int(y-y1)][int(math.fabs(x-x2-width)-1)]
    f24 = img[int(y-y4)][int(x-x2)]
    f31 = img[int(y-y1)][int(math.fabs(x+x3-width))]
    f34 = img[int(y-y4)][int(x+x3)]
    f41 = img[int(y-y1)][int(0)]
    f42 = img[int(y+y2)][int(0)]
    f43 = img[int(y-y3)][int(0)]
    f44 = img[int(y-y4)][int(0)]

    return f11, f12, f13, f14, f21, f24, f31, f34, f41, f42, f43, f44

def right_top(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width):
    f11 = img[int(y+y1)][int(x-x1)]
    f12 = img[int(y+y2)][int(x-x2)]
    f13 = img[int(y-y3)][int(x+x3)]
    f14 = img[int(y+y4)][int(math.fabs(x-x1-width)-1)]
    f21 = img[int(y+y1)][int(x-x2)]
    f24 = img[int(y+y4)][int(math.fabs(x-x2-width)-1)]
    f31 = img[int(y+y1)][int(x+x3)]
    f34 = img[int(y+y4)][int(math.fabs(x+x3-width)-1)]
    f41 = img[int(y+y1)][int(0)]
    f42 = img[int(y+y2)][int(0)]
    f43 = img[int(y-y3)][int(0)]
    f44 = img[int(y+y4)][int(0)]

    return f11, f12, f13, f14, f21, f24, f31, f34, f41, f42, f43, f44

def other(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width):
    f11 = img[int(y+y1)][int(x-x1)]
    f12 = img[int(y+y2)][int(x-x1)]
    f13 = img[int(y-y3)][int(x-x1)]
    f14 = img[int(y-y4)][int(x-x1)]
    f21 = img[int(y+y1)][int(x-x2)]
    f24 = img[int(y-y4)][int(x-x2)]
    f31 = img[int(y+y1)][int(x+x3)]
    f34 = img[int(y-y4)][int(x+x3)]
    f41 = img[int(y+y1)][int(x+x4)]
    f42 = img[int(y+y2)][int(x+x4)]
    f43 = img[int(y-y3)][int(x+x4)]
    f44 = img[int(y-y4)][int(x+x4)]

    return f11, f12, f13, f14, f21, f24, f31, f34, f41, f42, f43, f44

def correspondence(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width):
    if x-x1 < 0:                    # left
        if y+y1 >= height:          # left bottom
            return left_bottom(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width)
        elif y-y4 < 0:              # left top
            return left_top(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width)
        else:
            return left(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width)
    elif x+x4 >= width:             # right
        if y+y1 >= height:          # right bottom
            return right_bottom(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width)
        elif y-y4 < 0:              # right top
            return right_top(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width)
        else:
            return right(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width)
    elif y+y1 >= height:            # bottom
        return bottom(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width)
    elif y-y4 < 0:                  # top
        return top(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width)
    else:
        return other(img, x, y, x1, x2, x3, x4, y1, y2, y3, y4, height, width)
