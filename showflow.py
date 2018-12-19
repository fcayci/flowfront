# author: Furkan Cayci
# description:

import numpy as np
from common import *
from lims_common import *

BOARDSIZE = (0.2, 0.7) # board size in meters (y, x)
NODESIZE = (11, 36) # number of nodes in each direction (y, x)

#### Create target flowfront

# create coefficients
c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)

# create permeability map instance
# elements can be accessed by p.kxx
p_t = PMap(kxx=1e-10, kyy=1e-10)
# randomize if needed
#p_t.randomize()

# create gate locations
gatelocs = set_gatenodes(NODESIZE, 'sw')
# calculate target flow time
ft_l = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'run1', gatelocs)
#ft_p = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'run1', gatelocs)
print('lims', ft_l)
#print('pith', ft_p)
show_img(ft_l)
#show_img(ft_p)
#show_imgs(ft_l, ft_p)
