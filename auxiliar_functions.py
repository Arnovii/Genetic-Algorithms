import numpy as np
from rich import print
from models.knapsackModel import KnapSack
from models.populationModel import Population
from models.individualModel import Individual
from typing import Union
import argparse

# Procesar los argumentos de la línea de comandos
parser = argparse.ArgumentParser(description='Activate debug mode')
parser.add_argument('-d', '--debug', action='store_true', help='Activate debug mode')
args = parser.parse_args()

# Variable para controlar el modo debug
debugMode = args.debug

# Guardamos una referencia a la función original de print
old_print = print

# Sobrecargamos la función print
def print(*args, **kwargs):
    if debugMode:
        old_print(*args, **kwargs)



'''       Name:    AuxiliarFunctions
      Objetive:    Esta clase se encarga de contener métodos útiles para los algoritmos genéticos.    '''
class AuxiliarFunctions: 
#-------------------------------------- Print 

    def adaptative_tab(self, arraySize: int):   
        ''' Function to return the number of '\t' neccesary for a responsive table. ''' 
        if arraySize <= 5:
            return '\t' * int(arraySize / 2)
        else: 
            return '\t' * (int(arraySize / 2) - 1)

    def print_population_info(self, pop: Population):
        Population = pop.individuals
        ObjectiveFunctionArray = pop.individualsObjetiveFunctions
        weigthArray = pop.individualsWeights
        print(f"\n[yellow]NUMBER\tINDIVIDUAL{self.adaptative_tab(pop.genotypeLength)}O.F \tWEIGHT")
        for index, individual in enumerate(Population):
            print(f"{index}\t{individual}{self.adaptative_tab(pop.genotypeLength)}{ObjectiveFunctionArray[index]}\t{weigthArray[index]} ")
            
    def print_punishment_population_info(self, POPULATION: Population):
        Population = POPULATION.individuals
        ObjectiveFunctionArray = POPULATION.individualsObjetiveFunctions
        weigthArray = POPULATION.individualsWeights
        print(f"\n[yellow]NUMBER\tINDIVIDUAL{self.adaptative_tab(POPULATION.genotypeLength)}A.F \tWEIGHT")
        for index, individual in enumerate(Population):
            print(f"{index}\t{individual}{self.adaptative_tab(POPULATION.genotypeLength)}{ObjectiveFunctionArray[index]}\t{weigthArray[index]} ")
            
    def print_individual_info(self, title:str, indv:Individual):
        indv, ObjFunc, Weight = indv.genotype, indv.fenotype, indv.weight
        print(f"\n[yellow]{title} {self.adaptative_tab(indv.size)} O.F \t Weight")
        print(f"{indv} {self.adaptative_tab(indv.size-1)} {ObjFunc} \t {Weight} \n\n")

    def print_parents(self, p1: Individual, p2: Individual, index1, index2):
        print(f"\n[yellow]The parents are: [green]\n\tind1: [cyan]{p1} - index: {index1} [green]\n\tind2: [cyan]{p2} - index: {index2}\n")

    def print_knapsack_info(self, knapsack: KnapSack):
        print("[yellow] \n\n --- KNAPSACK PROBLEM ------------------------------ \n\n ")
        numberOfGens = knapsack.ItemsQuantity
        beneficitVectorForItem = knapsack.ItemsBeneficits
        weightVectorForItem = knapsack.ItemsWeights
        numberOfIndividuals = knapsack.IndividualsQuantity
        knapsackMaxCapacity = knapsack.MaxCapacity
        
        print(f"[yellow]\tknapsackMaxCapacity: \t\t[green] {knapsackMaxCapacity}")
        print(f"[yellow]\tNumber of gens: \t\t[green] {numberOfGens}")
        print("[yellow]\tItems: \t\t\t\t ", end="")
        for i in range(1, numberOfIndividuals + 1):
            print(f"[green]{i}", end=" ")
        
        print(f"\n[yellow]\tVector of Beneficits:\t\t [green]{beneficitVectorForItem}")
        print(f"[yellow]\tVector of weight:\t\t [green]{weightVectorForItem}")
        
        print("\n\n[yellow]--------------------------------------------------\n\n")
    
    def printTittle(self, message:str):
            print(f"[magenta]\n{message}\n")
#-------------------------------------- General

    def calculate_ObjFuncVector(self, PopOrInd: Union[Population, Individual], ks: KnapSack):
        if isinstance(PopOrInd, Population):
            return PopOrInd.individuals.dot(ks.ItemsBeneficits) 
        elif isinstance(PopOrInd, Individual):
            return PopOrInd.genotype.dot(ks.ItemsBeneficits)
            
    def calculate_WeightVector(self, PopOrInd: Union[Population, Individual], ks: KnapSack):
        if isinstance(PopOrInd, Population):
            return PopOrInd.individuals.dot(ks.ItemsWeights) 
        elif isinstance(PopOrInd, Individual):
            return PopOrInd.genotype.dot(ks.ItemsWeights)

