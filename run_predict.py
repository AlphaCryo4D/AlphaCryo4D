#!/bin/env python

import os
from keras.models import load_model, Model
import argparse
import numpy as np
np.random.seed(33)  # for reproducibility

parser = argparse.ArgumentParser()
parser.add_argument('--data', '-d', type=str, default="data_dl.npy",
                    help='input 3D data')
parser.add_argument('--model', '-m', type=str, default='checkpoint/check.h5',
                    help='model of network for feature extraction')
parser.add_argument('--batchsize', '-b', type=int, default=8,
                    help='batch size')
parser.add_argument('--feature', '-f', type=str, default='result/feature.npy',
                    help='output of feature engineering')
args = parser.parse_args()

DATA_SIZE = np.load(args.data, mmap_mode='r').shape[1]
BATCH_SIZE = args.batchsize

def feature():
    from run_resnet import resnet
    dm=resnet()
    dm.load_weights(args.model, by_name=True)
    dm.summary()
    em = Model(inputs=dm.input, outputs=dm.get_layer('encoded').output)
    print('model loaded')

    data = np.load(args.data, mmap_mode='r')
    data = data.reshape((data.shape[0], DATA_SIZE, DATA_SIZE, DATA_SIZE, 1))
    encode = em.predict(data, batch_size = BATCH_SIZE)
    print('shape of encoded:' + str(encode.shape))

    if args.feature == 'result/feature.npy' and not os.path.exists('result/'):
        os.mkdir('result/')
    np.save(args.feature, encode)
    print('results saved')

if __name__ == '__main__':
    feature()
