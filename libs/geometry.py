'''Holds Geometry class for problem setup
'''
import logging

class Geometry():

    backends = ['LIMS', 'PYT']

    def __init__(self, size, nodes):
        '''Geometry class for 2d flowfront calculation

        Args:
            size (tuple): Geometry size in meters (y, x)
            nodes (tuple): number of nodes in each direction (y, x)
        '''
        self.size = size
        self.y, self.x = size[0], size[1]
        self.nodes = nodes
        self.ynodes, self.xnodes = nodes[0], nodes[1]
        self.stepx = self.x / (self.xnodes - 1)
        self.stepy = self.y / (self.ynodes - 1)

        if self.stepx != self.stepy:
            logging.warning(">> stepx ({:.4f}) and stepy ({:.4f}) are not equal!"
              .format(self.stepx, self.stepy) )


    def set_gatenodes(self, gateloc):
        '''Set the gate node locations

        Args:
            gateloc (string): set the location of the gatenodes

            possible values are: 'w', 'nw', 'sw', 'mw, 'n', 's'
            west, north, south, middle
        '''
        from numpy import arange, array

        g = arange(1, self.xnodes*self.ynodes + 1)
        g.resize(self.nodes)

        if   gateloc ==  'w': self.gatenodes = g[:, 0]
        elif gateloc ==  'n': self.gatenodes = g[-1]
        elif gateloc ==  's': self.gatenodes = g[0]
        elif gateloc == 'nw': self.gatenodes = array(g[-1, 0])
        elif gateloc == 'sw': self.gatenodes = array(g[0, 0])
        elif gateloc == 'mw': self.gatenodes = array(g[self.ynodes//2, 0])
        else: raise ValueError('not a known gate location')


    def set_coeffs(self, mu, fi, deltaP):
        '''Sets coefficients for Darcy's equation

        Args:
            mu (float): mu coefficient
            fi (float): fi coefficient
            deltaP (float): deltaP coefficient
        '''
        self.mu = mu
        self.fi = fi
        self.deltaP = deltaP


    def set_permeability(self, kxx, kyy=0, kxy=0, krt=0):
        '''Sets permeability for each direction

        Args:
            kxx (float or numpy.ndarray): kxx values
        Kwargs:
            kyy (float or numpy.ndarray): kyy values
            kxy (float or numpy.ndarray): kxy values
            krt (float or numpy.ndarray): krt values
        '''
        self.__set_kxx(kxx)
        self.__set_kyy(kyy)
        self.__set_kxy(kxy)
        self.__set_krt(krt)


    def __set_kxx(self, kxx):
        '''set kxx values
        '''
        from numpy import full, ndarray

        if isinstance(kxx, float) or isinstance(kxx, int):
            self.kxx = full(self.nodes, float(kxx))

        elif isinstance(kxx, ndarray):
            if kxx.shape == self.nodes:
                self.kxx = kxx
            elif kxx.shape == (self.xnodes, ):
                self.kxx = ndarray(self.nodes)
                self.kxx[:] = kxx
            else:
                raise ValueError('ERROR >> kxx unknown shape')

        elif kxx is None:
            self.kxx = None

        else:
            raise TypeError('ERROR >> kxx type is not known')


    def __set_kyy(self, kyy):
        '''set kyy values
        '''
        from numpy import full, ndarray

        if isinstance(kyy, float) or isinstance(kyy, int):
            self.kyy = full(self.nodes, float(kyy))

        elif isinstance(kyy, ndarray):
            if kyy.shape == self.nodes:
                self.kyy = kyy
            elif kyy.shape == (self.ynodes, ):
                self.kyy = ndarray(self.nodes)
                self.kyy[:] = kyy
            else:
                raise ValueError('ERROR >> kyy unknown shape')

        elif kyy is None:
            self.kyy = None

        else:
            raise TypeError('ERROR >> kyy type is not known')


    def __set_kxy(self, kxy):
        '''set kxy values
        '''
        from numpy import full, ndarray

        if isinstance(kxy, float) or isinstance(kxy, int):
            self.kxy = full(self.nodes, float(kxy))

        elif isinstance(kxy, ndarray):
            if kxy.shape == self.nodes:
                self.kxy = kxy
            elif kxy.shape == (self.xnodes, ):
                self.kxy = ndarray(self.nodes)
                self.kxy[:] = kxy
            else:
                raise ValueError('ERROR >> kxy unknown shape')

        elif kxy is None:
            self.kxy = None

        else:
            raise TypeError('ERROR >> kxy type is not known')


    def __set_krt(self, krt):
        '''set krt values
        '''
        if krt is not 0:
            raise NotImplementedError('ERROR >> krt is not yet implemented')
        self.krt = krt


    def set_backend(self, backend):
        '''Choose a backend for flowfront calculation

        Args:
            backend (string): choose the backend

            possible values are: LIMS or PYT
        '''
        if backend not in self.backends:
            raise NotImplementedError('ERROR >> Unknown backend. should be either LIMS or PYT')

        self.backend = backend


    def get_flowfront(self, fname="run1"):
        '''Get flowfront
        '''
        from libs.flowfront import ft_1d, ft_lims

        if not hasattr(self, 'gatenodes'):
            raise AttributeError('ERROR >> Set gate node locations!')
        if not all(hasattr(self, attr) for attr in ['mu', 'fi', 'deltaP']):
            raise AttributeError('ERROR >> Set coefficients!')
        if not hasattr(self, 'backend'):
            raise AttributeError('ERROR >> Choose a backend!')
        if not any(hasattr(self, attr) for attr in ['kxx', 'kyy']):
            raise AttributeError('ERROR >> At least kxx or kyy should be set')

        if self.backend == 'LIMS':
            logging.info('>> Calculating flowfront in LIMS')
            self.ft, self.pr = ft_lims(self, fname)

        elif self.backend == 'PYT':
            logging.info('>> Calculating flowfront in python')
            self.ft, self.pr = ft_1d(self)


    def print_filltime(self, row=None):
        '''Print flowfront
        '''
        print('filltime:')
        if row is None:
            print(self.ft)
        else:
            print(self.ft[row])


    def print_pressure(self, row=None):
        '''Print pressure
        '''
        print('pressure data:')
        if row is None:
            print(self.pr)
        else:
            print(self.pr[row])


    def show_flowfront(self):
        '''Show flowfront
        '''
        import matplotlib.pyplot as plt
        from numpy import nanmax

        if not hasattr(self, 'ft'):
            logging.warning('>> no flowfront to show, calculating flowfront')
            self.get_flowfront()

        cmap = plt.cm.tab20b
        cmap.set_under(color='black')

        plt.title('flowfront')
        plt.imshow(self.ft, cmap=cmap, interpolation="bilinear", origin="lower", vmin=0.0000001)
        plt.colorbar()
        plt.show()


    def plot_filltime(self, showlegend=True):
        '''Plot filltime for all the rows

        Kwargs:
            showlegend (bool): Show legend on the plot
        '''
        import matplotlib.pyplot as plt
        from numpy import nanmax, transpose

        if not hasattr(self, 'ft'):
            logging.warning('WARNING >> no flowfront to plot, calculating flowfront')
            self.get_flowfront()

        plt.plot(transpose(self.ft))

        plt.title('filltime for all nodes')
        plt.xlabel('x nodes')
        plt.ylabel('filltime')
        if showlegend:
            plt.legend(['row' + str(i+1) for i in range(self.ynodes)])

        plt.show()


    def plot_pressure(self, showlegend=True):
        '''Plot pressure for all the rows

        Kwargs:
            showlegend (bool): Show legend on the plot
        '''
        import matplotlib.pyplot as plt
        from numpy import nanmax, transpose

        if not hasattr(self, 'pr'):
            logging.warning('WARNING >> no pressure data to plot, calculating flowfront/pressure')
            self.get_flowfront()

        plt.plot(transpose(self.pr))

        plt.title('pressure values for all nodes')
        plt.xlabel('x nodes')
        plt.ylabel('pressure level')
        if showlegend:
            plt.legend(['row' + str(i+1) for i in range(self.ynodes)])

        plt.show()


    def test(self, printfill=True, showflow=True, plotfill=True, printpressure=True, plotpressure=True):
        '''calculate flowfront with default values with the given geometry size/ndoes

        Kwargs:
            printflow (bool): Print flowfront values
            showflow  (bool): Show flowfront
            plotfill (bool): Plot filltime of each node
        '''
        from numpy import full

        try:
            self.set_gatenodes('w')
            self.set_coeffs(mu=0.1, fi=0.5, deltaP=1E5)
            self.set_backend('PYT')

            kxx = full(self.xnodes, 1e-10)
            kxx[self.xnodes//2:] = 2e-10

            self.set_permeability(kxx=kxx, kyy=None, kxy=None, krt=None)
            self.get_flowfront()
            if printfill:
                self.print_filltime()
            if showflow:
                self.show_flowfront()
            if plotfill:
                self.plot_filltime(showlegend=True)
            if printpressure:
                self.print_pressure()
            if plotpressure:
                self.plot_pressure(showlegend=True)

        except Exception as e:
            print(e)
            exit()
