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

    n_of_runs = 100
    avg_iter = []

    for t in range(n_of_runs):

        Starget = Stiffness(dim=dims, upper=1000, lower=1)
        C = Coeffs(dims)

        if DEBUG: print('choose kxx:', Starget.kx)

        target = flowgen1d(NUMBER_OF_NODES, AREA, Starget, C)
        if DEBUG:
            print('target flowfront:', target[0,:])
            show_img(target)

        # solver
        ########

        # gradient descent
        # 1. perturb for direction
        # 1. jump for faster converge
        # kxx(t+1) = kxx(t) - gain * F(J)

        # minimizing J (norm difference between vectors)
        score = 0
        prev_score = 0
        norm_score = 0

        threshold = 0.1
        gamma_l = 2000
        gamma_s = 0.6
        stiff = Stiffness(dim=dims, upper=1)
        C = Coeffs(dims)
        perturb = 0
        gain = 0
        maxscore = 0

        n_of_trials = 1000

        for trial in range(n_of_trials):

            # calculate the new flowfront
            # will be replaced with LIMS
            test = flowgen1d(NUMBER_OF_NODES, AREA, stiff, C)
            # save previous score
            prev_score = score
            # calculate new score
            score = l2norm(test, target)
            maxscore = max(score, maxscore)
            norm_score = np.sign(prev_score - score)  * (score / (0.1 + maxscore))
            #print("{:5},  kxx: {:14.6f}, score: {:8.2f} -> {:8.2f},norm_score: {:10.6f}, perturb: {: 2.4f}, gain: {: 2.4f}".format(trial, stiff.kx, prev_score, score, norm_score, perturb, gain))

            if score < threshold:
                avg_iter.append(trial)
                print("{:5}: solved {:14.6f} in {:5} trials with threshold < {}".format(t, Starget.kx, trial, threshold))
                break

            if trial % 2 == 0:
                # small perturb to figure out if going the correct direction
                perturb = gamma_s * (np.random.random() - 0.5) * norm_score # * stiff.kx
                stiff.kx = stiff.kx - perturb
                if DEBUG:
                    print("pert: {}, kxx: {}".format(perturb, stiff.kx))

            else:
                # jump the direction
                gain = np.sign(perturb) * gamma_l * norm_score # * stiff.kx
                stiff.kx = stiff.kx - gain
                if DEBUG:
                    print("leap: {}, kxx: {}".format(gain, stiff.kx))

        else:
            print("FAIL: could not find... for kxx: {}", Starget.kx)
            print("{:5}, kxx: {:14.6f}, score: {:8.2f} -> {:8.2f}, norm_score: {:14.6f}".format(trial, stiff.kx, prev_score, score, norm_score))
            break
    else:
        print("SUCCESS: solved {} runs with {} threshold achievement in average: {} trials".format(n_of_runs, threshold, np.mean(avg_iter)))

        #print("Target Combo:", target[0,:])
        #print("Winning Combo:", test[0,:])