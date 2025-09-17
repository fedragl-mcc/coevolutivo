########################################
# receives
#   type (string)
#   population (list) content: chromosome vector (list)
#   selection types                    
#       roulette_selection             
#       tournament_selection           
#       uniform_selection              
#######################################
import random
def selection_s(type,population):
    population = population
    if type=="uniform":
        p1,p2 = uniform(population)
    
    elif type == "roulette":
        p1,p2 = roulette()
    
    elif type=="tournament":
        p1,p2 = tournament()

    return p1,p2

def uniform(population):
    parent1,parent2 = random.choices(population, k=2)
    return parent1,parent2

def roulette(pop_fitness):
    """selección por ruleta"""
    #   evaluar el fitness de toda la poblacion
    fitness=sum(pop_fitness[1])
    probabilities=[]
    for _ in range (0,len(pop_fitness[1])):
        probabilities.append(pop_fitness[1][_]/fitness)
    parent1,parent2 = random.choices(pop_fitness[0], weights=probabilities, k=2)
    return parent1,parent2

def tournament(xy_values):
    opt1,opt2,opt3,opt4 = random.sample(range(len(xy_values[0])), k=4)
    if xy_values[1][opt1] > xy_values[1][opt2]:
        parent1 = xy_values[0][opt1]
    else:
        parent1 = xy_values[0][opt2]
    if xy_values[1][opt3] > xy_values[1][opt4]:
        parent2 = xy_values[0][opt3]
    else:
        parent2 = xy_values[0][opt4]
    return parent1,parent2


if __name__ == "__main__":
    poblacion = ['A', 'B', 'C', 'D']
    fitness = [0.2, 0.5, 0.9, 0.4]
    print(tournament([poblacion,fitness]))