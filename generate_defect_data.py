"""
Generate random defect data

Description
-----------
Generates random defect data for training purposes

Usage
-----
generate_defects.py -g <gatelocs>

gatelocs: w, n, s, nw, sw, mw

"""

import numpy as np
import sys, getopt

from lims.lims_wrapper import get_flowtime as lims
from libs.mesh import *
from common.plots import *


try:
    opts, args = getopt.getopt(sys.argv[1:], 'g')
except getopt.GetoptError:
    print(__doc__)
    sys.exit(2)

gateloc = 'w'

# Update backend and gatelocs if parameters are passed
for o, a in opts:
    if o == '-g':
        gateloc = a

defradius = 1
ynodes = 21
xnodes = 51

deltaP = 1e5
size = (.2, .5)
nodes = (ynodes, xnodes)
m = Mesh(size, nodes)
m.create_mesh()
m.set_gate_nodes(gateloc, dP=deltaP)

# defect list
klist = np.logspace(-10, -8, 1)

name = 'def1_' + str(defradius) + 'x' + str(defradius) + '_'

rng = np.random.default_rng()

# import matplotlib.pyplot as plt
# a = [rng.lognormal() * 1e-10 for i in range(1000)]
# plt.loglog(a)
# plt.show()
# raise

for i, ki in enumerate(klist):
    # Set all cells to the same values
    m.set_kxx(1e-11)
    m.set_kxy(4e-13)
    m.set_kyy(1e-11)
    r = rng.lognormal() * 1e-10
    x = rng.integers(1, xnodes)
    y = rng.integers(1, ynodes)
    m.set_kxx(r, x, y, defradius)
    m.set_kyy(r, x, y, defradius)
    n = '{}run{:04}_{:.1e}'.format(name, i+1, ki)
    m.run(n)
    m.show_kmaps()
    m.show_flowfront()

