#!/bin/env python

import time
import argparse
from sklearn.preprocessing import StandardScaler
import numpy as np

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', '-d', type=str, default='rdata.npy',
                        help='raw data')
    parser.add_argument('--feature', '-f', type=str, default='result/feature.npy',
                        help='deep feature')
    parser.add_argument('--std', '-s', type=bool, default=True,
                        help='if standardize the deep feature')
    args = parser.parse_args()

    starttime=time.time()

    data_d = np.load(args.feature, mmap_mode='r')
    if args.std:
        data_d = data_d.reshape((-1, data_d.shape[0]))
        scaler_d = StandardScaler().fit(data_d)
        data_d = scaler_d.transform(data_d)
        data_d = data_d.reshape((data_d.shape[-1],-1))
    else:
        data_d = data_d.reshape((data_d.shape[0],-1))

    data_r = np.load(args.data, mmap_mode='r')
    data_r = data_r.reshape((data_r.shape[0],-1))
    print('shape of feature: ' + str(data_d.shape))
    print('shape of data: ' + str(data_r.shape))

    data_t = np.memmap('input.dat', dtype='float32', mode='w+', shape=(data_d.shape[0], data_r.shape[1]+data_d.shape[1]))
    data_t = np.hstack((data_r, data_d))
    print('shape of t-SNE input: ' + str(data_t.shape))
    np.save("input.npy", data_t)

    endtime=time.time()
    print('time spent: ', endtime-starttime)
