"""
Holds the mesh for different geometries

Requires at least Python 3.7

"""

import numpy as np
from dataclasses import dataclass


@dataclass
class Cell:
    """
    Cell data class

    It holds the coordinates for a cell as well as all the other parameters.

    """

    idx: int
    nodes: np.ndarray((4,))
    h: np.float64 = 0.005 # thickness
    Vf: np.float64 = 0.5 # volume fraction
    kxx: np.float64 = 0.0
    kxy: np.float64 = 0.0
    kyy: np.float64 = 0.0
    kzx: np.float64 = 0.0
    kyz: np.float64 = 0.0
    kzz: np.float64 = 0.0
    active: int  = 1
    Type: str = 'QUAD'


@dataclass
class Node:
    """
    Node data class

    Holds the single node (x, y, z) location index

    """

    idx: int
    x: int
    y: int
    z: int = 0


@dataclass
class Gate:
    """
    Gate data class

    holds the pressure parameter with relative node.
    """

    node: int
    deltaP: np.float64


@dataclass
class Race:
    """
    Used for race tracking on the edges.

    """

    idx: int
    nodes: np.ndarray((2,))
    krt: np.float64 = 0.0


class Mesh():

    def __init__(self, size, shape):
        """
        2D mesh

        Parameters
        ----------
        size : tuple
            (y, x) tuple for the size of the mesh geometry in meters
        shape : tuple
            (y, x) tuple for the number of nodes in each direction

        """

        self.size = size
        self.shape = shape
        self.step = (size[0]/(shape[0]-1), size[1]/(shape[1]-1))
        self.numOfNodes = shape[0] * shape[1]
        self.nodes = []
        self.gates = []

        x, y = 0, 0
        for i in range(1, self.numOfNodes+1):
            if (i-1) % self.shape[1] == 0:
                x = 0
            else:
                x += 1

            y = ((i-1) // self.shape[1])
            self.nodes.append(Node(i, x, y))

        self.nodes = np.array(self.nodes).reshape(shape)

        self.mu = 0.1
        self.fi = 0.5

        if self.step[0] != self.step[1]:
            print(f"step x {self.step[0]} does not match step y {self.step[1]}")


    def create_mesh(self, nodes=4):
        """
        Create mesh

        Currently only supports 4 node mesh. Fills out cells array

        Parameters
        ----------
        nodes : int
            Number of nodes for the mesh. Not currently used.

        """

        _n = self.nodes

        self.numOfCells = (self.shape[0]-1) * (self.shape[1]-1)
        self.cells = np.ndarray((self.numOfCells), dtype=Cell)

        for i in range(self.shape[0]-1):
            for j in range(self.shape[1]-1):
                idx = i*(self.shape[1]-1) + j + 1
                self.cells[idx-1] = Cell(idx,
                    (_n[i, j], _n[i, j+1], _n[i+1, j+1], _n[i+1, j]))

        self.cells = self.cells.reshape(self.shape[0]-1, self.shape[1]-1)


    def set_gate(self, n, dP=1e5):
        """
        Set given node as gate

        Parameters
        ----------
        n : Node
            Selected node for the gate
        dP : float, optional
            Pressure

        Returns
        -------
        None

        """

        self.gates.append(Gate(n, dP))


    def set_gate_nodes(self, s, dP=1e5):
        """
        Set gate node locations

        Parameters
        ----------
        s : str
            Node locations. Possible values are w, e, s, n, nw, sw, mw.
        dP : float, optional
            Pressure

        Returns
        -------
        None

        """

        if   s ==  'w':
            for n in self.nodes[:, 0]:
                self.set_gate(n, dP)

        elif s ==  'e':
            for n in self.nodes[:, -1]:
                self.set_gate(n, dP)

        elif s ==  's':
            for n in self.nodes[0]:
                self.set_gate(n, dP)

        elif s ==  'n':
            for n in self.nodes[-1]:
                self.set_gate(n, dP)

        elif s == 'nw':
            n = self.nodes[-1, 0]
            self.set_gate(n, dP)

        elif s == 'sw':
            n = self.nodes[0, 0]
            self.set_gate(n, dP)

        elif s == 'mw':
            n = self.nodes[self.nodes.shape[0]//2, 0]
            self.set_gate(n, dP)

        else:
            raise ValueError('not a known gate location')


    def set_kxx(self, k, x=-1, y=-1, rx=1, ry=1):
        """
        Set Kxx

        Todo
        ----
        We can check boundaries instead of just ignoring the exception

        Parameters
        ----------
        k : float
            permeability value
        x : int
            x index
        y : int
            y index
        rx : int
            x length for the cells
        ry : int
            y length for the cells

        Returns
        -------
        None

        """

        if x < 0 and y < 0:
            for r in self.cells:
                for c in r:
                    c.kxx = k

        elif x < 0:
            for c in self.cells[y]:
                c.kxx = k

        elif y < 0:
            for r in self.cells:
                r[x].kxx = k

        else:
            try:
                for i in range(rx):
                    for j in range(ry):
                        self.cells[y+j, x+i].kxx = k
            # just ignore out of bounds
            except IndexError:
                pass


    def set_kyy(self, k, x=-1, y=-1, rx=1, ry=1):
        """
        Set Kyy

        Parameters
        ----------
        k : float
            permeability value
        x : int
            x index
        y : int
            y index
        rx : int
            x length for the cells
        ry : int
            y length for the cells

        Returns
        -------
        None

        """

        if x < 0 and y < 0:
            for r in self.cells:
                for c in r:
                    c.kyy = k

        elif x < 0:
            for c in self.cells[y]:
                c.kyy = k

        elif y < 0:
            for r in self.cells:
                r[x].kyy = k

        else:
            try:
                for i in range(rx):
                    for j in range(ry):
                        self.cells[y+j, x+i].kyy = k
            # just ignore out of bounds
            except IndexError:
                pass


    def set_kxy(self, k, x=-1, y=-1, rx=1, ry=1):
        """
        Set Kxy. Should be sqrt(kxx * kyy) > kxy

        Parameters
        ----------
        k : float
            permeability value
        x : int
            x index
        y : int
            y index
        rx : int
            x length for the cells
        ry : int
            y length for the cells

        Returns
        -------
        None

        """

        if x < 0 and y < 0:
            for r in self.cells:
                for c in r:
                    if np.sqrt(c.kxx * c.kxy) < c.kxy:
                        print("kxy is too big")
                    else:
                        c.kxy = k

        elif x < 0:
            for c in self.cells[y]:
                if np.sqrt(c.kxx * c.kxy) < c.kxy:
                    print("kxy is too big")
                else:
                    c.kxy = k

        elif y < 0:
            for r in self.cells:
                if np.sqrt(r[x].kxx * r[x].kxy) < r[x].kxy:
                    print("kxy is too big")
                else:
                    r[x].kxy = k

        else:
            try:
                for i in range(rx):
                    for j in range(ry):
                        c = self.cells[y+j, x+i]
                        if np.sqrt(c.kxx * c.kxy) < c.kxy:
                            print("kxy is too big")
                        else:
                            c.kxy = k
            # just ignore out of bounds
            except IndexError:
                pass


    def set_kall(self, kxx, kyy, kxy=None, x=-1, y=-1, rx=1, ry=1):
        """
        Set all kxx at the same time

        Parameters
        ----------
        kxx : float
            permeability value
        kyy : float
            permeability value
        kxy : float
            permeability value
        x : int
            x index
        y : int
            y index
        rx : int
            x length for the cells
        ry : int
            y length for the cells

        Returns
        -------
        None

        """

        if kxy is not None:
            if np.sqrt(kxx * kxy) < kxy:
                print('ERROR: kxy is too big. Not setting')
                return

        if x < 0 and y < 0:
            for r in self.cells:
                for c in r:
                    c.kxx = kxx
                    c.kyy = kyy
                    if kxy is not None:
                        c.kxy = kxy

        elif x < 0:
            for c in self.cells[y]:
                c.kxx = kxx
                c.kyy = kyy
                if kxy is not None:
                    c.kxy = kxy

        elif y < 0:
            for r in self.cells:
                r[x].kxx = kxx
                r[x].kyy = kyy
                if kxy is not None:
                    r[x].kxy = kxy

        else:
            try:
                for i in range(rx):
                    for j in range(ry):
                        self.cells[y+j, x+i].kxx = kxx
                        self.cells[y+j, x+i].kyy = kyy
                        if kxy is not None:
                            self.cells[y+j, x+i].kxy = kxy
            # just ignore out of bounds
            except IndexError:
                pass


    def delete_cells(self, x, y, rx=1, ry=1):
        """
        Delete given cells

        Parameters
        ----------
        x : int
            x index
        y : int
            y index
        rx : int
            x length for the cells
        ry : int
            y length for the cells

        Returns
        -------
        None

        """

        if x < 0:
            for c in self.cells[y]:
                if c.active:
                    c.active = 0
                    self.numOfCells -= 1

        elif y < 0:
            for r in self.cells:
                if r[x].active:
                    r[x].active = 0
                    self.numOfCells -= 1

        else:
            try:
                for i in range(rx):
                    for j in range(ry):
                        c = self.cells[y+j, x+i]
                        if c.active:
                            c.active = 0
                            self.numOfCells -= 1
            # just ignore out of bounds
            except IndexError:
                pass



        pass


    def activate_cells(self, x, y, rx=1, ry=1):
        """
        Activate given cells

        Parameters
        ----------
        x : int
            x index
        y : int
            y index
        rx : int
            x length for the cells
        ry : int
            y length for the cells

        Returns
        -------
        None

        """

        if x < 0:
            for c in self.cells[y]:
                if not c.active:
                    c.active = 1
                    self.numOfCells += 1

        elif y < 0:
            for r in self.cells:
                if not r[x].active:
                    r[x].active = 1
                    self.numOfCells += 1

        else:
            try:
                for i in range(rx):
                    for j in range(ry):
                        c = self.cells[y+j, x+i]
                        if not c.active:
                            c.active = 1
                            self.numOfCells += 1
            # just ignore out of bounds
            except IndexError:
                pass



        pass


    def set_racetrack(self, krt, loc='n'):
        """
        Set racetracking (Krt)

        """

        raise NotImplementedError("Not yet implemented")


    def get_cell_IDs(self):
        """
        Get cell ID
        """

        ids = np.zeros_like(self.cells, dtype=int)
        for i, cell in enumerate(self.cells):
            ids[i] = cell.idx

        return ids.reshape(self.cellShape)


    def get_cell_kxx(self):

        ks = np.zeros_like(self.cells, dtype=float)
        for i, r in enumerate(self.cells):
            for j, c in enumerate(r):
                ks[i, j] = c.kxx

        return ks


    def get_cell_kyy(self):

        ks = np.zeros_like(self.cells, dtype=float)
        for i, r in enumerate(self.cells):
            for j, c in enumerate(r):
                ks[i, j] = c.kyy

        return ks


    def get_cell_kxy(self):

        ks = np.zeros_like(self.cells, dtype=float)
        for i, r in enumerate(self.cells):
            for j, c in enumerate(r):
                ks[i, j] = c.kxy

        return ks


    def run(self, fname):
        """
        Run LIMS
        """

        from lims.lims_wrapper import get_flowtime as lims

        self.ft, self.pr = lims(self, fname)


    def show_flowfront(self):
        from common.plots import show_flowfront as pl

        pl(self.ft)


    def show_kmaps(self):
        from common.plots import show_kmaps as pl

        pl(self)


    def plot_filltime(self):
        from common.plots import plot_filltime as pl

        pl(self.ft)


    def plot_pressure(self):
        from common.plots import plot_pressure as pl

        pl(self.pr)

    def save(self, fname):

        print(self.ft)
        #np.save('runs/' + fname, self.ft)
