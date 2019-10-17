# wrapper for running lims
import logging

file_loc = 'runs/'

def create_lb(fname, gatenodes, deltaP):
    """creates the lb file

    Args:
        fname (string): is the name of the file to be generated
        gatenodes (list): is the gate node array
        deltaP (float): is the deltaP from equation
    """
    lb = fname + '.lb'
    dmp = fname + '.dmp'
    res = fname + '_res.dmp'

    f = open(file_loc + lb, 'w')
    f.write('PROC simu\r\n')
    f.write('  DO\r\n')
    f.write('    SOLVE\r\n')
    f.write('    EXITIF 0\r\n')
    f.write('  LOOP WHILE ((SONUMBEREMPTY() > 0) AND (SONUMBERFILLED() > 0))\r\n')
    f.write('ENDPROC\r\n')
    f.write('\r\n')
    f.write('CHANGEDIR "' + file_loc + '"\r\n')
    f.write('READ "' + dmp + '"\r\n')
    try:
        for node in gatenodes:
            f.write('SETGATE ' + str(node) + ', 1, ' + '{:.6e}'.format(deltaP) + '\r\n')
    except TypeError:
        f.write('SETGATE ' + str(gatenodes) + ', 1, ' + '{:.6e}'.format(deltaP) + '\r\n')

    f.write('\r\n')
    f.write('CALL simu\r\n')
    f.write('\r\n')
    #f.write('Print "# empty nodes =", sonumberempty\r\n')
    #f.write('\r\n')
    f.write('SETOUTTYPE "dump"\r\n')
    f.write('WRITE "' + res + '"\r\n')
    f.write('EXIT\r\n')
    f.close()

    l = 'created file: {}'.format(file_loc + lb)
    logging.debug(l)
    return file_loc + lb


def create_dmp(fname, boardsize, nodes, mu, fi, deltaP, kxx, kyy, kxy, krt):
    """creates the dmp file

    Args:
        fname (string): is the name of the file to be generated
    """
    from numpy import arange, mgrid

    # TODO: add kxx, kxy, kyy, krt shape checking

    model = 'NEWTON'
    viscosity = mu
    height = 0.005
    if fi > 1:
        raise ValueError('fi cannot be higher than 1')
    vf = 1 - fi
    dmp = fname + '.dmp'

    y, x = mgrid[0:boardsize[0]:nodes[0]*1j, 0:boardsize[1]:nodes[1]*1j]

    f = open(file_loc+dmp, 'w')
    f.write('Number of nodes : ' + str(len(y)*len(y[0])) + '\r\n')
    f.write('{:<12} {:<14} {:<14} {:<6}\r\n'.format(' Index', 'x', 'y', 'z'))
    f.write('===================================================\r\n')

    for i in range(nodes[0]):
        for j in range(nodes[1]):
            f.write('{:>6}{:>15.6f}{:>15.6f}{:>15.6}\r\n'.format(i*nodes[1]+j+1, x[i,j], y[i, j], 0.0))

    elements = (len(y)-1)*(len(y[0])-1)
    if krt is not None:
        elements += len(y[0]) -1
    f.write('Number of elements : ' + str(elements) + '\r\n')
    f.write('  Index  NNOD  N1    N2    N3   (N4)  (N5)  (N6)  (N7)  (N8)    h              Vf             Kxx             Kxy             Kyy           Kzz           Kzx            Kyz\r\n')
    f.write('==============================================================================================================================================================================\r\n')

    g = arange(1, nodes[0]*nodes[1] + 1)
    g.resize(nodes)

    t = 1
    for i in range(len(g)-1):
        for j in range(len(g[0])-1):
            f.write('{:>6}{:>5}{:>6}{:>6}{:>6}{:>6}'.format(t, 4, g[i, j], g[i, j+1],g[i+1, j+1], g[i+1, j]))
            f.write('                             ')
            f.write('{:>7.3f}{:>16.6f}{:> 16.4e}{:> 16.4e}{:> 16.4e}'.format(height, vf, kxx[i,j], kxy, kyy))
            f.write('\r\n')
            t += 1

    if krt is not None:
        for j in range(0, nodes[1]-1):
            f.write('{:>6}{:>5}{:>6}{:>6}'.format(t, 2, g[-1, j+1], g[-1, j]))
            f.write('                                         ')
            f.write('{:>7.4f}{:>16.6f}{:> 16.4e}'.format(0.0001, 0.01, krt))
            f.write('\r\n')
            t += 1

    f.write('Resin Viscosity model ' + model + '\r\n')
    f.write('Viscosity :            ' + str(viscosity) + '\r\n')
    f.close()

    l = 'created file: {}'.format(file_loc + dmp)
    logging.debug(l)
    #return file_loc + dmp


def run_lims(lb):
    from subprocess import run, check_call, STDOUT
    from tempfile import NamedTemporaryFile
    import platform

    limscmd = ['lims/lims', '-l'+lb]

    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        limscmd.insert(0, 'wine')
        with NamedTemporaryFile() as f:
            check_call(limscmd, stdout=f, stderr=STDOUT)
        #run(limscmd, capture_output=False)
    else:
        a = run(limscmd, capture_output=True)
        logging.debug(a)


def read_res(fname, nodes):
    """Reads the result dmp file and returns the fill time array
    and pressure values at each node
    fname: the name of the run file to read
    """
    from numpy import array, float64

    res = fname + '_res.dmp'

    with open(file_loc + res, 'r') as f:
        ff = []
        pr = []
        save = False
        for line in f:
            if save:
                try:
                    x = line.strip().split()
                    ff.append(float64(x[-1]))
                    pr.append(float64(x[1]))
                except:
                    l = 'skipping: {}'.format(line)
                    logging.debug(l)

            if "Fill Time" in line:
                save = True

    ff = array(ff)
    pr = array(pr)
    ff.resize(nodes)
    pr.resize(nodes)

    return ff, pr
