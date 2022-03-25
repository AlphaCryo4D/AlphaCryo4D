#!/bin/env python

from __future__ import division
import tensorflow as tf
from keras.layers import Input
from keras.layers import Conv3D, MaxPool3D, Dense, BatchNormalization, Activation, add, Conv3DTranspose, UpSampling3D
from keras.models import Model
from keras import regularizers
from keras.utils import multi_gpu_model
from keras.callbacks import ModelCheckpoint, TensorBoard, LearningRateScheduler, ReduceLROnPlateau
from keras import backend as K
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
os.environ['KERAS_BACKEND'] = 'tensorflow'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
np.random.seed(33)   # random seed to reproduce results

parser = argparse.ArgumentParser()
parser.add_argument('--epoch', '-e', type=int, default=80,
                    help='epochs')
parser.add_argument('--batchsize', '-b', type=int, default=8,
                    help='batch size')
parser.add_argument('--validationsize', '-v', type=int, default=80,
                    help='size of validation data')
parser.add_argument('--regularization', '-r', type=float, default=0,
                    help='L2 regularization coefficient')
parser.add_argument('--data', '-d', type=str, default="data_dl.npy",
                    help='input 3D data')
parser.add_argument('--checkpoint', '-c', type=str, default="checkpoint/check.h5",
                    help='path of best model')
parser.add_argument('--finalmodel', '-f', type=str, default="model/final_model.h5",
                    help='path of final model')
parser.add_argument('--gpu', '-g', type=str, default="0,1,2,3,4,5,6,7",
                    help='gpu utilization')
args = parser.parse_args()

os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
#os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"

GN=len(args.gpu.split(','))
EPOCHS = args.epoch
BATCH_SIZE = args.batchsize
VAL_SIZE = args.validationsize
REG_COFF = args.regularization
DATA_SIZE = np.load(args.data, mmap_mode='r').shape[1]

def conv3d_bn(x, nb_filter, kernel_size, strides=(1, 1, 1), padding='same', name=None):
    """
    conv3d -> batch normalization -> relu activation
    """
    x = Conv3D(nb_filter, kernel_size=kernel_size,
                          strides=strides,
                          padding=padding,
                          kernel_regularizer = regularizers.l2(REG_COFF), bias_regularizer = regularizers.l2(REG_COFF))(x)
    x = BatchNormalization()(x)
    x = Activation('relu', name=name)(x)
    return x

def transpose_conv3d_bn(x, nb_filter, kernel_size, strides=(1, 1, 1), padding='same'):
    """
    transpose_conv3d -> batch normalization -> relu activation
    """
    x = Conv3DTranspose(nb_filter, kernel_size=kernel_size,
                          strides=strides,
                          padding=padding,
                          kernel_regularizer = regularizers.l2(REG_COFF), bias_regularizer = regularizers.l2(REG_COFF))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    return x

def shortcut(input, residual, name=None):
    """
    short cut
    """
    input_shape = K.int_shape(input)
    residual_shape = K.int_shape(residual)
    stride_height = int(round(input_shape[1] / residual_shape[1]))
    stride_width = int(round(input_shape[2] / residual_shape[2]))
    stride_length = int(round(input_shape[3] / residual_shape[3]))
    equal_channels = input_shape[4] == residual_shape[4]

    identity = input

    if stride_width > 1 or stride_height > 1 or stride_length > 1 or not equal_channels:
        identity = Conv3D(filters=residual_shape[4],
                           kernel_size=(1, 1, 1),
                           strides=(stride_width, stride_height, stride_length),
                           padding="valid",
                           kernel_regularizer = regularizers.l2(REG_COFF), bias_regularizer = regularizers.l2(REG_COFF))(input)

    return add([identity, residual], name=name)

def transpose_shortcut(input, residual, name=None):
    """
    transpose short cut
    """
    input_shape = K.int_shape(input)
    residual_shape = K.int_shape(residual)
    stride_height = int(round(residual_shape[1] / input_shape[1]))
    stride_width = int(round(residual_shape[2] / input_shape[2]))
    stride_length = int(round(residual_shape[3] / input_shape[3]))
    equal_channels = input_shape[4] == residual_shape[4]

    identity = input

    if stride_width > 1 or stride_height > 1 or stride_length > 1 or not equal_channels:
        identity = Conv3DTranspose(filters=residual_shape[4],
                           kernel_size=(1, 1, 1),
                           strides=(stride_width, stride_height, stride_length),
                           padding="valid",
                           kernel_regularizer = regularizers.l2(REG_COFF), bias_regularizer = regularizers.l2(REG_COFF))(input)

    return add([identity, residual], name=name)

def residual_block(nb_filter, strides=(1, 1, 1), name=None):
    """
    ResNet building block
    """
    def f(input):

        conv1 = conv3d_bn(input, nb_filter, kernel_size=(3, 3, 3), strides=strides)
        residual = conv3d_bn(conv1, nb_filter, kernel_size=(3, 3, 3))

        return shortcut(input, residual, name=name)

    return f

def transpose_residual_block(nb_filter, strides=(1, 1, 1), name=None):
    """
    ResNet building block (transpose)
    """
    def f(input):

        conv1 = transpose_conv3d_bn(input, nb_filter, kernel_size=(3, 3, 3), strides=strides)
        residual = transpose_conv3d_bn(conv1, nb_filter, kernel_size=(3, 3, 3))

        return transpose_shortcut(input, residual,name=name)

    return f

