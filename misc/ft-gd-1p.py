# author: Furkan Cayci
# description:
#   gradient descent implementation over 1 parameter
#   on lims  -14 takes a long time to fill, threshold should be
#   somewhat relevant. if values are between -12 and -8, it should
#   work fine.
#
# result:
#   Success average is 10.52 iterations over 100 trials for python impl.
#   Success average is 10.4  iterations over 100 trials for lims
#     with gammax=.8, nodesize=(11,21), boardsize=(.2,.4), threshold=1

import numpy as np
from common import *
from lims_common import *
import logging

# set print logging level: INFO, WARNING, ERROR
logging.basicConfig(format='%(message)s', level=logging.INFO)

BOARDSIZE = (0.2, 0.4) # board size in meters (y, x)
NODESIZE = (11, 21)    # number of nodes in each direction (y, x)
trials = []            # array to hold trial numbers for each run
costs = []             # array to hold the costs for each run
backend = 'LIMS'       # choose backend : LIMS or XXX
threshold = 1          # l2 norm threshold
n_of_iters = 40000     # max number of iterations before giving up

# create a target kxx vector to test between given log space
# e.g: 100 kxx values between 1e-12 and 1e-8
k = np.logspace(-12, -8, 100)

logging.info('kxx values that are being tested:\n{}'.format(k))
logging.warning('testing for {} values'.format(len(k)))

m = lambda : np.ones(NODESIZE[1])

for r, kxx_t in enumerate(k):

    # create target flowfront
    c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)
    p_t = PMap(kxx=m()*kxx_t)

    # set up the gates
    # w  : west
    # nw : north west
    # sw : south west
    gatenodes = set_gatenodes(NODESIZE, 'w')

    # calculate target flow time
    if backend == 'LIMS':
        ft_t, pt_t = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)
    else:
        ft_t, pt_t = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)

    # initial educated guess.
    # Making this a big number helps with the iteration counts
    kxx_cur = 5e-8
    p = PMap(kxx=m()*kxx_cur) # current guess
    kxx_prev = 6e-8
    pp = PMap(kxx=m()*kxx_prev) # previous guess

    gammax = 0.8

    cost = 0
    pcost = 0
    mcost = 0
    ncost = 0
    costs = []

    for t in range(n_of_iters):

        l = '' # this is the logger string
        if backend == 'LIMS':
            ft, pt = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)
        else:
            ft, pt = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)

        pcost = cost
        cost = np.linalg.norm(ft_t - ft, 2)
        costs.append(cost)
        mcost = max(mcost, cost)
        ncost = abs(cost) / mcost

        l += '{:5} '.format(t)
        l += 'x: {:10.4e} '.format(kxx_cur)
        l += 'cost: {:10.4e} '.format(cost)
        l += 'normcost: {:7.6e} '.format(ncost)

        if cost < threshold:
            logging.info(l)
            l  = 'SUCCESS in {} iterations '.format(t)
            l += 'kxx target was {}'.format(kxx_t)
            logging.warning(l)

            trials.append(t)
            t = 'cost function for target kxx: {:14.4e}'.format(kxx_t)
            #plot_item(costs[1:], t)
            #print('lims', ft_t)
            #print('model', ft)
            t = 'Flowfront when kxx: {:14.4e}'.format(kxx_t)
            show_imgs(ft_t, ft, t)
            break

        update = np.sign(kxx_prev - kxx_cur) * np.sign(pcost - cost) * kxx_cur * gammax * ncost
        if update == 0:
            logging.error('FAIL: update value reached to 0')
            exit()
        pp.kxx = m() * kxx_cur
        kxx_cur -= update
        p.kxx = m() * kxx_cur
        l += 'update: {: 10.5e}'.format(update)
        logging.info(l)

    else:
        #print('lims', ft_t)
        #print('model', ft)
        logging.info(l)
        l  = 'FAIL in {}th trial. '.format(r)
        l += 'kxx target was {}. '.format(kxx_t)
        l += 'we ended at {}'.format(kxx_cur)
        logging.error(l)
        break

else:
    logging.error('Success average is {} iterations over {} trials'.format(np.mean(trials), len(k)))
