from models.knapsackModel import KnapSack
import numpy as np

class Population():
    def __init__(self, knapsack: KnapSack):
        self.knapsack = knapsack                    #       columnas    ,   filas
        self.individualsGenotypes = np.random.randint(0,2,(knapsack.ItemsQuantity, knapsack.IndividualsQuantity))
        self.individualsObjetiveFunctions = None
        self. individualsWeights = None
        self.genotypeLength = knapsack.ItemsQuantity


    def set_individuals_objFunc(self, value):
        self.individualsObjetiveFunctions = value
        
    def set_individuals_weights(self, value):
        self.individualsWeights = value