"""
Show flowfront for given permeability values

Description
-----------
Creates a 2D mesh with the predefined length and node sizes.
Runs LIMS and displays the flowfront along with kmaps (kxx, kyy, kxy) and
pressure

Usage
-----

Optinally pass argument `-g` for gatelocs. Possible values are: w, n, s, nw, sw, mw

>>> box2d.py -g <gatelocs>

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


deltaP = 1e5

# (y, x) distance
size = (.2, .4)
# (y, x) node size
nodes = (11, 21)

m = Mesh(size, nodes)
m.create_mesh()
m.set_gate_nodes(gateloc, dP=deltaP)

# Set all cells to the same values
m.set_kxx(1e-11)
m.set_kxy(4e-12)
m.set_kyy(2e-11)

m.run('run2')
m.show_flowfront()
m.show_kmaps()
m.plot_filltime()
m.plot_pressure()

