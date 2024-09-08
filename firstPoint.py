import numpy as np 
from auxiliar_functions import aux, debugMode
from models.knapsackModel import KnapSack
from models.populationModel import Population
from models.individualModel import Individual
from rich import print
import matplotlib.pyplot as plt 
from data.parametersInfo import ParametersInformation

'''       Name:     cycle_of_life
    Parameters:   
                    -POPULATION: Instancia de la clase Population que contiene toda la información relacionada a la población de individuos
                    -knapsack:   Instancia de la clase KnapSack que contiene toda la información relacionada a la Mochila
                    -aux:        Instancia de la clase AuxiliarFunctions, nos permite utilizar los métodos que esten dentro de esta clase.
        
        Objetive:   Esta función principalmente se encarga de recibir una población inicial junto con los parámetros de la mochila, ejecutar el ciclo de vida y retornar el incumbente de toda una generación.
                    Aplicar todo el ciclo de vida de una generación:
                    1. Evaluación a la población
                    2. Selección de Padres
                    3. Cruzamiento de Padres (Nacimiento del hijo)
                    4. Mutación del hijo
                    5. Evaluación del hijo
                    6. Actualizar población
                    7. Seleccion de incumbente      '''

def cycle_of_life(POPULATION:Population, knapsack:KnapSack):
    np.random.seed(0) #Para mantener estático el mismo caso. 
    
    aux.printTittle(" -----------------------------------  2. Evaluacion de la población (Castigo)")

    if knapsack.evaluativeMethod == "p":
        adaptativeFunction = aux.punish_population(POPULATION, knapsack)
        POPULATION.set_individuals_objFunc(adaptativeFunction)

        aux.print_punishment_population_info(POPULATION)
    
    elif knapsack.evaluativeMethod == "r":
        POPULATION = aux.repairPopulation(POPULATION,knapsack)
        aux.print_punishment_population_info(POPULATION)


    aux.printTittle(" -----------------------------------  3. Selección de los padres")

    indexParent1 = aux.get_parent_index_roulette(POPULATION.individualsObjetiveFunctions, 0)
    indexParent2 = aux.get_parent_index_roulette(POPULATION.individualsObjetiveFunctions, 1)

    parent1 = Individual(POPULATION.individualsGenotypes[indexParent1])
    parent2 = Individual(POPULATION.individualsGenotypes[indexParent2])

    aux.print_parents(parent1.genotype, parent2.genotype, indexParent1, indexParent2)


    aux.printTittle(" -----------------------------------  4. Cruzamiento de los 2 padres")

    child = Individual(aux.cross_parents_upx(parent1, parent2, 0))
    child.set_fenotype(aux.calculate_ObjFuncVector(child, knapsack))
    child.set_weight(aux.calculate_WeightVector(child, knapsack))

    aux.print_individual_info("El hijo es: ",child)

    aux.printTittle(" -----------------------------------  5. Mutacion del hijo")

    child.set_genotype(aux.mutate_binary_individual(child, knapsack.mutationRate, 0))  
    child.set_fenotype(aux.calculate_ObjFuncVector(child,knapsack))
    child.set_weight(aux.calculate_WeightVector(child,knapsack))

    aux.print_individual_info("HijoMutado:",child)

    aux.printTittle(" -----------------------------------  6. Evaluacion del hijo (Castigo)")

    if knapsack.evaluativeMethod == "p":
        child.set_fenotype(aux.punish_individual(child,knapsack))   #Si el individuo es factible, no resulta castigado.
        aux.print_individual_info("HijoEvaluado:", child)
    
    elif knapsack.evaluativeMethod == "r":
        child = aux.repair_individual(child,knapsack)


    aux.printTittle(" ----------------------------------- 7. Actualizar la población")

    POPULATION.individualsGenotypes = aux.try_update_population(POPULATION, child) #Se intenta actualizar la población con el hijo (Si es hijo no es mejor que el peor de la población, se falla el intento y no se actualiza nada.)
    aux.print_population_info(POPULATION)

    '''
    8. Incumbente

    Se busca al mejor individuo de la población en una determinada generacion
    '''
    aux.printTittle(" ----------------------------------- 8. Incumbente de la población")

    icmbt_index = aux.get_best_individual_index(POPULATION)
    incumbent = Individual(POPULATION.individualsGenotypes[icmbt_index])
    incumbent.set_fenotype(aux.calculate_ObjFuncVector(incumbent,knapsack))
    incumbent.set_weight(aux.calculate_WeightVector(incumbent,knapsack))
    aux.print_individual_info("Incumbente", incumbent)    
    return incumbent



