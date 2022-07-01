#!/bin/env python

import os
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--star', '-s', type=str, default='particles.star',
                        help='starfile of all particles')
    parser.add_argument('--number', '-n', type=int, default=100000,
                        help='particle number of each sub-dataset')
    parser.add_argument('--relion', '-r', type=int, default=2,
                        help='relion version')

    parser.add_argument('--fold', '-f', type=int, default=3,
                        help='fold of data augmentation')
    args = parser.parse_args()

    DIR = sys.path[0]
    CUR = os.getcwd()

    x1 = 'python ' + str(DIR) + '/randsf.py --star ' + str(args.star) + ' --number ' + str(args.number) + ' --relion ' + str(args.relion)
    os.system(x1)

    idx=1
    while 1:
        if os.path.exists('batch' + str(idx) + '.star'):
            if not os.path.exists('batch' + str(idx)):
                os.mkdir('batch' + str(idx))
            mv = 'mv batch' + str(idx) + '.star batch' + str(idx)
            os.system(mv)
            os.chdir(str(CUR) + '/batch' + str(idx))
            os.system('rm -f sub* union*')
            x2 = 'python ' + str(DIR) + '/resample.py --star ' + 'batch' + str(idx) + '.star --fold ' + str(args.fold) + ' --relion ' + str(args.relion)
            os.system(x2)
            os.chdir(str(CUR))
        else:
            break
        idx+=1

