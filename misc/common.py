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

    hx = lambda j, pr: c.mu * c.fi / (2 * p.kxx[j] * pr)

    for i in range(nsize[0]):
        if i*nsize[1]+1 in gatelocs:
            pr = c.deltaP
            for j in range(1, nsize[1]):
                #if j <= (nsize[1]/2):
                #g[i, j] = (j*stepx) * (j+1) * stepx * hx(j,pr)
                #g[i, j] = (((j+0.5)*stepx)**2 - ((j-0.5)*stepx)**2) * hx(j,pr)
                #g[i, j] = stepx**2 * (2*j) * hx(j-1,pr) + g[i, j-1]
                #g[i, j] = (((j+0.5)*stepx)**2 - ((j-0.5)*stepx)**2) * hx(j-1,pr) + g[i, j-1]
                g[i, j] = ((j+0.5)*stepx)**2 * hx(j-1,pr) - ((j-0.5)*stepx)**2 * hx(j-1,pr) + g[i, j-1]
                if p.kxx[j-1] != p.kxx[j]:
                    pr = c.deltaP*(nsize[1]-1)/(nsize[1]-j)
                #    g[i, j] =  ((j+0.5)**2 - (j-0.5)**2) * stepx**2 * hx(j-1, pr) + g[i, j-1]
                #  j**2 + j + 0.25 - j**2 + j - 0.25
                #g[i, j] =  hx(j-1, pr) * j * ((1.5*stepx)**2 - (0.5*stepx)**2)
                #pr = c.deltaP*(nsize[1]-j)/(nsize[1]-1)
                #print(hx(j-1, pr), end=' , ')
                # res = 0
                # for jj in range(j):
                #     res += (jj+.5)**2 * stepx**2 * hx(jj)
                # g[i, j] = res
                # else:
                #     z = j-int(nsize[1]/2)-1
                #     pr = c.deltaP - c.deltaP * ((nsize[1]-1)/2) / (nsize[1]-1)
                #     g[i, j] =  ((z+0.5)**2 - (z-0.5)**2) * stepx**2 * hx(j-1, pr) + g[i, j-1]

            # Fix for lims' last step
            #g[i, -1] = stepx**2 * (nsize[1]-1)**2 * hx(j, c.deltaP)

    return g


def _ft2d(bsize, nsize, p, c, gatelocs=None):
    """calculates 2 directional flow using kxx and kyy"""
    import numpy as np

    stepx = bsize[1] / (nsize[1]-1)
    stepy = bsize[0] / (nsize[0]-1)
    g = np.zeros(nsize)

    if type(gatelocs) is not np.ndarray:
        gatelocs = np.array(gatelocs)

    hx = lambda j, pr: 0.5 * c.mu * c.fi / (p.kxx[j] * pr)
    hy = lambda pr: 0.5 * c.mu * c.fi / (p.kyy * pr)

    pr = c.deltaP

    for i in range(nsize[0]):
        if i*nsize[1]+1 in gatelocs:
            for j in range(1, nsize[1]):
                pass
                #g[i, j] = ((j*stepx)**2 - ((j-1)*stepx)**2) * hx + g[i, j-1]
                #g[i, j] = 1/ (-1/(stepy**2 * (2*j) * hy(pr) + 1/(stepx**2 * (2*j) * hx(j-1, pr))) + g[i, j-1]
                #g[i, j] = (j*stepx) * (j+1) * stepx * hx
            # Fix for lims' last step
            #g[i, -1] = stepx**2 * (nsize[1]-1)**2 * hx(nsize[1]-1, pr)
    # for j in range(nsize[1]):
    #     for i in range(1, nsize[0]):
    #         g[i, j] = g[i-1, j] + 0.5 * (stepy) * (2 * stepy) * hy

    return g


def plot_item(c, t=''):
    import matplotlib.pyplot as plt
    plt.plot(c)
    plt.title(t)
    plt.xlabel('# of trials')
    plt.ylabel('cost')
    plt.show()


def show_img(t):
    import matplotlib.pyplot as plt

    cmap = plt.cm.tab20b
    cmap.set_under(color='black')

    plt.imshow(t, cmap=cmap, interpolation="bilinear", origin="lower", vmin=0.0000001)
    plt.colorbar()
    plt.show()


def show_imgs(a, b, t='', gatenodes=None):
    import matplotlib.pyplot as plt
    from numpy import nanmax

    cmap = plt.cm.tab20b
    cmap.set_under(color='black')

    if gatenodes is not None:
        print(gatenodes)
        #a[::-1,1:]

    fig = plt.figure()
    fig.suptitle(t)
    ax = plt.subplot(211)
    ax.set_title('target flow front')
    plt.imshow(a[::-1], cmap=cmap, interpolation="bilinear", origin="lower", vmin=0.0000001, vmax=max(nanmax(a), nanmax(b)))
    plt.colorbar()
    ax = plt.subplot(212)
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
