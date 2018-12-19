# author: Furkan Cayci
# description:

import numpy as np
from common import *
from lims_common import *

BOARDSIZE = (0.2, 0.7) # board size in meters (y, x)
NODESIZE = (11, 36) # number of nodes in each direction (y, x)
n_of_runs = 1 # repeated runs for trial averaging
trials = []   # array to hold trial numbers for each run
backend = 'PITON' # 'PITON'

#### Create target flowfront

# create coefficients
c = Coeffs(mu=0.1, fi=0.5, deltaP=1e5)

# create permeability map instance
# elements can be accessed by p.kxx
p_t = PMap(kxx=1e-10, kyy=1e-10, kxy=1e-12, krt=5e-10)
# randomize if needed
p_t.randomize()

params_opt = ('kxx')

# create gate locations
gatelocs = set_gatenodes(NODESIZE, 'sw')
# calculate target flow time
if backend == 'LIMS':
    ft_t = lims_flowtime(BOARDSIZE, NODESIZE, p_t, c, 'run1', gatelocs)
else:
    ft_t = calculate_flowtime(BOARDSIZE, NODESIZE, p_t, c)
#print(ft_t)

show_img(ft_t)
# create parameters
n_of_iters = 0
threshold = 0.01
p = PMap(kxx=1e-10)
pp = PMap(kxx=2e-10)
# p.randomize()

kxx_sign = 0
kyy_sign = 0
kxy_sign = 0
gammax = 0.3
gammay = 0.95
gammaz = 0.2

cost = 0
cost_prev = 0
cost_max = 0
cost_norm = 0

optnum = 0

for t in range(n_of_iters):

    # if t % 100 == 0:
    #     optnum += 1

    # if optnum == len(params_opt):
    #     optnum = 0


    if backend == 'LIMS':
        ft = lims_flowtime(BOARDSIZE, NODESIZE, p, c, 'solve3d', gatelocs)
    else:
        ft = calculate_flowtime(BOARDSIZE, NODESIZE, p, c, 'solve3d')

    if optnum == 0:
        kxx_sign = np.sign(pp.kxx - p.kxx)
    elif optnum == 1:
        kyy_sign = np.sign(pp.kyy - p.kyy)
    elif optnum == 2:
        kxy_sign = np.sign(pp.kxy - p.kxy)
    elif optnum == 3:
        kxy_sign = np.sign(pp.kxy - p.kxy)

    cost_prev = cost
    cost = np.linalg.norm(ft_t - ft, 2)
    cost_max = max(cost_max, cost)
    cost_norm = abs(cost) / cost_max

    print('{:5} '.format(t),end='')
    print('x: {:14.4e} '.format(p.kxx),end='')
   #print('y: {:14.4e} '.format(p.kyy),end='')
    #print('z: {:14.4e} '.format(p.kxy),end='')
    #print('r: {:14.4e} '.format(p.krt),end='')
    print('c: {:14.4e} '.format(cost),end='')
    print('cn: {:7.6e}'.format(cost_norm),end='')
    print()

    if cost < threshold:
        print('Success in {} iterations'.format(t))
        #trials.append(t)
        print('lims', ft_t)
        print('model', ft)
        show_imgs(ft_t, ft)
        break

    if optnum == 0:
        pp.kxx = p.kxx
        p.kxx -= kxx_sign * np.sign(cost_prev - cost) * gammax * p.kxx
    elif optnum == 1:
        pp.kyy = p.kyy
        p.kyy -= kyy_sign * np.sign(cost_prev - cost) * gammay * p.kyy * cost_norm
    elif optnum == 2:
        pp.kxy = p.kxy
        p.kxy -= kxy_sign * np.sign(cost_prev - cost) * gammaz * p.kxy * cost_norm

else:
    print('lims', ft_t)
    print('model', ft)
    print('kxx original', p_t.kxx)
    print('kyy original', p_t.kyy)
    print('Fail')
    #break

# else:
#     print('Success for {} runs with {} iters per run'.format(n_of_runs, np.mean(trials)))