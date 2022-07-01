#!/bin/env python
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--star', '-s', type=str, default="u123_p1c1.star",
                        help='star file')
    parser.add_argument('--head', '-he', type=str, default="head.star",
                        help='head of star file')
    parser.add_argument('--relion', '-r', type=int, default=2,
                        help='relion')
    args = parser.parse_args()
    
    lim=2
    star = args.star
    h = args.head

    with open(star, mode='r') as fi:
        fo=open(h, mode='w')
        head=True
        while 1:
            l=fi.readline()

            if args.relion>=3:
                if lim==2 and len(l.split(' ')) > 3:
                    lim-=1
                if lim==1 and len(l.split(' ')) <= 3:
                    lim-=1
                if lim==0 and len(l.split(' ')) > 3:
                    head=False

            elif args.relion==2:
                if lim==2 and len(l.split(' ')) > 3:
                    head=False

            if head:
                #fo=open(h, mode='a')
                fo.write(l)
                #fo.close()

            else:
                fo.close()
                break

if __name__ == '__main__':
    main()
