# author: Furkan Cayci
# description: gradient descent implementation over 1 parameter

import numpy as np
from common import *
from lims_common import *
import logging

logging.basicConfig(level=logging.WARNING)

BOARDSIZE = (0.2, 0.4) # board size in meters (y, x)
NODESIZE = (11, 21)    # number of nodes in each direction (y, x)
trials = []            # array to hold trial numbers for each run
costs = []             # array to hold the costs for each run
backend = 'G'          # choose backend : LIMS or XXX

k = np.logspace(-14, -8, 100)

logging.warning('kxx values that are being tested:\n{}'.format(k))
logging.info('testing for {} values'.format(len(k)))

for r in range(len(k)):

    ### Create target flowfront
    c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)
    p_t = PMap(kxx=k[r])
    # randomize kxx over the given bounds
    #p_t.randomize(lower=1e-14, upper=1e-8)
    # set up the gates
    # w  : west
    # nw : north west
    # sw : south west
    gatenodes = set_gatenodes(NODESIZE, 'w')

    # calculate target flow time
    if backend == 'LIMS':
        ft_t = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)
    else:
        ft_t = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)

    # create trial parameters
    n_of_iters = 40000
    threshold = 0.1
    p = PMap(kxx=1e-12)
    pp = PMap(kxx=2e-12)

    gammax = 0.8 #* BOARDSIZE[1] / (NODESIZE[1]-1)

    cost = 0
    pcost = 0
    mcost = 0
    ncost = 0
    costs = []

    for t in range(n_of_iters):

        if backend == 'LIMS':
            ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)
        else:
            ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)

        pcost = cost
        cost = np.linalg.norm(ft_t - ft, 2)
        costs.append(cost)
        mcost = max(mcost, cost)
        ncost = abs(cost) / mcost

        print('{:5} '.format(t),end='')
        print('x: {:14.4e} '.format(p.kxx),end='')
        print('c: {:14.4e} '.format(cost),end='')
        print('nc: {:7.6e} '.format(ncost),end='')

        if cost < threshold:
            print()
            print('Success in {} iterations'.format(t))
            print('kxx original', p_t.kxx)
            trials.append(t)
            #plot_item(costs[1:])
            #print('lims', ft_t)
            #print('model', ft)
            #show_imgs(ft_t, ft)
            break

        update = np.sign(pp.kxx - p.kxx) * np.sign(pcost - cost) * p.kxx * gammax * ncost
        pp.kxx = p.kxx
        p.kxx -= update
        print('u: {: 4.5e} '.format(update), end='')
        print()

    else:
        #print('lims', ft_t)
        #print('model', ft)
        print(r)
        print('kxx original', p_t.kxx)
        print('Fail')
        break

else:
    print('Success averate {} trials'.format(np.mean(trial)))
