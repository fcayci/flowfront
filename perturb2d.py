import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from numpy import linalg as LA
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
DEBUG = False

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

# gradient descent
# 1. perturb for direction
# 1. jump for faster converge
# kxx(t+1) = kxx(t) - gain * F(J)

# minimizing J (norm difference between vectors)
score = 0
prev_score = 0

threshold = 1
gamma_l = 20
gamma_s = 1.4
kxx = 1 # starting point
kyy = 1 # starting point
prev_kxx = 0
prev_kyy = 0
perturbx = 0
perturby = 0
gainx = 0
gainy = 0
diff_score = 0
maxscore = 0
A = 1
B = 1

nodes_x = np.linspace(0, x_length, num_of_nodes_x)
nodes_y = np.linspace(0, y_length, num_of_nodes_y)
s = np.zeros((num_of_nodes_y, num_of_nodes_x), dtype=float)

n_of_steps = 10

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
    if score < 0.01:
        maxscore = 1
    elif score < 1:
        maxscore = 10
    maxscore = max(score, maxscore)
    p_score = np.sign(score - prev_score) * (score / (0.1 + maxscore))
    print("{:6}, ps: {:8.2f}, cs: {:8.2f}, kxx: {:14.6f}, kyy: {:14.6f}, p_score: {:14.6f}".format(step, prev_score, score, kxx, kyy, p_score))

    if score < threshold:
        print("SUCCESS: achieved threshold < {}".format(threshold))
        break

    if step % 2 == 0:
        # small perturb to figure out if going the correct direction
        perturbx = gamma_s * kxx * (np.random.random() - 0.5) * p_score
        kxx = kxx - perturbx
        perturby = gamma_s * kyy * (np.random.random() - 0.5) * p_score
        kyy = kyy - perturby
        if DEBUG:
            print("pertx: {}, perty: {}, kxx: {}, kyy: {}".format(perturbx, perturby, kxx, kyy))

    else:
        # jump the direction
        #diff_score = (score - prev_score) / max(score, prev_score)
        gainx = gamma_l * perturbx * p_score #diff_score
        kxx = kxx + gainx
        gainy = gamma_l * perturby * p_score #diff_score
        kyy = kyy + gainy
        if DEBUG:
            print("leapx: {}, leapy: {}, kxx: {}, kyy: {}".format(gainx, gainy, kxx, kyy))

else:
    print("FAIL: could not find...")

print("Target Combo:", target[0,:])
print("Winning Combo:", s[0,:])