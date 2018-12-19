# author: Furkan Cayci
# description:

import numpy as np
from common import *
from lims_common import *

BOARDSIZE = (0.2, 0.7) # board size in meters (y, x)
NODESIZE = (11, 36) # number of nodes in each direction (y, x)
n_of_runs = 1 # repeated runs for trial averaging
trials = []   # array to hold trial numbers for each run
backend = 'LIMS' # 'PITON'

#### Create target flowfront
c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)
p_t = PMap(kxx=1e-10)
p_t.randomize()
gatenodes = set_gatenodes(NODESIZE, 'w')

# calculate target flow time
if backend == 'LIMS':
    ft_t = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'run1', gatenodes)
else:
    ft_t = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c)
#print(ft_t)
#show_img(ft_t)

# create parameters
n_of_iters = 1000
threshold = 0.1
p = PMap(kxx=1e-10)
pp = PMap(kxx=2e-10)

kxx_sign = 0
gammax = 0.2

cost = 0
cost_prev = 0
cost_max = 0
cost_norm = 0


for t in range(n_of_iters):

    if backend == 'LIMS':
        ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'solve3d', gatenodes)
    else:
        ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'solve3d')

    cost_prev = cost
    cost = np.linalg.norm(ft_t - ft, 2)
    cost_max = max(cost_max, cost)
    cost_norm = abs(cost) / cost_max

    print('{:5} '.format(t),end='')
    print('x: {:14.4e} '.format(p.kxx),end='')
    print('c: {:14.4e} '.format(cost),end='')
    print('cn: {:7.6e}'.format(cost_norm),end='')
    print()

    if cost < threshold:
        print('Success in {} iterations'.format(t))
        #trials.append(t)
        print('lims', ft_t)
        print('model', ft)
        show_imgs(ft_t, ft)
        break

    kxx_sign = np.sign(pp.kxx - p.kxx)
    pp.kxx = p.kxx
    p.kxx -= kxx_sign * np.sign(cost_prev - cost) * gammax * p.kxx

else:
    print('lims', ft_t)
    print('model', ft)
    print('kxx original', p_t.kxx)
    print('Fail')