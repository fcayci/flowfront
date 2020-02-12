# author: Furkan Cayci
# description:cost function plot for 3 parameters
#   sets random kxx, kyy and kxy based target flowfront,
#   then iterates through the given boundaries for
#   search kxx, kyy, and kxy and plots the resulting cost functions

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
ysamples = 101         # number of samples for kyy testing
zsamples = 101         # number of samples for kxy testing

kx = np.logspace(-14, -8, xsamples)
ky = np.logspace(-14, -8, ysamples)
kz = np.logspace(-14, -9, zsamples)

c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)
# set up the gates
# w  : west
# nw : north west
# sw : south west
gatenodes = set_gatenodes(NODESIZE, 'w')

### Create target flowfront
p_t = PMap(kxx=1.4213141e-11, kyy=8.4124e-11, kxy=3.4124e-12)

if backend == 'LIMS':
    ft_t = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)
else:
    ft_t = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)

f = open('sweep3d.txt', 'w')
l = '{:7}, {:10.4e}, {:10.4e}, {:10.4e}\n'.format('target', p_t.kxx, p_t.kyy, p_t.kxy)
f.write(l)
i = 1

start = time.time()
for rx in range(len(kx)):
    for ry in range(len(ky)):
        for rz in range(len(kz)):
            ### Create target flowfront
            p = PMap(kxx=kx[rx], kyy=ky[ry], kxy=kz[rz])

            # calculate target flow time
            if backend == 'LIMS':
                ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)
            else:
                ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)

            if np.count_nonzero(ft) < (NODESIZE[1]-1) * NODESIZE[0]:
                #print('skipping')
                pass
            else:
                cost = np.linalg.norm(ft_t - ft, 2)
                costs.append(cost)
                l = '{:7}, {:10.4e}, {:10.4e}, {:10.4e}, {:.4f}\n'.format(i, kx[rx], ky[ry], kz[rz], cost)
                f.write(l)
                i=i+1

print('took {} seconds'.format(time.time() - start))

f.close()

print('got {} samples'.format(len(costs)))
plt.semilogy(costs)
plt.title('3 parameter sweep on kxx, kyy and kxy for target\n kxx_t={:4.3e}, kyy_t={:4.3e} and kxy_t={:4.3e}'.format(p_t.kxx, p_t.kyy, p_t.kxy))
plt.xlabel('# of trials')
plt.ylabel('cost (l2norm of target and calculated flowfronts)')
#plt.show()
plt.savefig('sweep3d.png')