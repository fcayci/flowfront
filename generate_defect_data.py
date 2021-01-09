"""
Generate random defect data

Description
-----------
Generates random defect data for training purposes

Usage
-----
generate_defects.py -g <gatelocs>

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

rng = np.random.default_rng()

N = 100
defradius = 1
ynodes = 21
xnodes = 51

name = ''
name += str(xnodes) + 'x' + str(ynodes) + '_'
name += 'rad_' + str(defradius)

deltaP = 1e5
size = (.2, .5)
nodes = (ynodes, xnodes)
m = Mesh(size, nodes)
m.create_mesh()
m.set_gate_nodes(gateloc, dP=deltaP)


fts = []
ns = []

for i in range(N):

    # Set all cells to the same values
    m.set_kall(kxx=1e-11, kyy=1e-11, kxy=1e-12)

    # Generate random numbers
    k  = rng.lognormal() * 1e-10
    kp = rng.lognormal() * 1e-10
    x = rng.integers(1, xnodes)
    y = rng.integers(1, ynodes)

    if k < kp:
        temp = k
        k = kp
        kp = temp

    # Update permeabilities for random nodes with defradius
    m.set_kall(kxx=k, kyy=k, kxy=kp, x=x, y=y, r=defradius)

    # Run lims
    n = '{}_dx_{}_dy_{}_kx_{:.3f}_ky_{:.3f}_kxy_{:.3f}'.format(name, x, y, k*1e12, k*1e12, kp*1e12)
    m.run('run')

    fts.append(m.ft)
    ns.append(n)

    # Comment out to only generate
    #m.show_kmaps()
    #m.show_flowfront()
    #m.save(n)

sd = dict()

for i, n in enumerate(ns):
    sd[n] = fts[i]

np.savez("runs/def1.npz", **sd)
