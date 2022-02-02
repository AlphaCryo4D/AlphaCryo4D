#!/bin/env python
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--star', '-s', type=str, default="u123_p1c1.star",
                        help='star file')
    parser.add_argument('--head', '-he', type=str, default="head.star",
                        help='head of star file')
    args = parser.parse_args()

    star = args.star
    h = args.head

    with open(star, mode='r') as fi:
        fo=open(h, mode='w')    
        while 1:
            l=fi.readline()
            if len(l.split(' ')) <= 3:
                #fo=open(h, mode='a')
                fo.write(l)
                #fo.close()
            else:
                fo.close()
                break

if __name__ == '__main__':
    main()
