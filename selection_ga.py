########################################
# receives
#   type (string)
#   population (list) content: chromosome vectors (list)
#   selection types                    
#       roulette_selection             
#       tournament_selection           
#       uniform_selection      
# returns
#   parent1/p1 (index)
#   parent2/p2 (index)       
#######################################
import random
def selection_s(type,population,size):
    if type=="uniform":
        p1,p2 = uniform(size)
    
    elif type == "roulette":
        p1,p2 = roulette(population,size)
    
    elif type=="tournament":
        p1,p2 = tournament(population,size)

    return p1,p2

def uniform(size):
    p1,p2 = random.choices(range(size), k=2)
    return p1,p2

def roulette(population,size):
    #   calcular la probabilidad de cada individuo
    fitness=sum(population[1])
    probabilities=[]
    for _ in range (size):
        probabilities.append(population[1][_]/fitness)

    p1,p2 = random.choices(range(size),weights=probabilities,k=2)
    return p1,p2

def tournament(population,size):
    opt1,opt2,opt3,opt4 = random.sample(range(size), k=4)

    parent1 = max(opt1, opt2, key=lambda i: population[1][i])
    parent2 = max(opt3, opt4, key=lambda i: population[1][i])

    return parent1,parent2


if __name__ == "__main__":
    poblacion = ['A', 'B', 'C', 'D']
    fitness = [0.2, 0.5, 0.9, 0.4]
    population=[poblacion,fitness]
    print(roulette(population,4))