# author: Furkan Cayci
# description: gradient descent method
#   cost function is
#    l2norm(ff_target - ff_trial)

import numpy as np
from common import *

#AREA = (0.2, 0.7)
#NUMBER_OF_NODES = (11, 36)
x, y = np.mgrid[0:0.2:11j, 0:0.7:36j]
n_of_runs = 1
trials = []

for run in range(n_of_runs):

	# Create target vectors

	kx_t = ((np.random.random()+1.1) * 1E-8)
	ky_t = 0
	print(kx_t)
	a = 1
	ff_t = evaluate_lims(1, x, y, kx_t, ky_t, 1e5, a)
	print(ff_t)

	# create parameters
	n_of_iters = 1000
	threshold = 0.1

	ff = np.empty_like(ff_t)
	b = 1
	kx = 1e-8
	ky = 1e-8
	kx_prev = 2
	kx_sign = 0
	gammax = 0.1
	cost = 0
	cost_prev = 0

	for t in range(n_of_iters):

		ff = evaluate_lims(1, x, y, kx, ky, 1e5, a)
		kx_sign = np.sign(kx_prev - kx)

		cost_prev = cost
		cost = np.linalg.norm(ff_t - ff, 2)

		print('{:5}: kx: {:14.4E}, cost: {}'.format(t, kx, cost))

		if cost < threshold:
			print('Success in {} iterations'.format(t))
			print('cost: {}, kxo: {}, kx: {}, a: {}, b: {}'.format(cost, kx_t, kx, a, b))
			trials.append(t)
			show_imgs(ff_t, ff)
			break

		kx_prev = kx
		kx -= kx_sign * np.sign(cost_prev - cost) * gammax * kx

	else:
		print('cost: {}, kx_t: {}, kx: {}, a: {}, b: {}'.format(cost, kx_t, kx, a, b))
		#overlay_imgs(ff_t, ff)
		#show_imgs(ff_t, ff)
		print('Fail')
		break

else:
	print('Success for {} runs with {} iters per run'.format(n_of_runs, np.mean(trials)))