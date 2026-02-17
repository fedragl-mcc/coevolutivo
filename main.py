#   import modules part of the algoritthm
from genetic_algorithm import genetic_algorithm as ga
from ga_initial_population import initial_population
from topsis import topsis as topsis_ranking
from FAST import Dominance 

import random
import time
import copy
#   data handling
import csv
import datetime

class Species:
    def __init__(self, path, placeholder,selection,crossover,population_size):
        #   set initial population into the species instances
        population = placeholder[1]
        self.population=copy.deepcopy(population)
        self.population_size=population_size

        #   create instance of genetic algorithm
        self.species = ga(path,self.population,model=None)

        #   create children bag variable size = 4 ([chromosome, acc, auc, f1])
        self.new_individuals = [list() for i in range(len(self.population))]

        #   set initial selection an crossover
        self.species.s_type=selection
        self.species.c_type=crossover

    #   generate children
    # receives:     fitMetric default is 1 for acc, tells selection method which metric take into account
    # returns:      children bag list of binary vectors (not evaluated)
    def generate(self,fitMetric=1):
        children_bag=list()
        #   Generating random number of children
        #   parent selection: genetic_algorithm > selection_ga  | sends 
        parents_bag = self.species.selection(fitMetric) #fitmetric is used to tell the selection process which metric focus on when using probabilities
        pb_size = len(parents_bag)//2
        parent2=len(parents_bag)
        #   crossover: genetic_algorithm > crossover_ga | sends a pair of parent each iteration
        for parent1 in range(pb_size):
            off1,off2 = self.species.crossover(parents_bag[parent1],parents_bag[parent2])
            children_bag.append(off1)
            children_bag.append(off2)
        #   mutation
        mutation_prob = self.species.mutation_probability
        for index, child in enumerate(children_bag):
            if random.uniform(0,1) < mutation_prob:
                children_bag[index] = self.species.mutate(child)
        return children_bag
    
    #   evaluate children: receives a list of chromosomes only, returns a list 
    def evaluate_children(self,children_bag):
        #   evaluate the children population
        for child in children_bag:
        #   evaluate each children
            if any(child):  # make sure child isnt empty
                acc,auc,f1=self.species.fitness(child)
                #   append metrics to their lists
                self.new_individuals[0].append(child)
                self.new_individuals[1].append(acc)
                self.new_individuals[2].append(auc)
                self.new_individuals[3].append(f1)
            else:
                #   if child is empty
                print("empty child: ",child)
                self.new_individuals[0].append(0)
                self.new_individuals[1].append(0)
                self.new_individuals[2].append(0)
                self.new_individuals[3].append(0)
                pass
    

    #   SELECT POPULATION, receieves: type(fast/topsis), weights (for topsis)
    def merge_populations(self,type="fast",weights=None):
        #   use fast
        if type == "fast":
            d=Dominance()
            self.population=d.FAST(self.new_individuals,self.population,self.population_size)
        if type == "topsis":
            self.population=self.topsis(weights)

        #after merging population clear new_indiviuals bag
        [col.clear() for col in self.new_individuals]
        return
    
    def topsis(self,weights=None):
        metrics = len(self.new_individuals) # number of elements in the list
        joined_population = [list() for i in range(metrics)]
        #   unify population
        for i in range(metrics):
            joined_population[i] = self.population[i] + self.new_individuals[i]
        topsis_rank = topsis_ranking(population=joined_population,weights=weights) #assigning the biggest weight to F1
        
        return topsis_rank

def operators_parameters():
    #operators parameters
    #   species 1
    s1_crossp = random.choice([.2,.4,.8])
    s1_mutatep= random.choice([.8,.6,.2])
    model1 = random.choice(["RF","KNN","SVM"])
    select1 = random.choice(["uniform","tournament","roulette"])
    crossover1 = random.choice(["uniform","two_point"])

    #   species 2
    s2_crossp = random.choice([.3,.6,.9])
    s2_mutatep= random.choice([.7,.4,.1])
    model2 =  random.choice(["RF","KNN","SVM"])
    select2 = random.choice(["uniform","tournament","roulette"])
    crossover2 = random.choice(["uniform","two_point"])

    return s1_crossp,s1_mutatep,model1,select1,crossover1,s2_crossp,s2_mutatep,model2,select2,crossover2

if __name__ == "__main__":
    #   VARIABLES
    generations=300
    path = 'D:\Fedra\iCloudDrive\Mcc\Tesis\Instancias\\breast_cancer_coimbra\dataR2.csv'

    #   INITIAL POPULATION:         create initial population, send dataset path, return population
    population = initial_population(path)
    size = len(population[0])   #   population size 2(number of features) modify in initial_population()
    

    #   RANDOMLY SET OPERATORS:     for each species (use a function to prevent clutter)
    s1_crossp,s1_mutatep,model1,select1,crossover1,s2_crossp,s2_mutatep,model2,select2,crossover2 = operators_parameters()
    
    #   output: print operators
    print(f'Species 1 operators Cross:{crossover1} Mutation:{s1_mutatep} Model:{model1} Selection: {select1} Crossover probability: {s1_crossp}')
    print(f'Species 2 operators Cross:{crossover2} Mutation:{s2_mutatep} Model:{model2} Selection: {select2} Crossover probability: {s2_crossp}')

    #   CREATE INSTANCE OF GA
    #   <placeholder> is used to send a tuple instead of a list, refer to: https://web.archive.org/web/20200221224620id_/http://effbot.org/zone/default-values.htm
    s1 = Species(path, ("placeholder",population),selection=select1,crossover=crossover1,population_size=size)
    s2 = Species(path, ("placeholder",population),selection=select2,crossover=crossover2,population_size=size)
    

    #   COEVOLUTIVE PROCESS
    #==========================================================================
    #competition variables
    competition = 0
    winners=list()

    #   GENERATIONS
    for _ in range (1,generations):
        #print('generation {}'.format(_))

        #   genetic algorithm / generation of children
        s1.generation(gen=_,mutation_probability=s1_mutatep,cross_probability=s1_crossp,model=model1)
        s2.generation(gen=_,mutation_probability=s2_mutatep,cross_probability=s2_crossp,model=model2)

        #   competition
            #   retroalimentación
            #   species restart