# author: Furkan Cayci
# description:cost function plotter for 2 parameters
#   sets random kxx and krt based target flowfront,
#   then iterates through the given boundaries for
#   search kxx, krt and plots the resulting cost functions

import numpy as np
from common import *
from lims_common import *
import matplotlib.pyplot as plt
import time

BOARDSIZE = (0.2, 0.4) # board size in meters (y, x)
NODESIZE  = (11, 21)   # number of nodes in each direction (y, x)
costs = []             # array to hold the costs for each run
backend = 'LIMS'       # choose backend : LIMS or XXX
xsamples = 101         # number of samples for kxx testing
rsamples = 101         # number of samples for krt testing

kx = np.logspace(-14, -8, xsamples)
kr = np.logspace(-14, -8, rsamples)

c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)
# set up the gates
# w  : west
# nw : north west
# sw : south west
gatenodes = set_gatenodes(NODESIZE, 'w')

### Create target flowfront
p_t = PMap(kxx=1.421e-12, krt=4.63e-12)

if backend == 'LIMS':
    ft_t = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)
else:
    ft_t = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)

start = time.time()
for rx in range(len(kx)):
    for rr in range(len(kr)):
        ### Create target flowfront
        p = PMap(kxx=kx[rx], krt=kr[rr])
        # randomize kxx over the given bounds
        #p_t.randomize(lower=1e-14, upper=1e-8)

        # calculate target flow time
        if backend == 'LIMS':
            ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)
        else:
            ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)

        # if something is not filled, just skip it
        if np.count_nonzero(ft) < (NODESIZE[1]-1) * NODESIZE[0]:
            pass
        else:
            cost = np.linalg.norm(ft_t - ft, 2)
            costs.append(cost)

print(len(costs), len(kx), len(kr))
print('took {} seconds'.format(time.time() - start))
plt.semilogy(costs)
plt.title('2 parameter sweep on kxx and krt\n for target kxx_t={:4.3e} and krt_t={:4.3e}'.format(p_t.kxx, p_t.krt))
plt.xlabel('# of trials')
plt.ylabel('cost (l2norm of target and calculated flowfronts)')
#plt.show()
plt.savefig('sweep2d.png')