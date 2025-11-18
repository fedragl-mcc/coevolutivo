"""
    initial population currently being created: randomly
    population: list where all well performing chromosomes are going to be stored
    genes:      binary elements to choose from to create chromosome
    receives: population size, path
    returns: population = [[individuals][accuracy][auc][f1]]
"""
import random
from classifier import Classifier

def chromosome_creation(c_size):
    genes = [0, 1]
    chromosome=[]
    for _ in range(c_size):    #   using index 
        chromosome.append(random.choice(genes))
    return chromosome


def initial_population(population_size, path):
    individuals=[]
    individual=[]
    accs=[]
    aucs=[]
    f1s=[]

    dataset = Classifier(path)
    c_size = dataset.features
    ind=0

    while len(individuals) < population_size:
        while any(individual) == False: #   there must be at least one feature present (bc during coimbra dataset i had a lot of trouble)
            individual = chromosome_creation(c_size)

        #call methods from class classifier for fitness evaluation 
        model = random.choice(['SVM','RF','KNN'])   #randomly select a ml model
        dataset.model=model #set the model
        dataset.Training(individual)
        dataset.Classif_evaluation()
        
        # evaluate chromosoma
        fitness = dataset.accuracy
        if fitness > .5:
            individuals.append(individual.copy())	#	agregar cromosoma a la poblacion
            accs.append(dataset.accuracy)
            aucs.append(float(dataset.auc))
            f1s.append(dataset.f1_score)
        else:
            ind=ind-1
        individual.clear()

    population = individuals,accs,aucs,f1s

    return population

if __name__ == "__main__":
    print("initial population")
    path='D:\Fedra\iCloudDrive\Mcc\Tesis\Resources\DS_breast+cancer+wisconsin+diagnostic\wdbc.csv'
    pop=initial_population(10,path)
    print(pop)