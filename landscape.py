#!/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy import interpolate
from scipy import integrate

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--landscape', '-l', type=str, default='output.npy',
                        help='free energy landscape mapping by t-sne')
    parser.add_argument('--number', '-n', type=str, default='num.txt',
                        help='particle number file')
    parser.add_argument('--range', '-r', type=float, default=[-30,30,-45,20],
                        help='maximum value of the reaction coordinate of free energy landscape')
    parser.add_argument('--start', '-s', nargs='+', type=float, default=[-9.5, -7.7],
                        help='position around start point of transition path')
    parser.add_argument('--end', '-e', nargs='+', type=float, default=[7.0, -5.0],
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
    args = parser.parse_args()

    # free energy landscape and one transition path

    # initialize
    l=args.range
    x=np.linspace(args.start[0], args.end[0], 500)
    y=np.linspace(args.start[1], args.end[1], 500)
    grid_x, grid_y = np.mgrid[l[0]:l[1]:1000j, l[2]:l[3]:1000j]   # about from (-80,-80) to (80,80)
    print("range of free energy landscape: (" + str(l) + ")")
    print("initial transition path: from (" + str(x[0]) + "," + str(y[0]) + ") to (" + str(x[-1]) + "," + str(y[-1]) + ")")

    n1 = len(x)
    g1 = np.linspace(0,1,n1)
    dx = x-np.roll(x,1)
    dy = y-np.roll(y,1)
    dx[0] = 0
    dy[0] = 0
    lxy = np.cumsum(np.sqrt(dx**2+dy**2))
    lxy = lxy/lxy[-1]
    fx = interpolate.interp1d(lxy,x)
    xi = fx(g1)
    fy = interpolate.interp1d(lxy,y)
    yi = fy(g1)

    #hyper-parameters
    nstepmax = args.stepmax
    h = args.stepsize
    tol1 = args.tolerance
    d = 1e-5

    #free energy landscape
    k=1
    T=1
    x1 = np.load(args.landscape)
    z = np.loadtxt(args.number)

    sum_z = np.sum(z)
    z = z/sum_z
    g = -k*T*np.log(z)
    x2 = x1[0:,:]   # start from volume 0 to end
    if args.interpolate=='linear':
        Hfunc = interpolate.LinearNDInterpolator(x2, g)
    elif args.interpolate=='cubic':
        Hfunc = interpolate.CloughTocher2DInterpolator(x2, g)

    grid_z = Hfunc(grid_x, grid_y)

    '''
    # Main loop
    for nstep in range(nstepmax):

    # calculation of the x and y-components of the force, dVx and dVy respectively
        dVx=(Hfunc(xi+d,yi)-Hfunc(xi-d,yi))/(2*d)
        dVy=(Hfunc(xi,yi+d)-Hfunc(xi,yi-d))/(2*d)
        print("dV: ", np.mean(np.sqrt(dVx**2+dVy**2)))

        x0 = xi
        y0 = yi

    # string steps:
    # 1. evolve
        xi = xi - h*dVx
        yi = yi - h*dVy

    # 2. reparametrize
        dx = xi-np.roll(xi,1)
        dy = yi-np.roll(yi,1)
        print("dl: ", np.mean(np.sqrt(dx**2+dy**2)))
        dx[0] = 0
        dy[0] = 0
        lxy = np.cumsum(np.sqrt(dx**2+dy**2))
        lxy = lxy/lxy[-1]

        fx = interpolate.interp1d(lxy,xi)
        xi=fx(g1)
        fy = interpolate.interp1d(lxy,yi)
        yi=fy(g1)

        tol = (np.linalg.norm(xi-x0)+np.linalg.norm(yi-y0))/n1;
        print("tol:", tol)

        if tol <= tol1:
            break
    '''
    
    # results
    plt.figure(figsize=(5,5))
    plt.imshow(grid_z.T,extent=l,origin="lower",cmap=plt.cm.Spectral_r)
    plt.colorbar()

    plt.scatter(x2[:,0],x2[:,1],c='g',s=z*100)
    #plt.scatter(xi,yi,s=0.1,color='y')
    for i in np.arange(x2.shape[0]):
        plt.annotate(i+1,(x2[i,0],x2[i,1]),fontsize=1)

    plt.savefig('el.pdf',format='pdf')
    plt.show()

    '''
    print('String method calculation with %d images\n' % n1)
    if tol > tol1:
        print('The calculation failed to converge after %d iterations\n' % nstep)
    else:
        print('The calculation terminated after %d iterations\n' % nstep)

    # uniform clustering
    K=args.kcenters
    index = np.linspace(0, n1-1, K).astype('int')
    print('centers of x: ' + str(xi[index]))
    print('centers of y: ' + str(yi[index]))
    centers=np.hstack((xi[index].reshape((-1,1)),yi[index].reshape(-1,1)))
    np.save('centers_k.npy', centers)
    '''
