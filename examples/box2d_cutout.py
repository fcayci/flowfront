"""
2D box with a cutout

Description
-----------
Creates a 2D mesh with the predefined length and node sizes.
Shows how to create cutouts in the mesh.

"""

import numpy as np
import sys, getopt

from libs.mesh import *

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

# Create a cutout 3x5 cells from 5,2 origin
m.delete_cells(x=5, y=2, rx=3, ry=5)
# Create a cutout 3x3 cell from 10,3 origin
m.delete_cells(x=10, y=3, rx=3, ry=3)


m.run('box2d_cutout')
m.show_flowfront()

