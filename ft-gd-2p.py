# author: Furkan Cayci
# description: gradient descent implementation over 2 parameters

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
threshold = 3000       # l2 norm threshold
n_of_iters = 40000     # max number of iterations before giving up

# create a target kxx vector to test between given log space
# e.g: 100 kxx values between 1e-11 and 1e-8
# np.logspace(-11, -8, 100)
kx  = np.logspace(-14, -8, 10)
kr1 = np.logspace(-14, -8, 10)

logging.info('kxx values that are being tested:\n{}'.format(kx))
logging.info('krt values that are being tested:\n{}'.format(kr1))
logging.warning('testing kxx for {} values'.format(len(kx)))
logging.warning('testing krt for {} values'.format(len(kr1)))

for rx in range(len(kx)):
	for rr in range(len(kr1)):

		### Create target flowfront
		c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)
		p_t = PMap(kxx=kx[rx], krt=kr1[rr])
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

		if np.count_nonzero(ft_t) < (NODESIZE[1]-1) * NODESIZE[0]:
			logging.warning('skipping')
			break
		# initial educated guess.
		# Making this a big number helps with the iteration counts
		p = PMap(kxx=5e-8, krt=1e-8)
		pp = PMap(kxx=6e-8, krt=2e-8)

		gammax = 0.8

		cost = 0
		pcost = 0
		mcost = 0
		ncost = 0
		costs = []
		mux = 0

		l = 'Run {:5} {}\n'.format(rx*len(kx)+rr, '#'*70)
		l += 'Testing for kxx: {:14.4e}, krt: {:14.4e}\n'.format(p_t.kxx, p_t.krt)
		l += '{}\n'.format('#'*80)
		logging.warning(l)

		for t in range(n_of_iters):

			if t % 30 == 0:
				mux = 1 - mux

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
			l += 'r: {:14.4e} '.format(p.krt)
			l += 'c: {:14.4e} '.format(cost)
			l += 'nc: {:7.6e} '.format(ncost)

			if cost < threshold:
				logging.info(l)
				l  = 'SUCCESS in {} iters '.format(t)
				l += 'kxx was {} '.format(p_t.kxx)
				l += 'krt was {}'.format(p_t.krt)
				logging.warning(l)

				trials.append(t)
				#plot_item(costs[1:])
				#print('lims', ft_t)
				#print('model', ft)
				show_imgs(ft_t, ft)
				break

			if mux == 0:
				# update kxx
				update = np.sign(pp.kxx - p.kxx) * np.sign(pcost - cost) * p.kxx * gammax * ncost
				pp.kxx = p.kxx
				p.kxx -= update
				l += 'ux: {: 4.5e} '.format(update)
			else:
				# update krt
				update = np.sign(pp.krt - p.krt) * np.sign(pcost - cost) * p.krt * gammax * ncost
				pp.krt = p.krt
				p.krt -= update
				l += 'ur: {: 4.5e} '.format(update)

			logging.info(l)

		else:
			#print('lims', ft_t)
			#print('model', ft)
			logging.info(l)
			l  = 'FAIL in {}th trial. '.format(r)
			l += 'kxx was {}. '.format(p_t.kxx)
			l += 'krt was {}. '.format(p_t.krt)
			l += 'we ended at kxx: {}'.format(p.kxx)
			l += 'we ended at krt; {}'.format(p.krt)
			logging.error(l)
			break

else:
	logging.error('Success average is {} iterations over {} trials'.format(np.mean(trials), len(kx)*len(kr1)))
