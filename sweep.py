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

print(p_t.kxx)

# calculate target flow time
if backend == 'LIMS':
    ft_t = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'run1', gatenodes)
else:
    ft_t = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c)

p = PMap(kxx=1e-15)

cost = 0
cost_max = 0
cost_norm = 0

kxxvec = np.linspace(1e-12, 1e-7, 500)

costvec = []
normvec = []

for i, t in enumerate(kxxvec):

    p.kxx = t
    if backend == 'LIMS':
        ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'solve3d', gatenodes)
    else:
        ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'solve3d')

    cost = np.linalg.norm(ft_t - ft, 2)
    cost_max = max(cost_max, cost)
    cost_norm = abs(cost) / cost_max
    costvec.append(cost)
    normvec.append(cost_norm)
    print('{:4}: {:10.8e}'.format(i, t), end='')
    print('{:10.4f}, {:7.6f}'.format(cost, cost_norm))

plot_item(costvec[1:])
plot_item(normvec[1:])