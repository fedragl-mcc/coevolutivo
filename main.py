from genetic_algorithm import genetic_algorithm
from ga_initial_population import initial_population
import random

class Species:
    def __init__(self, path, population,selection,crossover):
        self.population=population
        self.species = genetic_algorithm(path,population=self.population,model=None)
        self.species.s_type=selection
        self.species.c_type=crossover
        self.species.set_dataset(path)

    def generation(self,gen,mutation_probability,cross_probability,model):
        self.species.model=model
        self.species.cross_probability=cross_probability

        #   select two chromosomes for crossover
        parent1, parent2 = self.species.selection()

        #   perform crossover to generate two new chromosomes
        child1, child2 = self.species.crossover(self.species.population[0][parent1],self.species.population[0][parent2])

        #   perform mutation on the two new chromosomes
        if random.uniform(0, 1) < mutation_probability:
            child1 = self.species.mutate(child1)
        if random.uniform(0, 1) < mutation_probability:
            child2 = self.species.mutate(child2)

        acc,auc,f1=self.species.fitness(child1)
        child1= child1,acc,auc,f1
        acc,auc,f1=self.species.fitness(child2)
        child2= child2,acc,auc,f1

        #   revisar que eventualmente podria agregar al mismo padre form: (fitness,chromosome)
        child = self.species.compare(child1[1],parent1,parent2)
        if child:
            self.species.update_population(child1)
        child = self.species.compare(child2[1],parent1,parent2)
        if child:
            self.species.update_population(child2)

if __name__ == "__main__":
    path='D:\Fedra\iCloudDrive\Mcc\Tesis\Resources\DS_breast+cancer+wisconsin+diagnostic\wdbc.csv'
    population = initial_population(60,path)
    s1 = Species(path, population,selection="uniform",crossover="uniform")
    for _ in range (20):
        print('generation {}'.format(_))
        s1.generation(_,.8,.2,"RF")
    print(s1.population)

