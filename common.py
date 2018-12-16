def evaluate(dim, x, y, kx_t, ky_t, mu, a):
    if dim == 1:
        d1d = lambda x, kx, a: x**2 * (kx * a)

        return d1d(y, kx_t, a)
    elif dim == 2:
        pass


def evaluate_lims(dim, x, y, kx_t, ky_t, mu, a):
    from lims import lims_wrapper as lw
    import numpy as np

    filename = 'run1'
    s = np.arange(1, 36*11, 36)

    lb = lw.create_lb(filename, s, mu)
    dmp = lw.create_dmp(filename, x, y, kx_t, ky_t)
    lw.run_lims(lb, dmp)

    f = open('runs/' + filename + '_res.dmp', 'r')

    ff = []
    save = False
    for line in f:
        if save == True:
            try:
                ff.append(np.float64(line.strip().split(' ')[-1]))
            except:
                print('skipping', line)

        if "Fill Time" in line:
            save = True

    ff = np.array(ff)
    ff.resize(11, 36)
    return ff


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
