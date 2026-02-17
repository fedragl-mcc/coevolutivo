########################################
# receives
#   type (string)
#   population (list) content: chromosome vectors (list)
#   selection types                    
#       roulette_selection             
#       tournament_selection           
#       uniform_selection
#   fitmetric int()     : tells selection which metric use to evaluate probabilities
# returns
#   parents_bag = list of indexes   
#######################################
import random
from random import getrandbits

def selection_s(type,population,size,fitMetric=1):
    if type=="uniform":
        parents_bag = uniform(population,size)
    
    elif type == "roulette":
        parents_bag = roulette(population,size,fitMetric)
    
    elif type=="tournament":
        parents_bag = tournament(population,size,fitMetric)

    return parents_bag

def uniform(population,size):
    #   two parents
    if False:
        p1,p2 = random.choices(range(size), k=2)
        parents_bag = [p1,p2]

    #   parents bags
    #parents_bag = [list() for i in range (len(population))]
    parents_bag=list()
    if True:
        for i in range(size):
            if not getrandbits(1):
                parents_bag.append(i)
                # # add elements to parents population (having 2 different bags)
                # for x,row in enumerate(parents_bag):
                #     row.append(population[x][i])
    return parents_bag

def roulette(population,size,fitMetric):
    #   calcular la probabilidad de cada individuo
    fitness=sum(population[fitMetric])
    probabilities=[]
    for _ in range (size):
        probabilities.append(population[fitMetric][_]/fitness)

    if False:
        p1,p2 = random.choices(range(size),weights=probabilities,k=2)
        parents_bag=p1,p2
    
    #   parents bag
    # parents_bag = [list() for i in range (len(population))]
    parents_bag = list()
    if False:
        x=random.randrange(0, fitness)
        cumu_prob = 0
        #   iterate over the population (using the probabilities)
        for i,probability in enumerate(probabilities):
            cumu_prob=cumu_prob+probability
            if cumu_prob > x:
                # add indexes to parents bag
                parents_bag.append(i)
    if True:
        #   iterate over the population (using the probabilities)
        for i,probability in enumerate(probabilities):
            x=random.randrange(0, fitness)
            if probability > x:
                parents_bag.append(i)
                # #   add to parents bag: chromosome + metrics
                # for x,row in enumerate(parents_bag):
                #     row.append(population[x][i])
    return parents_bag

def tournament(population,size,fitMetric):
    parents_bag = list()
    fitness = population[fitMetric] #choosing metric

    if False:
        opt1,opt2,opt3,opt4 = random.sample(range(size), k=4)

        parent1 = max(opt1, opt2, key=lambda i: fitness[i])
        parent2 = max(opt3, opt4, key=lambda i: fitness[i])
        parents_bag = parent1,parent2

    #   process continues until [desired] number of elements have been selected
    #deterministic
    if False:
        n_parents = random.randrange(size//2,size) #keep a random number of children being created between half and full pop
        for parents in range(n_parents/2):
            opt1,opt2 = random.sample(range(size), k=2)
            parent = opt1 if fitness[opt1] > fitness[opt2] else opt2
            parents_bag.append(parent)

    #   probabilistic [taken from: notas de clase coello]
    if True:
        n_parents = random.randrange(size // 2, size)
        p = random.uniform(0.5, 1.0)
        parents_bag = []
        for _ in range(n_parents):
            i, j = random.sample(range(size), 2)
            better, worse = (i, j) if fitness[i] > fitness[j] else (j, i)
            parent = better if random.random() < p else worse
            parents_bag.append(parent)
    return parents_bag


if __name__ == "__main__":
    poblacion = ['A', 'B', 'C', 'D']
    fitness = [0.2, 0.5, 0.9, 0.4]
    population=[poblacion,fitness]
    print(uniform(population,4))