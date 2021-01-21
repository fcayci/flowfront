"""
2D Box example with a given defect

Description
-----------
Creates a 2D mesh with the predefined length and node sizes.
Shows how to add defects to given locations.

"""

import numpy as np
import sys, getopt

from lims.lims_wrapper import get_flowtime as lims
from libs.mesh import *
from common.plots import *

# Gate location is in the west
# Can be mw for single middle west node
gateloc = 'w'

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

# Individual cells can be changed by passing x and/or y parameters
#m.set_kxx(3e-10, x=5) # all cells with x = 5
#m.set_kyy(4e-10, y=3) # all cells with y = 3
#m.set_kyy(5e-10, x=5, y=8) # cell with x = 5, y = 8
m.set_kxx(4e-10, x=5, y=3, rx=2, ry=1) # rx = 2, ry = 1 (2x1 cell)

# all the values can be passed using single call
m.set_kall(kxx=3e-10, kyy=4e-10, kxy=2e-11, x=12, y=6, rx=2, ry=2)

m.run('box2d_defect')
m.show_flowfront()
m.show_kmaps()

