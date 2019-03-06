# author: Furkan Cayci
# description: cost function plot for 1 parameter

import numpy as np
from common import *
from lims_common import *
import matplotlib.pyplot as plt

BOARDSIZE = (0.2, 0.7) # board size in meters (y, x)
NODESIZE  = (11, 36)   # number of nodes in each direction (y, x)
costs = []             # array to hold the costs for each run
backend = 'LIMS'       # choose backend : LIMS or XXX

# create a target kxx vector to test between given log space
# e.g: 100 kxx values between 1e-11 and 1e-8
# np.logspace(-11, -8, 100)
k = np.logspace(-14, -8, 100)
c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)
# set up the gates
# w  : west
# nw : north west
# sw : south west
gatenodes = set_gatenodes(NODESIZE, 'w')

### Create target flowfront
p_t = PMap(kxx=1.4213141e-13)

if backend == 'LIMS':
	ft_t = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)
else:
	ft_t = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'target', gatenodes)

for r in range(len(k)):

	### Create target flowfront
	p = PMap(kxx=k[r])
	# randomize kxx over the given bounds
	#p_t.randomize(lower=1e-14, upper=1e-8)

	# calculate target flow time
	if backend == 'LIMS':
		ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)
	else:
		ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'trial', gatenodes)

	cost = np.linalg.norm(ft_t - ft, 2)
	costs.append(cost)

print(costs)

plt.semilogy(costs)
plt.title('1 parameter sweep on kxx')
plt.xlabel('# of trials')
plt.ylabel('cost')
plt.show()