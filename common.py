def calculate_flowtime(bsize, nsize, p, c, name=None, gatelocs=None):
    """calculate and return the flow time based on the given parameters
    bsize = board size (y, x) in meters
    nsize = node size (y, x) node numbers
    p = PMap instance
    c = Coeff instance
    """
    from numpy import mgrid

    if hasattr(p, 'kyy'):
        return _ft2d(bsize, nsize, p, c, gatelocs)
    else:
        return _ft1d(bsize, nsize, p, c, gatelocs)


def _ft1d(bsize, nsize, p, c, gatelocs=None):
    """calculates 1 directional flow using kxx only"""
    import numpy as np

    stepx = bsize[1] / (nsize[1]-1)
    g = np.zeros(nsize)

    if type(gatelocs) is not np.ndarray:
        gatelocs = np.array(gatelocs)

    h = c.mu * c.fi / (p.kxx * c.deltaP)

    for i in range(nsize[0]):
        if i*nsize[1]+1 in gatelocs:
            for j in range(1, nsize[1]):
                g[i, j] = 0.5 * (j*stepx) * (j*stepx + stepx) * h
            # Fix for lims' last step
            g[i, -1] = 0.5 * stepx**2 * (nsize[1]-1)**2 * h

    return g


def _ft2d(bsize, nsize, p, c, gatelocs=None):
    """calculates 2 directional flow using kxx and kyy"""
    import numpy as np

    stepx = bsize[1] / (nsize[1]-1)
    stepy = bsize[0] / (nsize[0]-1)
    g = np.zeros(nsize)

    if type(gatelocs) is not np.ndarray:
        gatelocs = np.array(gatelocs)

    hx = c.mu * c.fi / (p.kxx * c.deltaP)
    hy = c.mu * c.fi / (p.kyy * c.deltaP)

    for i in range(nsize[0]):
        if i*nsize[1]+1 in gatelocs:
            for j in range(1, nsize[1]):
                g[i, j] = 0.5 * (j*stepx) * (j*stepx + stepx) * hx
            # Fix for lims' last step
            g[i, -1] = 0.5 * stepx**2 * (nsize[1]-1)**2 * hx
    for j in range(nsize[1]):
        for i in range(1, nsize[0]):
            g[i, j] = g[i-1, j] + 0.5 * (stepy) * (2 * stepy) * hy

    return g


def plot_item(t):
    import matplotlib.pyplot as plt
    plt.plot(t)
    plt.show()


def show_img(t):
    import matplotlib.pyplot as plt

    cmap = plt.cm.tab20b
    cmap.set_under(color='black')

    plt.imshow(t, cmap=cmap, interpolation="bilinear", origin="lower", vmin=0.0000001)
    plt.colorbar()
    plt.show()


def show_imgs(a, b, gatenodes=None):
    import matplotlib.pyplot as plt
    from numpy import nanmax

    cmap = plt.cm.tab20b
    cmap.set_under(color='black')

    if gatenodes is not None:
        print(gatenodes)
        #a[::-1,1:]

    plt.subplot(211)
    plt.imshow(a[::-1], cmap=cmap, interpolation="bilinear", origin="lower", vmin=0.0000001, vmax=max(nanmax(a), nanmax(b)))
    plt.colorbar()
    plt.subplot(212)
    plt.imshow(b[::-1], cmap=cmap, interpolation="bilinear", origin="lower", vmin=0.0000001, vmax=max(nanmax(a), nanmax(b)))
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
