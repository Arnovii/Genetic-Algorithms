from auxiliar_functions import aux, debugMode
from models.knapsackModel import KnapSack
from models.populationModel import Population
from models.individualModel import Individual
from data.parametersInfo import ParametersInformation
import matplotlib.pyplot as plt 
from rich import print
import numpy as np 
import time


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

def get_knapsack_instance(data:dict) -> KnapSack:

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
    # np.random.seed(0) #Para mantener estático el mismo caso. 
    debugMode and print("\n[red]Población al principio de generación...\n")
    debugMode and aux.print_population_info(POPULATION)
    debugMode and input()
    
    if knapsack.evaluativeMethod == "p":
        adaptativeFunction = aux.punish_population(POPULATION, knapsack)
        POPULATION.set_individuals_objFunc(adaptativeFunction)
        debugMode and print("[red]Población después de castigar...")
        debugMode and aux.print_population_info(POPULATION)
        debugMode and input()

    elif knapsack.evaluativeMethod == "r":
        POPULATION = aux.repairPopulation(POPULATION,knapsack)
        debugMode and print("[red]Población después de reparar...")
        debugMode and aux.print_population_info(POPULATION)
        debugMode and input()


    indexParent1 = aux.get_parent_index_roulette(POPULATION.individualsObjetiveFunctions, 0)
    indexParent2 = aux.get_parent_index_roulette(POPULATION.individualsObjetiveFunctions, 1)
    parent1 = Individual(POPULATION.individualsGenotypes[indexParent1])
    parent2 = Individual(POPULATION.individualsGenotypes[indexParent2])

    child = Individual(aux.cross_parents_upx(parent1, parent2, 0))
    child.set_fenotype(aux.calculate_ObjFuncVector(child, knapsack))
    child.set_weight(aux.calculate_WeightVector(child, knapsack))

    debugMode and print("[red]Creacion del hijo...")
    debugMode and aux.print_individual_info("child\t", child)
    debugMode and input()

    child.set_genotype(aux.mutate_binary_individual(child, knapsack.mutationRate, 0))  
    child.set_fenotype(aux.calculate_ObjFuncVector(child,knapsack))
    child.set_weight(aux.calculate_WeightVector(child,knapsack))

    debugMode and print("[red]Mutación del hijo...")
    debugMode and aux.print_individual_info("child\t", child)
    debugMode and input()

    if knapsack.evaluativeMethod == "p":
        child.set_fenotype(aux.punish_individual(child,knapsack))   #Si el individuo es factible, no resulta castigado.
        debugMode and print("[red]Hijo después de castigar...")
        debugMode and aux.print_individual_info("child\t", child)
        debugMode and input()
    elif knapsack.evaluativeMethod == "r":
        child = aux.repair_individual(child,knapsack)
        debugMode and print("[red]Hijo después de reparar...")
        debugMode and aux.print_individual_info("child\t", child)
        debugMode and input()


    POPULATION.individualsGenotypes = aux.try_update_population(POPULATION, child) #Se intenta actualizar la población con el hijo (Si es hijo no es mejor que el peor de la población, se falla el intento y no se actualiza nada.)

    icmbt_index = aux.get_best_individual_index(POPULATION)
    incumbent = Individual(POPULATION.individualsGenotypes[icmbt_index])
    incumbent.set_fenotype(aux.calculate_ObjFuncVector(incumbent,knapsack))
    incumbent.set_weight(aux.calculate_WeightVector(incumbent,knapsack))
    # incumbent.set_fenotype(POPULATION.individualsObjetiveFunctions[icmbt_index])
    # incumbent.set_weight(POPULATION.individualsWeights[icmbt_index])

    debugMode and print("\n[red]Poblacion al final de la generación...\n")
    aux.print_population_info(POPULATION)
    debugMode and print("\n[red]Incumbente...\n")
    debugMode and print("indice Incumbente:", icmbt_index, end="")
    aux.print_individual_info(f"Incumbente", incumbent)    
    debugMode and input()

    return incumbent


def main() -> None:
    np.random.seed(565456) #Esta semilla el caso "0" tiene una leve variación

    prmtrsInfo = ParametersInformation.data
    option = select_option(prmtrsInfo)
    start_time = time.time()
    debugMode and print(prmtrsInfo[option])

    KNAPSACK = get_knapsack_instance(prmtrsInfo[option])
    aux.print_knapsack_info(KNAPSACK)

    POPULATION = Population(KNAPSACK)
    POPULATION.set_individuals_objFunc(aux.calculate_ObjFuncVector(POPULATION, KNAPSACK))   
    POPULATION.set_individuals_weights(aux.calculate_WeightVector(POPULATION, KNAPSACK))


    generations = KNAPSACK.crossingRate*KNAPSACK.IndividualsQuantity #retorna 4
    # Listas para almacenar las generaciones y sus fenotipos
    generations_list = []
    fenotype_list = []
    print(f"[yellow]\n\nEl porcentaje de cruzamiento es: [cyan]{KNAPSACK.crossingRate*100}%,[yellow] con una población total de: [cyan]{KNAPSACK.IndividualsQuantity},[yellow] la cantidad de generaciones seran: [cyan]{KNAPSACK.crossingRate*KNAPSACK.IndividualsQuantity}\n", )

    for i in range(int(generations)):
        icmbt_index = cycle_of_life(POPULATION, KNAPSACK)
        generations_list.append(i)
        fenotype_list.append(icmbt_index.fenotype)

    # Dibujar la línea en lugar de solo puntos
    plt.plot(generations_list, fenotype_list, marker='o', linestyle='-', color='b')

    plt.xlabel('$generations$')
    plt.ylabel('$objectiveFunction$')
    plt.grid()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execute time: {execution_time:.4f} seconds") 
    plt.show()
 




main()

