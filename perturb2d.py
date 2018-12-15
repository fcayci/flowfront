import numpy as np
from common import *

if __name__ == "__main__":

    np.set_printoptions(precision=2)
    np.set_printoptions(suppress=True)
    DEBUG = False

    # parameters
    AREA = (0.2, 1.0)
    NUMBER_OF_NODES = (11, 36)
    dims = 2

    n_of_runs = 1
    avg_iter = []

    for t in range(n_of_runs):

        Starget = Stiffness(dim=dims, upper=1000, lower=1)
        Ctarget = Coeffs(dims)

        if DEBUG:
            print('choose kxx: {}, kyy: {}'.format(Starget.kx, Starget.ky))

        target = flowgen2d(NUMBER_OF_NODES, AREA, Starget, Ctarget)

        if DEBUG:
            print('target flowfront:', target)
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
        gamma_l = 1000 # 0.01 * NUMBER_OF_NODES[0] * NUMBER_OF_NODES[1]
        gamma_s = 60 # 0.6 * NUMBER_OF_NODES[0] * NUMBER_OF_NODES[1]
        stiff = Stiffness(dim=dims, upper=1)
        Ctest = Coeffs(dims)
        perturbx = 0
        perturby = 0
        gainx = 0
        gainy = 0
        maxscore = 0

        n_of_trials = 10000

        # keep optimization on single parameter
        # and swap parameters every so often (swaptime trial)
        swaptime = 4 * 15
        xflag = False

        for trial in range(n_of_trials):

            if trial % swaptime == 0:
                xflag = not xflag

            # calculate the new flowfront
            # will be replaced with LIMS
            test = flowgen2d(NUMBER_OF_NODES, AREA, stiff, Ctest)
            # save previous score
            prev_score = score
            # calculate new score
            score = l2norm(test, target)
            maxscore = max(score, maxscore)
            norm_score = (score / (0.1 + maxscore))
            print("{:5}, kxx: {:8.3f}, kyy: {:8.3f}, score: {:9.5f} -> {:9.5f}, norm_score: {:7.6f}, pertx: {: 2.4f}, gainx: {: 2.4f}, perty: {: 2.4f}, gainy: {: 2.4f}".format(trial, stiff.kx, stiff.ky, prev_score, score, norm_score, perturbx, gainx, perturby, gainy))

            if score < threshold:
                avg_iter.append(trial)
                print("{:5}: target kx: {:14.6f}, ky: {:14.6f}, {:.6f}, {:.6f}".format(trial, Starget.kx, Starget.ky, Ctarget.x, Ctarget.y))
                print("{:5}: solved kx: {:14.6f}, ky: {:14.6f}, {:.6f}, {:.6f} in {:5} trials with threshold < {}".format(trial, stiff.kx, stiff.ky, Ctest.x, Ctest.y, trial, threshold))
                show_img_on(test, target)
                break

            if trial % 2 == 0:
                # small perturb to figure out if going the correct direction
                if xflag:
                    perturbx = gamma_s * (np.random.random() - 0.5) * norm_score # * stiff.kx
                    stiff.kx = stiff.kx - perturbx
                else:
                    perturby = gamma_s * (np.random.random() - 0.5) * norm_score # * stiff.ky
                    stiff.ky = stiff.ky - perturby
                if DEBUG:
                    print("pertx: {}, perty: {}, kx: {}, ky: {}".format(perturbx, perturby, stiff.kx, stiff.ky))

            else:
                # jump the direction
                if xflag:
                    gainx = np.sign(perturbx) * gamma_l * np.sign(prev_score - score) * norm_score # * stiff.kx
                    stiff.kx = stiff.kx - gainx
                else:
                    gainy = np.sign(perturby) * gamma_l * np.sign(prev_score - score) * norm_score # * stiff.ky
                    stiff.ky = stiff.ky - gainy
                if DEBUG:
                    print("pertx: {}, perty: {}, kx: {}, ky: {}".format(gainx, gainy, stiff.kx, stiff.ky))

            #print("{:6}, ps: {:8.2f}, cs: {:8.2f}, kxx: {:14.6f}, kyy: {:14.6f}, pertx: {:10.4f}, perty: {:10.4f}, gainx: {:10.4f}, gainy: {:10.4f}, p_score: {:10.4f}".format(trial, prev_score, score, kxx, kyy, perturbx, perturby, gainx, gainy, p_score))

        else:
            print("FAIL: could not find... for kx: {}, ky: {}".format(Starget.kx, Starget.ky))
            print("{:5}, kxx: {:14.6f}, kyy: {:14.6f}, score: {:8.2f} -> {:8.2f}".format(trial, stiff.kx, stiff.ky, prev_score, score))
            break

    else:
        print("SUCCESS: solved {} runs with {} threshold achievement in average: {}".format(n_of_runs, threshold, np.mean(avg_iter)))

        #print("Target Combo:", target[0,:])
        # print("Winning Combo:", s[0,:])
