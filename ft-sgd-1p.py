# author: Furkan Cayci
# description:

import numpy as np
from common import *
from lims_common import *

BOARDSIZE = (0.2, 0.7) # board size in meters (y, x)
NODESIZE = (11, 36) # number of nodes in each direction (y, x)
n_of_runs = 1 # repeated runs for trial averaging
backend = 'S' # LIMS / PITON

#### Create target flowfront
c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)
p_t = PMap(kxx=1e-10)
p_t.randomize()
gatenodes = set_gatenodes(NODESIZE, 'w')

# calculate target flow time
if backend == 'LIMS':
    ft_t = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)
else:
    ft_t = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)

# create parameters
n_of_iters = 40
threshold = 0.1
normalize = 1e+15
p = PMap(kxx=1e-10)
pp = PMap(kxx=1e-10)

pert = 0.008
leap = 0.8

cost = 0
cost_prev = 0
cost_max = 0
#cost_min =
cost_norm = 0

# starting point for minimum cost
cost_min = 1e-6

for t in range(n_of_iters):

    if backend == 'LIMS':
        ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)
    else:
        ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)

    pcost = cost
    cost = np.linalg.norm(ft_t - ft, 2)
    cost_max = max(cost_max, cost)
    cost_min = min(cost_min, cost)
    # if cost_norm < cost_max / 2:
    #     cost_max = cost_max/2
    cost_norm = abs(cost) / cost_max

    print('{:5} '.format(t),end='')
    print('x: {:14.4e} '.format(p.kxx),end='')
    print('c: {:14.4e} '.format(cost),end='')
    print('cn: {:7.6e} '.format(cost_norm),end='')

    if cost < threshold:
        print()
        print('Success in {} iterations'.format(t))
        #print('lims', ft_t)
        #print('model', ft)
        show_imgs(ft_t, ft)
        break

    if t % 2 == 0:
        # perturb
        update = pert * np.random.random() * p.kxx
        p.kxx -= update
        print('p: {} '.format(update), end='')
    else:
        # leap
        if np.sign(pcost - cost) is not 0:
            update = leap * np.sign(pcost - cost) * cost_norm * p.kxx
        else:
            update = leap * cost_norm * p.kxx
        # update = leap * np.sign(pp.kxx - p.kxx) * np.sign(cost_prev - cost) * p.kxx * cost_norm
        p.kxx -= update
        print('l: {} '.format(update), end='')
    
    print()


else:
    #print('lims', ft_t)
    #print('model', ft)
    print('kxx original', p_t.kxx)
    print('Fail')