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

    #   generate children, default is 2
    def generate(self,children):
        children_bag=list()
        for _ in range(children//2):
            #   select two chromosomes for crossover, index: int()
            parent1, parent2 = self.species.selection()

            #   perform crossover to generate two new chromosomes (index [0]: chromosome )
            child1, child2 = self.species.crossover(self.species.population[0][parent1],self.species.population[0][parent2])

            #   perform mutation on the two new chromosomes
            if random.uniform(0, 1) < self.species.mutation_probability:
                child1 = self.species.mutate(child1)
            if random.uniform(0, 1) < self.species.mutation_probability:
                child2 = self.species.mutate(child2)
            
            #   add children to the bag
            children_bag.append(child1)
            children_bag.append(child2)
        
        # if True:
        #     parents_bag = self.species.selection()
        #     pb_size = len(parents_bag)//2
        #     for parent 


        return children_bag
    
    #   evaluate children: receives a list of chromosomes only, returns a list 
    def evaluate_children(self,children_bag):
        #   evaluate the children population
        for child in children_bag:
        #   evaluate each children
            if any(child):
                acc,auc,f1=self.species.fitness(child)
                #   append metrics to their lists
                self.new_individuals[0].append(child)
                self.new_individuals[1].append(acc)
                self.new_individuals[2].append(auc)
                self.new_individuals[3].append(f1)
            else:
                print(child)
                pass
        
    def compare_populations(self,children_bag):
        averages = [list() for i in range (len(self.population)-1)]
        averages = [sum(i)/len(i) for i in (self.population[1:])]

        new_pop=[list() for i in range (len(self.population))] 

        #   compare the children against the mean of the population
        comparison=list()
        for i in range (len(children_bag[0])):     #   iterate as many children are there are in the bag
            child = [x[i] for x in children_bag[1:]]
            for metric,average in zip(child,averages):
                comparison.append(metric > average)
            #   determine if it is added or not, in at least
            if comparison.count(True) >= round((len(self.population)-1)/2):
                for fitness in new_pop:
                    fitness.append(children_bag[i])
            comparison.clear()
        return new_pop

    #   a generation
    def generation(self,gen,mutation_probability,cross_probability,model,children=2):
        #   set parameters
        self.species.model=model
        self.species.cross_probability=cross_probability
        self.species.mutation_probability=mutation_probability

        #   generate children: determine the amount of children that are to be created, default is 2
        children_bag=self.generate(children)

        #   evaluate the children an store their fitness
        children_bag=self.evaluate_children(children_bag)

    def repopulate(self, shared_pop):
        for new_individual in shared_pop[0]:
            self.species.update_population(new_individual)
    
    def merge_populations(self,type="fast",weights=None):    #merging children and parents through either dominance or metric
        #   use fast
        if type == "fast":
            d=Dominance()
            self.population=d.FAST(self.new_individuals,self.population,self.population_size)
        if type == "topsis":
            self.population=self.topsis(weights)
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

    
#def coevolutivo(s1_crossp,s1_mutatep,model1,select1,crossover1,s2_crossp,s2_mutatep,model2,select2,crossover2,experiment):
if __name__ == "__main__":
    for csv_out in range(0,30):
        print(f'execution: {csv_out}')
        start_time = time.time()
        now = datetime.datetime.now()

        #create initial population, sending path and size
        path='D:\Fedra\iCloudDrive\Mcc\Tesis\Instancias\\breast_cancer_coimbra\dataR2.csv'
        population = initial_population(path)
        size = len(population[0])   #población 2n del número de caracteristicas, esto se modifica en ^^
        generations=301

        #determine operators thru a function
        s1_crossp,s1_mutatep,model1,select1,crossover1,s2_crossp,s2_mutatep,model2,select2,crossover2 = operators_parameters()
        
        #   output: print operators
        print(f'Species 1 operators Cross:{crossover1} Mutation:{s1_mutatep} Model:{model1} Selection: {select1} Crossover probability: {s1_crossp}')
        print(f'Species 2 operators Cross:{crossover2} Mutation:{s2_mutatep} Model:{model2} Selection: {select2} Crossover probability: {s2_crossp}')

        #   create: instances, <placeholder> is used to send a tuple instead of a list, refer to: https://web.archive.org/web/20200221224620id_/http://effbot.org/zone/default-values.htm
        s1 = Species(path, ("placeholder",population),selection=select1,crossover=crossover1,population_size=size)
        s2 = Species(path, ("placeholder",population),selection=select2,crossover=crossover2,population_size=size)
        
        #competition variables
        competition = 0
        winners=list()

        #coevolution generations
        for _ in range (1,generations):
            #print('generation {}'.format(_))

            #genetic algorithm / generation of children
            s1.generation(gen=_,mutation_probability=s1_mutatep,cross_probability=s1_crossp,model=model1)
            s2.generation(gen=_,mutation_probability=s2_mutatep,cross_probability=s2_crossp,model=model2)


            if (_%15)==0 & _!=generations:
                s1.merge_populations("topsis",[6,2,2])
                s2.merge_populations("topsis",[6,2,2])

            if(_%30)==0 & _!=generations:
                print('generation {}'.format(_))
                d=Dominance()
                p1=s1.population
                p2=s2.population
                merged_pop=d.FAST(p1,p2,size)
                insert= [list() for i in range(len(population))]
                for i,col in enumerate(insert):
                    col = merged_pop[i][:size%10]
                s1.repopulate(insert)
                s2.repopulate(insert)
                
        
        end = time.time()
        elapsed=(end-start_time) #seconds
        print(elapsed)

        #   print to see the population:
        population_print = False
        if population_print:
            print(f'Number of competitions {len(winners)}')
            #   print(f'Winner of each competition {winners}')
            
            for chromosome,acc,auc,f1 in zip(s1.population[0],s1.population[1],s1.population[2],s1.population[3]):
                print(f'chromosome: {chromosome}     acc: {acc}     auc: {auc}      f1: {f1}')
        
            for chromosome,acc,auc,f1 in zip(s2.population[0],s2.population[1],s2.population[2],s2.population[3]):
                print(f'chromosome: {chromosome}     acc: {acc}     auc: {auc}      f1: {f1}')

        #   print to csv
        csv_print=True
        if csv_print:
            route = f'D:\Fedra\iCloudDrive\Mcc\Tesis\\04_Semestre\Experimentacion\\coimbra\\cexp5_{csv_out}.csv'
            #   Open the CSV file in append mode
            wbcd = open(route, 'a', newline='')
            #   Create a CSV writer
            writer = csv.writer(wbcd)
            
            #   set time
            version = now.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([version])
            writer.writerow([f' gen: 300, pop_size=2n,15gen=indivtopsis[6,2,2] 30gen= sharedfast'])
            print(version)

            
            #   Headings
            heading = ['chromosome','acc','auc','f1']
            writer.writerow(['usando acc'])
            writer.writerow(heading)

            population1=s1.population
            population2=s2.population

            #write the initial population
            writer.writerow(['initial population'])
            for _ in range(size):
                chromosome = population[0][_]
                acc = population[1][_]
                auc = population[2][_]
                f1 = population[3][_]
                writer.writerow([chromosome,acc,auc,f1])

            #out csv of population
            writer.writerow(['species 1'])
            writer.writerow([f'Species 1 operators Cross:{crossover1} Mutation:{s1_mutatep} Model:{model1} Selection: {select1} Crossover probability: {s1_crossp}'])
            writer.writerow([s1_crossp,s1_mutatep,model1,select1,crossover1])
            for _ in range(size):
                chromosome = population1[0][_]
                acc = population1[1][_]
                auc = population1[2][_]
                f1 = population1[3][_]
                writer.writerow([chromosome,acc,auc,f1])

            #out csv of population
            writer.writerow(['species 2'])
            writer.writerow([f'Species 2 operators Cross:{crossover2} Mutation:{s2_mutatep} Model:{model2} Selection: {select2} Crossover probability: {s2_crossp}'])
            writer.writerow([s2_crossp,s2_mutatep,model2,select2,crossover2])
            for _ in range(size):
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

# if __name__ == "__main__":
#     s1_crossp = [.2,.4,.8]
#     s1_mutatep= [.8,.6,.2]
#     s2_crossp =[.3,.6,.9]
#     s2_mutatep= [.7,.4,.1]
#     experiment = 0
#     for crossp1,crossp2 in zip(s1_crossp,s2_crossp):
#         for muta1,muta2 in zip(s1_mutatep,s2_mutatep):
#             experiment=experiment+1
#             print(experiment)
#             select1 = random.choice(["uniform","tournament","roulette"])
#             crossover1 = random.choice(["uniform","two_point"])
#             model1 = random.choice(["RF","KNN","SVM"])
#             model2 = random.choice(["RF","KNN","SVM"])
#             select2 = random.choice(["uniform","tournament","roulette"])
#             crossover2 = random.choice(["uniform","two_point"])

#             coevolutivo(crossp1,muta1,model1,select1,crossover1,crossp2,muta2,model2,select2,crossover2,experiment)