#!/bin/env python

import os
import argparse
import sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--classes', '-c', type=str, default="c1_small",
                        help='classes to vote')
    parser.add_argument('--head', '-he', type=str, default="head.star",
                        help='head of star file')
    parser.add_argument('--relion', '-r', type=int, default=2,
                        help='relion version')
    parser.add_argument('--threshold', '-t', type=int, default=2,
                        help='threshold for voting')
    args = parser.parse_args()

    DIR = sys.path[0]
    CUR = os.getcwd()

    x11 = 'cp ' + str(DIR) + '/vote_prepare.sh . '
    os.system(x11)
    x12 = 'sed -i "s#data.log#../../data.log#g" vote_prepare.sh'
    os.system(x12)
    x13 = 'sed -i "s#your_path#../..#g" vote_prepare.sh'
    os.system(x13)
    x14 = 'sh vote_prepare.sh ' + str(args.classes)
    os.system(x14)

    for f in os.listdir('./'):
        if f[-4:] == 'star':
            star=f
            break
    x2 = 'python ' + str(DIR) + '/gethead.py --star ' + str(star) + ' --relion ' + str(args.relion)
    os.system(x2)

    x31 = 'cp ' + str(DIR) + '/post_and_f.sh .'
    os.system(x31)
    x32 = 'sed -i "s#th=2#th=' + str(args.threshold) + '#g" post_and_f.sh'
    os.system(x32)
    x33 = 'sh post_and_f.sh'
    os.system(x33)

