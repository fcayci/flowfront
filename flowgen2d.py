# generate and show flowfront for 2D

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

def darcy2d(x, y, kxx, kyy, A=1, B=1):
    return (x**2 * (A * kxx)) + (y**2 * (B * kyy))

def flowgen2d(x_length, y_length, num_of_nodes_x, num_of_nodes_y, kxx=1, kyy=1, A=1, B=1):

    s = np.zeros((num_of_nodes_y, num_of_nodes_x), dtype=float)

    nodes_x = np.linspace(0, x_length, num_of_nodes_x)
    nodes_y = np.linspace(0, y_length, num_of_nodes_y)
    for i, x in enumerate(nodes_x):
        for j, y in enumerate(nodes_y):
            s[j,i] = darcy2d(x, y, kxx, kyy, A, B)

    return s

def show_img(s):
    plt.imshow(s, cmap="tab20b", interpolation="bicubic", origin="lower")
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
    x_length = 0.7
    y_length = 0.2
    num_of_nodes_x = 36
    num_of_nodes_y = 10
    A = 1
    B = 1
    kxx = 1
    kyy = 0.6

    s = flowgen2d(x_length, y_length, num_of_nodes_x, num_of_nodes_y, kxx, kyy, A, B)
    show_img(s)
