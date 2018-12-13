# read and show flowfront

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import pandas as pd

DEBUG = False
csv_file = "data2d.csv"

np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)

x_length = 0.7
num_of_nodes_x = 36
num_of_nodes_y = 10

df = pd.read_csv(csv_file)
flowfront = df.S4
target = np.array(flowfront)
target.resize(num_of_nodes_y, num_of_nodes_x)

nodes = np.linspace(0, x_length, num_of_nodes_x)
plt.imshow(target, cmap="tab20b", interpolation="bicubic", origin="upper")
plt.colorbar()
plt.show()
