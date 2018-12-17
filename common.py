class PMap():
    """Permeability map class"""

    def __init__(self, kxx=0, kyy=None, kxy=None, krt=None):
        """initialize permeability based on what is passed passed"""
        if kxx : self.kxx = kxx
        if kyy : self.kyy = kyy
        if kxy :
            self.kxy = kxy
            self.cpd()
        if krt : self.krt = krt


    def __len__(self):
        """return the item count as length"""
        return len(self.__dict__)


    def __getitem__(self, key):
        return self.__getattribute__(key)


    def __setitem__(self, key, value):
        self.__setattr__(key, value)


    def cpd(self):
        """check positive definitive
        TODO: needs fine exception refinement
        """
        try:
            if self.kxy**2 >= self.kxx * self.kyy:
                raise ValueError('kxy^2 cannot be bigger than kxx*kyy')
        except:
            raise AttributeError('one of the permeability is missing')

    def randomize(self, lower=1e-15, upper=1e-7):
        """randomize all the parameters based on the passed boundaries
        TODO: check positive definite when generating random values
        """
        from numpy import random

        if lower > upper:
           raise ValueError('lower should be lower than upper')

        for key in self.__dict__:
            self[key] = (random.random() + lower) * (upper - lower)



class Coeffs():
    """Coefficients class"""

    def __init__(self, mu=0.2, fi=0.5, deltaP=1e5):
        """initialize coefficients based on what is passed passed"""
        self.mu = mu
        self.fi = fi
        self.deltaP = deltaP


    def __len__(self):
        return len(self.__dict__)


    def __getitem__(self, key):
        return self.__getattribute__(key)


    def __setitem__(self, key, value):
        self.__setattr__(key, value)


def calculate_flowtime(bsize, nsize, p, c):
    """calculate and return the flow time based on the given parameters
    bsize = board size (y, x) in meters
    nsize = node size (y, x) node numbers
    p = PMap instance
    c = Coeff instance
    """
    from numpy import mgrid

    ft1d = lambda x, p, c: x**2 * c.mu * c.fi / (p.kxx * c.deltaP)
    ft2d = lambda x, y, p, c: (x**2 * c.mu * c.fi / (p.kxx * c.deltaP)) - (x*y)**2 * c.mu * c.fi / (p.kyy * c.deltaP)
    ft3d = lambda x, y, p, c: (x**2 * c.mu * c.fi / (p.kxx * c.deltaP)) - (x*y)**2 * c.mu * c.fi / (p.kyy * c.deltaP)

    y, x = mgrid[0:bsize[0]:nsize[0]*1j, 0:bsize[1]:nsize[1]*1j]

    if hasattr(p, 'kxx') and hasattr(p, 'kyy') and hasattr(p, 'kxy'):
        return ft3d(x, y, p, c)
    elif hasattr(p, 'kxx') and hasattr(p, 'kyy'):
        return ft2d(x, y, p, c)
    else:
        return ft1d(x, p, c)


def lims_flowtime(bsize, nsize, p, c, fname='run1'):
    """call lims and return the flow time based on the given parameters
    bsize = board size (y, x) in meters
    nsize = node size (y, x) node numbers
    p = PMap instance
    c = Coeff instance
    """
    from lims import lims_wrapper as lw
    from numpy import arange, mgrid

    gatenodes = arange(1, nsize[0]*nsize[1], nsize[1])

    lb = lw.create_lb(fname, gatenodes, c.deltaP)
    dmp = lw.create_dmp(fname, bsize, nsize, p, c)
    lw.run_lims(lb, dmp)
    return lw.read_res(fname, nsize)


def show_img(t):
    import matplotlib.pyplot as plt
    plt.imshow(t, cmap="tab20b", interpolation="bicubic", origin="lower")
    plt.colorbar()
    plt.show()


def show_imgs(a, b):
    import matplotlib.pyplot as plt
    from numpy import amax

    plt.subplot(211)
    plt.imshow(a, cmap="tab20b", interpolation="bicubic", origin="lower", vmax=max(amax(a), amax(b)))
    plt.colorbar()
    plt.subplot(212)
    plt.imshow(b, cmap="tab20b", interpolation="bicubic", origin="lower", vmax=max(amax(a), amax(b)))
    plt.colorbar()
    plt.show()


def show_img_on(a, b):
    import matplotlib.pyplot as plt

    fig = plt.figure(frameon=True)
    plt.imshow(a, cmap="tab20b", interpolation="bicubic", origin="lower")
    #plt.colorbar()
    plt.imshow(b, cmap="tab20b", interpolation="bicubic", origin="lower", alpha=.7)
    #plt.colorbar()
    plt.show()


def overlay_imgs(a, b):
    pass
