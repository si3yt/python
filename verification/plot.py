import numpy as np
import math
import matplotlib.pyplot as plt
#import seaborn as sns
from PIL import Image

import sphere_rerotate as horizon

plt.figure(figsize=(25,10))

#rotate_angle = 90
#rad_angle = horizon.rad_conv(rotate_angle)

#r, im = horizon.horizon_rotate(rad_angle)
#plt.imshow(im)              # 画像貼り付け

nt_x = np.linspace(0, 2*math.pi, 360)
width = 1000
height = 500
amp_rad = math.pi / 2
phase = math.pi

plt.plot(nt_x, - width/(2*np.pi) * np.arcsin( np.sin(amp_rad) * np.sin(np.arctan2(np.sin(nt_x+phase), np.cos(amp_rad)*np.cos(nt_x+phase)))) + height/2)

#plt.plot(nt_x, - (width*np.sin(amp_rad)*np.cos(amp_rad)*np.cos(np.arctan2(np.sin(nt_x+phase),np.cos(amp_rad)*np.cos(nt_x+phase)))) / (2*np.pi*(((np.cos(nt_x+phase))**2)*(np.cos(amp_rad)**2)+(np.sin(nt_x+phase)**2))*np.sqrt(1-(np.sin(amp_rad)**2)*(np.sin(np.arctan2(np.sin(nt_x+phase),np.cos(amp_rad)*np.cos(nt_x+phase)))**2))))

plt.show()

#plt.savefig('output.png')