#-------------------------------------- Evaluation
    
    def punish_individual(self, indv:Individual, ks:KnapSack):
        AdapFunc=indv.fenotype
        if indv.weight > ks.MaxCapacity:
            print("[red]The individial has been punished")
            AdapFunc = indv.fenotype - indv.weight
        else: print("[green]The individial hasn't been punished")
        return AdapFunc

    def w_m_c(self, weightIndividual, knapsackCapacity):
        return 1 if weightIndividual > knapsackCapacity else 0
        
    def punish_population(self, pop: Population, ks: KnapSack):
        ObjFuncArray, WeightArray, maxCapacityKnapsack = pop.individualsObjetiveFunctions, pop.individualsWeights, ks.MaxCapacity
        finalList = []
        for index, O_F in enumerate(ObjFuncArray):
            individualWeight = WeightArray[index]
            itemList = O_F - individualWeight * self.w_m_c(individualWeight, maxCapacityKnapsack)
            finalList.append(itemList)
        adaptFuncArray = np.array(finalList)
        
        if (pop.individualsObjetiveFunctions.all() == adaptFuncArray.all()):
            print("[green]The population haven't been punished")
        else: 
            print("[red]The population haven been punished")
        return adaptFuncArray

    def repair_individual(self, ind: Individual, ks: KnapSack):
        while ind.weight > ks.MaxCapacity:
            randomGen = np.random.randint(0, ind.genotype.size)
            ind.genotype[randomGen] = 0
            ind.weight = self.calculate_WeightVector(ind.genotype, ks.ItemsWeights)
        return ind.genotype

    def repairPopulation(self, population, vectorWeightForPop, knapsackItemsWeight, knapsackCapacity):
        for index, individual in enumerate(population):
            individualWeight = vectorWeightForPop[index]
            if individualWeight > knapsackCapacity:
                population[index] = self.repair_individual(individual, individualWeight, knapsackCapacity, knapsackItemsWeight)
        return population
        

#-------------------------------------- Parents Selection

    def get_parent_index_random(self, KnapsackItemQuantity, randomSeed: int):
        return np.random.randint(0, KnapsackItemQuantity)

    def get_parent_index_roulette(self, ObjFuncPop, randomSeed: int):
        proportionsForPop = ObjFuncPop / np.sum(ObjFuncPop)
        acumulatedProportionsForPop = np.cumsum(proportionsForPop)
        np.random.seed(randomSeed)
        AP = np.random.rand()
        conditionList = acumulatedProportionsForPop < AP
        parentIndex = np.argmin(conditionList)
        return parentIndex

#-------------------------------------- Crossing 

    def cross_parents_upx(self, p1, p2, randomSeed: int):
        parent1, parent2 = p1.genotype, p2.genotype 
        np.random.seed(randomSeed)
        genotypeLength = parent1.size
        mask = np.random.randint(0, 2, genotypeLength)
        parent1 = parent1.tolist()
        parent2 = parent2.tolist()
        mask = mask.tolist()
        children = []
        for i in range(genotypeLength):
            if mask[i] == 1:
                children.append(parent1[i])
            else:
                children.append(parent2[i])
        return np.array(children)

#-------------------------------------- Mutation

    def mutate_binary_individual(self, indiv: Individual, MutationRate, RandomSeed: int):
        np.random.seed(RandomSeed)
        randomProbability = np.random.rand()
        
        if randomProbability < MutationRate:
            print("[red]The individual has been mutated")
            indexMutatedGen = np.random.randint(0, indiv.genotype.size)
            indiv.genotype[indexMutatedGen] = 0 if indiv.genotype[indexMutatedGen] == 1 else 1
        else:
            print("[green]The individual hasn't been mutated")
        return indiv.genotype


#-------------------------------------- Updating Population

    
    def get_worst_individual_index(self, pop: Population) -> int:
        return np.argmin(pop.individualsObjetiveFunctions)

    def try_update_population(self, pop:Population, child: Individual):
        index = self.get_worst_individual_index(pop)
        print("[blue]Índice peor individuo: ", index)

        if child.fenotype > pop.individualsObjetiveFunctions[index]:
            print("[green]The generation was improved")
            pop.individuals[index] = child.genotype
            pop.individualsObjetiveFunctions[index] = child.fenotype
            pop.individualsWeights[index] = child.weight
        else:
            print("[red]Lost generation")
        return pop.individuals
    
#-------------------------------------- Incumbent
    
    def get_best_individual_index(self, pop: Population) -> int:
        return np.argmax(pop.individualsObjetiveFunctions) 
    
    