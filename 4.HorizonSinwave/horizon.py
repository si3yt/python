# import library
import math
import numpy as np

# import files
import constant as const

# horizon
def get_fx(x, amp, phs):
    w = const.get_img_width()
    h = const.get_img_height()

    fx = w/(2*math.pi) * math.asin( math.sin(amp) * math.sin(math.atan2(math.sin(2*math.pi*x/w+phs), math.cos(amp)*math.cos(2*math.pi*x/w+phs)))) + h/2

    return fx

# differential
def get_dx(x, amp, phs):
    w = const.get_img_width()
    h = const.get_img_height()

    dx = (math.sin(amp)*math.cos(amp)*math.cos(math.atan2(math.sin(2*math.pi *x/w+phs),math.cos(amp)*math.cos(2*math.pi*x/w+phs)))) / ((((math.cos(2*math.pi*x/w+phs))**2)*((math.cos(amp))**2)+((math.sin(2*math.pi*x/w+phs))**2))*math.sqrt(1-((math.sin(amp))**2)*((math.sin(math.atan2(math.sin(2*math.pi *x/w+phs),math.cos(amp)*math.cos(2*math.pi*x/w+phs))))**2)))

    return dx

# 0 = horizon
def get_fx0(a, b, x, amp, phs):
    w = const.get_img_width()
    h = const.get_img_height()

    fx0 = a * x + b - w/(2*math.pi) * math.asin( math.sin(amp) * math.sin(math.atan2(math.sin(2*math.pi*x/w+phs), math.cos(amp)*math.cos(2*math.pi*x/w+phs)))) - h/2

    return fx0

# 0 = differential
def get_dx0(a, x, amp, phs):
    w = const.get_img_width()
    h = const.get_img_height()
    dx0 = a - (math.sin(amp)*math.cos(amp)*math.cos(math.atan2(math.sin(2*math.pi*x/w+phs),math.cos(amp)*math.cos(2*math.pi*x/w+phs)))) / ((((math.cos(2*math.pi*x/w+phs))**2)*((math.cos(amp))**2)+((math.sin(2*math.pi*x/w+phs))**2))*math.sqrt(1-((math.sin(amp))**2)*((math.sin(math.atan2(math.sin(2*math.pi*x/w+phs),math.cos(amp)*math.cos(2*math.pi*x/w+phs))))**2)))

    return dx0
