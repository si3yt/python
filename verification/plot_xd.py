import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

import sphere_rerotate as horizon

def rad_conv(a):
    a = a * math.pi / 180
    return a

plt.figure(figsize=(23,10))

for angle in [80]:#0, 10, 20, 30, 40, 50, 60, 70, 80, 90]:
    angle_rad = rad_conv(angle)

    x = np.linspace(-math.pi, math.pi, 360)
    # 【位相】xに値をずれせば
    xd = np.arctan2( np.sin(x), np.cos(angle_rad) * np.cos(x) )
    # 【振幅】値を掛ければ振幅が伸びる
    # 【縦位置】値を足すことでグラフが上下する
    # plt.plot(x, np.arctan2(np.sin(angle_rad) * np.sin(xd), np.sqrt(1-(np.sin(xd))**2 * (np.sin(angle_rad)**2))))
    plt.plot(x, np.arcsin(np.sin(angle_rad) * np.sin(xd)))


plt.show()

#plt.savefig('output.png')
