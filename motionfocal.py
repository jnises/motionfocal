#!/usr/bin/env python

from numpy import *
from PIL import Image
import os
import os.path
import re
from scipy.ndimage import interpolation
import logging
import multiprocessing as mp

logging.basicConfig(level = logging.INFO)

def _shift_image(image, offset):
    return interpolation.shift(image, (0, offset, 0), mode = 'nearest')

def compose(images, offset, scale = 1.0):
    '''
    images: asyncresults of images
    TODO might want to linearize the input images before composition
    '''
    firstimage = images[0].get()
    out = zeros(firstimage.shape)
    shifted = [pool.apply_async(_shift_image, [image.get(), (len(images) * 0.5 - inum) * offset]) for inum, image in enumerate(images)]
    for inum, image in enumerate(shifted):
        logging.info('processing image %d', inum)
        out += image.get()
    out /= len(images)
    out *= scale
    out[out > 255] = 255
    out[out < 0] = 0
    return Image.fromarray(out.astype(uint8))


def _load_image(image):
    logging.info('loading image %s', image)
    return asarray(Image.open(image))


def load_images(images):
    '''
    load images using processpool
    retuns a list of asyncresults
    '''
    return [pool.apply_async(_load_image, [image]) for image in images]


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


pool = mp.Pool()

if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description = 'utility for generating images with short focal depth using multiple images')
    parser.add_argument('--input', help = 'the base path of the frames would be asdf if you have frames named like asdf001.png', required = True)
    parser.add_argument('--offset', default = 1, help = 'how much to offset each image. should be negative if things are going right to left')
    parser.add_argument('--output', required = True, help = 'the output filename')
    parser.add_argument('--begin', help = 'the number of the first frame')
    parser.add_argument('--end', help = 'the number of the frame after the last')
    parser.add_argument('--brightness', default = 1, help = 'scale the output using this value before qunatizing to 8 bit')
    args = parser.parse_args()
    files = file_list(args.input, int(args.begin) if args.begin else None, int(args.end) if args.end else None)
    logging.info('will compose using the files %s', files)
    compose(load_images(files), float(args.offset), float(args.brightness)).save(args.output)
