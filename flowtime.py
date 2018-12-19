# author: Furkan Cayci
# description:

import numpy as np
from common import *
from lims_common import *

BOARDSIZE = (0.2, 0.7) # board size in meters (y, x)
NODESIZE = (11, 36) # number of nodes in each direction (y, x)
n_of_runs = 1 # repeated runs for trial averaging
trials = []   # array to hold trial numbers for each run
backend = 'PITON' # 'PITON'

#### Create target flowfront

# create coefficients
c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)

# create permeability map instance
# elements can be accessed by p.kxx
p_t = PMap(kxx=132.4124e-10, kyy=2.31424e-10, kxy=5.42143e-11)
# randomize if needed
# p_t.randomize()

# calculate target flow time
if backend == 'LIMS':
    ft_t = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'run1')
else:
    ft_t = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c)
#print(ft_t)

# create parameters
n_of_iters = 1000
threshold = 0.01
p = PMap(kxx=1e-10, kyy=1e-10, kxy=5.42143e-11)
pp = PMap(kxx=2e-10, kyy=2e-10, kxy=2e-10)
# p.randomize()

kxx_sign = 0
kyy_sign = 0
kxy_sign = 0
gammax = 0.9
gammay = 0.8
gammaz = 0.2

cost = 0
cost_prev = 0
cost_max = 0
cost_norm = 0

for t in range(n_of_iters):

    if backend == 'LIMS':
        ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'solve3d')
    else:
        ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'solve3d')

    kxx_sign = np.sign(pp.kxx - p.kxx)
    kyy_sign = np.sign(pp.kyy - p.kyy)
    kxy_sign = np.sign(pp.kxy - p.kxy)

    cost_prev = cost
    cost = np.linalg.norm(ft_t - ft, 2)
    cost_max = max(cost_max, cost)
    cost_norm = abs(cost) / cost_max

    print('{:5}'.format(t),end='')
    print('{:14.4e}'.format(p.kxx),end='')
    print('{:14.4e}'.format(p.kyy),end='')
    print('{:14.4e}'.format(p.kxy),end='')
    print('{:14.4e}'.format(cost),end='')
    print()

    if cost < threshold:
        print('Success in {} iterations'.format(t))
        #trials.append(t)
        #print('lims', ft_t)
        #print('model', ft)
        show_imgs(ft_t, ft)
        break

    pp.kxx = p.kxx
    pp.kyy = p.kyy
    pp.kxy = p.kxy
    p.kxx -= kxx_sign * np.sign(cost_prev - cost) * gammax * p.kxx * cost_norm
    p.kyy -= kyy_sign * np.sign(cost_prev - cost) * gammay * p.kyy * cost_norm
    #p.kxy -= kxy_sign * np.sign(cost_prev - cost) * gammaz * p.kxy

else:
    print('Fail')
    #break

# else:
#     print('Success for {} runs with {} iters per run'.format(n_of_runs, np.mean(trials)))