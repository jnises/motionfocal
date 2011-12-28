#!/usr/bin/env python

from numpy import *
from PIL import Image
import argparse
import os
import os.path
import re
from scipy.ndimage import interpolation
import logging

logging.basicConfig(level = logging.INFO)

def compose(images, offset):
    '''
    TODO might want to linearize the input images before composition
    '''
    firstimage = asarray(Image.open(images[0]))
    out = zeros(firstimage.shape)
    firstimage = None
    for inum, image in enumerate(images):
        logging.info('loading image %s', image)
        img = asarray(Image.open(image))
        imgoffset = (len(images) * 0.5 - inum) * offset
        out += interpolation.shift(img, (0, imgoffset, 0), mode = 'nearest')
    out /= len(images)
    return Image.fromarray(out.astype(uint8))


def file_list(basepath, begin = None, end = None):
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
            if begin is None or num >= begin:
                inrange.append(match)
    return sort([os.path.join(directory, x.group(0)) for x in inrange])


if '__main__' == __name__:
    parser = argparse.ArgumentParser(description = 'utility for generating images with short focal depth using multiple images')
    parser.add_argument('--input', help = 'the base path of the frames would be asdf if you have frames named like asdf001.png', required = True)
    parser.add_argument('--offset', default = 1, help = 'how much to offset each image. should be negative if things are going right to left')
    parser.add_argument('--output', required = True, help = 'the output filename')
    parser.add_argument('--begin', help = 'the number of the first frame')
    parser.add_argument('--end', help = 'the number of the frame after the last')
    args = parser.parse_args()
    files = file_list(args.input, int(args.begin) if args.begin else None, int(args.end) if args.end else None)
    logging.info('will compose using the files %s', files)
    compose(files, float(args.offset)).save(args.output)
