
import random

from ga_initial_population import initial_population
from selection_ga import selection_s
from crossover_ga import selection_c
from classifier import Classifier

import time

class genetic_algorithm:
    def __init__(self,path,population,model):
        self.repository_path = path
        self.model=model

        #   genetic algorithm parameters
        self.population = population
        self.population_size = len(population)
        self.s_type = None #   type of selection
        self.c_type = None #   type of cross
        self.cross_probability = None
        self.mutation_probability = None

        self.dataset = None

        self.auc=None
        self.f1_score=None
        self.accuracy=None

    def selection(self):
    #   selection sends: type, population   |  return index
        parent1, parent2 = selection_s(self.s_type, self.population)
        return parent1,parent2

    def crossover(self, parent1, parent2):
    #   crossover sends type: list, parent1: chromosome vector, parent2: chromosome vector, cross probability: float  |    return offspring1/2: chromosome vector
        offspring1, offspring2 = selection_c(self.c_type,parent1,parent2,self.cross_probability)
        return offspring1, offspring2

    def mutate(self,chromosome):
    #   mutation receives:chromosome | return (mutated)chromosome
        mutation_point = random.randint(0, len(chromosome)-1)
        if chromosome[mutation_point] == 0:
            chromosome[mutation_point] = 1
            #print("Performed mutation on a chromosome")
        else:
            chromosome[mutation_point] = 0
        return chromosome

    def set_dataset(self):
        self.dataset = Classifier(path)

    def fitness(self,chromosome):
    #   fitness evaluation receives: chromosome |   return metrics 
        self.dataset.model=self.model
        self.dataset.Training(chromosome)
        self.dataset.Classif_evaluation()

        accuracy=self.dataset.accuracy
        auc=self.dataset.auc
        f1_score=self.dataset.f1_score

        return accuracy,auc,f1_score

    def evaluate_population(self): 
        #topsis??
        #use topsis to know which individuals i am going to delete?
        #find out which metric gives me the best results in my species
        auc_values=[]
        acc_values=[]
        f1_values=[]

        for chromosome in self.population:
            acc,auc,f1_score =self.fitness(chromosome)

            acc_values.append(acc) #auc
            auc_values.append(auc) #acc
            f1_values.append(f1_score) #f1

    def update_population(self,new_individual):
    #   update population   receives individual = [[chromosome],acc,auc,f1] | returns: none
        #randomly delete from the population???
        i=0
        index = random.choice(range(self.population_size))
        for individual in self.population:
            del individual[index]
            individual.append(new_individual[i])
            i+=1


    def update_species_population(self,individuals,size):
        del self.population[-size] 
        self.population = self.population + individuals

    def take_from_population(self,size):
        #takes individuals from the population
        individuals = random.sample(self.population, size) #stores them in a new list
        return individuals

    def compare(self,child,index1,index2): #recibe el fitness nadamas
        if child > self.population[1][index1]:
            return True
        elif child > self.population[1][index2]:
            return True
        else:
            return False

if __name__ == "__main__":
    start_time = time.time()
    print(start_time)

    path='D:\Fedra\iCloudDrive\Mcc\Tesis\Resources\DS_breast+cancer+wisconsin+diagnostic\wdbc.csv'
    population = initial_population(60,path)

    species = genetic_algorithm(path,population,model='RF')
    species.s_type="uniform"
    species.c_type="uniform"
    species.set_dataset()

    #Define parameters for each instance [ ](modify) #randomly assign?
    generations=200
    species.cross_probability=.8
    mutation_probability=.02
	#_______________________________________________________________________________________________________

    for _ in range(generations):
        print('generation {}'.format(_))
        #   select two chromosomes for crossover
        parent1, parent2 = species.selection()

        #   perform crossover to generate two new chromosomes
        child1, child2 = species.crossover(population[0][parent1],population[0][parent2])

        #   perform mutation on the two new chromosomes
        if random.uniform(0, 1) < mutation_probability:
            child1 = species.mutate(child1)
        if random.uniform(0, 1) < mutation_probability:
            child2 = species.mutate(child2)

        acc,auc,f1=species.fitness(child1)
        child1= child1,acc,auc,f1
        acc,auc,f1=species.fitness(child2)
        child2= child2,acc,auc,f1

        #   revisar que eventualmente podria agregar al mismo padre form: (fitness,chromosome)
        child = species.compare(child1[1],parent1,parent2)
        if child:
            species.update_population(child1)
        child = species.compare(child2[1],parent1,parent2)
        if child:
            species.update_population(child2)

    end = time.time()
    elapsed=end-start_time
    print((end - start_time)/60)
    print(species.population)
