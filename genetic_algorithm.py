import random
import ML_module
from selection_ga import selection
import crossover_module

import time

class genetic_algorithm:
    def __init__(self,path,repository,population,model):
        self.chromosome_size = None
        self.repository_path = path
        self.repository = repository
        self.model=model

        #   genetic algorithm parameters
        self.population = population
        self.s_type = "uniform" #   type of selection
        self.c_type = "uniform" #   type of cross
        self.cross=.8
        self.mutation_probability=.02

        self.auc=None
        self.f1_score=None
        self.accuracy=None

    def initial_population(self,population_size):
        """
        initial population currently being created: randomly
        population: list where all well performing chromosomes are going to be stored
        genes:      binary elements to choose from to create chromosome
        """
        population = []
        genes = [0, 1]

        # Create an class instance for the dataset choosing between a path (repository_path) and a uci repository (repository) code 
        ip_ml = ML_module.ModeloML(self.repository,self.repository_path)
        ip_ml.dataset_PATH() #set dataset to get the number of features = chromosome_size
        self.chromosome_size=ip_ml.features

        size=1

        while size <= population_size:
            chromosome=[]
            for _ in range(self.chromosome_size):    #   using index 
                chromosome.append(random.choice(genes))

            #call methods from class ml for fitness evaluation
            ip_ml.dataset_PATH()
            ip_ml.chromosome=chromosome                 #set the chromosome in the instance to select which features will be used
            ip_ml.data_preprocessing()                  #process data with chromosome = active features
            model = random.choice(['SVM','RF','KNN'])   #randomly select a ml model
            ip_ml.ML_model(model)                       #evaluate performance = chromosome fitness

            # evaluar chromosoma
            fitness = ip_ml.accuracy 
            if fitness > .5:
                #print(ip_ml.accuracy)
                #print(chromosome)
                size+=1
                population.append(chromosome)	#	agregar cromosoma a la poblacion

        self.population=population

    #   selection 
    #   sends: ?????????? type: string, population?????? 
    #   return parent1,parent2
    def selection(self):
        parent1, parent2 = selection(self.s_type, self.population[0])
        return parent1,parent2

    #   crossover
    #   return offspring1, offspring2
    def crossover(self, parent1, parent2):
        if self.c_type == "uniform":
            offspring1, offspring2 = ga_crossover_module.uniform_crossover(parent1,parent2,self.cross)

        elif self.c_type == "two_point":
            offspring1, offspring2 = ga_crossover_module.two_point(parent1,parent2,self.cross)

        return offspring1, offspring2

    #   mutation
    #   return (mutated)chromosome
    def mutate(self,chromosome):
        mutation_point = random.randint(0, len(chromosome)-1)
        if chromosome[mutation_point] == 0:
            chromosome[mutation_point] = 1
            #print("Performed mutation on a chromosome")
        else:
            chromosome[mutation_point] = 0
        return chromosome

    #   fitness evaluation
    #   return evaluate.accuracy 
    def fitness_evaluation(self,chromosome):
        #   mas adelante separar esto o agregarlo a _init__ y fijarlo para la instancia para dejar "abierta" la instancia de ML_module??
        evaluate=ML_module.ModeloML(self.repository,self.repository_path)
        evaluate.dataset_PATH()         #get&set dataset
        evaluate.chromosome=chromosome
        evaluate.data_preprocessing()   ##process data with chromosome = active features
        evaluate.ML_model(self.model)

        return [evaluate.fitness,evaluate.auc,evaluate.accuracy,evaluate.f1_score]   #add other metrics, if need in a matrix?

    def evaluate_population(self):
        fitness_values=[]
        auc_values=[]
        acc_values=[]
        f1_values=[]

        for chromosome in self.population:
            evaluation = self.fitness_evaluation(chromosome)

            fitness_values.append(evaluation[0]) #mean
            auc_values.append(evaluation[1]) #auc
            acc_values.append(evaluation[2]) #acc
            f1_values.append(evaluation[3]) #f1

        max_value = max(fitness_values)
        max_index = fitness_values.index(max_value)
        best_chromosome=self.population[max_index]
        pop_fitness = self.population,fitness_values,auc_values,acc_values,f1_values
        return(pop_fitness)

    #   update population
    def update_population(self,new1,new2):
        self.population=[new1[1], new2[1]] + self.population[:-2]

    def update_species_population(self,individuals,size):
        del self.population[-size] 
        self.population = self.population + individuals

    def take_from_population(self,size):
        #takes individuals from the population
        individuals = random.sample(self.population, size) #stores them in a new list
        return individuals


if __name__ == "__main__":
    start_time = time.time()
    print(start_time)
    path='D:\Fedra\iCloudDrive\Mcc\Tesis\Resources\DS_breast+cancer+wisconsin+diagnostic\wdbc.csv'

    init_pop=genetic_algorithm(path,repository=None,population=None,model=None)
    init_pop.initial_population(population_size=60)

    initial_population=init_pop.population

    S1 = genetic_algorithm(path,repository=None,population=initial_population,model='RF')
    # S2 = genetic_algorithm(path,repository=None,population=initial_population,model='KNN')
    # S3 = genetic_algorithm(path,repository=None,population=initial_population,model='SVM')

    #Define parameters for each instance [ ](modify)
    generations=300
    cross=.8
    mutation_probability=.02
	#_______________________________________________________________________________________________________


    for _ in range(generations):
        #   select two chromosomes for crossover
        S1_parent1, S1_parent2 = S1.selection()

        #   perform crossover to generate two new chromosomes
        S1_child1, S1_child2 = S1.crossover(S1_parent1, S1_parent2)

        #   perform mutation on the two new chromosomes
        if random.uniform(0, 1) < mutation_probability:
            S1_child1 = S1.mutate(S1_child1)
        if random.uniform(0, 1) < mutation_probability:
            S1_child2 = S1.mutate(S1_child2)

        #   agregar evalucion de si son mejoresQUE SUS PADRES para agregar  solo me quedo con las dos mejpres
        S1_c1=S1.fitness_evaluation(S1_child1)
        S1_c2=S1.fitness_evaluation(S1_child2)
        S1_p1=S1.fitness_evaluation(S1_parent1)
        S1_p2=S1.fitness_evaluation(S1_parent2)

        #   revisar que eventualmente podria agregar al mismo padre form: (fitness,chromosome)
        S1_add1 = max((S1_c1,S1_child1),(S1_p1,S1_parent1),(S1_p2,S1_parent2))
        S1_add2 = max((S1_c2,S1_child2),(S1_p1,S1_parent1),(S1_p2,S1_parent2))

        S1.update_population(S1_add1,S1_add2)


    S1.evaluate_population()

    end = time.time()
    elapsed=end-start_time
    print(end - start_time)