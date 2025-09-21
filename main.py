from genetic_algorithm import genetic_algorithm
from ga_initial_population import initial_population

import random
import time
import csv
import datetime
import copy
class Species:
    def __init__(self, path, placeholder,selection,crossover):
        population = placeholder[1]
        self.population=copy.deepcopy(population)
        self.species = genetic_algorithm(path,self.population,model=None)
        self.species.s_type=selection
        self.species.c_type=crossover

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
    start_time = time.time()

    #   Open the CSV file in append mode
    wbcd = open('D:\Fedra\iCloudDrive\Mcc\Tesis\Experimentacion\ouputs\wbcd_coevolutivo_7.csv', 'a', newline='')
    #   Create a CSV writer
    writer = csv.writer(wbcd)
    #__________________________________________
    #   set time
    now = datetime.datetime.now()
    version = now.strftime("%Y-%m-%d %H:%M:%S")
    writer.writerow([version])
    print(version)
    #__________________________________________
    #   Headings
    heading = ['chromosome','acc','auc','f1','time']
    writer.writerow(heading)
    #_________________
    
    path='D:\Fedra\iCloudDrive\Mcc\Tesis\Resources\DS_breast+cancer+wisconsin+diagnostic\wdbc.csv'
    size=60
    population = initial_population(size,path)
    s1_crossp =.8
    s1_mutatep=.2
    s2_crossp =.6
    s2_mutatep=.4
    #place holder is used to send a tuple insteadof a list, refer to: https://web.archive.org/web/20200221224620id_/http://effbot.org/zone/default-values.htm
    s1 = Species(path, ("placeholder",population),selection="uniform",crossover="uniform")
    s2 = Species(path, ("placeholder",population),selection="tournament",crossover="uniform")

    writer.writerow(['initial population'])
    for _ in range(60):
        chromosome = population[0][_]
        acc = population[1][_]
        auc = population[2][_]
        f1 = population[3][_]
        writer.writerow([chromosome,acc,auc,f1])


    for _ in range (200):
        print('generation {}'.format(_))
        s1.generation(gen=_,mutation_probability=s1_mutatep,cross_probability=s1_crossp,model="RF")
        s2.generation(gen=_,mutation_probability=s2_mutatep,cross_probability=s2_crossp,model="KNN")

    end = time.time()
    elapsed=(end-start_time) #seconds
    print(elapsed)

    #out csv of population
    writer.writerow(['species 1'])
    for _ in range(60):
        chromosome = s1.population[0][_]
        acc = s1.population[1][_]
        auc = s1.population[2][_]
        f1 = s1.population[3][_]
        writer.writerow([chromosome,acc,auc,f1])
    
    #out csv of population
    writer.writerow(['species 2'])
    for _ in range(60):
        chromosome2 = s2.population[0][_]
        acc2 = s2.population[1][_]
        auc2 = s2.population[2][_]
        f12 = s2.population[3][_]
        writer.writerow([chromosome2,acc2,auc2,f12])

    now = datetime.datetime.now()  
    version = now.strftime("%Y-%m-%d %H:%M:%S")
    writer.writerow([version])
    print(version)
    wbcd.close()

