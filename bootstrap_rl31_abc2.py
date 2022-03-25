#!/bin/env python

import numpy as np
import argparse
import linecache

def subid(num_sub):
    return chr(num_sub+64) if num_sub<27 else chr(num_sub+70)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    np.random.seed(0)

    # origin dataset
    parser.add_argument('--star', '-s', type=str, default='batch1.star',
                        help='starfile of a batch of dataset')
    parser.add_argument('--fold', '-f', type=int, default=3,
                        help='fold of data augmentation')
    parser.add_argument('--num_sub', '-n', type=int, default=10,
                        help='number of subset')
    args = parser.parse_args()

    filename=args.star
    fold=args.fold#+1
    num_sub=args.num_sub

    x=0 # lines of head
    r=0 # remaining lines in starfile
    head=True
    after_optic=False
    # compute total particle number
    count=0
    for count, line in enumerate(open(filename, 'r')):
        if line.startswith('data_particles'):
            after_optic=True
            x+=1
        elif not after_optic and head:
            x+=1
        elif len(line.split(' '))<=3 and head:
            x+=1
        else:
            head=False
        if len(line.split(' ')) <= 3 or not after_optic:
            r+=1
        count += 1
    num=int((count-r)/num_sub)
    print('number of particles per subset: ',num) # number of particles

    print('start augmenting particles...')
    order=np.random.permutation(range(x+1,count-r+x+1))
    for i in range(1,num_sub+1):
        f=open("sub" + subid(i) + ".star",'a')
        for j in range(1,x+1):
            line=linecache.getline(filename,j)
            f.write(line)
        if i<num_sub:
            for j in range(1,num+1):
                l=(i-1)*num+j
                line=linecache.getline(filename,order[l-1])
                f.write(line)
        else:
            for j in range(1,num+1+count-r-num*num_sub):
                l=(i-1)*num+j
                line=linecache.getline(filename,order[l-1])
                f.write(line)
        f.close()

    '''
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
    '''
    
    l_ = [subid(a) for a in range(1, num_sub+1)]
    for i in range(1,num_sub+1):
        u=''.join('%s' % id for id in l_)
        if i <= fold + 1:
            for j in range(i, num_sub-fold+i):
                u=u.replace(subid(j),'')
        else:
            for j in range(i, num_sub+1):
                u=u.replace(subid(j),'')
            for j in range(1, i-fold):
                u=u.replace(subid(j),'')
        f=open("union" + str(u) + ".star",'a')
        for j in range(1,x+1):
            line=linecache.getline(filename,j)
            f.write(line)
        for s in list(u):
            if s<list(u)[-1]:
                for j in range(x+1,x+num+1):
                    line=linecache.getline("sub" + s + ".star",j)
                    f.write(line)
            else:
                for j in range(x+1,x+num+1+count-r-num*num_sub):
                    line=linecache.getline("sub" + s + ".star",j)
                    f.write(line)
        f.close()
    print('starfile resampling done')
