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
n_of_iters = 400
threshold = 0.1
p = PMap(kxx=1e-10)
kx = p.kxx * c.deltaP

pert = 0.01
leap = 30

cost = 0
pcost = 0
ncost = 0
mcost = 0

for t in range(n_of_iters):

    if backend == 'LIMS':
        ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)
    else:
        ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)

    pcost = cost
    cost = np.linalg.norm(ft_t - ft, 2)
    mcost = max(mcost, cost)
    ncost = cost / mcost
    scost = np.sign(pcost - cost)

    print('{:5} '.format(t),end='')
    print('kxx: {:14.4e} '.format(p.kxx),end='')
    print('c: {:14.4e} '.format(cost),end='')
    print('nc: {:7.6e} '.format(ncost),end='')

    if cost < threshold:
        print()
        print('Success in {} iterations'.format(t))
        #print('lims', ft_t)
        #print('model', ft)
        show_imgs(ft_t, ft)
        break

    if t % 2 == 0:
        update = pert * np.random.random() * p.kxx
        print('p: {} '.format(update), end='')
    else:
        update = leap * ncost * p.kxx
        print('l: {} '.format(update), end='')

    kx -= update
    p.kxx = kx / c.deltaP
    print()


else:
    #print('lims', ft_t)
    #print('model', ft)
    print('kxx original', p_t.kxx)
    print('Fail')