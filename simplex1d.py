# Simplex 1D solver

import numpy as np
from common import *

if __name__ == "__main__":

    np.set_printoptions(precision=2)
    np.set_printoptions(suppress=True)
    DEBUG = False

    # parameters
    AREA = (0.2, 0.7)
    NUMBER_OF_NODES = (11, 36)
    dims = 1

    n_of_runs = 10000
    avg_iter = []

    for t in range(n_of_runs):

        Starget = Stiffness(dim=dims, upper=1000000, lower=1)
        C = Coeffs(dims)

        if DEBUG: print('choose kxx:', Starget.kx)

        target = flowgen1d(NUMBER_OF_NODES, AREA, Starget, C)
        if DEBUG:
            print('target flowfront:', target[0,:])
            show_img(target)

        # solver
        ########

        # minimizing score (norm difference between vectors)
        score = 0
        prev_score = 0

        threshold = 0.1
        gammax = 0.9 # should be less than 1
        stiff = Stiffness(dim=dims, upper=1000)
        stiff_prev = Stiffness(dim=dims, upper=1)
        deltakxx = 0
        maxscore = 0
        A=1

        n_of_trials = 20000

        for trial in range(n_of_trials):
            # calculate the new flowfront
            # will be replaced with LIMS
            test = flowgen1d(NUMBER_OF_NODES, AREA, stiff, C)
            # save previous score
            prev_score = score
            # calculate new score
            score = l2norm(test, target)
            # normalize score based on the max we've seen.
            # so that deltakxx doesn't blow up
            maxscore = max(score, maxscore)
            norm_score = np.sign(prev_score - score)  * (score / (0.1 + maxscore))
            deltakxx = np.sign(stiff_prev.kx - stiff.kx) * gammax * norm_score * stiff.kx
            #print("{:5},  kxx: {:14.6f}, score: {:8.2f} -> {:8.2f}, deltakxx: {:10.6f}".format(trial, stiff.kx, prev_score, score, deltakxx))

            if score < threshold:
                avg_iter.append(trial)
                print("{:5}: solved {:14.6f} in {:5} trials with threshold < {}".format(t, Starget.kx, trial, threshold))
                break

            stiff_prev.kx = stiff.kx
            stiff.kx = stiff.kx - deltakxx
        else:
            print("FAIL: could not find... for kxx: {}".format(Starget.kx))
            print("{:5}, kxx: {:14.6f}, score: {:8.2f} -> {:8.2f}, deltakxx: {:14.6f}".format(trial, stiff.kx, prev_score, score, deltakxx))
            break
    else:
        print("SUCCESS: solved {} runs with {} threshold achievement in average: {}".format(n_of_runs, threshold, np.mean(avg_iter)))

        #print("Target Combo:", target[0,:])
        # print("Winning Combo:", s[0,:])
