import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

import sphere_rerotate as horizon

def rad_conv(a):
    a = a * math.pi / 180
    return a

plt.figure(figsize=(23,10))

for angle in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]:
    angle_rad = rad_conv(angle)

    x = np.linspace(-math.pi, math.pi, 180)
    # 【疑似位相】プラスすることでグラフを左右にずらせる
    xd = np.arctan2( np.cos(angle_rad) * np.sin(x) ,np.cos(x) ) + math.pi - rad_conv(20)
    for i in range(0,len(xd)):
        if xd[i] < 0:
            xd[i] = xd[i] + 2*math.pi

    # 【振幅】値を掛ければ振幅が伸びる
    # 【縦位置】値を足すことでグラフが上下する
    plt.plot(xd, np.arctan2(np.sin(angle_rad) * np.sin(x), np.sqrt(1-(np.sin(x))**2 * (np.sin(angle_rad)**2))))

plt.show()

#plt.savefig('output.png')
