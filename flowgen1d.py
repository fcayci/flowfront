# generate and show flowfront for 1D

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

# darcy equation
# tfill = x**2 (mu * fi) / (2 * kxx * deltaP)

DEBUG = False

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

# parameters
x_length = 0.7
num_of_nodes_x = 36
num_of_nodes_y = 10
mu = 0.2
fi = 0.5
dP = 1E5
kxx = 1.19E-10


def darcy(x, kxx):
    return x**2 * ((mu * fi) / (2 * kxx * dP))

nodes = np.linspace(0, x_length, num_of_nodes_x)
if DEBUG:
    print('generated {} nodes: '.format(nodes.shape), nodes)

# create one dimensional array
s = np.zeros((num_of_nodes_y, num_of_nodes_x), dtype=float)

for i, node in enumerate(nodes):
    s[:,i] = darcy(node, kxx)

print('arrival times at each node:', s[0,:])

plt.imshow(s, cmap="plasma", interpolation="nearest", origin="upper")
plt.colorbar()
plt.show()

#####
#fig, ax = plt.subplots()
#im = ax.imshow(s, cmap="plasma", interpolation="nearest", origin="lower")
#ax.set_xticks(np.arange(num_of_nodes_x))
#ax.set_xticklabels(s[0,:])
#plt.setp(ax.get_xticklabels(),rotation = 90)
