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
    h: np.float64 = 0.005
    Vf: np.float64 = 0.5
    kxx: np.float64 = 0.0
    kxy: np.float64 = 0.0
    kyy: np.float64 = 0.0


@dataclass
class Node:
    """
    Node data class

    Holds the single node (x, y, z) location

    """

    idx: int
    x: np.float64
    y: np.float64
    z: np.float64 = 0.0


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

        x, y = 0.0, 0.0
        for i in range(1, self.numOfNodes+1):
            if (i-1) % self.shape[1] == 0:
                x = 0.0
            else:
                x += self.step[1]

            y = ((i-1) // self.shape[1]) * self.step[1]
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
        self.cellShape = (self.shape[0]-1, self.shape[1]-1)

        for i in range(self.shape[0]-1):
            for j in range(self.shape[1]-1):
                idx = i*(self.shape[1]-1) + j + 1
                self.cells[idx-1] = Cell(idx,
                    (_n[i, j], _n[i, j+1], _n[i+1, j+1], _n[i+1, j]))


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


    def set_kxx(self, k, cell=0):
        """
        Set Kxx

        """

        if cell > 0 and cell <= self.numOfCells:
            self.cells[cell-1].kxx = k

        elif cell == 0:
            for c in self.cells:
                c.kxx = k

        else:
            raise ValueError(f"Wrong cell number {cell} passed")


    def set_kxy(self, k, cell=0):
        """
        Set Kxy

        """

        if cell > 0 and cell <= self.numOfCells:
            self.cells[cell-1].kxy = k

        elif cell == 0:
            for c in self.cells:
                c.kxy = k

        else:
            raise ValueError(f"Wrong cell number {cell} passed")


    def set_kyy(self, k, cell=0):
        """
        Set Kyy

        """

        if cell > 0 and cell <= self.numOfCells:
            self.cells[cell-1].kyy = k

        elif cell == 0:
            for c in self.cells:
                c.kyy = k

        else:
            raise ValueError(f"Wrong cell number {cell} passed")


    def set_racetrack(self, krt, loc='n'):
        """
        Set racetracking (Krt)

        """

        raise NotImplementedError("Not yet implemented")


    def get_cell_IDs(self):
        """
        Get cell ID
        """

        ids = np.zeros(len(self.cells), dtype=int)
        for i, cell in enumerate(self.cells):
            ids[i] = cell.idx

        return ids.reshape(self.cellShape)


    def get_cell_kxx(self):

        ks = np.zeros(len(self.cells))
        for i, cell in enumerate(self.cells):
            ks[i] = cell.kxx

        return ks.reshape(self.cellShape)


    def get_cell_kxy(self):

        ks = np.zeros(len(self.cells))
        for i, cell in enumerate(self.cells):
            ks[i] = cell.kxy

        return ks.reshape(self.cellShape)


    def get_cell_kyy(self):

        ks = np.zeros(len(self.cells))
        for i, cell in enumerate(self.cells):
            ks[i] = cell.kyy

        return ks.reshape(self.cellShape)

