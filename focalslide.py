#!/usr/bin/env python

import motionfocal as mf
from numpy import *
import logging
import multiprocessing as mp

if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description = 'generating multiple images with different focal points')
    parser.add_argument('--input', help = 'the base path of the frames would be asdf if you have frames named like asdf001.png', required = True)
    parser.add_argument('--begin-offset', dest = 'begin_offset', default = 0, help = 'the beginning of the offset range')
    parser.add_argument('--end-offset', dest = 'end_offset', default = 50, help = 'the end of the offset range')
    parser.add_argument('--output-frames', dest = 'output_frames', default = 10, help = 'the number of frames to output')
    parser.add_argument('--output', required = True, help = 'the output filename base. asdf will result in files like asdf001.png')
    parser.add_argument('--output-type', dest = 'output_type', default = 'png')
    parser.add_argument('--begin', help = 'the number of the first frame')
    parser.add_argument('--end', help = 'the number of the frame after the last')
    parser.add_argument('--brightness', default = 1, help = 'scale the output using this value before qunatizing to 8 bit')
    args = parser.parse_args()
    logging.info('operating using %d processes', mp.cpu_count())
    pool = mp.Pool()
    files = mf.file_list(args.input, int(args.begin) if args.begin else None, int(args.end) if args.end else None) 
    logging.info('will compose using the files %s', files)
    images = mf.load_images(pool, files)
    framedigits = int(ceil(log10(int(args.output_frames))))
    outtemplate = '%s%0' + str(framedigits) + 'd.%s'
    for i, offset in enumerate(linspace(float(args.begin_offset), float(args.end_offset), int(args.output_frames))):
        output = outtemplate % (args.output, i, args.output_type)
        logging.info('generating output image %s for offset %f', output, offset)
        
        mf.compose(pool, images, offset, float(args.brightness)).save(output)
        