'''       Name:    main
    Parameters:    No recibe parámetros
      Objetive:    Inicializar los parámetros de la población (POPULATION) y de la mochila (knapsack)
                   En su interior, a través de un ciclo se realizan la cantidad de generaciones correspondientes a la taza de crecimiento, y a su vez por cada
                   iteración conseguimos el incumbente (gracias a cycle_of_life)    '''
def main():

    np.random.seed(34343)

    aux.printTittle(" ----------------------------------- 1. Población Inicial")
    
    # KnapsackItemsQuantity = 5   #Longitud de las soluciones
    # SolutionsQuantity = 10      #Cantidad de soluciones
    # ItemsBeneficits = np.array([51, 36, 83, 65, 40])
    # ItemsWeights = np.array([30, 38, 54, 21, 32])
    # MaxCapacity = 110
    # mutationRate = 0.02
    # crossingRate = 0.8
    # evaluativeMethod = "r"

    '''-----------------------------------------------------------------------------------'''
    data = ParametersInformation.data
    print(data["0"]["N"])

    heigth = aux.generateItemsBeneficitsVector(data["0"]["b_range"],data["0"]["n"])
    weight = aux.generateItemsWeightsVector(data["0"]["w_range"],data["0"]["n"])
    maxCap = aux.generateMaxCapacity(weight, data["0"]["alpha"])

    print(heigth)
    print(weight)
    print(maxCap)
    input()
    KnapsackItemsQuantity = data["0"]["n"]
    SolutionsQuantity = data["0"]["N"]      #Cantidad de soluciones
    ItemsBeneficits = heigth
    ItemsWeights = weight
    MaxCapacity = maxCap
    mutationRate = data["0"]["mutationRate"]
    crossingRate = data["0"]["crossingRate"]
    evaluativeMethod = data["0"]["evaluativeMethod"]

    '''------------------------------------------------------------------'''




    # knapsack = KnapSack(SolutionsQuantity, KnapsackItemsQuantity, ItemsBeneficits, ItemsWeights, MaxCapacity, crossingRate, mutationRate, evaluativeMethod)
    knapsack = KnapSack(KnapsackItemsQuantity, SolutionsQuantity, ItemsBeneficits, ItemsWeights, MaxCapacity, crossingRate, mutationRate, evaluativeMethod)
    aux.print_knapsack_info(knapsack)
    
    POPULATION = Population(knapsack)  
    print(POPULATION.individualsGenotypes.shape)
    print(knapsack.ItemsBeneficits.shape)
    print(knapsack.ItemsWeights.shape)
    input()
    POPULATION.set_individuals_objFunc(aux.calculate_ObjFuncVector(POPULATION, knapsack))   
    POPULATION.set_individuals_weights(aux.calculate_WeightVector(POPULATION, knapsack))


    
    aux.print_population_info(POPULATION)
    
    
    generations = knapsack.crossingRate*knapsack.IndividualsQuantity #retorna 4

    # Listas para almacenar las generaciones y sus fenotipos
    generations_list = []
    fenotype_list = []

    for i in range(int(generations)):
        debugMode and print(f"\n[red]---GENERACIÓN #{i}\n")
        icmbt_index = cycle_of_life(POPULATION, knapsack)
        generations_list.append(i)
        fenotype_list.append(icmbt_index.fenotype)

    # Dibujar la línea en lugar de solo puntos
    plt.plot(generations_list, fenotype_list, marker='o', linestyle='-', color='b')


    aux.printTittle(" ----------------------------------- 9. Gráfica | Incumbentes vs Generaciones")
    print(f"[yellow]\n\nEl porcentaje de cruzamiento es: [cyan]{crossingRate*100}%,[yellow] con una población total de: [cyan]{knapsack.IndividualsQuantity},[yellow] la cantidad de generaciones seran: [cyan]{crossingRate*knapsack.IndividualsQuantity}\n", )

    plt.xlabel('$generations$')
    plt.ylabel('$objectiveFunction$')
    plt.grid()
    plt.show()
    

main()
