## 2D solver

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from numpy import linalg as LA

def darcy2d(x, y, kxx, kyy, A=1, B=1):
    return (x**2 * (A * kxx)) + (y**2 * (B * kyy))

def flowgen2d(x_length, y_length, num_of_nodes_x, num_of_nodes_y, kxx=1, kyy=1, A=1, B=1):

    nodes_x = np.linspace(0, x_length, num_of_nodes_x)
    nodes_y = np.linspace(0, y_length, num_of_nodes_y)

    # create one dimensional array
    s = np.zeros((num_of_nodes_y, num_of_nodes_x), dtype=float)

    for i, x in enumerate(nodes_x):
        for j, y in enumerate(nodes_y):
            s[j,i] = darcy2d(x, y, kxx, kyy)

    return s

def show_img(s):
    plt.imshow(s, cmap="tab20b", interpolation="bicubic", origin="lower")
    plt.colorbar()
    plt.show()

# get the l2 norm of matrices
def l2norm(x, y):
    return LA.norm(x-y)

np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)
DEBUG = True

x_length = 0.7
y_length = 0.2
num_of_nodes_x = 36
num_of_nodes_y = 11
A = 1
B = 1
kxx = 312.421
kyy = 100.7325

target = flowgen2d(x_length, y_length, num_of_nodes_x, num_of_nodes_y, kxx, kyy, A, B)

if DEBUG:
   print('target flowfront:', target)
   #show_img(target)

# solver
########

# minimizing score (norm difference between vectors)
score = 0
prev_score = 0

threshold = 1
gamma_xx = 0.4
gamma_yy = 0.2
kxx = 1 # starting point
kyy = 1 # starting point
prev_kxx = 0
prev_kyy = 0
deltakxx = 0
deltakyy = 0
maxscore = 0
A=1
B=1

nodes_x = np.linspace(0, x_length, num_of_nodes_x)
nodes_y = np.linspace(0, y_length, num_of_nodes_y)
s = np.zeros((num_of_nodes_y, num_of_nodes_x), dtype=float)

n_of_steps = 2000

for step in range(n_of_steps):
    # This part will be handed off to LIMS
    #   We will get the new s matrix in return
    # calculate the new s vectors
    for i, x in enumerate(nodes_x):
        for j, y in enumerate(nodes_y):
            s[j,i] = darcy2d(x, y, kxx, kyy, A, B)

    # save previous score
    prev_score = score
    # calculate new score
    score = l2norm(s, target)
    if score < threshold:
        print("Success: achieved threshold < {}".format(threshold))
        break

    # normalize score based on the max we've seen.
    # so that deltakxx doesn't blow up
    maxscore = max(score, maxscore)
    p_score = (score / (0.1 + maxscore))
    deltakxx = np.sign(prev_kxx - kxx) * kxx * gamma_xx * p_score
    deltakyy = np.sign(prev_kyy - kyy) * kyy * gamma_yy * p_score
    print("{:6}, ps: {:8.2f}, cs: {:8.2f}, kxx: {:14.6f}, kyy: {:14.6f}, dkxx: {:14.6f}, dkyy: {:14.6f}, p_score: {:14.6f}".format(step, prev_score, score, kxx, kyy, deltakxx, deltakyy, p_score))

    prev_kxx = kxx
    kxx = kxx - np.sign(prev_score - score) * deltakxx
    prev_kyy = kyy
    kyy = kyy - np.sign(prev_score - score) * deltakyy

else:
    print("FAIL: could not find...")

print("Target Combo:", target[5,:])
print("Winning Combo:", s[5,:])
