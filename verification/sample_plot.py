import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

import sphere_rerotate as horizon

def rad_conv(a):
    a = a * math.pi / 180
    return a

plt.figure(figsize=(23,10))
phs = 0
width = 1000
height = 500

for amp in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]:
    amp_rad = rad_conv(amp)

    x = np.linspace(0, width, width)

    plt.plot(x, (height/np.pi)*amp_rad*np.sin((2*np.pi*x)/(width)+phs)+(height/2))

plt.show()
