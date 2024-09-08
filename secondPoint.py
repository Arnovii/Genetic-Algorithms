from auxiliar_functions import aux, debugMode
from models.knapsackModel import KnapSack
from models.populationModel import Population
from models.individualModel import Individual
from data.parametersInfo import ParametersInformation
import matplotlib.pyplot as plt 
from rich import print
import numpy as np 

# ItemsQuantityList = [200, 500, 750, 1000]
# w_range = np.arange(1, 21)
# b_range = np.arange(10, 101)
# alpha = 1/2

#Codificar los metodos generateItemsWeights generateItemsBeneficits generateMaxCapacity

def select_option(prmtrsInfo: dict) -> str:
    first_key = next(iter(prmtrsInfo))
    last_key = next(reversed(prmtrsInfo))

    print('[yellow]\n--------------BIENVENIDO\n\nInstancias disponibles:\n')

    # Mostrar opciones disponibles al usuario
    for instance_key, instance_info in prmtrsInfo.items():
        print(f"\t[{instance_key}] - N: {instance_info['N']}, n: {instance_info['n']}, evaluative method: [cyan]{instance_info['evaluativeMethod']}")

    # Solicitar al usuario que elija una opción
    while True:
        option = input(f"\nSeleccione una opción ({first_key}-{last_key}): ")
        
        if option in prmtrsInfo:
            print(f"\nHa seleccionado la instancia {option} con N: {prmtrsInfo[option]['N']} y n: {prmtrsInfo[option]['n']}")
            return option
        else:

            print(f"\n[red]Opción inválida. Por favor, seleccione una opción válida entre {first_key} y {last_key}.")

def knapsack_instances(data:dict) -> KnapSack:

    weights = aux.generateItemsWeightsVector(data["w_range"], data["n"])
    beneficits = aux.generateItemsBeneficitsVector(data["b_range"], data["n"])
    capacity = aux.generateMaxCapacity(weights, data["alpha"])

    ks = KnapSack(ItemsQuantity= data["n"],                         #Longitud de los individuos
                  IndividualsQuantity= data["N"],                   #Cantidad de los individuos
                  ItemsBeneficits= beneficits,                      #Array de Beneficios
                  ItemsWeights= weights,                            #Array de Pesos
                  MaxCapacity= capacity,                            #Capacidad máxima de la mochila
                  crossingRate= data["crossingRate"],               #Porcentaje de cruzamiento
                  mutationRate= data["mutationRate"],               #Porcentaje de mutación
                  evaluativeMethod= data["evaluativeMethod"]        #Método de evaluación (Reparar o Castigar)
                  )
    return ks


def cycle_of_life(POPULATION:Population, knapsack:KnapSack) -> Individual:
    np.random.seed(0) #Para mantener estático el mismo caso. 
    if knapsack.evaluativeMethod == "p":
        adaptativeFunction = aux.punish_population(POPULATION, knapsack)
        POPULATION.set_individuals_objFunc(adaptativeFunction)
        aux.print_punishment_population_info(POPULATION)
    elif knapsack.evaluativeMethod == "r":
        POPULATION = aux.repairPopulation(POPULATION,knapsack)
        aux.print_punishment_population_info(POPULATION)

    indexParent1 = aux.get_parent_index_roulette(POPULATION.individualsObjetiveFunctions, 0)
    indexParent2 = aux.get_parent_index_roulette(POPULATION.individualsObjetiveFunctions, 1)
    parent1 = Individual(POPULATION.individualsGenotypes[indexParent1])
    parent2 = Individual(POPULATION.individualsGenotypes[indexParent2])

    child = Individual(aux.cross_parents_upx(parent1, parent2, 0))
    child.set_fenotype(aux.calculate_ObjFuncVector(child, knapsack))
    child.set_weight(aux.calculate_WeightVector(child, knapsack))

    child.set_genotype(aux.mutate_binary_individual(child, knapsack.mutationRate, 0))  
    child.set_fenotype(aux.calculate_ObjFuncVector(child,knapsack))
    child.set_weight(aux.calculate_WeightVector(child,knapsack))

    if knapsack.evaluativeMethod == "p":
        child.set_fenotype(aux.punish_individual(child,knapsack))   #Si el individuo es factible, no resulta castigado.
    elif knapsack.evaluativeMethod == "r":
        child = aux.repair_individual(child,knapsack)

    POPULATION.individualsGenotypes = aux.try_update_population(POPULATION, child) #Se intenta actualizar la población con el hijo (Si es hijo no es mejor que el peor de la población, se falla el intento y no se actualiza nada.)

    icmbt_index = aux.get_best_individual_index(POPULATION)
    incumbent = Individual(POPULATION.individualsGenotypes[icmbt_index])
    incumbent.set_fenotype(aux.calculate_ObjFuncVector(incumbent,knapsack))
    incumbent.set_weight(aux.calculate_WeightVector(incumbent,knapsack))
    aux.print_individual_info("Incumbente", incumbent)    

    return incumbent


def main() -> None:
    prmtrsInfo = ParametersInformation.data
    option = select_option(prmtrsInfo)
    debugMode and print(prmtrsInfo[option])

    KNAPSACK = knapsack_instances(prmtrsInfo[option])

    POPULATION = Population(KNAPSACK)
    print(POPULATION.individualsGenotypes.shape)
    print(KNAPSACK.ItemsBeneficits.shape)
    print(KNAPSACK.ItemsWeights.shape)
    input()
    POPULATION.set_individuals_objFunc(aux.calculate_ObjFuncVector(POPULATION, KNAPSACK))   
    POPULATION.set_individuals_weights(aux.calculate_WeightVector(POPULATION, KNAPSACK))

    generations = KNAPSACK.crossingRate*KNAPSACK.IndividualsQuantity #retorna 4

    # Listas para almacenar las generaciones y sus fenotipos
    generations_list = []
    fenotype_list = []

    for i in range(int(generations)):
        icmbt_index = cycle_of_life(POPULATION, KNAPSACK)
        generations_list.append(i)
        fenotype_list.append(icmbt_index.fenotype)

    # Dibujar la línea en lugar de solo puntos
    plt.plot(generations_list, fenotype_list, marker='o', linestyle='-', color='b')

    plt.xlabel('$generations$')
    plt.ylabel('$objectiveFunction$')
    plt.grid()
    plt.show()


main()

