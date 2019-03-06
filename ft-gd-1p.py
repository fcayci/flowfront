# author: Furkan Cayci
# description: gradient descent implementation over 1 parameter
#   takes on averate 14.85 iterations over 100 trials with 0.1 threshold
#   11x21 nodes with 0.2x0.4 meter board
#   on lims  -14 takes a long time to fill, threshold should be
#     somewhat relevant. if values are between -12 and -8, it should
#     work fine.

import numpy as np
from common import *
from lims_common import *
import logging
import matplotlib.pyplot as plt

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

	# initial educated guess.
	# Making this a big number helps with the iteration counts
	p = PMap(kxx=5e-8)
	pp = PMap(kxx=6e-8)

	gammax = 0.8

	cost = 0
	pcost = 0
	mcost = 0
	ncost = 0
	costs = []

	for t in range(n_of_iters):

		l = '' # this is the logger string
		if backend == 'LIMS':
			ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)
		else:
			ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)

		pcost = cost
		cost = np.linalg.norm(ft_t - ft, 2)
		costs.append(cost)
		mcost = max(mcost, cost)
		ncost = abs(cost) / mcost

		l += '{:5} '.format(t)
		l += 'x: {:14.4e} '.format(p.kxx)
		l += 'c: {:14.4e} '.format(cost)
		l += 'nc: {:7.6e} '.format(ncost)

		if cost < threshold:
			logging.info(l)
			l  = 'SUCCESS in {} iterations '.format(t)
			l += 'kxx target was {}'.format(p_t.kxx)
			logging.warning(l)

			trials.append(t)
			t = 'cost function for target kxx: {:14.4e}'.format(p_t.kxx)
			plot_item(costs[1:], t)
			#print('lims', ft_t)
			#print('model', ft)
			t = 'Flowfront when kxx: {:14.4e}'.format(p_t.kxx)
			show_imgs(ft_t, ft, t)
			break

		update = np.sign(pp.kxx - p.kxx) * np.sign(pcost - cost) * p.kxx * gammax * ncost
		if update == 0:
			logging.error('FAIL: update value reached to 0')
			exit()
		pp.kxx = p.kxx
		p.kxx -= update
		l += 'u: {: 4.5e}'.format(update)
		logging.info(l)

	else:
		#print('lims', ft_t)
		#print('model', ft)
		logging.info(l)
		l  = 'FAIL in {}th trial. '.format(r)
		l += 'kxx target was {}. '.format(p_t.kxx)
		l += 'we ended at {}'.format(p.kxx)
		logging.error(l)
		break

else:
	logging.error('Success average is {} iterations over {} trials'.format(np.mean(trials), len(k)))
