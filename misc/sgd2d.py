# author: Furkan Cayci
# description: stochastic gradient descent method 2d
#   cost function is
#    l2norm(ff_target - ff_trial)

import numpy as np
from common import show_imgs, overlay_imgs

# 2d function
d2d = lambda x, y, kx, ky, a, b: x**2 * (kx * a) + y**2 * (ky * b)

#AREA = (0.2, 0.7)
#NUMBER_OF_NODES = (11, 36)
x, y = np.mgrid[0:0.2:11j, 0:0.7:36j]
n_of_runs = 1
trials = []

for run in range(n_of_runs):

    # Create target vectors
    kx_t = ((np.random.random()+1.1) * 1E6)
    ky_t = ((np.random.random()+1.1) * 1E6)
    a = 1 #np.random.random()
    b = 1 #np.random.random()
    ff_t = d2d(y, x, kx_t, ky_t, a, b)

    # create parameters
    n_of_iters = 40000
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
    pert = 0.42
    leap = 0.33
    cost = 0
    cost_prev = 0

    for t in range(n_of_iters):

        ff = d2d(y, x, kx, ky, a, b)

        kx_sign = np.sign(kx_prev - kx)
        kx_norm = abs(kx_prev - kx) / max(kx_prev, kx)

        ky_sign = np.sign(ky_prev - ky)
        ky_norm = abs(ky_prev - ky) / max(ky_prev, ky)

        cost_prev = cost
        cost = np.linalg.norm(ff_t - ff, 2)

        print('{:5}: cost: {:14.6f}, kx: {:14.6f}, kxnorm: {: 4.3f}, ky: {:14.6f}, kynorm: {: 4.3f} '.format(t, cost, kx, kx_norm, ky, ky_norm), end='')

        if cost < threshold:
            print('\nSuccess in {} iterations'.format(t))
            print('cost: {}, kxt: {}, kx: {}, kyt: {}, ky: {}, a: {}, b: {}'.format(cost, kx_t, kx, ky_t, ky, a, b))
            trials.append(t)
            #show_imgs(ff_t, ff)
            break

        if t % 2 == 0:
            # perturb
            kx_prev = kx
            pkx = pert * (np.random.random()-0.5)
            kx -= pkx

            ky_prev = ky
            pky = pert * (np.random.random()-0.5)
            ky -= pky

            print('p kx: {: 16.8f}, p ky: {: 16.8f}'.format(pkx, pky))

        else:
            # leap
            lkx = leap * kx_sign * np.sign(cost_prev - cost) * cost
            kx -= lkx

            lky = leap * ky_sign * np.sign(cost_prev - cost) * cost
            ky -= lky

            print('l kx: {: 16.8f}, l ky: {: 16.8f}'.format(lkx, lky))

    else:
        print('Fail')
        print('cost: {}, kxt: {}, kx: {}, kyt: {}, ky: {},a: {}, b: {}'.format(cost, kx_t, kx, ky_t, ky, a, b))
        #overlay_imgs(ff_t, ff)
        #show_imgs(ff_t, ff)
        break

else:
    print('Success for {} runs with {} iters per run'.format(n_of_runs, np.mean(trials)))