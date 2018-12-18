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
    if hasattr(p, 'krt'):
        return _ft2drt(x, y, p, c)
    elif hasattr(p, 'kxy'):
        return _ft2d(x, y, p, c)
    else:
        print('1d')
        return _ft1d(x, p, c)


def _ft1d(x, p, c):
    import numpy as np

    s = np.array(x)
    stepx = x[0,1] - x[0,0]
    for i, _ in enumerate(x):
        for j, xj in enumerate(x[i]):
            s[i, j] = 0.5 * xj * (xj + stepx) * c.mu * c.fi / (p.kxx * c.deltaP)
        # Fix for lims' last step
        s[i, -1] = 0.5 * x[i, -1]**2 * c.mu * c.fi / (p.kxx * c.deltaP)
    return s


def _ft2d(x, y, p, c):
    import numpy as np

    s = np.array(x)
    stepx = x[0,1] - x[0,0]
    stepy = y[1,0] - y[0,0]
    stepd = np.sqrt(stepx**2 + stepy**2)
    print('steps', stepx, stepy, stepd)

    for i in range(len(x)):
        for j in range(len(x[i])):
            tx = 0.5 * x[i, j] * (x[i, j] + stepx) * c.mu * c.fi / ( p.kxx * c.deltaP)
            ty = 0.5 * x[i, j] * (x[i, j] + stepy) * c.mu * c.fi / ( p.kyy * c.deltaP)
            tz = 0.5 * x[i, j] * (x[i, j] + stepx) * c.mu * c.fi / ( p.kxy * c.deltaP)
            s[i, j] = 1 / (1/tx + 1/tz + 1/ty)
        # # Fix lims' last step
        # s[i, -1] = 0.5 * x[i, -1] * (x[i, -1]) * c.mu * c.fi  / (p.kxx * c.deltaP)

    # for i in range(len(x)):
    #     for j in range(len(x[i])):
    #         ty = 0.5 * s[i, j] * (s[i, j] + stepy) * c.mu * c.fi / ( p.kyy * c.deltaP)
    #         s[i, j] = s[i, j] - 1/ty

    # for i in range(1, len(x)-1):
    #     for j in range(1, len(x[i])-1):
    #         tz = 0.5 * x[i, j] * (x[i, j] + stepx) * c.mu * c.fi / ( p.kxy * c.deltaP)
    #         #print(tz)
    #         s[i, j] = 1/ ( 1/s[i, j] + 1/(tz) )

    return s


def _ft2drt(x, y, p, c):
    import numpy as np

    s = np.array(x)
    stepx = x[0,1] - x[0,0]
    stepy = y[1,0] - y[0,0]
    stepd = np.sqrt(stepx**2 + stepy**2)
    print('steps', stepx, stepy, stepd)

    for i in range(len(x)):
        for j in range(len(x[i])):
            tx = 0.5 * x[i, j] * (x[i, j] + stepx) * c.mu * c.fi / ( p.kxx * c.deltaP)
            #ty = 0.5 * x[i, j] * (x[i, j] + stepy) * c.mu * c.fi / ( p.kyy * c.deltaP)
            #tz = 0.5 * x[i, j] * (x[i, j] + stepx) * c.mu * c.fi / ( p.kxy * c.deltaP)
            tr = 100 * x[i, j] * (x[i, j] + stepx) * c.mu * c.fi / ( p.krt * c.deltaP)
            s[i, j] = 1 / (1/tr + 1/tx)
        # # Fix lims' last step
        # s[i, -1] = 0.5 * x[i, -1] * (x[i, -1]) * c.mu * c.fi  / (p.kxx * c.deltaP)

    # for i in range(len(x)):
    #     for j in range(len(x[i])):
    #         ty = 0.5 * s[i, j] * (s[i, j] + stepy) * c.mu * c.fi / ( p.kyy * c.deltaP)
    #         s[i, j] = s[i, j] - 1/ty

    # for i in range(1, len(x)-1):
    #     for j in range(1, len(x[i])-1):
    #         tz = 0.5 * x[i, j] * (x[i, j] + stepx) * c.mu * c.fi / ( p.kxy * c.deltaP)
    #         #print(tz)
    #         s[i, j] = 1/ ( 1/s[i, j] + 1/(tz) )

    return s


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
    from numpy import nanmax

    plt.subplot(211)
    plt.imshow(a[::-1], cmap="tab20b", interpolation="bicubic", origin="lower", vmax=max(nanmax(a), nanmax(b)))
    plt.colorbar()
    plt.subplot(212)
    plt.imshow(b[::-1], cmap="tab20b", interpolation="bicubic", origin="lower", vmax=max(nanmax(a), nanmax(b)))
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
