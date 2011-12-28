#!/usr/bin/env python

import numpy
from PIL import Image
import argparse
import os
import os.path
import re
from scipy.ndimage import interpolation

def compose(images, offset):
    firstimage = asarray(Image.open(images[0]))
    out = zeros_like(firstimage)
    firstimage = None
    for inum, image in enumerate(images):
        img = asarray(Image.open(image))
        imgoffset = (len(images) - inum) * offset
        out += interpolation.shift(img, (0, imgoffset, 0), mode = 'nearest')
    out /= len(images)
    return Image.fromarray(out)


def file_list(basepath, start = None, end = None):
    directory, filename = os.path.split(basepath)
    if 0 == len(directory):
        directory = '.'
    basere = re.compile(filename + r'(\d+)\.(\w*)$')
    files = os.listdir(directory)
    matches = [y for y in [basere.match(x) for x in files] if None != y]
    inrange = []
    for match in matches:
        num = int(match.group(1))
        if end is None or num < end:
            if start is None or num >= start:
                inrange.append(match)
    return inrange    


if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--offset', default = 1)
    parser.add_argument('--output')
    parser.add_argument('--start')
    parser.add_argument('--end')
    args = parser.parse_args()
    files = file_list(args.input, args.start, args.end)
    compose(files, args.offset).save(args.output)
