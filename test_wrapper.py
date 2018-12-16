from lims import lims_wrapper as lw
import numpy as np

filename = 'run1'
s = np.arange(1, 36*11, 36)
dP = 1e+005

x, y = np.mgrid[0:0.2:11j, 0:0.7:36j]

lb = lw.create_lb(filename, s, dP)
dmp = lw.create_dmp(filename, x, y, 1e-10, 1e-10)
lw.run_lims(lb, dmp)

f = open('runs/' + filename + '_res.dmp', 'r')

ff = []
save = False
for line in f:
    if save == True:
        try:
            ff.append(int(line.strip().split(' ')[-1]))
        except:
            print('skipping', line)

    if "Fill Time" in line:
        save = True

x = np.array(ff)
x.resize(11, 36)