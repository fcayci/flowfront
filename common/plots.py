"""
Plot helpers

"""

import matplotlib.pyplot as plt
import numpy as np


def plot_pressure(pr, showlegend=True):
    """
    Plot pressure for all the rows

    Parameters
    ----------
    pr : np.ndarray
        Pressure values
    showlegend : bool
        Show legend on the plot

    Returns
    -------
    None

    """
    plt.plot(np.transpose(pr))

    plt.title('Pressure values for all nodes')
    plt.xlabel('x nodes')
    plt.ylabel('pressure level')
    #if showlegend:
    #    plt.legend(['row' + str(i+1) for i in range(self.ynodes)])

    plt.show()


def plot_filltime(ft, showlegend=True):
    """
    Plot filltime for all the rows

    Parameters
    ----------
    ft : np.ndarray
        Filltime for all nodes
    showlegend : bool
        Show legend on the plot

    Returns
    -------
    None

    """

    plt.plot(np.transpose(ft))

    plt.title('filltime for all nodes')
    plt.xlabel('x nodes')
    plt.ylabel('filltime')
    #if showlegend:
    #    plt.legend(['row' + str(i+1) for i in range(self.ynodes)])

    plt.show()


def show_flowfront(ft):
    """
    Show flowfront

    Parameters
    ----------
    ft: np.ndarray
        flowtime

    Returns
    -------
    None

    """

    from copy import copy

    #cmap = copy(plt.cm.get_cmap("tab20b"))
    cmap = copy(plt.cm.get_cmap("jet"))
    cmap.set_under(color='white')

    plt.title('flowfront')
    #plt.imshow(ft, cmap=cmap, interpolation="bilinear", origin="lower", vmin=1e-12)
    plt.imshow(ft, cmap=cmap, origin="lower", vmin=1e-12)
    plt.xlim(0.5, ft.shape[1]-.5)
    plt.ylim(0.5, ft.shape[0]-.5)
    plt.colorbar()
    plt.show()


def show_kmaps(m):
    """
    Show K maps

    Parameters
    ----------
    m: Mesh
        Mesh data to be shown

    Returns
    -------
    None

    """

    from copy import copy

    cmap = copy(plt.cm.get_cmap("tab20b"))
    cmap.set_under(color='black')

    kxx = m.get_cell_kxx()
    kyy = m.get_cell_kyy()
    kxy = m.get_cell_kxy()

    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('K maps for the mesh')

    #im = ax1.imshow(kxx, cmap=cmap, interpolation="bilinear", origin="lower")
    im = ax1.imshow(kxx, cmap=cmap, origin="lower")
    ax1.set_xlim(0, kxx.shape[1]-1)
    ax1.set_ylim(0, kxx.shape[0]-1)
    ax1.set_title('Kxx')
    fig.colorbar(im, ax=ax1)

    ax2.imshow(kyy, cmap=cmap, origin="lower")
    ax2.set_xlim(0, kyy.shape[1]-1)
    ax2.set_ylim(0, kyy.shape[0]-1)
    ax2.set_title('Kyy')
    fig.colorbar(im, ax=ax2)

    ax3.imshow(kxy, cmap=cmap, origin="lower")
    ax3.set_xlim(0, kxy.shape[1]-1)
    ax3.set_ylim(0, kxy.shape[0]-1)
    ax3.set_title('Kxy')
    fig.colorbar(im, ax=ax3)

    plt.show()

