#!/usr/bin/python3

import math
import urllib.request

data_url = 'http://www.cis.rit.edu/research/mcsl2/online/munsell_data/all.dat'
data_file = 'all.dat'

def fetch(url = data_url, fname = data_file, clobber = False):
    # If we're not clobbering the file, quit early if we can read it.
    if not clobber:
        try:
            with open(fname) as f:
                return
        except FileNotFoundError:
            pass
    # Fetch the data from the internet.
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

def average_triplets(triplets, ignore_nones = False):
    ans = [None, None, None]
    for i in range(3):
        filtered_values = list(filter(lambda x: x is not None, [t[i] for t in triplets]))
        num_values = len(filtered_values)
        if ((num_values != len(triplets)) and not ignore_nones) or num_values < 1:
            continue
        ans[i] = sum(filtered_values) / len(filtered_values)
    return ans

def process():
    entries = parse(load())
    for entry in entries:
        entry[-3:] = rgb_delinearize(*xyy_to_rgb_linear(*entry[-3:]))
    # Fill the table that our javascript will read.
    c = [[[[None,None,None] for k in range(27)] for j in range(16)] for i in range(40)]
    for entry in entries:
        c[round(entry[0] * 0.4 - 1)][
            round((entry[1] > 1) and (entry[1] + 4) or (entry[1] * 5))
            ][round(entry[2]/2)] = entry[-3:]
    # Insert grays (chroma = 0) by averaging diametric opposites.
    # The source of our data doesn't include grays, so we interpolate.
    for j in range(15):
        gray = average_triplets(
            [average_triplets([c[i][j][1], c[i+20][j][1]]) for i in range(20)],
            ignore_nones = True)
        for i in range(40):
            c[i][j][0] = gray
    # Insert black
    for i in range(40):
        for k in range(27):
            c[i][0][k] = [0, 0, 0]
    return c

def prettify(c):
    return '[\n%s\n]' % ',\n'.join([
        '[\n%s\n]' % ',\n'.join([
            ' [%s]' % ','.join([
                '[%s]' % ','.join([
                    ((w is None) and 'NaN' or ('%.5f' % w)) for w in z])
                for z in y])
            for y in x])
        for x in c])

def main():
    fetch()
    print('var Munsell =', prettify(process()))

if __name__ == '__main__':
    main()

