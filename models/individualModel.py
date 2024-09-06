import numpy as np

class Individual():
    def __init__(self, genotype: np.ndarray):
        self.genotype = genotype                    
        self.fenotype = None
        self.weight = None

    def set_fenotype(self, value:int):
        self.fenotype = value
        
    def set_weight(self, value:int):
        self.weight = value
        
    def set_genotype(self, newValue: np.ndarray):
        self.genotype = newValue