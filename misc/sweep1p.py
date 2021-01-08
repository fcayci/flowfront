'''cost function plotter for 1 permeability value (kxx)

Description:
------------
  sets a random kxx based target flowfront,
  then iterates through the given boundaries for
  search kxx and plots the resulting cost functions

Usage:
------
  test_sweep1p.py -b <backend> -w <gatelocs>
    backends: LIMS, PYT
    gatelocs: w, n, s, nw, sw, ww
    -v for verbose
'''

import sys, getopt
import numpy as np
import matplotlib.pyplot as plt
import copy

from libs.geometry import *
from libs.flowfront import *

try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:w:v')
except getopt.GetoptError:
    print(__doc__)
    sys.exit(2)

backend = 'PYT'
gateloc = 'w'
verbose = False

# Update backend and gatelocs if parameters are passed
for o, a in opts:
    if o == '-b':
        backend = a
    if o == '-w':
        gateloc = a
    if o == '-v':
        verbose = True

 # create array of values for kxx testing
xsamples = 101
kxx_list = np.logspace(-14, -8, xsamples)

target = Geometry(size=(0.2, 0.4), nodes=(11, 21))
target.set_gatenodes(gateloc)
target.set_coeffs(mu=0.1, fi=0.5, deltaP=1e5)
target.set_backend(backend)

# deep copy target geometry
trial = copy.deepcopy(target)

kxx = np.random.uniform(1, 100) * 1e-12
print('Target kxx:', kxx)
target.set_permeability(kxx=kxx)
target.get_flowfront('target')

if verbose:
    print('Target flowfront:')
    target.print_filltime()

costs = []
for k in kxx_list:
    trial.set_permeability(kxx=k)
    trial.get_flowfront('trial')
    cost = np.linalg.norm(target.ft - trial.ft, 2)
    costs.append(cost)

# hacky way to get the 2 precision numbers from the array to display...
xpts = np.arange(0, xsamples, xsamples//10)
labels = np.array2string(kxx_list[xpts], precision=2).strip('][').split(' ')

plt.semilogy(costs)
plt.title('1 parameter sweep on kxx for target kxx_t={:4.3e}'.format(target.kxx[0,0]))
plt.xlabel('kxx')
plt.xticks(xpts, labels, rotation=30)
plt.ylabel('cost (l2norm of target and calculated flowfronts)')
plt.show()
