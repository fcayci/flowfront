'''Flowfront calculation functions
'''

raise DeprecationWarning ("Deprecated. Keeping here in case this works get picked up again")

def ft_1d(geom):
    '''Calculate 1d flowfront
    '''
    from numpy import zeros

    if not isinstance(geom, Geometry):
        raise ValueError('ERROR >> parameter geom is not instance of Geometry')

    if hasattr(geom, 'kxx'):
        hx = lambda i, j, pr: geom.mu * geom.fi / (2 * geom.kxx[i, j] * pr)
    else:
        raise ValueError('ERROR >> geom does not have kxx attribute')

    stepx = geom.stepx
    deltaP = geom.deltaP
    xnodes, ynodes = geom.xnodes, geom.ynodes
    g = zeros(geom.nodes)
    p = zeros(geom.nodes)

    # absolute truth without pr change
    # g[i, j] = ((j+0.5)*stepx)**2 * hx(i, j-1, pr) - ((j-0.5)*stepx)**2 * hx(i, j-1, pr) + g[i, j-1]
    # g[i, j] =  ((j+0.5)**2 - (j-0.5)**2) * stepx**2 * hx(i, j-1, pr) + g[i, j-1] # same as above

    for i in range(ynodes):
        if i*xnodes+1 in geom.gatenodes:
            pr = deltaP
            p[i, 0] = pr
            for j in range(1, xnodes):
                p[i, j] = pr
                #g[i, j] = 2 * stepx**2 * hx(i, j-1, pr) + g[i, j-1]
                pr = deltaP - (deltaP * (j*stepx/geom.x))
                g[i, j] =  ((j+0.5)**2 - (j-0.5)**2) * stepx**2 * hx(i, j-1, deltaP) + g[i, j-1]
            # Fix for lims' last step
            g[i, -1] = stepx**2 * (geom.xnodes-1)**2 * hx(i, j, deltaP)

    return g, p
