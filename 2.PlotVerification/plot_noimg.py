import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

import sphere_rerotate as horizon

def rad_conv(a):
    a = a * math.pi / 180
    return a

plt.figure(figsize=(23,10))

angle = 90
angle_rad = rad_conv(angle)
r, im = horizon.horizon_rotate(angle_rad)
plt.imshow(im)

x = np.linspace(-math.pi, math.pi, 360)
xd = np.arctan2( np.cos(angle_rad) * np.sin(x) ,np.cos(x) ) / math.pi * 100+99.5

plt.plot(xd, np.arctan2(np.sin(angle_rad) * np.sin(x), np.sqrt(1-(np.sin(x))**2 * (np.sin(angle_rad)**2))) / math.pi * 100 + 49.5 )
plt.xlim(-10,210)
plt.ylim(110, -10)
plt.show()

#plt.savefig('output.png')
