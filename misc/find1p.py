'''1 parameter optimization for kxx only

Description:
------------
  find the kxx value

Usage:
------
  find1p.py -b <backend> -g <gatelocs>
    backends: LIMS, PYT
    gatelocs: w, n, s, nw, sw, mw
    -v for verbose
'''

import numpy as np
import sys, getopt
import copy
import logging

from libs.geometry import *
from libs.flowfront import *
from libs.gss_solver import *

logging.basicConfig(format='%(message)s')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:g:v:n')
except getopt.GetoptError:
    print(__doc__)
    sys.exit(2)

backend = 'LIMS'
gateloc = 'mw'
num_of_trials = 1000
verbose = False
normbase = 1e-14

for o, a in opts:
    if o == '-b':
        backend = a
    if o == '-g':
        gateloc = a
    if o == '-v':
        verbose = True
    if o == '-n':
        num_of_trials = a

# create target geometry
target = Geometry(size=(0.2, 0.4), nodes=(11, 21))
target.set_gatenodes(gateloc)
target.set_coeffs(mu=0.1, fi=0.5, deltaP=1e5)
target.set_backend(backend)

s = Solver()
s.set_target_gemoetry(target)

# assign a random target kxx value
# first multiplicand is there to give 0 - 1 multiplication.
# second multiplicand is to give power 1, 10, 100, ... 1e7 multiplication
# last multiplicand is the base.
kxx = np.random.random() * np.power(1e1, np.random.uniform(1, 7)) * normbase
print('Target kxx:', kxx)
target.set_permeability(kxx=kxx)
target.get_flowfront('target')

s.set_target_flowtime(target.ft)

s.solve()
