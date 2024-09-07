from auxiliar_functions import AuxiliarFunctions, debugMode
from models.knapsackModel import KnapSack
from models.populationModel import Population
from models.individualModel import Individual
import matplotlib.pyplot as plt 
from rich import print
import numpy as np 



def main() -> None:
    KnapsackItemsQuantity = 5   #Longitud de las soluciones
    SolutionsQuantity = 10      #Cantidad de soluciones
    ItemsBeneficits = np.array([51, 36, 83, 65, 40])
    ItemsWeights = np.array([30, 38, 54, 21, 32])
    MaxCapacity = 110
    mutationRate = 0.02
    crossingRate = 0.8

    knapsack = KnapSack(KnapsackItemsQuantity, SolutionsQuantity, ItemsBeneficits, ItemsWeights, MaxCapacity, crossingRate, mutationRate)
    aux.print_knapsack_info(knapsack)
    
    POPULATION = Population(knapsack)  
    POPULATION.set_individuals_objFunc(aux.calculate_ObjFuncVector(POPULATION, knapsack))   
    POPULATION.set_individuals_weights(aux.calculate_WeightVector(POPULATION, knapsack))
    aux.print_population_info(POPULATION)

main()

