# author: Furkan Cayci
# description: gradient descent method
#   cost function is
#    l2norm(ff_target - ff_trial)
#    cost  -> 1/N * SUM i:1->n ((xi**2 * kx * a) + (yi**2 * ky * b) - di)

import numpy as np
from common import show_imgs, overlay_imgs

# 2d function
d2d = lambda x, y, kx, ky, a, b: x**2 * (kx * a) + y**2 * (ky * b)

#AREA = (0.2, 0.7)
#NUMBER_OF_NODES = (11, 36)
x, y = np.mgrid[0:0.2:11j, 0:0.7:36j]
n_of_runs = 100
trials = []

for run in range(n_of_runs):

	# Create target vectors
	kx_t = ((np.random.random()+1.1) * 1E3)
	ky_t = ((np.random.random()+1.1) * 1E3)
	a = np.random.random()
	b = np.random.random()
	ff_t = d2d(y, x, kx_t, ky_t, a, b)

	# create parameters
	n_of_iters = 4000
	threshold = 0.1

	ff = np.empty_like(ff_t)
	a = 1
	b = 1
	kx = 1
	kx_prev = 2
	kx_sign = 0
	ky = 1
	ky_prev = 2
	ky_sign = 0
	gammax = 0.22
	gammay = 0.22
	cost = 0
	cost_prev = 0

	flag = True

	for t in range(n_of_iters):

		if t % 12 == 0:
			flag = not flag

		if flag:
			kx_sign = np.sign(kx_prev - kx)
			kx_prev = kx
		else:
			ky_sign = np.sign(ky_prev - ky)
			ky_prev = ky
		cost_prev = cost

		ff = d2d(y, x, kx, ky, a, b)
		cost = np.linalg.norm(ff_t - ff, 2)

		print('{:5}: cost: {: 10.4f}, kx: {:14.4f}, ky: {:14.4f}'.format(t, cost, kx, ky))

		if cost < threshold:
			print('Success in {} iterations'.format(t))
			print('cost: {}, kxt: {}, kx: {}, kyt: {}, ky: {}, a: {}, b: {}'.format(cost, kx_t, kx, ky_t, ky, a, b))
			trials.append(t)
			#show_imgs(ff_t, ff)
			break

		if flag:
			kx -= kx_sign * np.sign(cost_prev - cost) * gammax * cost
		else:
			ky -= ky_sign * np.sign(cost_prev - cost) * gammay * cost

	else:
		print('cost: {}, kx_t: {}, kx: {}, ky_t: {}, ky: {}, a: {}, b: {}'.format(cost, kx_t, kx, ky_t, ky, a, b))
		#overlay_imgs(ff_t, ff)
		#show_imgs(ff_t, ff)
		print('Fail')
		break

else:
	print('Success for {} runs with {} iters per run'.format(n_of_runs, np.mean(trials)))