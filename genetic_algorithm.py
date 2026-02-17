import random
import numpy as np

from ga_initial_population import initial_population
from selection_ga import selection_s
from crossover_ga import selection_c
from classifier import Classifier
from topsis import topsis as topsis_ranking

import time
import copy

class genetic_algorithm:
    def __init__(self,path,population,model):

        #   genetic algorithm parameters
        self.population = list(population)
        self.population_size = len(population[0])

        #   genetic algorithm operators
        self.s_type = None #   type of selection, selected randomly when GA instance created
        self.c_type = None #   type of cross, selected randomly when GA instance created
        self.cross_probability = None
        self.mutation_probability = None

        #set the dataset instance
        self.dataset = Classifier(path)
        #assign model
        self.model=model

        #metrics
        self.auc=None
        self.f1_score=None
        self.accuracy=None

#   selection sends: type, population, metric   |  return index / list of indexes
    def selection(self,fitMetric):
        #   if using a different metric
        #   fitMetric = acc 2...
        parents_bag = selection_s(self.s_type, self.population,self.population_size)
        return parents_bag

#   crossover sends type: list, parent1: chromosome vector, parent2: chromosome vector, cross probability: float  |    return offspring1/2: chromosome vector
    def crossover(self, parent1, parent2):
        offspring1, offspring2 = selection_c(self.c_type,parent1,parent2,self.cross_probability)
        return offspring1, offspring2

#   mutation: bit-flip | receives:chromosome | return mutated chromosome
    def mutate(self,chromosome):
        mutation_point = random.randint(0, len(chromosome)-1)
        if chromosome[mutation_point] == 0:
            chromosome[mutation_point] = 1
            #print("Performed mutation on a chromosome")
        else:
            chromosome[mutation_point] = 0
        return chromosome

#   fitness evaluation receives: chromosome     |   return metrics 
    def fitness(self,chromosome):
        self.dataset.model=self.model
        self.dataset.Training(chromosome)
        self.dataset.Classif_evaluation()

        accuracy=self.dataset.accuracy
        auc=self.dataset.auc
        f1_score=self.dataset.f1_score

        return accuracy,float(auc),f1_score
    
#   evaluate population using the means only: receives nothing, uses self only    |  returns the means of that population
    def evaluate_population(self):
        acc_mean = sum(self.population[1])/self.population_size
        auc_mean = sum(self.population[2])/self.population_size
        f1_mean = sum(self.population[3])/self.population_size
        gen_averages=[acc_mean,auc_mean,f1_mean]
        return gen_averages

#   Comparing a children against parents (or other elements): receives: fitness     |   returns: the index of the one which was best
    def compare(self,child,index1,index2): 
            if child > self.population[1][index1] & child > self.population[1][index2]:
                return True
            else:
                return False

if __name__ == "__main__":
    start_time = time.time()
    print(start_time)

    #   set path for dataset
    path='Instancias/DS_breast+cancer+wisconsin+diagnostic/wdbc.csv'
    population = initial_population(path)
    population_size=len(population[0])

    species = genetic_algorithm(path,population,model='RF')
    species.s_type="uniform"
    species.c_type="uniform"
    fitMetric = 1

    generations=5

    #Define parameters for each species
    species.cross_probability=.8
    mutation_probability=.02
	#_______________________________________________________________________________________________________
    for _ in range(generations):
        print('generation {}'.format(_))

        #   select parents and place them on a bag for crossover
        parents_bag = species.selection(fitMetric)

        #   perform crossover to generate two new chromosomes per couple of parents
        children = list()
        index2 = len(parents_bag)
        half_pointer=len(parents_bag)//2
        for index1 in range(half_pointer):
            child1,child2 = species.crossover(population[0][index1],population[0][index2])  #   call for crossover
            children.append(child1)
            children.append(child2)
            index2 -= 1     #   from the end

        #   perform (if its the case) mutation new chromosomes
        children_bag = [list() for metric in range(len(population))]
        for child in children:
            if random.uniform(0, 1) < mutation_probability:
                mchild = species.mutate(child)
            else:
                mchild=child
        #   add child (mutated or not) into the bag
            children_bag[0].append(mchild)

        #   get fitness for each children
        for child in children_bag[0]:
            acc,auc,f1=species.fitness(child)
            children_bag[1].append(acc)
            children_bag[2].append(auc)
            children_bag[3].append(f1)

        #   select individuals that will stay in the population: topsis?fast?NSGAII
        #   variables
        metrics = len(children_bag)
        joined_population = [list() for i in range(metrics)]
        # weights=[]    #   weights if using topsis
        new_pop = [list() for i in range(metrics)]
        
        #   unify population
        for i in range(metrics):
            joined_population[i] = population[i] + children_bag[i]
        
        #   rank population
        ranked_population = topsis_ranking(population=joined_population)
        
        #   slice to fit population size
        for i,metric in enumerate(new_pop):
            metric.extend(ranked_population[i][:population_size-1])

        #   stablish the population for the next generation
        species.population = copy.deepcopy(new_pop)

    end = time.time()
    elapsed=end-start_time
    print((end - start_time)/60)
