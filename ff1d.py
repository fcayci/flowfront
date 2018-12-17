# author: Furkan Cayci
# description:

import numpy as np
from common import *
from lims_common import *

BOARDSIZE = (0.2, 0.7) # board size in meters (y, x)
NODESIZE = (2, 36) # number of nodes in each direction (y, x)
n_of_runs = 1 # repeated runs for trial averaging
trials = []   # array to hold trial numbers for each run
backend = 'LIMS' # 'PITON'

#### Create target flowfront

# create coefficients
c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)

# create permeability map instance
# elements can be accessed by p.kxx
p = PMap(kxx=1e-10, kyy=1, kxy=1e-11)
# randomize if needed
# p.randomize()

# calculate target flow time
ft_t = calculate_flowtime(BOARDSIZE, NODESIZE, p, c)
print(ft_t)
#ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'run2')
#print(ft)
#show_imgs(ft, ft_t)
#plot_item(ft_t[0])

#for run in range(n_of_runs):

    # create solver
    # solver = Solver(bsize, nsize)
    # solver.set_target(ft_t)
    # solver.set_threshold(0.1)
    # solver.

#     # create parameters
#     n_of_iters = 1000
#     threshold = 1

#     ff = np.empty_like(ff_t)
#     b = 1
#     kx = 1e-8
#     kx_prev = 2e-8
#     kx_sign = 0
#     ky = 0
#     gammax = 0.1
#     cost = 0
#     cost_prev = 0

#     for t in range(n_of_iters):

#         ff = evaluate_lims(1, x, y, kx, ky, 1e5, a)
#         kx_sign = np.sign(kx_prev - kx)

#         cost_prev = cost
#         cost = np.linalg.norm(ff_t - ff, 2)

#         print('{:5}: kx: {:14.4E}, cost: {}'.format(t, kx, cost))

#         if cost < threshold:
#             print('Success in {} iterations'.format(t))
#             print('cost: {}, kxo: {}, kx: {}, a: {}, b: {}'.format(cost, kx_t, kx, a, b))
#             trials.append(t)
#             show_imgs(ff_t, ff)
#             break

#         kx_prev = kx
#         kx -= kx_sign * np.sign(cost_prev - cost) * gammax * kx

#     else:
#         print('cost: {}, kx_t: {}, kx: {}, a: {}, b: {}'.format(cost, kx_t, kx, a, b))
#         #overlay_imgs(ff_t, ff)
#         #show_imgs(ff_t, ff)
#         print('Fail')
#         break

# else:
#     print('Success for {} runs with {} iters per run'.format(n_of_runs, np.mean(trials)))