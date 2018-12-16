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