def block(nb_filter, repetitions, bin2=True, name=None):
    """
    conv3d_x -> encoded
    """
    def f(input):
        for i in range(repetitions-1):
            strides = (1, 1, 1)
            if i == 0 and bin2:
                strides = (2, 2, 2)
            input = residual_block(nb_filter, strides)(input)
        strides = (1, 1, 1)
        if repetitions-1 == 0 and bin2:
            strides = (2, 2, 2)
        input = residual_block(nb_filter, strides, name=name)(input)
        return input

    return f

def transpose_block(nb_filter, repetitions, bin2=True, name=None):
    """
    transpose_conv3d_x -> decoded
    """
    def f(input):
        for i in range(repetitions-1):
            strides = (1, 1, 1)
            if i == 0 and bin2:
                strides = (2, 2, 2)
            input = transpose_residual_block(nb_filter, strides)(input)
        strides = (1, 1, 1)
        if repetitions-1 == 0 and bin2:
            strides = (2, 2, 2)
        input = transpose_residual_block(nb_filter, strides, name=name)(input)
        return input

    return f

def resnet(input_shape=(DATA_SIZE, DATA_SIZE, DATA_SIZE, 1)):
    input_ = Input(shape=input_shape, name='input')

    conv1 = conv3d_bn(input_, 2, kernel_size=(5, 5, 5), strides=(1, 1, 1), name='conv1')

    rb2 = block(2, 2, bin2=True, name='rb2')(conv1)
    rb3 = block(1, 2, bin2=True, name='rb3')(rb2)

    encoded = block(1, 1, bin2=False, name='encoded')(rb3)

    trb5 = transpose_block(1, 2, bin2=True, name='trb5')(encoded)
    trb6 = transpose_block(2, 2, bin2=True, name='trb6')(trb5)

    tconv7 = BatchNormalization(name='tconv7')(Conv3DTranspose(1, (5, 5, 5), strides = (1, 1, 1), kernel_regularizer = regularizers.l2(REG_COFF), bias_regularizer = regularizers.l2(REG_COFF), padding='same')(trb6))

    output_ = Activation('sigmoid', name='decoded')(tconv7)

    autoencoder = Model(inputs=input_, outputs=output_)
    autoencoder.summary()

    return autoencoder

def minibatch(inputs=None, targets=None, batch_size=None, shuffle=False):
    while 1:
        assert len(inputs) == len(targets)
        if shuffle:
            indices = np.arange(len(inputs))
            np.random.shuffle(indices)
        for start_idx in range(0, len(inputs) - batch_size + 1, batch_size):
            if shuffle:
                excerpt = indices[start_idx:start_idx + batch_size]
            else:
                excerpt = slice(start_idx, start_idx + batch_size)
            yield inputs[excerpt], targets[excerpt]

def train(x_train):
    assert VAL_SIZE % BATCH_SIZE == 0, 'validation size should be multiple of batch size'
    with tf.device("/cpu:0"):
        autoencoder = resnet()
    parallel_ae = multi_gpu_model(autoencoder, gpus=GN)

    # compile autoencoder
    parallel_ae.compile(optimizer='adam', loss='mean_squared_error')

    #training
    checkpoint_foldpath = './checkpoint/'
    if args.checkpoint == "checkpoint/check.h5" and not os.path.exists(checkpoint_foldpath):
        os.mkdir(checkpoint_foldpath)
    checkpoint = ModelCheckpoint(args.checkpoint,
                                 monitor='val_loss', save_weights_only=True, verbose=1, save_best_only=True, period=1)
    if os.path.exists(args.checkpoint):
        parallel_ae.load_weights(args.checkpoint)
        print('checkpoint loaded, continuing...')
    #tb = TensorBoard(log_dir='log', histogram_freq=1)
    reduce_lr = ReduceLROnPlateau(monitor='loss', patience=3, mode='auto', verbose=1)
    callback_lists = [checkpoint, reduce_lr]

    # need return history
    model_foldpath = './model/'
    if args.finalmodel == 'model/final_model.h5' and not os.path.exists(model_foldpath):
        os.mkdir(model_foldpath)
    if os.path.exists(args.finalmodel):
        os.remove(args.finalmodel)
        print('old model file deleted')
    history_record = parallel_ae.fit_generator(minibatch(x_train, x_train, batch_size=BATCH_SIZE, shuffle=True), epochs=EPOCHS, validation_data=(x_train[:VAL_SIZE], x_train[:VAL_SIZE]), steps_per_epoch=len(x_train) // BATCH_SIZE, shuffle=True, callbacks=callback_lists)
    autoencoder.save(args.finalmodel)
    return parallel_ae, history_record


def plot_accuray(history_record):
    """
    plot the accuracy/loss line
    """
    loss = history_record.history["loss"]
    epochs = range(len(loss))
    np.savez('train_process.npz', epochs=epochs, loss=loss)
    plt.figure()
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.title('Training loss')
    plt.legend()
    plt.show()

def main():
    x_train = np.load(args.data, mmap_mode='r')
    # Step3: reshape data, x_train: (252, 300, 300, 300, 1), one row denotes one sample.
    x_train = x_train.reshape((x_train.shape[0], DATA_SIZE, DATA_SIZE, DATA_SIZE, 1))
    print('shape of data: ', x_train.shape)

    # Step4: train
    autoencoder, history_record = train(x_train=x_train)

    # show train process
    plot_accuray(history_record)

if __name__ == '__main__':
    main()
