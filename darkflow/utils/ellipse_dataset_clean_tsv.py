"""
parse PASCAL VOC xml annotations
"""

import os
import sys
import numpy as np
import xml.etree.ElementTree as ET
import glob


def _pp(l):  # pretty printing
    for i in l: print('{}: {}'.format(i, l[i]))


def ellipse_dataset_tsv(ANN, pick, exclusive=False):
    print('Parsing for {} {}'.format(
        pick, 'exclusively' * int(exclusive)))

    dumps = list()
    cur_dir = os.getcwd()
    os.chdir(ANN)

    annotations = ANN + '/dataset.txt'



    with open(annotations, 'r') as f:
        lines =  f.readlines()
        size = len(lines)
        for i, line in enumerate(lines):
            # progress bar
            sys.stdout.write('\r')
            percentage = 1. * (i + 1) / size
            progress = int(percentage * 20)
            bar_arg = [progress * '=', ' ' * (19 - progress), percentage * 100]

            sys.stdout.write('[{}>{}]{:.0f}% '.format(*bar_arg))
            sys.stdout.flush()

            # actual parsing
            jpg, xc, yc, a,b,angle = line.split('\t')
            xc = int(xc)
            yc = int(yc)
            a = int(a)
            b = int(b)
            angle = int(angle)

            w = 648
            h = 432
            all = list()


            r =  np.max((a,b))
            xn = int(xc - r * np.cos(np.pi / 180 * angle))
            xx = int(xc +  r * np.cos(np.pi / 180 * angle))

            yn = int(yc - r * np.sin(np.pi / 180 * angle))
            yx = int(yc +  r * np.sin(np.pi / 180 * angle))

            current = [xn, yn, xx, yx, angle]
            all += [current]

            add = [[jpg, [w, h, all]]]
            dumps += add


    # gather all stats
    stat = dict()
    for dump in dumps:
        all = dump[1][2]
        for current in all:
            if current[0] in pick:
                if current[0] in stat:
                    stat[current[0]] += 1
                else:
                    stat[current[0]] = 1

    print('\nStatistics:')
    _pp(stat)
    print('Dataset size: {}'.format(len(dumps)))

    os.chdir(cur_dir)
    return dumps