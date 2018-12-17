def calculate_flowtime(bsize, nsize, p, c):
    """calculate and return the flow time based on the given parameters
    bsize = board size (y, x) in meters
    nsize = node size (y, x) node numbers
    p = PMap instance
    c = Coeff instance
    """
    from numpy import mgrid

    # s[i, j] = xj * 0.5 * (xj + stepx) * c.mu * c.fi  / (p.kxx * c.deltaP)
    #ft2d = lambda x, y, p, c: (x**2 * c.mu * c.fi / ( 2 * (p.kxx + p.kxy) * c.deltaP)) - (x*y)**2 * c.mu * c.fi / ( (p.kyy + p.kxy) * c.deltaP)

    y, x = mgrid[0:bsize[0]:nsize[0]*1j, 0:bsize[1]:nsize[1]*1j]

    #print(x)

    if hasattr(p, 'kxx') and hasattr(p, 'kyy') and hasattr(p, 'kxy'):
        return _ft2d(x, y, p, c)
    else:
        print('1d')
        return _ft1d(x, p, c)


def _ft1d(x, p, c):
    import numpy as np

    sx = np.array(x)
    step = x[0,1] - x[0,0]
    print('step',step)
    for i, _ in enumerate(x):
        for j, xj in enumerate(x[i]):
            sx[i, j] = 0.5 * xj * (xj + step) * c.mu * c.fi / (p.kxx * c.deltaP)
        # Fix lims' last step
        sx[i, -1] = 0.5 * x[i, -1] * (x[i, -1]) * c.mu * c.fi / (p.kxx * c.deltaP)
    return sx


def _ft2d(x, y, p, c):
    import numpy as np

    sx = np.array(x)
    stepx = x[0,1] - x[0,0]
    stepy = y[0,1] - y[0,0]

    for i, xi in enumerate(x):
        for j, xj in enumerate(x[i]):
            kx = 0.5 * xj * (xj + stepx) * c.mu * c.fi / ( p.kxx * c.deltaP)
            ky = p.kyy * stepx * j * 0.01 #0.5 * (y[i, j] + stepy) * c.mu * c.fi / ( p.kyy * c.deltaP)
            kz = 0.0005 * xj * y[i, j] * (y[i, j] + stepy) * c.mu * c.fi / ( p.kxy * c.deltaP)
            sx[i, j] = kx + ky - kz
        # # Fix lims' last step
        # s[i, -1] = 0.5 * x[i, -1] * (x[i, -1]) * c.mu * c.fi  / (p.kxx * c.deltaP)
    return sx


def plot_item(t):
    import matplotlib.pyplot as plt
    plt.plot(t)
    plt.show()


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
