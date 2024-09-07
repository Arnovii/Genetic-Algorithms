from auxiliar_functions import aux, debugMode
from models.knapsackModel import KnapSack
from models.populationModel import Population
from models.individualModel import Individual
import matplotlib.pyplot as plt 
from rich import print
import numpy as np 

# ItemsQuantityList = [200, 500, 750, 1000]
# w_range = np.arange(1, 21)
# b_range = np.arange(10, 101)
# alpha = 1/2

#Codificar los metodos generateItemsWeights generateItemsBeneficits generateMaxCapacity


def knapsack_instances(n, w_range, b_range, alpha) -> KnapSack:
    weights = aux.generateItemsWeights(w_range)
    beneficits = aux.generateItemsBeneficits(b_range)
    capacity = aux.generateMaxCapacity(alpha)

    ks = KnapSack(ItemsQuantity= n,                      #Longitud de los individuos
                  IndividualsQuantity= n*2,              #Cantidad de los individuos
                  ItemsBeneficits= beneficits,           #Array de Beneficios
                  ItemsWeights= weights,                 #Array de Pesos
                  MaxCapacity= capacity,                 #Capacidad máxima de la mochila
                  crossingRate= 0.8,                     #Porcentaje de cruzamiento del 80%
                  mutationRate= 0.02,                    #Porcentaje de mutación del 2%
                  )

    return ks


def main() -> None:
    '''Un switch/case para seleccionar la instancia'''
    '''Dependiendo de la instancia elegida, se hará la lectura en una estructura de datos/clase que contenga la informacón necesaria para rellenar knapsack_instances'''
    '''con knapsack_instances crearemos la poblacion'''
    ''' con ks y pop ya crearemos un algoritmo similar a cycle of life pero sin tanto print.'''
    ''' Realizar el ciclo con las generaciones dependiendo de la taza de cruzamiento.'''



main()

