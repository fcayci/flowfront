"""Flowfront calculation functions
"""

from libs.geometry import Geometry

def ff_1d(geom):
    """Calculate 1d flowfront
    """
    from numpy import zeros

    if not isinstance(geom, Geometry):
        raise ValueError('ERROR >> parameter geom is not instance of Geometry')

    if hasattr(geom, 'kxx'):
        hx = lambda i, j, pr: geom.mu * geom.fi / (2 * geom.kxx[i, j] * pr)
    else:
        raise ValueError('ERROR >> geom does not have kxx attribute')

    stepx, stepy = geom.stepx, geom.stepy
    g = zeros(geom.nodes)

    for i in range(geom.ynodes):
        if i*geom.xnodes+1 in geom.gatenodes:
            pr = geom.deltaP
            for j in range(1, geom.xnodes):
                g[i, j] = ((j+0.5)*stepx)**2 * hx(i, j-1, pr) - ((j-0.5)*stepx)**2 * hx(i, j-1,pr) + g[i, j-1]
            # Fix for lims' last step
            #g[i, -1] = stepx**2 * (geom.xnodes-1)**2 * hx(i, j, pr)

    return g


def ff_lims(geom, fname='run1'):
    """call lims and return the flow time based on the given parameters

    Args:
        geom (Geometry) : Geometry class object

    Kwargs:
        fname (string) : filename for the run
    """
    from lims import lims_wrapper as lw
    from numpy import arange, mgrid

    if not isinstance(geom, Geometry):
        raise ValueError('ERROR >> parameter geom is not instance of Geometry')

    lb = lw.create_lb(fname, geom.gatenodes, geom.deltaP)

    lw.create_dmp(fname, geom.size, geom.nodes, geom.mu, geom.fi, geom.deltaP, geom.kxx, geom.kyy, geom.kxy, geom.krt)
    lw.run_lims(lb)
    return lw.read_res(fname, geom.nodes)