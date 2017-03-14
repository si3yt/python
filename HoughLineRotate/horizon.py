# import library
import math
import numpy as np

# horizon
def get_fx(x, amp, phs, h, w):
    fx = w/(2*math.pi) * math.asin( math.sin(amp) * math.sin(math.atan2(math.sin(2*math.pi*x/w+phs), math.cos(amp)*math.cos(2*math.pi*x/w+phs)))) + h/2

    return fx

# differential
def get_dx(x, amp, phs, h, w):
    dx = (math.sin(amp)*math.cos(amp)*math.cos(math.atan2(math.sin(2*math.pi *x/w+phs),math.cos(amp)*math.cos(2*math.pi*x/w+phs)))) / ((((math.cos(2*math.pi*x/w+phs))**2)*((math.cos(amp))**2)+((math.sin(2*math.pi*x/w+phs))**2))*math.sqrt(1-((math.sin(amp))**2)*((math.sin(math.atan2(math.sin(2*math.pi *x/w+phs),math.cos(amp)*math.cos(2*math.pi*x/w+phs))))**2)))

    return dx

# 0 = horizon
def get_fx0(a, b, x, amp, phs, h, w):
    fx0 = a * x + b - w/(2*math.pi) * math.asin( math.sin(amp) * math.sin(math.atan2(math.sin(2*math.pi*x/w+phs), math.cos(amp)*math.cos(2*math.pi*x/w+phs)))) - h/2

    return fx0

# 0 = differential
def get_dx0(a, x, amp, phs, h, w):
    dx0 = a - (math.sin(amp)*math.cos(amp)*math.cos(math.atan2(math.sin(2*math.pi*x/w+phs),math.cos(amp)*math.cos(2*math.pi*x/w+phs)))) / ((((math.cos(2*math.pi*x/w+phs))**2)*((math.cos(amp))**2)+((math.sin(2*math.pi*x/w+phs))**2))*math.sqrt(1-((math.sin(amp))**2)*((math.sin(math.atan2(math.sin(2*math.pi*x/w+phs),math.cos(amp)*math.cos(2*math.pi*x/w+phs))))**2)))

    return dx0
