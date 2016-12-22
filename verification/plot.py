import numpy as np
import math
import matplotlib.pyplot as plt
#import seaborn as sns
from PIL import Image

import sphere_rerotate as horizon

plt.figure(figsize=(25,10))

rotate_angle = 90
rad_angle = horizon.rad_conv(rotate_angle)

r, im = horizon.horizon_rotate(rad_angle)
plt.imshow(im)              # 画像貼り付け

x = np.linspace(0, 200, 200)
a = 100 * ( rotate_angle / 180 )

plt.plot(x, a * np.cos( x / 100 * math.pi) + 50.5)
plt.xlim(0,200)
plt.ylim(48 - a, 52 + a)
#plt.show()

plt.savefig('output.png')
