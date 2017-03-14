import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image

import sphere_rerotate as horizon

def rad_conv(a):
    a = a * math.pi / 180
    return a

plt.figure(figsize=(23,10))

width = 1000
height = 500

for angle in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]:
    x = np.linspace(0, width, width+1)
    nt_x = np.linspace(0, width-1, width)
    nt_x = np.append(nt_x, np.array([0]))
    amp_rad = rad_conv(angle)
    phase = 0

    plt.plot(x, height/np.pi * np.arcsin( np.sin(amp_rad) * np.sin(np.arctan2(np.sin(2*nt_x*np.pi/width+phase), np.cos(amp_rad)*np.cos(2*nt_x*np.pi/width+phase)))) + height/2, "b")

plt.xlim(-10, width+10)
plt.ylim(height+10, -10)
plt.xlabel("x [pixel]")
plt.ylabel("y [pixel]")
plt.rcParams["font.size"] = 25

#plt.show()

plt.savefig('output.png')
