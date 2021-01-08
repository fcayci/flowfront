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

    cmap = copy(plt.cm.get_cmap("tab20b"))
    cmap.set_under(color='black')

    plt.title('flowfront')
    #plt.imshow(ft, cmap=cmap, interpolation="bilinear", origin="lower", vmin=0.0000001)
    plt.imshow(ft, cmap=cmap, origin="lower", vmin=0.0000001)
    plt.colorbar()
    plt.show()

