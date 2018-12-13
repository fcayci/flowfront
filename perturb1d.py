import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
from numpy import linalg as LA
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
DEBUG = False

x_length = 0.7
num_of_nodes_x = 2600
num_of_nodes_y = 100
A = 1
B = 1

n_of_runs = 100

for t in range(n_of_runs):

    kxx = (np.random.random() + 1) * 100
    if DEBUG:
        print('choose kxx:', kxx)

    target = flowgen1d(x_length, num_of_nodes_x, num_of_nodes_y, kxx, A)

    if DEBUG:
        print('target flowfront:', target[0,:])
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

    threshold = 0.001
    gamma_l = 0.7
    gamma_s = 0.2
    kxx = 1 # starting point
    prev_kxx = 0
    perturb = 0
    gain = 0
    diff_score = 0
    maxscore = 0
    A = 1

    nodes = np.linspace(0, x_length, num_of_nodes_x)
    s = np.zeros((num_of_nodes_y, num_of_nodes_x), dtype=float)

    n_of_steps = 200

    for step in range(n_of_steps):
        # calculate the new s vectors
        for i, node in enumerate(nodes):
            s[:,i] = darcy1d(node, kxx, A)
        # save previous score
        prev_score = score
        # calculate new score
        score = l2norm(s, target)
        maxscore = max(score, maxscore)
        p_score = np.sign(prev_score - score)  * (score / (0.1 + maxscore))
        #print("{:2}, ps: {:8.2f}, cs: {:8.2f}, kxx: {:14.6f}, p_score: {:14.6f}".format(step, prev_score, score, kxx, p_score))

        if score < threshold:
            print("SUCCESS: solved in {} steps with threshold < {}".format(step, threshold))
            break

        if step % 2 == 0:
            # small perturb to figure out if going the correct direction
            perturb = gamma_s * kxx * (np.random.random() - 0.5) * p_score
            kxx = kxx - perturb
            if DEBUG:
                print("pert: {}, kxx: {}".format(perturb, kxx))

        else:
            # jump the direction
            #diff_score = (score - prev_score) / max(score, prev_score)
            gain = np.sign(perturb) * gamma_l * kxx * p_score #diff_score
            kxx = kxx - gain
            if DEBUG:
                print("leap: {}, diff score: {}, kxx: {}".format(gain, diff_score, kxx))
    else:
        print("FAIL: could not find...")
        break
else:
    print("SUCCESS: solved {} runs with {} threshold achievement".format(n_of_runs, threshold))

    #print("Target Combo:", target[0,:])
    #print("Winning Combo:", s[0,:])