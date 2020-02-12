'''

Description:
------------

Usage:
------
  generate_defects.py -b <backend> -g <gatelocs>
    backends: LIMS, PYT
    gatelocs: w, n, s, nw, sw, mw
    -v for verbose
'''
import numpy as np
import sys, getopt

from libs.geometry import *
from libs.flowfront import *

def fill_around(x, y, kx, xsize, ysize):
    for i in range(xsize):
        for j in range(ysize):
            g.kxx[y+j, x+i] = kx
            g.kyy[y+j, x+i] = kx

try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:g:v')
except getopt.GetoptError:
    print(__doc__)
    sys.exit(2)

backend = 'LIMS'
gateloc = 'w'
verbose = False

# Update backend and gatelocs if parameters are passed
for o, a in opts:
    if o == '-b':
        backend = a
    if o == '-g':
        gateloc = a
    if o == '-v':
        verbose = True

# set geometry size and number of nodes (y, x)
g = Geometry(size=(0.2, 0.5), nodes=(21, 51))

# set the gate locations: w, nw, sw, ww
g.set_gatenodes(gateloc)

# set coefficients
g.set_coeffs(mu=0.1, fi=0.5, deltaP=1e5)

# set backend for flowfront calculation: PYT, LIMS
g.set_backend(backend)

kxx = 1 * 1e-11
kyy = 1 * 1e-11
kxy = 0
krt = 0

# defect list
klist = np.linspace(1e-10, 1e-8, 100)
# defect nodes
defx = 16
defy = 4
xsize = 5
ysize = 5
name = 'strength' + str(xsize) + 'x' + str(ysize) + '_' + str(defx) + '_' + str(defy) + '_'

for i, ki in enumerate(klist):
    g.set_permeability(kxx=kxx, kxy=kxy, kyy=kyy, krt=krt)
    fill_around(defx, defy, ki, xsize, ysize)
    n = '{}run{}_{:.1e}'.format(name, i+1, ki)
    g.get_flowfront(fname=n)
    #g.show_flowfront()
