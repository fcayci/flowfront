# author: Furkan Cayci
# description: shows the flowfront
#   based on the given parameters

import numpy as np
from common import *
from lims_common import *
import matplotlib.pyplot as plt

BOARDSIZE = (0.2, 0.7) # board size in meters (y, x)
NODESIZE  = (11, 36)   # number of nodes in each direction (y, x)

#### Create target flowfront

# create coefficients
c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)

kxx = np.ones(NODESIZE[1]) * 1e-10

#kxx[int(kxx.size/2):] = 2e-12
kxx[5:] = 2e-12

# create permeability map instance
# elements can be accessed by p.kxx
#p = PMap(kxx=kxx, kyy=1e-10, kxy=1e-12, krt=1e-9)
p = PMap(kxx=kxx)
# randomize if needed
#p.randomize(lower=1e-14, upper=1e-8)

# set up the gates
# w  : west
# nw : north west
# sw : south west
gatenodes = set_gatenodes(NODESIZE, 'w')

# calculate target flow time
ft1, pr1 = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'target', gatenodes)
ft2 = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'target', gatenodes)
print('lims', ft1[0])
print('mine', ft2[0])
plt.plot(ft1[0], '-')
plt.plot(ft2[0], '.')
plt.show()
#show_img(ft)
