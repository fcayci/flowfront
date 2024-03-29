"""
LIMS Wrapper for creating and parsing data files.
Accepts mesh object for creating the dmp data file.

"""

from .mesh import *
import numpy as np


__all__ = ['get_flowtime', 'create_lb', 'create_dmp', 'run_lims', 'read_res']


run_loc = 'runs/'


def get_flowtime(m, fname):
    """
    Call lims and return the flow time based on the given parameters

    Parameters
    ----------
    m : Mesh
        Mesh object
    fname : string
        filename for the run

    Returns
    -------


    """

    if not isinstance(m, Mesh):
        raise ValueError("ERROR: parameter m is not instance of Mesh")

    lb = create_lb(m, fname)
    create_dmp(m, fname)
    run_lims(lb)
    return read_res(fname, m.shape)


def create_lb(m, fname):
    """ Creates lb script file

    Parameters
    fname : string
        the name of the file to be generated
    m : Mesh
        Mesh object

    """

    if not isinstance(m, Mesh):
        raise ValueError("ERROR: parameter m is not instance of Mesh")

    lb = fname + '.lb'
    dmp = fname + '.dmp'
    res = fname + '_res.dmp'
    f_loc = run_loc + lb

    f = open(f_loc, 'w')
    f.write('PROC simu\r\n')
    f.write('  DO\r\n')
    f.write('    SOLVE\r\n')
    f.write('    EXITIF 0\r\n')
    f.write('  LOOP WHILE ((SONUMBEREMPTY() > 0) AND (SONUMBERFILLED() > 0))\r\n')
    f.write('ENDPROC\r\n')
    f.write('\r\n')
    f.write('CHANGEDIR "' + run_loc + '"\r\n')
    f.write('READ "' + dmp + '"\r\n')

    for g in m.gates:
        f.write('SETGATE ' + str(g.node.idx) + ', 1, ' + '{:.6e}'.format(g.deltaP) + '\r\n')

    f.write('\r\n')
    f.write('CALL simu\r\n')
    f.write('\r\n')
    #f.write('Print "# empty nodes =", sonumberempty\r\n')
    #f.write('\r\n')
    f.write('SETOUTTYPE "dump"\r\n')
    f.write('WRITE "' + res + '"\r\n')
    f.write('EXIT\r\n')
    f.close()

    l = 'created file: {}'.format(f_loc)
    return f_loc


def create_dmp(m, fname):
    """
    Creates the dmp file

    Parameters
    ----------
    fname : string
        the name of the file to be generated
    m : Mesh
        mesh file

    Returns
    -------

    """

    model = 'NEWTON'

    dmp = fname + '.dmp'
    f_loc = run_loc + dmp

    y, x = np.mgrid[0:m.size[0]:m.shape[0]*1j, 0:m.size[1]:m.shape[1]*1j]

    f = open(f_loc, 'w')
    f.write('#============================================================================\r\n\
#Unit System Information:\r\n\
#!SI\r\n\
#Last Displayed In:\r\n\
#0 System_International_(SI) Meter Meter² Meter Kelvin Pascal Pascal*Second Meter² Second Numeric Numeric(Fibre) Meter³_per_Seconds\r\n\
#Check for orphans: OK\r\n\
#Check for duplicates: OK\r\n\
#User Origin x:0 y:0 z:0 unit:\r\n\r\n')

    #
    # WRITE NODES
    #
    f.write('Number of nodes : ' + str(m.numOfNodes) + '\r\n')
    f.write(' Index       x              y              z\r\n')
    f.write('===================================================\r\n')


    for n in m.nodes.flatten():
        _x = n.x * m.step[1]
        _y = n.y * m.step[0]
        try:
            _z = n.z * m.step[2]
        except:
            _z = 0.0
        f.write(f"{n.idx:>6}{_x:>15.6f}{_y:>15.6f}{_z:>15.6}\r\n")

    #
    # WRITE Cells
    #
    elements = m.numOfCells
    #if krt != 0:
    #    elements += len(y[0]) -1
    f.write('Number of elements : ' + str(elements) + '\r\n')
    f.write('  Index  NNOD  N1    N2    N3   (N4)  (N5)  (N6)  (N7)  (N8)    h              Vf             Kxx             Kxy             Kyy           Kzz           Kzx            Kyz\r\n')
    f.write('==============================================================================================================================================================================\r\n')

    i = 1
    for c in m.cells.flatten():
        if c.active:
            l = len(c.nodes)
            #f.write(f"{c.idx:>6}{l:>5}{c.nodes[0].idx:>6}{c.nodes[1].idx:>6}{c.nodes[2].idx:>6}{c.nodes[3].idx:>6}")
            f.write(f"{i:>6}{l:>5}{c.nodes[0].idx:>6}{c.nodes[1].idx:>6}{c.nodes[2].idx:>6}{c.nodes[3].idx:>6}")
            f.write("                             ")
            f.write(f"{c.h:>7.3f}{c.Vf:>16.6f}{c.kxx:> 16.4e}{c.kxy:> 16.4e}{c.kyy:> 16.4e}\r\n")
            i += 1

    # if krt != 0:
    #     for j in range(0, nodes[1]-1):
    #         f.write('{:>6}{:>5}{:>6}{:>6}'.format(t, 2, g[-1, j+1], g[-1, j]))
    #         f.write('                                         ')
    #         f.write('{:>7.4f}{:>16.6f}{:> 16.4e}'.format(0.0001, 0.01, krt))
    #         f.write('\r\n')
    #         t += 1

    f.write('Resin Viscosity model ' + model + '\r\n')
    f.write('Viscosity :            ' + str(m.mu) + '\r\n')
    f.close()

    l = 'created file: {}'.format(f_loc)


def run_lims(lb):

    from subprocess import run, check_call, STDOUT
    from tempfile import NamedTemporaryFile
    import platform

    limscmd = ['lims', '-l' + lb]

    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        limscmd.insert(0, 'wine')
        with NamedTemporaryFile() as f:
            check_call(limscmd, stdout=f, stderr=STDOUT)
        #run(limscmd, capture_output=False)
    else:
        a = run(limscmd, capture_output=True)


def read_res(fname, s):
    """
    Reads the result dmp file and returns the fill time array
    and pressure values at each node

    Parameters
    ----------
    fname: string
        the name of the run file to read
    s :

    Returns
    -------

    """

    res = fname + '_res.dmp'

    with open(run_loc + res, 'r') as f:
        ft = []
        pr = []
        save = False
        for line in f:
            if save:
                try:
                    x = line.strip().split()
                    ft.append(np.float64(x[-1]))
                    pr.append(np.float64(x[1]))
                except:
                    l = 'skipping: {}'.format(line)

            if "Fill Time" in line:
                save = True

    ft = np.array(ft)
    pr = np.array(pr)

    ft.resize(s)
    pr.resize(s)

    return ft, pr
