from genetic_algorithm import genetic_algorithm as ga
from ga_initial_population import initial_population
from topsis import topsis as topsis_ranking

import random
import time
import csv
import datetime
import copy
class Species:
    def __init__(self, path, placeholder,selection,crossover):
        population = placeholder[1]
        self.population=copy.deepcopy(population)
        self.species = ga(path,self.population,model=None)
        self.species.s_type=selection
        self.species.c_type=crossover

        self.diversity = list() #flag tells if during a generation there was an improvement in either of the children
        self.gen_fitness=list()

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

        #stablish flag as false (meaning if there isnt improvement ) 
        improvement = False
        #update population if ceither of the children were better
        child = self.species.compare(child1[1],parent1,parent2)
        if child:
            self.species.update_population(child1)
            improvement = True
        child = self.species.compare(child2[1],parent1,parent2)
        if child:
            self.species.update_population(child2)
            improvement = True

        #add to logs    
        self.diversity.append(improvement)
        self.gen_fitness.append(self.species.evaluate_population())
    
    def repopulate(self, new_individual):
        self.species.update_population(new_individual)

    def topsis(self,weights=None):
        topsis_rank = topsis_ranking(self.species.population,weights)
        return topsis_rank

def operators_parameters():
    #operators parameters
    s1_crossp = random.choice([.2,.4,.8])
    s1_mutatep= random.choice([.8,.6,.2])
    model1 = random.choice(["RF","KNN","SVM"])
    select1 = random.choice(["uniform","tournament","roulette"])
    crossover1 = random.choice(["uniform","two_point"])
    s2_crossp = random.choice([.3,.6,.9])
    s2_mutatep= random.choice([.7,.4,.1])
    model2 =  random.choice(["RF","KNN","SVM"])
    select2 = random.choice(["uniform","tournament","roulette"])
    crossover2 = random.choice(["uniform","two_point"])

    return s1_crossp,s1_mutatep,model1,select1,crossover1,s2_crossp,s2_mutatep,model2,select2,crossover2

