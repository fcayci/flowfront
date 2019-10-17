class PMap():
    """Permeability map class"""

    def __init__(self, kxx=0, kyy=None, kxy=None, krt=None):
        """initialize permeability based on what is passed passed"""
        if kxx.any() : self.kxx = kxx
        if kyy : self.kyy = kyy
        if kxy :
            self.kxy = kxy
            #self.cpd()
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


    def randomize(self, lower=1e-14, upper=1e-8):
        """randomize all the parameters based on the passed boundaries
        TODO: check positive definite when generating random values
        """
        from numpy import random

        if lower > upper:
           raise ValueError('lower should be lower than upper')

        for key in self.__dict__:
            self[key] = random.uniform(lower, upper)


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


def lims_flowtime(bsize, nsize, p, c, fname='run1', gatenodes=None):
    """call lims and return the flow time based on the given parameters
    bsize = board size (y, x) in meters
    nsize = node size (y, x) node numbers
    p = PMap instance
    c = Coeff instance
    """
    from lims import lims_wrapper as lw
    from numpy import arange, mgrid

    # default gatenodes are placed on the west side of the board
    if gatenodes is None:
        gatenodes = arange(1, nsize[0]*nsize[1], nsize[1])

    lb = lw.create_lb(fname, gatenodes, c.deltaP)

    if not hasattr(p, 'kxy') or kxy is None:
        kxy = 0
    else:
        kxy = p.kxy
    if not hasattr(p, 'kyy') or kyy is None:
        kyy = 0
    else:
        kyy = p.kyy
    if not hasattr(p, 'krt') or krt is None:
        krt = 0
    else:
        krt = p.krt

    lw.create_dmp(fname, bsize, nsize, c.mu, c.fi, c.deltaP, p.kxx, kyy, kxy, krt)
    lw.run_lims(lb)
    return lw.read_res(fname, nsize)


def set_gatenodes(nsize, gateloc):
    """decide on gatenodes (inlets) based on gateloc"""
    from numpy import arange

    g = arange(1, nsize[0]*nsize[1] + 1)
    g.resize(nsize)

    # west
    if gateloc == 'w':
        return g[:, 0]
    # north
    elif gateloc == 'n':
        return g[-1]
    # south
    elif gateloc == 's':
        return g[0]
    # north west
    elif gateloc == 'nw':
        return g[-1, 0]
    # south west
    elif gateloc == 'sw':
        return g[0, 0]
    # middle of west
    elif gateloc == 'ww':
        return g[nsize[0]//2, 0]
    else:
        raise ValueError('not a known gate location')
