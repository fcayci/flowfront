# wrapper for running lims

file_loc = 'runs/'


def create_lb(filename, s, dP):
    """creates the lb file
    filename is the name of the file to be generated
    s is the gate node matrix
    """
    lb = filename + '.lb'
    dmp = filename + '.dmp'
    res = filename + '_res.dmp'

    f = open(file_loc+lb, 'w')
    f.write('PROC simu\r\n')
    f.write('  DO\r\n')
    f.write('    SOLVE\r\n')
    f.write('    EXITIF 0\r\n')
    f.write('  LOOP WHILE ((SONUMBEREMPTY() > 0) AND (SONUMBERFILLED() > 0))\r\n')
    f.write('ENDPROC\r\n')
    f.write('\r\n')
    f.write('CHANGEDIR "' + file_loc + '"\r\n')
    f.write('READ "' + dmp + '"\r\n')
    for i in s:
        f.write('SETGATE ' + str(i) + ', 1, ' + '{:.6e}'.format(dP) + '\r\n')
    f.write('\r\n')
    f.write('CALL simu\r\n')
    f.write('\r\n')
    f.write('Print "# empty nodes =", sonumberempty\r\n')
    f.write('\r\n')
    f.write('SETOUTTYPE "dump"\r\n')
    f.write('WRITE "' + res + '"\r\n')
    f.write('EXIT\r\n')
    f.close()

    print('created file', file_loc + lb)
    return file_loc + lb


def create_dmp(filename, x, y, kxx, kyy, kxy=0):
    """creates the dmp file
    filename is the name of the file to be generated
    s is the node locations
    """
    from numpy import arange

    model = 'NEWTON'
    viscosity = 0.1
    height = 0.005
    vf = 0.5
    dmp = filename + '.dmp'

    f = open(file_loc+dmp, 'w')
    f.write('Number of nodes : ' + str(len(y)*len(y[0])) + '\r\n')
    f.write('{:<12} {:<14} {:<14} {:<6}\r\n'.format(' Index', 'x', 'y', 'z'))
    f.write('===================================================\r\n')

    for i in range(len(y)):
        for j in range(len(y[0])):
            f.write('{:>6} {:14.6f} {:14.6f} {:14.6f}\r\n'.format(i*len(y[0])+j+1, y[i][j], x[i][j], 0))

    elements = (len(y)-1)*(len(y[0])-1)
    f.write('Number of elements : ' + str(elements) + '\r\n')
    f.write('  Index  NNOD  N1    N2    N3   (N4)  (N5)  (N6)  (N7)  (N8)    h              Vf             Kxx             Kxy             Kyy           Kzz           Kzx            Kyz\r\n')
    f.write('==============================================================================================================================================================================\r\n')

    g = arange(1, (len(y))*(len(y[0])) +1)
    g.resize(len(y), len(y[0]))

    t = 1
    for i in range(len(g)-1):
        for j in range(len(g[0])-1):
            f.write('{:>6}{:>5}{:>6}{:>6}{:>6}{:>6}'.format(t, 4, g[i][j], g[i][j+1],g[i+1][j+1], g[i+1][j]))
            f.write('                             ')
            f.write('{:>7.3f}{:>16.6f}{:> 16.4e}{:> 16.4e}{:> 16.4e}'.format(height, vf, kxx, kxy, kyy))
            f.write('\r\n')
            t += 1

    f.write('Resin Viscosity model ' + model + '\r\n')
    f.write('Viscosity :            ' + str(viscosity) + '\r\n')
    f.close()

    print('created file', file_loc + dmp)
    return file_loc + dmp


def run_lims(lb, dmp):
    from subprocess import call

    call(['wine', 'lims/lims', '-l'+lb])


def read_res(res):
    f = open(file_loc+res, 'r')
