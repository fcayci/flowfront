# author: Furkan Cayci
# description: gradient descent method
#   cost function is
#   f(pkx) = SUM 1->x*y ((x**2 * pkx * a)**2 - ((x**2 * kx * b)**2))
#   tries to minimize this by playing with pkx parameter

import numpy as np
from common import show_imgs, overlay_imgs

# 1d function
d1d = lambda x, kx, a: x**2 * (kx * a)

# cost func
# f(pkx) = SUM 0->x*y ((x**2 * pkx * a)**2 - ((x**2 * kx * b)**2))
# f'(pkx) = 2 * x**2 * a * pkx

x, y = np.mgrid[0:0.2:11j, 0:0.7:36j]
a = 1

n_of_runs = 1

for run in range(n_of_runs):

    kx_o = ((np.random.random()+1.1) * 1E6)
    ff_o = d1d(y, kx_o, a)

    n_of_trials = 1000
    threshold = 0.1

    ff = np.empty_like(ff_o)
    b = 1 # np.random.random()
    kx = 1
    kx_prev = 2
    gammax = 0.1 #2*a*0.03
    cost = 0
    cost_prev = 0
    #cost_norm = 0

    for t in range(n_of_trials):

        ff = d1d(y, kx, b)
        kx_sign = np.sign(kx_prev - kx)

        cost_prev = cost
        cost = np.linalg.norm(ff_o - ff, 2)
        #cost_norm = (cost_prev - cost) / max(cost, cost_prev)
        print('{:5}: kx: {:14.4f}, cost: {}'.format(t, kx, cost))

        if cost < threshold:
            print('Success in {} iterations'.format(t))
            #show_imgs(ff_o, ff)
            break

        kx_prev = kx
        kx -= kx_sign * np.sign(cost_prev - cost) * gammax * cost
    else:
        print('cost: {}, kxo: {}, kx: {}, a: {}, b: {}'.format(cost, kx_o, kx, a, b))
        #overlay_imgs(ff_o, ff)
        show_imgs(ff_o, ff)
        print('Fail')
        break

else:
    print('Success for {} runs...'.format(n_of_runs))