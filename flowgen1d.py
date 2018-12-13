# generate and show flowfront for 1D

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

def darcy1d(x, kxx, A=1):
    return x**2 * (A * kxx)

def flowgen1d(x_length, num_of_nodes_x, num_of_nodes_y, kxx=1, A=1):

    s = np.zeros((num_of_nodes_y, num_of_nodes_x), dtype=float)

    nodes_x = np.linspace(0, x_length, num_of_nodes_x)
    for i, x in enumerate(nodes_x):
        s[:,i] = darcy1d(x, kxx, A)

    return s

def show_img(s):
    plt.imshow(s, cmap="tab20b", interpolation="bicubic", origin="lower")
    plt.colorbar()
    plt.show()

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

if __name__ == "__main__":
    x_length = 0.7
    num_of_nodes_x = 36
    num_of_nodes_y = 10
    A = 1
    B = 1
    kxx = 124.319

    s = flowgen1d(x_length, num_of_nodes_x, num_of_nodes_y, kxx, A)
    show_img(s)
