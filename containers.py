class ModelSetup:
    def __init__(self, origin, spacing, vp, nbpml, spc_order=2):
        self.vp = vp
        self.origin = origin
        self.spacing = spacing
        self.nbpml = nbpml
        self.model = DenseData()

    @property
    def dimensions(self):
        return self.vp.shape

    @property
    def shape(self):
        return [x+2*self.nbpml for x in self.vp.shape]

    def shift_origin(self, shift):
        self.origin = [x - shift*spacing for x, spacing in zip(self.origin, self.spacing)]

    def get_critical_dt(self):
        """ Return the computational time step value from the CFL condition"""
        # limit for infinite stencil of √(a1/a2) where a1 is the
        #  sum of absolute values of the time discretisation
        # and a2 is the sum of the absolute values of the space discretisation
        #
        # example, 2nd order in time and space in 2D
        # a1 = 1 + 2 + 1 = 4
        # a2 = 2*(1+2+1)  = 8
        # coeff = √(1/2) = 0.7
        # example, 2nd order in time and space in 3D
        # a1 = 1 + 2 + 1 = 4
        # a2 = 3*(1+2+1)  = 12
        # coeff = √(1/3) = 0.57

        # For a fixed time order this number goes down as the space order increases.
        #
        # The CFL condtion is then given by
        # dt <= coeff * h / (max(velocity))
        if len(self.vp.shape) == 3:
            coeff = 0.38
        else:
            coeff = 0.42
        return coeff * self.spacing[0] / (self.scale*np.max(self.vp))
