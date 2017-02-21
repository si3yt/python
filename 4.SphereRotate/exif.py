#!/bin/python2
import os
import subprocess
import struct

def find_data(s, tag):
    ix = s.find(tag)
    if ix < 0:
        raise Exception('Cannot find tag')
    return ix + len(tag)

def parse_u_rational(s):
    a, b = struct.unpack('>II', s)
    return float(a) / float(b)

def parse_s_rational(s):
    a, b = struct.unpack('>ii', s)
    return float(a) / float(b)

def get_angles(path):
    f = open(path, 'rb')
    head = f.read(10 * 1000)  # take long enough header

    # Find CompassEs
    ix = find_data(head, b"\x00\x04\x00\x05\x00\x00\x00\x01")  # search CompassEs,UnsignedRational,1
    offset = struct.unpack('>I', head[ix : ix + 4])[0] + 12
    compass = parse_u_rational(head[offset : offset + 8])

    # Find ZenithEs
    ix = find_data(head, b"\x00\x03\x00\x0a\x00\x00\x00\x02")  # search ZenithEs,SignedRational,2
    offset = struct.unpack('>I', head[ix : ix + 4])[0] + 12
    zenith_x = parse_s_rational(head[offset : offset + 8])
    zenith_y = parse_s_rational(head[offset + 8 : offset + 16])

    return [zenith_x , zenith_y, compass]
