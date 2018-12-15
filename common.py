class Stiffness():
    """Stiffness class that holds kx / ky / kz / kr coeffs"""

    def __init__(self, dim=2, upper=1000, lower=1E-10):
        """
        dim: optional dimension parameter to decide which coeffs to create.
        r: randomization upper limit upon initialization, if 0 is given, creates with 1
        """

        self.dim = dim
        if dim >= 1: self.kx = randomize(lower, upper)
        if dim >= 2: self.ky = randomize(lower, upper)
        if dim >= 3: self.kz = randomize(lower, upper)
        if dim >= 4: self.kr = randomize(lower, upper)

    def randomize(self, upper=1000, lower=1E-10):
        """randomize coeffs with the given upper limit"""

        if self.dim >= 1: self.kx = randomize(lower, upper)
        if self.dim >= 2: self.ky = randomize(lower, upper)
        if self.dim >= 3: self.kz = randomize(lower, upper)
        if self.dim >= 4: self.kr = randomize(lower, upper)


class Coeffs():
    """ """

    def __init__(self, dim=2, upper=0.9, lower=1E-10):
        """create and initialize coeffs with the given lower / upper limits"""

        self.dim = dim
        if dim >= 1: self.x = 0.7 #randomize(lower, upper)
        if dim >= 2: self.y = 0.7 #randomize(lower, upper)
        if dim >= 3: self.z = 0.7 #randomize(lower, upper)
        if dim >= 4: self.r = 0.7 #randomize(lower, upper)


def randomize(lower=1E-10, upper=1):
    from numpy import random

    return (random.random() * (upper-lower)) + lower


def darcy1d(nodex, kx, cx):
    """
    calculate and return the time for a given node coordinate

    params:
    nodex : node x coordinate
    kx    : kxx value
    cx    : coefficient
    """

    return nodex**2 * (kx * cx)


def darcy2d(nodex, nodey, kx, ky, cx, cy):
    return (nodex**2 * (cx * kx)) + (nodey**2 * (cy * ky))


def flowgen1d(non, area, s, coeffs):
    """
    create flowfront for one direction
    non  : number of nodes (y, x) pair
    area : board area (y, x) pair
    s    : Stiffness instance
    """
    from numpy import zeros, linspace

    t = zeros(non)

    nodes_x = linspace(0, area[1], non[1])
    for i, x in enumerate(nodes_x):
        t[:,i] = darcy1d(x, s.kx, coeffs.x)

    return t


def flowgen2d(non, area, s, coeffs):
    from numpy import zeros, linspace

    t = zeros(non)

    nodes_x = linspace(0, area[1], non[1])
    nodes_y = linspace(0, area[0], non[0])
    for i, x in enumerate(nodes_x):
        for j, y in enumerate(nodes_y):
            t[j,i] = darcy2d(x, y, s.kx, s.ky, coeffs.x, coeffs.y)

    return t

def l2norm(x, y):
    """get l2 norm of given two matrices"""
    from numpy import linalg as LA

    return LA.norm(x-y)


# get the l2 norm of matrices
def l1norm(x, y):
    """get l1 norm of given two matrices"""
    from numpy import linalg as LA

    return LA.norm(x-y, 1)


def show_img(t):
    import matplotlib.pyplot as plt
    plt.imshow(t, cmap="tab20b", interpolation="bicubic", origin="lower")
    plt.colorbar()
    plt.show()


def compare_img(a, b):
    import matplotlib.pyplot as plt

    plt.subplot(211)
    plt.imshow(a, cmap="tab20b", interpolation="bicubic", origin="lower")
    plt.subplot(212)
    plt.imshow(b, cmap="tab20b", interpolation="bicubic", origin="lower")
    plt.show()


def show_img_on(a, b):
    import matplotlib.pyplot as plt

    fig = plt.figure(frameon=True)
    plt.imshow(a, cmap="tab20b", interpolation="bicubic", origin="lower")
    #plt.colorbar()
    plt.imshow(b, cmap="tab20b", interpolation="bicubic", origin="lower", alpha=.7)
    #plt.colorbar()
    plt.show()