if __name__ == "__main__":
    start_time = time.time()
    now = datetime.datetime.now()

    #create initial population, sending path and size
    path='D:\Fedra\iCloudDrive\Mcc\Tesis\Resources\DS_breast+cancer+wisconsin+diagnostic\wdbc.csv'
    size=60
    population = initial_population(size,path)

    #determine operators thru a function
    s1_crossp,s1_mutatep,model1,select1,crossover1,s2_crossp,s2_mutatep,model2,select2,crossover2 = operators_parameters()
    
    #print operators
    print(f'Species 1 operators Cross:{crossover1} Mutation:{s1_mutatep} Model:{model1} Selection: {select1} Crossover probability: {s1_crossp}')
    print(f'Species 2 operators Cross:{crossover2} Mutation:{s2_mutatep} Model:{model2} Selection: {select2} Crossover probability: {s2_crossp}')

    #placeholder is used to send a tuple insteadof a list, refer to: https://web.archive.org/web/20200221224620id_/http://effbot.org/zone/default-values.htm
    s1 = Species(path, ("placeholder",population),selection=select1,crossover=crossover1)
    s2 = Species(path, ("placeholder",population),selection=select2,crossover=crossover2)
    
    #competition variables
    competition = 0
    winners=list()

    #coevolution generations
    for _ in range (200):
        print('generation {}'.format(_))
        #genetic algorithm / generation of children
        s1.generation(gen=_,mutation_probability=s1_mutatep,cross_probability=s1_crossp,model=model1)
        s2.generation(gen=_,mutation_probability=s2_mutatep,cross_probability=s2_crossp,model=model2)

        #competencia aqui (diversity tells me how many times a better child was not created (maximum 2 by generation))
        d1=s1.diversity.copy()
        d2=s2.diversity.copy()
        shared_population=[list(),list(),list(),list(),list()]

        if (d1[-5:].count(False))>=3 or (d2[-5:].count(False))>=3:
            #rank populations for each individual
            population1 = s1.topsis()
            population2 = s2.topsis()

            #determine how many individuals are the 10%
            percent=size//10
            
            # add best individuals of each species into a pool population
            for c,acc,auc,f1 in zip(population1[0][:percent],population1[1][:percent],population1[2][:percent],population1[3][:percent]):
                shared_population[0].append(c)
                shared_population[1].append(acc)
                shared_population[2].append(auc)
                shared_population[3].append(f1)
                shared_population[4].append(1)
            for c,acc,auc,f1 in zip(population2[0][:percent],population2[1][:percent],population2[2][:percent],population2[3][:percent]):
                shared_population[0].append(c)
                shared_population[1].append(acc)
                shared_population[2].append(auc)
                shared_population[3].append(f1)
                shared_population[4].append(2)
            
            #apply ranking to the pool population
            shared_population = topsis_ranking(population=shared_population,shared=True) #they chop the part where i say who is the winner species
            
            #log of which species had the most contribution
            if shared_population[-1][:percent//2].count(1) > shared_population[-1][:percent//2].count(2):
                winners.append(1)
            else:
                winners.append(2)

            #delete the last column for the "species" as i already kept the log 
            del shared_population[-1]

            # chop shared population to only the 10% best, store it in "elite population" by individual of the form (chromosome, acc,auc,f1), this log is reloaded each time the competition criteria is met
            elite_population=[]
            for i in range (percent):
                elite_population.append([])
                elite_population[i]=[shared_population[_][i] for _ in range (len(shared_population))]
            
            #mix population, call update population
            for individual in elite_population:
                s1.repopulate(individual)
                s2.repopulate(individual)
    
    print(f'Number of competitions {len(winners)}')
    #   print(f'Winner of each competition {winners}')
    if winners.count(1) > winners.count(2):
        print(s1.population)
    else:
        print(s2.population) 


    end = time.time()
    elapsed=(end-start_time) #seconds
    print(elapsed)

    csv_print=False
    if csv_print:
        #   Open the CSV file in append mode
        wbcd = open('D:\Fedra\iCloudDrive\Mcc\Tesis\Experimentacion\ouputs\wbcd_coevolutivo_pool_wbdc_29092025.csv', 'a', newline='')
        #   Create a CSV writer
        writer = csv.writer(wbcd)
        
        #   set time
        version = now.strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([version])
        print(version)
        writer.writerow([f'Species 1 operators Cross:{crossover1} Mutation:{s1_mutatep} Model:{model1} Selection: {select1} Crossover probability: {s1_crossp}'])
        writer.writerow([f'Species 2 operators Cross:{crossover2} Mutation:{s2_mutatep} Model:{model2} Selection: {select2} Crossover probability: {s2_crossp}'])

        
        #   Headings
        heading = ['chromosome','acc','auc','f1','time']
        writer.writerow(heading)
        writer.writerow(['usando f1score'])

        #write the initial population
        writer.writerow(['initial population'])
        for _ in range(60):
            chromosome = population[0][_]
            acc = population[1][_]
            auc = population[2][_]
            f1 = population[3][_]
            writer.writerow([chromosome,acc,auc,f1])

        #out csv of population
        writer.writerow(['species 1'])
        writer.writerow([s1_crossp,s1_mutatep,model1,select1,crossover1])
        for _ in range(60):
            chromosome = population1[0][_]
            acc = population1[1][_]
            auc = population1[2][_]
            f1 = population1[3][_]
            writer.writerow([chromosome,acc,auc,f1])

        #out csv of population
        writer.writerow(['species 2'])
        writer.writerow([s2_crossp,s2_mutatep,model2,select2,crossover2])
        for _ in range(60):
            chromosome = population2[0][_]
            acc = population2[1][_]
            auc = population2[2][_]
            f1 = population2[3][_]
            writer.writerow([chromosome,acc,auc,f1])
        
        now = datetime.datetime.now()  
        version = now.strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([version])
        print(version)
        wbcd.close()

