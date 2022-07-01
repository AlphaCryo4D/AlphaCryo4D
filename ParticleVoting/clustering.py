#!/bin/env python
import numpy as np
import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--points', '-p', type=str, default="output.npy",
                        help='files of data points')
    parser.add_argument('--centers', '-c', type=str, default="centers_k.npy",
                        help='files of clustering centers')
    parser.add_argument('--radius', '-r', type=float, default=30.0,
                        help='clustering radius')
    args = parser.parse_args()

    x = np.load(args.points)
    x=x[0:] # from 0 to end
    c = np.load(args.centers)

    for n in range(c.shape[0]):
        if not os.path.exists('c' + str(n+1)):
            os.mkdir('c' + str(n+1))

    for i in range(x.shape[0]):
        print('item:' + str(i+1))
        dist=[]
        for n in range(c.shape[0]):
            dist.append([n, np.linalg.norm(x[i]-c[n])])
        dist=sorted(dist, key=lambda x:x[1])
        if dist[0][1]<args.radius:
            print(dist[0])
            for n in range(c.shape[0]):
                if dist[0][0] == n:
                    with open('c' + str(n+1) + '/c' + str(n+1), 'a') as f:
                        f.write(str(i+1) + " " + str(dist[0][1]) + "\n")

if __name__ == '__main__':
    main()
