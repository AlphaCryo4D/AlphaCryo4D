#!/bin/env python

import os
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--folder', '-f', type=str, default='./maps_aligned/',
                        help='folder of maps')
    parser.add_argument('--stars', '-a', type=str, default='./star/',
                        help='path of starfiles')
    parser.add_argument('--std', '-s', type=bool, default=True,
                        help='if standardize the maps')


    parser.add_argument('--epoch', '-e', type=int, default=50,
                        help='training epochs')
    parser.add_argument('--batchsizetrain', '-b', type=int, default=8,
                        help='training batch size')
    parser.add_argument('--validationsize', '-v', type=int, default=800,
                        help='size of validation data when training')
    parser.add_argument('--regularization', '-r', type=float, default=0,
                        help='L2 regularization coefficient when training')
    parser.add_argument('--gpu', '-g', type=str, default="0,1,2,3",
                        help='gpu utilization')

    parser.add_argument('--batchsizepredict', '-B', type=int, default=8,
                    help='predicting batch size')



    parser.add_argument('--seed', '-S', type=int, default=0,
                        help='random seed of t-SNE')
    parser.add_argument('--perplexity', '-p', type=float, default=30.0,
                        help='perplexity of t-SNE')
    parser.add_argument('--niter', '-N', type=int, default=1000,
                        help='maximum number of iterations in t-SNE')
    parser.add_argument('--outputtsne', '-o', type=str, default='output.npy',
                        help='output of t-SNE')

    parser.add_argument('--landscape', '-l', type=str, default='output.npy',
                        help='free energy landscape points mapping by t-sne')
    parser.add_argument('--number', '-n', type=str, default='num.txt',
                        help='particle number file')
    parser.add_argument('--range', '-G', type=float, default=100.0,
                        help='maximum value of the reaction coordinate of free energy landscape')
    parser.add_argument('--start', '-A', nargs='+', type=float, default=[-80.0, -80.0],
                        help='position around start point of transition path')
    parser.add_argument('--end', '-E', nargs='+', type=float, default=[80.0, 80.0],
                        help='position around end point of transition path')
    parser.add_argument('--stepmax', '-m', type=int, default=100000,
                        help='maximum steps in String method algorithm')
    parser.add_argument('--stepsize', '-i', type=float, default=1e-1,
                        help='step size in String method algorithm')
    parser.add_argument('--tolerance', '-t', type=float, default=1e-7,
                        help='convergence condition in String method algorithm')
    parser.add_argument('--interpolate', '-I', type=str, default='linear',
                        help='interplotion method used in free energy landscape plotting, linear or cubic')
    parser.add_argument('--kcenters', '-k', type=int, default=20,
                        help='k clustering centers along transition path')



    parser.add_argument('--radius', '-u', type=float, default=30.0,
                        help='clustering radius along transition path')

    args = parser.parse_args()

    DIR = sys.path[0]
    CUR = os.getcwd()

    x1 = 'python ' + str(DIR) + '/Resample/bigdata.py --folder ' + str(args.folder) + ' --std ' + str(args.std)
    os.system(x1)
    x71 = 'cp ' + str(DIR) + '/ManifoldLandscape/enumerate.sh .'
    os.system(x71)
    x72 = 'sed -i "s#stars#' + str(args.stars) +'#g" enumerate.sh'
    os.system(x72)
    x73 = 'sh enumerate.sh'
    os.system(x73)

    if not os.path.exists('Deep/'):
        os.mkdir('Deep/')
    os.chdir(str(CUR) + '/Deep/')

    x2 = 'python ' + str(DIR) + '/DeepFeature/run_prepare.py --data ../rdata_3d.npy'
    os.system(x2)
    x3 = 'python ' + str(DIR) + '/DeepFeature/run_resnet.py --data data_dl.npy --epoch ' + str(args.epoch) + ' --batchsize ' + str(args.batchsizetrain) + ' --validationsize ' + str(args.validationsize) + ' -r ' + str(args.regularization) + ' --gpu ' + str(args.gpu)
    os.system(x3)
    x4 = 'python ' + str(DIR) + '/DeepFeature/run_predict.py --data data_dl.npy --batchsize ' + str(args.batchsizepredict)
    os.system(x4)

    os.chdir(str(CUR))


    if not os.path.exists('Manifold/'):
        os.mkdir('Manifold/')
    os.chdir(str(CUR) + '/Manifold/')

    x5 = 'python ' + str(DIR) + '/ManifoldLandscape/tsne_prepare.py --data ../rdata.npy --feature ../Deep/result/feature.npy'
    os.system(x5)
    x61 = 'python ' + str(DIR) + '/ManifoldLandscape/tsne_rd.py --input input.npy -s ' + str(args.seed) + ' --perplexity ' + str(args.perplexity) + ' --niter ' + str(args.niter) + ' --output ' + str(args.outputtsne) 
    os.system(x61)
    x62 = 'cp ' + str(args.outputtsne) + ' ..'
    os.system(x62)

    os.chdir(str(CUR))
    x8 = 'python ' + str(DIR) + '/ManifoldLandscape/string_method.py --landscape ' + str(args.landscape) +' --number ' + str(args.number) + ' --range ' + str(args.range) + ' --start ' + ' '.join([str(x) for x in args.start]) + ' --end ' + ' '.join([str(x) for x in args.end]) + ' --stepmax ' + str(args.stepmax) +' --stepsize '+ str(args.stepsize) + ' --tolerance '+ str(args.tolerance) + ' --interpolate ' + str(args.interpolate) + ' --kcenters ' + str(args.kcenters)
    os.system(x8)


    if not os.path.exists('Vote/'):
        os.mkdir('Vote/')
    os.chdir(str(CUR) + '/Vote/')

    x9 = 'python ' + str(DIR) + '/ParticleVoting/clustering.py --points ../' + str(args.landscape) + ' --centers ../centers_k.npy --radius ' + str(args.radius)
    os.system(x9)




