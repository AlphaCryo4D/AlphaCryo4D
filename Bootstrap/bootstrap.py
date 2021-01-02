#!/bin/env python

import numpy as np
import argparse
import linecache

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    np.random.seed(0)

    # origin dataset
    parser.add_argument('--star', '-s', type=str, default='batch1.star',
                        help='starfile of a batch of dataset')
    parser.add_argument('--fold', '-f', type=int, default=3,
                        help='fold of data augmentation')
    args = parser.parse_args()

    filename=args.star
    fold=args.fold+1

    x=0 # lines of head
    r=0 # remaining lines in starfile
    head=True
    # compute total particle number
    count=0
    for count, line in enumerate(open(filename, 'r')):
        if len(line.split(' '))<=3 and head:
            x+=1
        else:
            head=False
        if len(line.split(' ')) <= 3:
            r+=1
        count += 1
    num=int((count-r)/fold)
    print('number of particles per fold: ',num) # number of particles

    print('start augmenting particles...')
    for i in range(1,fold+1):
        f=open("sub" + str(i) + ".star",'a')
        for j in range(1,x+1):
            line=linecache.getline(filename,j)
            f.write(line)
        for j in range(x+1,x+num+1):
            l=(i-1)*num+j
            line=linecache.getline(filename,l)
            f.write(line)
        f.close()

    if num*fold != count-r:
        f=open("sub" + str(fold+1) + "_extra.star",'a')
        for j in range(1,x+1):
            line=linecache.getline(filename,j)
            f.write(line)
        for k in range(x+num*fold+1,count):
            line=linecache.getline(filename,k)
            f.write(line)
        f.close()
    print('starfile splitting done')

    l_ = [a for a in range(1, fold+1)]
    for i in range(1,fold+1):
        u=''.join('%s' % id for id in l_).replace(str(i), '')
        f=open("union" + str(u) + ".star",'a')
        for j in range(1,x+1):
            line=linecache.getline(filename,j)
            f.write(line)
        for s in list(u):
            for j in range(x+1,x+num+1):
                line=linecache.getline("sub" + s + ".star",j)
                f.write(line)
        f.close()
    print('starfile resampling done')
