from libs.geometry import Geometry
import numpy as np

class Solver():

    def __init__(self):
        '''defaults for the solver'''
        self._threshold = 0.01
        self._normbase = 1e-14
        self._kxx = 1
        self._timeout = 1000000
        self._stepsize = 0.1
        self._costnorm = 10000000
        self._cost = self._costnorm


    def set_target_gemoetry(self, target):
        '''set target geometry'''
        from copy import deepcopy

        if not isinstance(target, Geometry):
            raise ValueError('ERROR >> parameter target is not instance of Geometry')

        self._trial = target


    def set_target_flowtime(self, targetft):
        '''set target flowtime matrix'''

        self._targetft = targetft


    def set_threshold(self, t):
        '''set success threshold'''
        self._threshold = t


    def set_normbase(self, n):
        '''set normalization base'''
        self._normbase = n


    def set_timeout(self, t):
        '''set the timeout iteration number. if 0, it will go indefinite'''
        self._timeout = t


    def evaluate(self):
        '''evaluate the trial against the target flow time'''
        self._costp = self._cost
        self._cost = np.linalg.norm(self._targetft - self._trial.ft, 2)


    def perturb(self):
        self._kxx += self._kxx * self._stepsize


    def solve(self):
        for i in range(1, self._timeout):
            self._trial.set_permeability(kxx=self._kxx * self._normbase)
            self._trial.get_flowfront('trial')
            self.evaluate()
            print('{:6d}: knorm: {:11.4f}\tkxx: {:.4e}\t\tcost: {:10.2f}'.format(i+1, self._kxx, self._kxx*self._normbase, self._cost))
            if self._cost < self._threshold:
                print('Success in iteration # {}'.format(i))
                break

            self._stepsize = (self._cost/self._costnorm)
            if self._costp < self._cost:
                self._stepsize = -self._stepsize

            self.perturb()
