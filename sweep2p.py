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

backend = 'LIMS'
gateloc = 'mw'
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
xsamples = 100
ysamples = 10
kx_list = np.logspace(-14, -8, xsamples)
ky_list = np.logspace(-14, -8, ysamples)

target = Geometry(size=(0.2, 0.4), nodes=(11, 21))
target.set_gatenodes(gateloc)
target.set_coeffs(mu=0.1, fi=0.5, deltaP=1e5)
target.set_backend(backend)

# deep copy target geometry
trial = copy.deepcopy(target)

kxx = np.random.uniform(1, 1e6) * 1e-14
print('Target kxx:', kxx)
kyy = np.random.uniform(1, 1e6) * 1e-14
print('Target kyy:', kyy)
kxy = np.sqrt(kxx * kyy) - kxx
print('Target kxy:', kxy)
target.set_permeability(kxx=kxx, kyy=kyy, kxy=kxy)
target.get_flowfront('target')

if verbose:
    print('Target flowfront:')
    target.print_filltime()

costs = np.ndarray((xsamples, ysamples))
for i, kx in enumerate(kx_list):
    for j, ky in enumerate(ky_list):
        trial.set_permeability(kxx=kx, kyy=ky, kxy=np.sqrt(kx*ky)/2)
        trial.get_flowfront('trial')
        cost = np.linalg.norm(target.ft - trial.ft, 2)
        costs[i, j] = cost
        print('#', end='')

# hacky way to get the 2 precision numbers from the array to display...
#xpts = np.arange(0, xsamples, xsamples//10)
#labels = np.array2string(k_list[xpts], precision=2).strip('][').split(' ')

#print(costs)
plt.imshow(costs)
plt.colorbar()
#plt.semilogy(costs)
plt.title('2 parameter sweep on kxx and kyy for target kxx={:4.3e} and kyy={:4.3e}'.format(target.kxx[0,0], target.kyy[0,0]))
#plt.xlabel('kxx')
#plt.xticks(xpts, labels, rotation=30)
#plt.ylabel('cost (l2norm of target and calculated flowfronts)')
plt.xlabel('kyy')
plt.ylabel('kxx')
plt.show()
