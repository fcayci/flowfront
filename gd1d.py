# author: Furkan Cayci
# description: gradient descent method
#   cost function is
#    l2norm(ff_target - ff_trial)

import numpy as np
from common import show_imgs, overlay_imgs

# 1d function
# tfill = x**2 (mu * fi) / (2 * kxx * deltaP)
mu = 0.2
fi = 0.5
dP = 1E5

d1d = lambda x, kx, a: x**2 * mu * fi / (kx * dP)

#AREA = (0.2, 0.7)
#NUMBER_OF_NODES = (11, 36)
x, y = np.mgrid[0:0.2:11j, 0:0.7:36j]
n_of_runs = 1
trials = []

for run in range(n_of_runs):

	# Create target vectors
	kx_t = ((np.random.random()+1.1) * 1E-8)
	a = np.random.random()
	ff_t = d1d(y, kx_t, a)

	# create parameters
	n_of_iters = 1000
	threshold = 1

	ff = np.empty_like(ff_t)
	b = 1
	kx = 1
	kx_prev = 2
	kx_sign = 0
	gammax = 0.34
	cost = 0
	cost_prev = 0

	for t in range(n_of_iters):

		ff = d1d(y, kx, b)
		kx_sign = np.sign(kx_prev - kx)

		cost_prev = cost
		cost = np.linalg.norm(ff_t - ff, 2)

		print('{:5}: kx: {: 14.4e}, cost: {}'.format(t, kx, cost))

		if cost < threshold:
			print('Success in {} iterations'.format(t))
			print('cost: {}, kxo: {}, kx: {}, a: {}, b: {}'.format(cost, kx_t, kx, a, b))
			trials.append(t)
			#show_imgs(ff_t, ff)
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