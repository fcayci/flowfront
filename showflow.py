"""
Show flowfront for given permeability values

Description
-----------
  display flowfront for given permeability values.

Usage
-----
  showflow.py -g <gatelocs>
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


deltaP = 1e5
size = (.2, .4)
nodes = (11, 21)
m = Mesh(size, nodes)
m.create_mesh()
m.set_gate_nodes(gateloc, dP=deltaP)

# Set all cells to the same values
m.set_kxx(1e-11)
m.set_kxy(4e-12)
m.set_kyy(2e-11)

# Individual cells can be changed by passing x and/or y parameters
#m.set_kxx(3e-10, x=5) # all cells with x = 5
#m.set_kyy(4e-10, y=3) # all cells with y = 3
#m.set_kyy(5e-10, x=5, y=8) # cell with x = 5, y = 8
m.set_kxx(4e-10, x=5, y=3, rx=2) # rx = 2

# all the values can be passed using single call
m.set_kall(kxx=3e-10, kyy=4e-10, kxy=2e-11, x=5, y=8, rx=2, ry=2)

# Delete 3x5 cells from 5,2 origin
#m.delete_cells(x=5, y=2, rx=3, ry=5)
# Delete 3x3 cell from 10,3 origin
#m.delete_cells(x=10, y=3, rx=3, ry=3)


m.run('run2')
m.show_flowfront()
m.show_kmaps()
#m.plot_filltime()
#m.plot_pressure()

