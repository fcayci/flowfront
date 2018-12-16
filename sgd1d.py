# author: Furkan Cayci
# description: stochastic gradient descent method
#   cost function is
#    l2norm(ff_target - ff_trial)

import numpy as np
from common import show_imgs, overlay_imgs

# 1d function
d1d = lambda x, kx, a: x**2 * (kx * a)

#AREA = (0.2, 0.7)
#NUMBER_OF_NODES = (11, 36)
x, y = np.mgrid[0:0.2:11j, 0:0.7:36j]
n_of_runs = 1000
trials = []

for run in range(n_of_runs):

    # Create target vectors
    kx_t = ((np.random.random()+1.1) * 1E6)
    a = 1 #np.random.random()
    ff_t = d1d(y, kx_t, a)

    # create parameters
    n_of_iters = 40
    threshold = 0.1

    ff = np.empty_like(ff_t)
    b = 1
    kx = 1
    kx_prev = 2
    kx_sign = 0
    pertx = 0.02
    leapx = 0.22
    cost = 0
    cost_prev = 0
    perturb = 0
    leap = 0

    for t in range(n_of_iters):

        ff = d1d(y, kx, b)
        kx_sign = np.sign(kx_prev - kx)
        kx_norm = abs(kx_prev - kx) / max(kx_prev, kx)

        cost_prev = cost
        cost = np.linalg.norm(ff_t - ff, 2)

        print('{:5}: cost: {:14.6f}, kx: {:14.6f}, kxnorm: {: 10.9f}'.format(t, cost, kx, kx_norm))

        if cost < threshold:
            print('Success in {} iterations'.format(t))
            print('cost: {}, kxo: {}, kx: {}, a: {}, b: {}'.format(cost, kx_t, kx, a, b))
            trials.append(t)
            #show_imgs(ff_t, ff)
            break

        if t % 2 == 0:
            # perturb
            kx_prev = kx
            kx -= pertx * (np.random.random()-0.5) * kx_norm
        else:
            # leap
            kx -= leapx * kx_sign * np.sign(cost_prev - cost) * cost

    else:
        print('cost: {}, kx_t: {}, kx: {}, a: {}, b: {}'.format(cost, kx_t, kx, a, b))
        #overlay_imgs(ff_t, ff)
        #show_imgs(ff_t, ff)
        print('Fail')
        break

else:
    print('Success for {} runs with {} iters per run'.format(n_of_runs, np.mean(trials)))