###########################################
#   receives: type (string), p1/p2 binaryvector (list), probability (float)
#   crossover                             #
#   uniform_crossover                     #
#   two_point                             #
###########################################
import random

def selection_c(type,p1,p2,probability):
    if type=="uniform":
        offspring1,offspring2 = uniform(p1,p2,probability)
    
    elif type == "two_point":
        offspring1,offspring2 = two_point(p1,p2,probability)
    
    return offspring1, offspring2

def uniform(parent1, parent2, cross):
    # Verify that both parents have the same length
    if len(parent1) != len(parent2):
        raise ValueError("Parents must be of same lenght")
    
    # Generate two children using uniform crossover
    offspring1 = []
    offspring2 = []
    for gen1, gen2 in zip(parent1, parent2):
        # Randomly assign genes to the two offspring
        if random.random() < cross:
            offspring1.append(gen1)
            offspring2.append(gen2)
        else:
            offspring1.append(gen2)
            offspring2.append(gen1)
    return offspring1, offspring2

def two_point(parent1,parent2,cross):
    # Verify that both parents have the same length
    if len(parent1) != len(parent2):
        raise ValueError("Parents must be of same lenght")
    
    if random.random() < cross:
        # Choose two cross points 
        p1, p2 = sorted(random.sample(range(len(parent1)), 2))

        # Crear hijos
        offspring1 = parent1[:p1] + parent2[p1:p2] + parent1[p2:]
        offspring2 = parent2[:p1] + parent1[p1:p2] + parent2[p2:]
    else:
        offspring1=parent1
        offspring2=parent2

    return offspring1, offspring2

if __name__ == "__main__":
    o1,o2=two_point([0,1,1,0,1,0],[0,0,0,1,1,1],.8)
    print(o1,o2)