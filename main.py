#   import modules part of the algoritthm
from genetic_algorithm import genetic_algorithm as ga
from ga_initial_population import initial_population
from topsis import topsis as topsis_ranking
from FAST import Dominance 

import random
import copy
import time
#   data handling
import csv
import datetime

class Species:
    def __init__(self, path, placeholder,selection,crossover,population_size,dominanceT):
        #   set initial population into the species instances
        population = placeholder[1]
        self.population=copy.deepcopy(population)
        self.population_size=population_size
        self.metrics = len(population)

        #   create instance of genetic algorithm
        self.species = ga(path,self.population,model=None)

        #   create children bag variable size = 4 ([chromosome, acc, auc, f1])
        self.new_individuals = [list() for i in range(self.metrics)]

        #   set initial selection crossover dominance type
        self.species.s_type=selection
        self.species.c_type=crossover
        self.dominanceT = dominanceT

    #   GENERATE CHILDREN
    def offsprings(self,fitMetric):
    #   receives:     fitMetric default is 1 for acc, tells selection method which metric consider
    #   returns:      children bag list of binary vectors (not evaluated)
        children_bag=list()
        #   parent selection: genetic_algorithm > selection_ga | receives a list of indexes
        parents_bag = self.species.selection(fitMetric)
        #   crossover: genetic_algorithm > crossover_ga | sends a pair of parent each iteration
        crossings = (len(parents_bag))//2
        parents1 = parents_bag[:crossings]
        parents2 = parents_bag[crossings:]
        for parent1,parent2 in zip(parents1,reversed(parents2)):
            p1 = population[0][parent1]
            p2 = population[0][parent2]
            off1,off2 = self.species.crossover(p1,p2)
            children_bag.append(off1)
            children_bag.append(off2)
            parent2-=1
        #   mutation
        mutation_prob = self.species.mutation_probability
        for index, child in enumerate(children_bag):
            if random.uniform(0,1) < mutation_prob:
                children_bag[index] = self.species.mutate(child)
        return children_bag
    
    #   EVALUATE CHILDREN AND ADD TO SELF.NEW_INDIVIDUALS: receives a list of chromosomes only, sets in self new_individuals [list(list())
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
                self.new_individuals[0].append(child)
                self.new_individuals[1].append(0)
                self.new_individuals[2].append(0)
                self.new_individuals[3].append(0)
    
    #   SELECT POPULATION, receieves: type(fast/topsis), weights (for topsis)
    def merge_populations(self,weights):
        #   unify population =======================================================
        joined_population = [list() for i in range(self.metrics)]
        for i in range(self.metrics):
            joined_population[i] = self.population[i] + self.new_individuals[i]
        #   ========================================================================
        #   use fast ===============================================================
        if self.dominanceT == "fast":
            print("New gen: pareto front")
            d=Dominance()
            self.population=d.FAST(joined_population,self.population_size)
        #   ========================================================================
        #   use topsis =============================================================
        elif self.dominanceT == "topsis":
            ranked=topsis_ranking(joined_population,weights)
            self.population=[rankedM[:self.population_size] for rankedM in (ranked)]
        #   ========================================================================
        #   after merging population clear new_indiviuals bag ======================
        [col.clear() for col in self.new_individuals]
        # ==========================================================================

        return

    #   A GENERATION: setting instance parameters, creation (selection,crossover,mutation), evaluation of offsprings
    def generation(self,mutation_probability,cross_probability,model,fitMetric=1,weights=None):
        #   set parameters
        self.species.model=model
        self.species.cross_probability=cross_probability
        self.species.mutation_probability=mutation_probability

        #   generate offsprings
        children_bag=self.offsprings(fitMetric)

        #   evaluate the children an store their fitness
        self.evaluate_children(children_bag)

        #   chop population to fit size (final population)
        self.merge_populations(weights)
    
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
    weights=[[3,3,9],[3,9,3],[9,3,3]]
    weights = random.choice(weights)

    return s1_crossp,s1_mutatep,model1,select1,crossover1,s2_crossp,s2_mutatep,model2,select2,crossover2,weights

if __name__ == "__main__":
    #   VARIABLES
    generations=5
    # path = 'D:\Fedra\iCloudDrive\Mcc\Tesis\Instancias\\breast_cancer_coimbra\dataR2.csv'
    path = 'Instancias/DS_breast+cancer+wisconsin+diagnostic/wdbc.csv'

    #   INITIAL POPULATION:         create initial population, send dataset path, return population
    population = initial_population(path)
    size = len(population[0])   #   population size 2(number of features) modify in initial_population()
    

    #   RANDOMLY SET OPERATORS:     for each species (use a function to prevent clutter)
    s1_crossp,s1_mutatep,model1,select1,crossover1,s2_crossp,s2_mutatep,model2,select2,crossover2, weights = operators_parameters()
    
    #   output: print operators
    print(f'Species 1 FAST Cross: {crossover1} Mutation: {s1_mutatep} Model: {model1} Selection: {select1} Crossover probability: {s1_crossp}')
    print(f'Species 2 TOPSIS Cross: {crossover2} Mutation: {s2_mutatep} Model: {model2} Selection: {select2} Crossover probability: {s2_crossp}')

    #   CREATE INSTANCE OF GA
    #   <placeholder> is used to send a tuple instead of a list, refer to: https://web.archive.org/web/20200221224620id_/http://effbot.org/zone/default-values.htm
    s1 = Species(path, ("placeholder",population),select1,crossover1,size,"fast")
    s2 = Species(path, ("placeholder",population),select2,crossover2,size,"topsis")
    

    #   COEVOLUTIVE PROCESS
    #==========================================================================
    #competition variables
    competition = 0
    winners=list()

    #   GENERATIONS
    for _ in range (1,generations):
        #print('generation {}'.format(_))

        #   genetic algorithm / generation of children  mutation prob, cross prob, ML model, fitness metric, weights (if required)
        s1.generation(s1_mutatep,s1_crossp,model1,1)
        s2.generation(s2_mutatep,s2_crossp,model2,1,weights)

        #   competition
            #   retroalimentación
            #   species restart