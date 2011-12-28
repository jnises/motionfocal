#!/usr/bin/env python

import motionfocal as mf
from numpy import *

if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description = 'generating multiple images with different focal points')
    parser.add_argument('--input', help = 'the base path of the frames would be asdf if you have frames named like asdf001.png', required = True)
    parser.add_argument('--begin-offset', default = 0, help = 'the beginning of the offset range')
    parser.add_argument('--end-offset', default = 50, help = 'the end of the offset range')
    parser.add_argument('--output-frames', default = 10, help = 'the number of frames to output')
    parser.add_argument('--output', required = True, help = 'the output filename base. asdf will result in files like asdf001.png')
    parser.add_argument('--output-type', default = 'png')
    parser.add_argument('--begin', help = 'the number of the first frame')
    parser.add_argument('--end', help = 'the number of the frame after the last')
    args = parser.parse_args()
    files = mf.file_list(args.input, int(args.begin) if args.begin else None, int(args.end) if args.end else None) 
    logging.info('will compose using the files %s', files)
    images = mf.load_images(files)
    framedigits = int(ceil(log10(args.output-frames)))
    outtemplate = '%s%0' + framedigits + 'd.%s'
    for i, offset in enumerate(linspace(args.begin-offset, args.end-offset, args.output-frames)):
        logging.info('generating output for offset %f', offset)
        mf.compose(images, offset).save(outtemplate % (args.output, i, args.output-type))
        
