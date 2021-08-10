#!/bin/env python

import numpy as np
import argparse

def pre():
    # Step1: load data
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', '-d', type=str, default='rdata_3d.npy',
                        help='epochs')
    args = parser.parse_args()

    data = np.load(args.data, mmap_mode='r')
    print('shape of data:' + str(data.shape))

    x_train = np.memmap('data_dl.dat', dtype='float32', mode='w+', shape=(data.shape[0], data.shape[1], data.shape[2], data.shape[3]))
    x_train = data.copy()
    print('shape of training data:' + str(x_train.shape))

    # Step2: normalize
    print('data normalizing...')
    for i in range(x_train.shape[0]):
        x_train[i] = (x_train[i]-x_train.min())/(x_train.max()-x_train.min())

    np.save('data_dl.npy', x_train)
    print('preprocess done')

if __name__ == '__main__':
    pre()
