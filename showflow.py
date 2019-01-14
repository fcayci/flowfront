# author: Furkan Cayci
# description:

import numpy as np
from common import *
from lims_common import *

BOARDSIZE = (0.2, 0.7) # board size in meters (y, x)
NODESIZE  = (11, 36)   # number of nodes in each direction (y, x)

#### Create target flowfront

# create coefficients
c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)

# create permeability map instance
# elements can be accessed by p.kxx
#p = PMap(kxx=1e-10, kyy=1e-10, kxy=1e-12, krt=1e-9)
p = PMap(kxx=1e-10,  krt=1e-9, kyy=5e-11, kxy=5e-12)
# randomize if needed
#p.randomize(lower=1e-14, upper=1e-8)

# set up the gates
# w  : west
# nw : north west
# sw : south west
gatenodes = set_gatenodes(NODESIZE, 'w')

# calculate target flow time
ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'target', gatenodes)
print('lims', ft)
show_img(ft)
