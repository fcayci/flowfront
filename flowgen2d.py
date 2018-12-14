# generate and show flowfront for 2D

from common import *
import numpy as np

if __name__ == "__main__":

    np.set_printoptions(precision=3)
    np.set_printoptions(suppress=True)

    # parameters
    AREA = (0.2, 0.7)
    NUMBER_OF_NODES = (11, 36)

    Scur = Stiffness(dim=2, r=1000)
    C = Coeffs(2)

    s = flowgen2d(NUMBER_OF_NODES, AREA, Scur, C)
    show_img(s)