#!/bin/env python

import numpy as np
import argparse
import linecache

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    np.random.seed(0)

    # origin dataset
    parser.add_argument('--star', '-s', type=str, default='particles.star',
                        help='starfile of all particles')
    parser.add_argument('--number', '-n', type=int, default=100000,
                        help='particle number of each sub-dataset')

    args = parser.parse_args()
    filename=args.star

    n=args.number # particle number of each sub-dataset

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

    a=range(x+1,count-(r-x)+1)
    b=np.random.permutation(a) # random order of a
    d=dict(zip(a,b))
    num=int((count-r)/n)
    print('number of sub-datasets: ',num) # number of subset

    print('start splitting particles...')
    for i in range(1,num+1):
        f=open("batch" + str(i) + ".star",'a')
        for j in range(1,x+1):
            line=linecache.getline(filename,j)
            f.write(line)
        for j in range(x+1,x+n+1):
            l=d[(i-1)*n+j]
            line=linecache.getline(filename,l)
            f.write(line)
        f.close()

    if num*n != count-r:
        f=open("batch" + str(num+1) + "_extra.star",'a')
        for j in range(1,x+1):
            line=linecache.getline(filename,j)
            f.write(line)
        for k in range(x+num*n+1,count):
            line=linecache.getline(filename,d[k])
            f.write(line)
        f.close()
    print('starfile splitting done')
