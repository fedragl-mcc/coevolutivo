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
        self.gen_fitness=list() #keeps a log of the means of each generation

    def generation(self,gen,mutation_probability,cross_probability,model):
        #   set parameters
        self.species.model=model
        self.species.cross_probability=cross_probability

        #   select two chromosomes for crossover, index: int()
        parent1, parent2 = self.species.selection()

        #   perform crossover to generate two new chromosomes (index [0]: chromosome )
        child1, child2 = self.species.crossover(self.species.population[0][parent1],self.species.population[0][parent2])

        #   perform mutation on the two new chromosomes
        if random.uniform(0, 1) < mutation_probability:
            child1 = self.species.mutate(child1)
        if random.uniform(0, 1) < mutation_probability:
            child2 = self.species.mutate(child2)

        #   determine children fitness (reusing variables)
        acc,auc,f1=self.species.fitness(child1)
        child1= child1,acc,auc,f1
        acc,auc,f1=self.species.fitness(child2)
        child2= child2,acc,auc,f1

        #stablish flag as false (meaning if there is/isnt improvement ) 
        improvement = False

        #   update substitution of parent in order (1,2)
        #   first child
        child = self.species.compare(child1[1],parent1,parent2)
        if child:
            self.species.update_population(child1,parent1)
            improvement = True
        #   second child
        child = self.species.compare(child2[1],parent1,parent2)
        if child:
            self.species.update_population(child2,parent2)
            improvement = True

        #add to logs    
        self.diversity.append(improvement)  #   form: true/false
        self.gen_fitness.append(self.species.evaluate_population()) #   form: [acc_mean,auc_mean,f1_mean]
    
    def repopulate(self, new_individual,index=None):
        self.species.update_population(new_individual,index)

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
    print(f'Species 1 operators Cross: {crossover1}   Mutation: {s1_mutatep}   Model: {model1}  Selection: {select1}    Crossover probability: {s1_crossp}')
    print(f'Species 2 operators Cross: {crossover2}   Mutation: {s2_mutatep}   Model: {model2}  Selection: {select2}    Crossover probability: {s2_crossp}')

    #create instances
    #placeholder is used to send a tuple insteadof a list, refer to: https://web.archive.org/web/20200221224620id_/http://effbot.org/zone/default-values.htm
    s1 = Species(path, ("placeholder",population),selection=select1,crossover=crossover1)
    s2 = Species(path, ("placeholder",population),selection=select2,crossover=crossover2)
    
    #competition variables
    competition = 0
    winners=list()

    #coevolution generations
    for _ in range (1,201):
        #   prints
        print('generation {}'.format(_))

        #genetic algorithm / generation of children
        s1.generation(gen=_,mutation_probability=s1_mutatep,cross_probability=s1_crossp,model=model1)
        s2.generation(gen=_,mutation_probability=s2_mutatep,cross_probability=s2_crossp,model=model2)

        #   evaluation
        if (_%5)==0:
            #   get the fitness of the current generation 
            curr_fit1=s1.gen_fitness[-1]
            curr_fit2=s2.gen_fitness[-1]

            #   create variables
            shared_population=[list(),list(),list(),list(),list()]
            diversity1=list()
            diversity2=list()

            #   get the values
            for i in range(_-1,_-6,-1):
                diversity1.append((s1.gen_fitness[i][0] < curr_fit1[0] )& (s1.gen_fitness[i][1] < curr_fit1[1]) & (s1.gen_fitness[i][2] < curr_fit1[2])) 
                diversity2.append((s2.gen_fitness[i][0] < curr_fit2[0]) & (s2.gen_fitness[i][1] < curr_fit2[1]) & (s1.gen_fitness[i][2] < curr_fit2[2]) ) 
            
            #   counters
            diversity1 = diversity1.count(True)
            diversity2 = diversity2.count(True)

            #   comparisons
            if diversity1 > 3 or diversity2 >3:
                print("sharedpopulation")
                winners.append(1)
    #   timer
    end = time.time()
    elapsed=(end-start_time) #seconds
    print(elapsed)

    #   print to see the population:
    population_print = False
    if population_print:
        print(f'Number of competitions {len(winners)}')
        #   print(f'Winner of each competition {winners}')
        if diversity1 > diversity2:
            for chromosome,acc,auc,f1 in zip(s1.population[0],s1.population[1],s1.population[2],s1.population[3]):
                print(f'chromosome: {chromosome}     acc: {acc}     auc: {auc}      f1: {f1}')
        else:
            for chromosome,acc,auc,f1 in zip(s2.population[0],s2.population[1],s2.population[2],s2.population[3]):
                print(f'chromosome: {chromosome}     acc: {acc}     auc: {auc}      f1: {f1}')

    #   print to csv
    csv_print=True
    if csv_print:
        #   Open the CSV file in append mode
        wbcd = open('D:\Fedra\iCloudDrive\Mcc\Tesis\Experimentacion\ouputs\wbcd_no_sharedpopulation.csv', 'a', newline='')
        #   Create a CSV writer
        writer = csv.writer(wbcd)
        
        #   set time
        version = now.strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([version])
        writer.writerow(["Populations arent being shared, only does the comparison"])
        print(version)

        
        #   Headings
        heading = ['chromosome','acc','auc','f1','time']
        writer.writerow(['usando acc'])
        writer.writerow(heading)

        population1=s1.population
        population2=s2.population

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
        writer.writerow([f'Species 1 operators Cross:{crossover1} Mutation:{s1_mutatep} Model:{model1} Selection: {select1} Crossover probability: {s1_crossp}'])
        writer.writerow([s1_crossp,s1_mutatep,model1,select1,crossover1])
        for _ in range(60):
            chromosome = population1[0][_]
            acc = population1[1][_]
            auc = population1[2][_]
            f1 = population1[3][_]
            writer.writerow([chromosome,acc,auc,f1])

        #out csv of population
        writer.writerow(['species 2'])
        writer.writerow([f'Species 2 operators Cross:{crossover2} Mutation:{s2_mutatep} Model:{model2} Selection: {select2} Crossover probability: {s2_crossp}'])
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

