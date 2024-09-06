import numpy as np
from rich import print
from models.knapsackModel import KnapSack
from models.populationModel import Population
from models.individualModel import Individual
from typing import Union

class AuxiliarFunctions: 

#-------------------------------------- Print 

    def adaptative_tab(self, arraySize: int):   
        ''' Function to return the number of '\t' neccesary for a responsive table. ''' 
        if arraySize <= 5:
            return '\t' * int(arraySize / 2)
        else: 
            return '\t' * (int(arraySize / 2) - 1)

    def print_population_info_1(self, POPULATION: Population):
        Population = POPULATION.individuals
        ObjectiveFunctionArray = POPULATION.individualsObjetiveFunctions
        weigthArray = POPULATION.individualsWeights
        print(f"\n[yellow]NUMBER\tINDIVIDUAL{self.adaptative_tab(POPULATION.genotypeLength)}O.F \tWEIGHT")
        for index, individual in enumerate(Population):
            print(f"{index}\t{individual}{self.adaptative_tab(POPULATION.genotypeLength)}{ObjectiveFunctionArray[index]}\t{weigthArray[index]} ")
            
    def print_punishment_population_info(self, POPULATION: Population):
        Population = POPULATION.individuals
        ObjectiveFunctionArray = POPULATION.individualsObjetiveFunctions
        weigthArray = POPULATION.individualsWeights
        print(f"\n[yellow]NUMBER\tINDIVIDUAL{self.adaptative_tab(POPULATION.genotypeLength)}A.F \tWEIGHT")
        for index, individual in enumerate(Population):
            print(f"{index}\t{individual}{self.adaptative_tab(POPULATION.genotypeLength)}{ObjectiveFunctionArray[index]}\t{weigthArray[index]} ")
            
    def print_individual_info(self, indv:Individual):
        indv, ObjFunc, Weight = indv.genotype, indv.fenotype, indv.weight
        print(f"\n[yellow]Individual {self.adaptative_tab(indv.size)} O.F \t Weight")
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
        else: print("[red]The individial hasn't been punished")
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
        return adaptFuncArray

    def repair_individual(self, individual, individualWeight, knapsackCapacity, knapsackItemsWeigth):
        while individualWeight > knapsackCapacity:
            randomGen = np.random.randint(0, individual.size)
            individual[randomGen] = 0
            individualWeight = self.calculate_WeightVector(individual, knapsackItemsWeigth)
        return individual

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

    #-------------------------------------- Cruzamiento 

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

    #-------------------------------------- Mutacion

    def mutate_binary_individual(self, indiv: Individual, MutationRate, RandomSeed: int):
        np.random.seed(RandomSeed)
        randomProbability = np.random.rand()
        
        if randomProbability < MutationRate:
            print("[red]The individual has been mutated")
            indexMutatedGen = np.random.randint(0, indiv.genotype.size)
            indiv.genotype[indexMutatedGen] = 0 if indiv.genotype[indexMutatedGen] == 1 else 1
        else:
            print("[red]The individual hasn't been mutated")
        return indiv.genotype
