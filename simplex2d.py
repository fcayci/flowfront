## 2D solver

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from numpy import linalg as LA
import pandas as pd

DEBUG = True
csv_file = "data2d.csv"

# equation
# tfill = x**2 (mu * fi) / (2 * kxx * deltaP)

# parameters
x_length = 0.7
num_of_nodes_x = 36
num_of_nodes_y = 11
k1 = 25E-8 # mu * fi / 2 dP
k2 = 25E-10
kxx = 1E-10
kyy = 1E-10
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)


def darcy(x, kxx):
    return x**2 * (k1 / kxx)

def darcy2d(x, kxx, kyy):
    return (x**2 * (k1 / kxx)) + (k2 / kyy)

# get the l2 norm of matrices
def l2norm(x, y):
    return LA.norm(x-y)

# create node locations
nodes = np.linspace(0, x_length, num_of_nodes_x)
if DEBUG:
    print('node locations:', nodes)

# create two dimensional array
s = np.zeros((num_of_nodes_y, num_of_nodes_x), dtype=np.float32)

# This is the target array to get to.
# For now this requires hardcoded dimensions
df = pd.read_csv(csv_file)
flowfront = df.S2
target = np.array(flowfront)
target.resize(num_of_nodes_y, num_of_nodes_x)

if DEBUG:
   print('target flowfront:', target)

# solver
########

# minimizing score (norm difference between vectors)
score = 0
prev_score = 0

threshold = 1
gamma_xx = 0.6
gamma_yy = 0.2
kxx = 1E-10 # starting point
kyy = 1E-10 # starting point
prev_kxx = 0
prev_kyy = 0
maxscore = 0

n_of_steps = 1000

for step in range(n_of_steps):
    # calculate the new s vectors
    for i, node in enumerate(nodes):
        s[:,i] = darcy2d(node, kxx, kyy)
    # save previous score
    prev_score = score
    # calculate new score
    score = l2norm(s[5], target[5])
    if score < threshold:
        print("Success: achieved threshold < {}".format(threshold))
        break
    # normalize score based on the max we've seen.
    # so that deltakxx doesn't blow up
    maxscore = max(score, maxscore)
    deltakxx = np.sign(prev_kxx - kxx) * kxx * gamma_xx * (score / (0.1 + maxscore))
    deltakyy = np.sign(prev_kyy - kyy) * kyy * gamma_yy * (score / (0.1 + maxscore))
    print("{:2}, ps: {:8.2f}, cs: {:8.2f}, kxx: {}, kyy: {}".format(step, prev_score, score, kxx, kyy))

    prev_kxx = kxx
    prev_kyy = kyy
    kxx = kxx - np.sign(prev_score - score) * deltakxx
    kyy = kyy + np.sign(prev_score - score) * deltakyy
else:
    print("FAIL: could not find...")

print("Target Combo:", target[5,:])
print("Winning Combo:", s[5,:])
