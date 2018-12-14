## Simplex 2D solver
import numpy as np
from common import *

if __name__ == "__main__":

    np.set_printoptions(precision=2)
    np.set_printoptions(suppress=True)
    DEBUG = False

    # parameters
    AREA = (0.2, 0.7)
    NUMBER_OF_NODES = (11, 36)
    dims = 2

    n_of_runs = 1
    avg_iter = []

    for t in range(n_of_runs):

        Starget = Stiffness(dim=dims, upper=1000, lower=900)
        C = Coeffs(dims)

        if DEBUG:
            print('choose kxx: {}, kyy: {}'.format(Starget.kx, Starget.ky))

        target = flowgen2d(NUMBER_OF_NODES, AREA, Starget, C)
        if DEBUG:
            print('target flowfront:', target)
            show_img(target)

        # solver
        ########

        # minimizing score (norm difference between vectors)
        score = 0
        prev_score = 0

        threshold = 0.1
        gammax = 0.9 # should be less than 1
        gammay = 0.9 # should be less than 1
        stiff = Stiffness(dim=dims, upper=1000)
        stiff_prev = Stiffness(dim=dims, upper=1)
        C = Coeffs(dims)
        deltakx = 0
        deltaky = 0
        maxscore = 0

        n_of_trials = 2000

        swaptime = 100
        xflag = True

        for trial in range(n_of_trials):
            if trial % swaptime == 0:
                xflag = not xflag

            # calculate the new flowfront
            # will be replaced with LIMS
            test = flowgen2d(NUMBER_OF_NODES, AREA, stiff, C)
            # save previous score
            prev_score = score
            # calculate new score
            score = l2norm(test, target)
            # normalize score based on the max we've seen.
            # so that deltakx doesn't blow up
            maxscore = max(score, maxscore)
            norm_score = np.sign(prev_score - score)  * (score / (0.1 + maxscore))
            if xflag:
                deltakx = np.sign(stiff_prev.kx - stiff.kx) * gammax * norm_score * stiff.kx
            else:
                deltaky = np.sign(stiff_prev.ky - stiff.ky) * gammay * norm_score * stiff.ky

            print("{:5}, ps: {:8.2f}, cs: {:8.2f}, kxx: {:14.6f}, kyy: {:14.6f}, dkxx: {:14.6f}, dkyy: {:14.6f}, norm_score: {:14.6f}".format(trial, prev_score, score, stiff.kx, stiff.ky, deltakx, deltaky, norm_score))

            if score < threshold:
                avg_iter.append(trial)
                print("{:5}: solved kx: {:14.6f}, ky: {:14.6f} in {:5} trials with threshold < {}".format(t, Starget.kx, Starget.ky, trial, threshold))
                break

            if xflag:
                stiff_prev.kx = stiff.kx
                stiff.kx = stiff.kx - deltakx
            else:
                stiff_prev.ky = stiff.ky
                stiff.ky = stiff.ky - deltaky

        else:
            print("FAIL: could not find... for kx: {}, ky: {}".format(Starget.kx, Starget.ky))
            print("{:5}, kxx: {:14.6f}, kyy: {:14.6f}, score: {:8.2f} -> {:8.2f}, deltakx: {:14.6f}, deltaky: {:14.6f}".format(trial, stiff.kx, stiff.ky, prev_score, score, deltakx, deltaky))
            break
    else:
        print("SUCCESS: solved {} runs with {} threshold achievement in average: {}".format(n_of_runs, threshold, np.mean(avg_iter)))

        #print("Target Combo:", target[0,:])
        # print("Winning Combo:", s[0,:])
