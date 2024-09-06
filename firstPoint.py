import numpy as np 
from auxiliar_functions import AuxiliarFunctions
from models.knapsackModel import KnapSack
from models.populationModel import Population
from models.individualModel import Individual
from rich import print

aux = AuxiliarFunctions()
def printTittle(message:str):
    print(f"[magenta]\n\n---\n{message}\n---\n\n")

printTittle("1. Población Inicial")

KnapsackItemsQuantity = 5   #Longitud de las soluciones
SolutionsQuantity = 10      #Cantidad de soluciones
ItemsBeneficits = np.array([51, 36, 83, 65, 40])
ItemsWeights = np.array([30, 38, 54, 21, 32])
MaxCapacity = 110
rateMutation = 0.02

knapsack = KnapSack(KnapsackItemsQuantity, SolutionsQuantity, ItemsBeneficits, ItemsWeights, MaxCapacity)

aux.print_knapsack_info(knapsack)
np.random.seed(0) 
               
POPULATION = Population(knapsack)  

POPULATION.set_individuals_objFunc(aux.calculate_ObjFuncVector(POPULATION, knapsack))   
POPULATION.set_individuals_weights(aux.calculate_WeightVector(POPULATION, knapsack))

aux.print_population_info_1(POPULATION)



printTittle("2. Evaluacion de la población (Castigo)")


adaptativeFunction = aux.punish_population(POPULATION, knapsack)
POPULATION.set_individuals_objFunc(adaptativeFunction)

aux.print_punishment_population_info(POPULATION)


printTittle("3. Selección de los padres")

indexParent1 = aux.get_parent_index_roulette(POPULATION.individualsObjetiveFunctions, 0)
indexParent2 = aux.get_parent_index_roulette(POPULATION.individualsObjetiveFunctions, 1)

parent1 = Individual(POPULATION.individuals[indexParent1])
parent2 = Individual(POPULATION.individuals[indexParent2])

aux.print_parents(parent1.genotype, parent2.genotype, indexParent1, indexParent2)


printTittle("4. Cruzamiento de los 2 padres")

children = Individual(aux.cross_parents_upx(parent1, parent2, 0))
children.set_fenotype(aux.calculate_ObjFuncVector(children, knapsack))
children.set_weight(aux.calculate_WeightVector(children, knapsack))

aux.print_individual_info(children)

printTittle("5. Mutacion del hijo")

children.set_genotype(aux.mutate_binary_individual(children, rateMutation, 0))  
children.set_fenotype(aux.calculate_ObjFuncVector(children,knapsack))
children.set_weight(aux.calculate_WeightVector(children,knapsack))

aux.print_individual_info(children)


printTittle("6. Evaluacion del hijo (Castigo)")


children.set_fenotype(aux.punish_individual(children,knapsack))
aux.print_individual_info(children)


'''
7. Actualizar población

Se toma de referencia al peor individuo de la población (el individuo factible que tenga la funcion objetivo mas baja)

Si el hijo es mejor que el peor de la población, el hijo reemplaza su lugar como nuevo integrante de la población.


'''

printTittle("7. Actualizar la población")



'''
8. Incumbente

Se busca al mejor individuo de la población en una determinada generacion
'''
printTittle("8. Incumbente de la población")


'''
9. Gráfica

Se hace una gráfica de FuncionObjetivo del incumbente vs número de la generación

'''

printTittle("9. Gráfica | Incumbentes vs Generaciones")
