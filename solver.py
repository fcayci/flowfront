class Solver():

    def __init__(self, bsize, nsize):
        self.bsize = bsize
        self.nsize = nsize

    def set_threshold(self, t):
        self.threshold = t

    def set_target(self, ft):
        self.target = ft

    def set_params(self, **args):
        params = []
        for k in args:
            params.append(k)

    def set_method(self, m):
        self.method = m
