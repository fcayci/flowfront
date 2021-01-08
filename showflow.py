""" Show flowfront for given permeability values

Description:
------------
  display flowfront for given permeability values.

Usage:
------
  showflow.py -b <backend> -g <gatelocs>
    backends: LIMS, PYT
    gatelocs: w, n, s, nw, sw, mw
    -v for verbose
"""

import numpy as np
import sys, getopt

from lims.lims_wrapper import get_flowtime as lims
from libs.mesh import *
from common.plots import *


try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:g:v')
except getopt.GetoptError:
    print(__doc__)
    sys.exit(2)

gateloc = 'w'

# Update backend and gatelocs if parameters are passed
for o, a in opts:
    if o == '-b':
        backend = a
    if o == '-g':
        gateloc = a


if __name__ == "__main__":

    size = (.2, .4)
    nodes = (11, 21)
    m = Mesh(size, nodes)
    m.create_mesh()
    #g.set_coeffs(mu=0.1, fi=0.5, deltaP=1e5)
    m.set_gate_nodes(gateloc)
    # Set all cells to the same values
    m.set_kxx(1e-10)
    m.set_kxy(4e-11)
    m.set_kyy(2e-10)
    # Individual cells can be changed by passing cell parameter
    #m.set_kxx(1e-10, cell=3)
    #krt = 5 * 1e-9

    ft, pr = lims(m, 'run2')

    plot_filltime(ft)
    show_flowfront(ft)
    plot_pressure(pr)
