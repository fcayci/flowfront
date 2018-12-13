import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from numpy import linalg as LA

DEBUG = True

# equation
# tfill = x**2 (mu * fi) / (2 * kxx * deltaP)

# parameters
x_length = 0.7
num_of_nodes_x = 36
num_of_nodes_y = 10
mu = 0.2
fi = 0.5
dP = 1E5
kxx = 1E-10
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)

def darcy(x, kxx):
    return x**2 * ((mu * fi) / (2 * kxx * dP))

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
#   this will be read from a csv file
target = np.zeros((num_of_nodes_y, num_of_nodes_x), dtype=np.float32)
target[:] = [    0.        ,     1.68067227 ,    6.72268908,    15.12605042,    26.8907563,
    42.01680672,    60.50420168 ,   82.35294118,   107.56302521,   136.13445378,
   168.06722689,   203.36134454 ,  242.01680672,   284.03361345,   329.41176471,
   378.1512605 ,   430.25210084 ,  485.71428571,   544.53781513,   606.72268908,
   672.26890756,   741.17647059 ,  813.44537815,   889.07563025,   968.06722689,
  1050.42016807,  1136.13445378 , 1225.21008403,  1317.64705882,  1413.44537815,
  1512.60504202,  1615.12605042 , 1721.00840336,  1830.25210084,  1942.85714286,
  2058.82352941]

if DEBUG:
    print('target flowfront:', target)

# solver
########

# gradient descent
# 1. perturb for direction
# 1. jump for faster converge
# kxx(t+1) = kxx(t) - gain * F(J)

# minimizing J (norm difference between vectors)
score = 0
prev_score = 0

gamma_l = 0.9
gamma_s = 0.05
kxx = 1E-10 # starting point
perturb = 0
gain = 0
diff_score = 0

n_of_steps = 10

for step in range(n_of_steps):
    # calculate the new s vectors
    for i, node in enumerate(nodes):
        s[:,i] = darcy(node, kxx)
    # save previous score
    prev_score = score
    # calculate new score
    score = l2norm(s, target)
    print("{:2}, prev score: {:8.2f}, curr score: {:8.2f}, kxx: {}".format(step, prev_score, score, kxx))
    if step % 2 == 0:
        # small perturb to figure out if going the correct direction
        perturb = gamma_s * kxx * (np.random.random() - 0.5)
        kxx = kxx - perturb
        if DEBUG:
            print("pert: {}, kxx: {}".format(perturb, kxx))

    else:
        # jump the direction
        diff_score = (score - prev_score) / max(score, prev_score)
        gain = gamma_l * perturb * diff_score
        kxx = kxx + gain
        if DEBUG:
            print("leap: {}, diff score: {}, kxx: {}".format(gain, diff_score, kxx))


print(s[0,:])
print(target[0,:])
