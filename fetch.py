#!/usr/bin/python

import math
import urllib.request

data_url = 'http://www.cis.rit.edu/research/mcsl2/online/munsell_data/all.dat'
data_file = 'all.dat'

def fetch(url = data_url, fname = data_file):
    data = urllib.request.urlopen(url)
    with open(fname, 'w') as f:
        f.write(data.read().decode())

def load(fname = data_file):
    with open(fname) as f:
        return [line for line in f]

hues = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
hues = dict((v, 10 * k) for k, v in enumerate(hues))
def parse_hue(hue):
    """Parse a hue name into a float from 0 to 100."""
    for i, v in enumerate(hue):
        if v.isalpha():
            return float(hue[:i]) + hues[hue[i:]]

def parse(lines):
    def parse_one(line):
        ans = line.split()
        ans[0] = parse_hue(ans[0])
        for i, v in enumerate(ans[1:]):
            ans[i + 1] = float(v)
        return ans
    return [parse_one(line) for line in lines[1:]]

def xyy_to_rgb_linear(x, y, y2):
    if abs(y) < 1e-100:
        y = 1e-100
    y2 /= 100
    x2 = y2 * x / y
    z2 = y2 * (1 - x - y) / y
    return (3.2406 * x2 - 1.5372 * y2 - 0.4986 * z2,
        -0.9689 * x2 + 1.8758 * y2 + 0.0415 * z2,
        0.0557 * x2 - 0.2040 * y2 + 1.0570 * z2)

def rgb_delinearize(*rgb):
    ans = [0, 0, 0]
    for i, c in enumerate(rgb):
        if c <= 0.0031308:
            ans[i] = 12.92 * c
        else:
            ans[i] = 1.055 * math.pow(c, 1/2.4) - 0.055
    return ans

def hls_to_hlc(h, l, s):
    return h, l, s * (1 - abs(2 * l - 1))

def process():
    entries = parse(load())
    for entry in entries:
        entry[-3:] = rgb_delinearize(*xyy_to_rgb_linear(*entry[-3:]))
    c = [[[[0,0,0] for i in range(25)] for j in range(14)] for k in range(40)]
    for entry in entries:
        c[round(entry[0] * 0.4 - 1)][
            round((entry[1] > 1) and (entry[1] + 3) or (entry[1] * 5 - 1))
            ][round(entry[2]/2 - 1)] = entry[-3:]
    return c

def prettify(c):
    return '[\n%s\n]' % ',\n'.join([
        '[\n%s\n]' % ',\n'.join([
            ' [%s]' % ','.join([
                '[%s]' % ','.join([
                    ((w == 0) and '0' or ('%.5f' % w)) for w in z])
                for z in y])
            for y in x])
        for x in c])

def main():
    fetch()
    print('var Munsell =', prettify(process()))

if __name__ == '__main__':
    main()

