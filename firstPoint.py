import numpy as np 
from auxiliar_functions import AuxiliarFunctions
from models.knapsackModel import KnapSack
from models.populationModel import Population
from models.individualModel import Individual
from rich import print

np.random.seed(0) #Para mantener estático el mismo caso. 

aux = AuxiliarFunctions()
def printTittle(message:str):
    print(f"[magenta]\n{message}\n")

printTittle(" ----------------------------------- 1. Población Inicial")

KnapsackItemsQuantity = 5   #Longitud de las soluciones
SolutionsQuantity = 10      #Cantidad de soluciones
ItemsBeneficits = np.array([51, 36, 83, 65, 40])
ItemsWeights = np.array([30, 38, 54, 21, 32])
MaxCapacity = 110
mutationRate = 0.02
crossingRate = 0.8

knapsack = KnapSack(KnapsackItemsQuantity, SolutionsQuantity, ItemsBeneficits, ItemsWeights, MaxCapacity)
aux.print_knapsack_info(knapsack)

               
POPULATION = Population(knapsack)  
POPULATION.set_individuals_objFunc(aux.calculate_ObjFuncVector(POPULATION, knapsack))   
POPULATION.set_individuals_weights(aux.calculate_WeightVector(POPULATION, knapsack))
aux.print_population_info(POPULATION)

printTittle(" -----------------------------------  2. Evaluacion de la población (Castigo)")

adaptativeFunction = aux.punish_population(POPULATION, knapsack)
POPULATION.set_individuals_objFunc(adaptativeFunction)

aux.print_punishment_population_info(POPULATION)

printTittle(" -----------------------------------  3. Selección de los padres")

indexParent1 = aux.get_parent_index_roulette(POPULATION.individualsObjetiveFunctions, 0)
indexParent2 = aux.get_parent_index_roulette(POPULATION.individualsObjetiveFunctions, 1)

parent1 = Individual(POPULATION.individuals[indexParent1])
parent2 = Individual(POPULATION.individuals[indexParent2])

aux.print_parents(parent1.genotype, parent2.genotype, indexParent1, indexParent2)


printTittle(" -----------------------------------  4. Cruzamiento de los 2 padres")

child = Individual(aux.cross_parents_upx(parent1, parent2, 0))
child.set_fenotype(aux.calculate_ObjFuncVector(child, knapsack))
child.set_weight(aux.calculate_WeightVector(child, knapsack))

aux.print_individual_info("El hijo es: ",child)

printTittle(" -----------------------------------  5. Mutacion del hijo")

child.set_genotype(aux.mutate_binary_individual(child, mutationRate, 0))  
child.set_fenotype(aux.calculate_ObjFuncVector(child,knapsack))
child.set_weight(aux.calculate_WeightVector(child,knapsack))

aux.print_individual_info("HijoMutado:",child)

printTittle(" -----------------------------------  6. Evaluacion del hijo (Castigo)")

child.set_fenotype(aux.punish_individual(child,knapsack))   #Si el individuo es factible, no resulta castigado.
aux.print_individual_info("HijoEvaluado:", child)

printTittle(" ----------------------------------- 7. Actualizar la población")

POPULATION.individuals = aux.try_update_population(POPULATION, child) #Se intenta actualizar la población con el hijo (Si es hijo no es mejor que el peor de la población, se falla el intento y no se actualiza nada.)
aux.print_population_info(POPULATION)

'''
8. Incumbente

Se busca al mejor individuo de la población en una determinada generacion
'''
printTittle(" ----------------------------------- 8. Incumbente de la población")

print(f"El porcentaje de cruzamiento es: {crossingRate*100}%, con una población total de: {knapsack.IndividualsQuantity}, la cantidad de iteraciones será de: [green]{crossingRate*knapsack.IndividualsQuantity}\n", )

'''
9. Gráfica

Se hace una gráfica de FuncionObjetivo del incumbente vs número de la generación

'''

printTittle(" ----------------------------------- 9. Gráfica | Incumbentes vs Generaciones")
