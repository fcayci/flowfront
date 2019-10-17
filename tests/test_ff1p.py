"""Test flowfront for single permeability value (kxx)

Description:
------------
  creates a kxx based flowfront with the given inlet
  locations. Then assigns a kxx value and a single
  defact to test the flowfront.

  Plots the results

Usage:
------
  test_ff1p.py -b <backend> -w <nodelocs>
    backends: LIMS, PYT
    nodelocs: w, n, s, nw, sw, ww
    -v for verbose
"""
import numpy as np
import sys, getopt

from libs.geometry import *
from libs.flowfront import *

try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:w:v')
except getopt.GetoptError:
    print(__doc__)
    sys.exit(2)

backend = None
nodeloc = None
verbose = False
for o, a in opts:
    if o == '-b':
        backend = a
    if o == '-w':
        nodeloc = a
    if o == '-v':
        verbose = True

if backend is None:
    backend = 'PYT'
if nodeloc is None:
    nodeloc = 'w'

#for opt, arg in opts:

# set geometry size and number of nodes (y, x)
g = Geometry(size=(0.2, 0.4), nodes=(11, 21))
#g.test() # Auto test

# set the gate locations: w, nw, sw, ww
g.set_gatenodes(nodeloc)

# set coefficients
g.set_coeffs(mu=0.1, fi=0.5, deltaP=1e5)

# set backend for flowfront calculation: PYT, LIMS
g.set_backend(backend)

# create a uniform kxx array
kxx = np.random.uniform(1, 100) * 1e-11
# set permeability of the geometry
g.set_permeability(kxx=kxx)
# create and place a signal defect point
defx = np.random.randint(3, g.xnodes)
defy = np.random.randint(3, g.ynodes)
print('placed defect on: x:{} and y:{} nodes'.format(defx, defy))
g.kxx[defx, defy] = np.random.uniform(1, 100) * 1e-13

# calculate flowfront
g.get_flowfront()

# print flowfront
if verbose:
    g.print_flowfront()

# display flowfront and fill times
g.show_flowfront()
g.plot_filltimes(showlegend=True)
