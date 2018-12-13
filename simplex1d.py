import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from numpy import linalg as LA

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

# get the l2 norm of matrices
def l2norm(x, y):
    return LA.norm(x-y)

np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)
DEBUG = True

x_length = 0.7
num_of_nodes_x = 36
num_of_nodes_y = 10
A = 1
B = 1
kxx = 124.319

target = flowgen1d(x_length, num_of_nodes_x, num_of_nodes_y, kxx, A)

if DEBUG:
   print('target flowfront:', target)
   #show_img(target)

# solver
########

# minimizing score (norm difference between vectors)
score = 0
prev_score = 0

threshold = 1
gamma = 0.2 # should be less than 1
kxx = 1 # starting point
prev_kxx = 0
deltakxx = 0
maxscore = 0
A=1

nodes = np.linspace(0, x_length, num_of_nodes_x)
s = np.zeros((num_of_nodes_y, num_of_nodes_x), dtype=float)

n_of_steps = 1000

for step in range(n_of_steps):
    # calculate the new s vectors
    for i, node in enumerate(nodes):
        s[:,i] = darcy1d(node, kxx, A)
    # save previous score
    prev_score = score
    # calculate new score
    score = l2norm(s, target)
    if score < threshold:
        print("SUCCESS: achieved threshold < {}".format(threshold))
        break
    # normalize score based on the max we've seen.
    # so that deltakxx doesn't blow up
    maxscore = max(score, maxscore)
    deltakxx = np.sign(prev_kxx - kxx) * kxx * gamma * (score / (0.1 + maxscore))
    print("{:2}, ps: {:8.2f}, cs: {:8.2f}, kxx: {:14.6f}, dkxx: {:14.6f}".format(step, prev_score, score, kxx, deltakxx))

    prev_kxx = kxx
    kxx = kxx - np.sign(prev_score - score) * deltakxx
else:
    print("FAIL: could not find...")

print("Target Combo:", target[0,:])
print("Winning Combo:", s[0,:])
