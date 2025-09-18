"""
    initial population currently being created: randomly
    population: list where all well performing chromosomes are going to be stored
    genes:      binary elements to choose from to create chromosome
"""
import random
from classifier import Classifier

def chromosome_creation(c_size):
    genes = [0, 1]
    chromosome=[]
    for _ in range(c_size):    #   using index 
        chromosome.append(random.choice(genes))
    return chromosome

def dataset(path):
    # Create an class instance for the dataset choosing between a path (repository_path) and a uci repository (repository) code 
    dataset = Classifier(path)
    return dataset

def initial_population(population_size, path):
    population = []
    dataset = Classifier(path)
    c_size = dataset.features

    while len(population) <= population_size:
        individual = chromosome_creation(c_size)

        #call methods from class classifier for fitness evaluation 
        model = random.choice(['SVM','RF','KNN'])   #randomly select a ml model
        dataset.model=model #set the model
        dataset.Training(individual)
        dataset.Classif_evaluation()
        
        # evaluate chromosoma
        fitness = dataset.accuracy
        if fitness > .5:
            population.append(individual)	#	agregar cromosoma a la poblacion
        else:
            ind=ind-1

    return population

if __name__ == "__main__":
    print("initial population")
    path='D:\Fedra\iCloudDrive\Mcc\Tesis\Resources\DS_breast+cancer+wisconsin+diagnostic\wdbc.csv'
    pop=initial_population(10,path)
    print(pop)