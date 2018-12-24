# author: Furkan Cayci
# description: currently pretty good estimation. sometimes it blows up

import numpy as np
from common import *
from lims_common import *

BOARDSIZE = (0.2, 0.4) # board size in meters (y, x)
NODESIZE = (11, 21) # number of nodes in each direction (y, x)
n_of_runs = 1 # repeated runs for trial averaging
trials = []   # array to hold trial numbers for each run
backend = 'G' # 'PITON'

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
n_of_iters = 400
threshold = 0.1
p = PMap(kxx=1e-12)
pp = PMap(kxx=2e-12)

gammax = 0.4 * BOARDSIZE[1] / (NODESIZE[1]-1)

cost = 0
pcost = 0
mcost = 0
ncost = 0


for t in range(n_of_iters):

    if backend == 'LIMS':
        ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)
    else:
        ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)

    pcost = cost
    cost = np.linalg.norm(ft_t - ft, 2)
    mcost = max(mcost, cost)
    ncost = abs(cost) / mcost

    print('{:5} '.format(t),end='')
    print('x: {:14.4e} '.format(p.kxx),end='')
    print('c: {:14.4e} '.format(cost),end='')
    print('nc: {:7.6e} '.format(ncost),end='')

    if cost < threshold:
        print()
        print('Success in {} iterations'.format(t))
        print('kxx original', p_t.kxx)
        #trials.append(t)
        #print('lims', ft_t)
        #print('model', ft)
        #show_imgs(ft_t, ft)
        break

    update = np.sign(pp.kxx - p.kxx) * np.sign(pcost - cost) * gammax * cost * p.kxx
    pp.kxx = p.kxx
    p.kxx -= update
    print('u: {: 4.5e} '.format(update), end='')
    print()

else:
    #print('lims', ft_t)
    #print('model', ft)
    print('kxx original', p_t.kxx)
    print('Fail')