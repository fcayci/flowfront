# wrapper for running lims
import logging

file_loc = 'runs/'

def create_lb(fname, gatenodes, deltaP):
    """creates the lb file
    fname is the name of the file to be generated
    gatenodes is the gate node array
    deltaP is the deltaP
    """
    lb = fname + '.lb'
    dmp = fname + '.dmp'
    res = fname + '_res.dmp'

    f = open(file_loc + lb, 'w')
    f.write('PROC simu\n')
    f.write('  DO\n')
    f.write('    SOLVE\n')
    f.write('    EXITIF 0\n')
    f.write('  LOOP WHILE ((SONUMBEREMPTY() > 0) AND (SONUMBERFILLED() > 0))\n')
    f.write('ENDPROC\n')
    f.write('\n')
    f.write('CHANGEDIR "' + file_loc + '"\n')
    f.write('READ "' + dmp + '"\n')
    try:
        for node in gatenodes:
            f.write('SETGATE ' + str(node) + ', 1, ' + '{:.6e}'.format(deltaP) + '\n')
    except TypeError:
        f.write('SETGATE ' + str(gatenodes) + ', 1, ' + '{:.6e}'.format(deltaP) + '\n')

    f.write('\n')
    f.write('CALL simu\n')
    f.write('\n')
    #f.write('Print "# empty nodes =", sonumberempty\n')
    #f.write('\n')
    f.write('SETOUTTYPE "dump"\n')
    f.write('WRITE "' + res + '"\n')
    f.write('EXIT\n')
    f.close()

    l = 'created file: {}'.format(file_loc + lb)
    logging.debug(l)
    return file_loc + lb


def create_dmp(fname, bsize, nsize, p, c):
    """creates the dmp file
    fname is the name of the file to be generated
    """
    from numpy import arange, mgrid

    kxx = p.kxx
    try: kyy = p.kyy
    except: kyy = 0

    try: kxy = p.kxy
    except: kxy = 0

    model = 'NEWTON'
    viscosity = c.mu
    height = 0.005
    if c.fi > 1:
        raise ValueError('fi cannot be higher than 1')
    vf = 1 - c.fi
    dmp = fname + '.dmp'

    y, x = mgrid[0:bsize[0]:nsize[0]*1j, 0:bsize[1]:nsize[1]*1j]

    f = open(file_loc+dmp, 'w')
    f.write('Number of nodes : ' + str(len(y)*len(y[0])) + '\n')
    f.write('{:<12} {:<14} {:<14} {:<6}\n'.format(' Index', 'x', 'y', 'z'))
    f.write('===================================================\n')

    for i in range(nsize[0]):
        for j in range(nsize[1]):
            f.write('{:>6}{:>15.6f}{:>15.6f}{:>15.6}\n'.format(i*nsize[1]+j+1, x[i,j], y[i, j], 0.0))

    elements = (len(y)-1)*(len(y[0])-1)
    if hasattr(p, 'krt'):
        elements += len(y[0]) -1
    f.write('Number of elements : ' + str(elements) + '\n')
    f.write('  Index  NNOD  N1    N2    N3   (N4)  (N5)  (N6)  (N7)  (N8)    h              Vf             Kxx             Kxy             Kyy           Kzz           Kzx            Kyz\n')
    f.write('==============================================================================================================================================================================\n')

    g = arange(1, nsize[0]*nsize[1] + 1)
    g.resize(nsize)

    t = 1
    for i in range(len(g)-1):
        for j in range(len(g[0])-1):
            f.write('{:>6}{:>5}{:>6}{:>6}{:>6}{:>6}'.format(t, 4, g[i, j], g[i, j+1],g[i+1, j+1], g[i+1, j]))
            f.write('                             ')
            f.write('{:>7.3f}{:>16.6f}{:> 16.4e}{:> 16.4e}{:> 16.4e}'.format(height, vf, kxx, kxy, kyy))
            f.write('\n')
            t += 1

    if hasattr(p, 'krt'):
        for j in range(0, nsize[1]-1):
            f.write('{:>6}{:>5}{:>6}{:>6}'.format(t, 2, g[-1, j+1], g[-1, j]))
            f.write('                                         ')
            f.write('{:>7.4f}{:>16.6f}{:> 16.4e}'.format(0.0001, 0.01, p.krt))
            f.write('\n')
            t += 1

    f.write('Resin Viscosity model ' + model + '\n')
    f.write('Viscosity :            ' + str(viscosity) + '\n')
    f.close()

    l = 'created file: {}'.format(file_loc + dmp)
    logging.debug(l)
    #return file_loc + dmp


def run_lims(lb):
    from subprocess import run
    import platform

    limscmd = ['lims/lims', '-l'+lb]

    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        limscmd.insert(0, 'wine')

    a = run(limscmd, capture_output=True)
    logging.debug(a)


def read_res(fname, nsize):
    """Reads the result dmp file and returns the fill time array
    fname: the name of the run file to read
    """
    from numpy import array, float64

    res = fname + '_res.dmp'

    with open(file_loc + res, 'r') as f:
        ff = []
        save = False
        for line in f:
            if save == True:
                try:
                    ff.append(float64(line.strip().split(' ')[-1]))
                except:
                    l = 'skipping: {}'.format(line)
                    logging.debug(l)

            if "Fill Time" in line:
                save = True

    ff = array(ff)
    ff.resize(nsize)

    return ff
