import copy
import numpy as np

class Dominance:
    def __init__(self):
        pass
    
    def isNonDominated(self,ind1,ind2):
        NonDominated=bool()
        metrics=len(ind1)
        for i in range (metrics):
            NonDominated+=(ind1[i]>=ind2[i])
        return NonDominated
    #   creates the front, receives population, # of metrics
    def frontier(self, population,metrics):
        #   define variables
        front = list()
        lenght_pop = len(population[0]) #  number of individuals
        
        #   outer for
        for i in range(lenght_pop):
            #   define individual = [[chromosome],acc,auc,f1...metrics...]
            NonDominated = int()
            individual = [population[metric][i] for metric in range(1,metrics)]
            #   inner for
            for ii in range(lenght_pop):
                individual2 = [population[i][ii] for i in range(1,metrics)]
                if i != ii:
                    if self.isNonDominated(individual,individual2) < 2:
                        break
                    else:
                        NonDominated += 1
            if NonDominated == lenght_pop-1:
                front.append(i) #   adds the index
        return front

    def FAST(self,children_bag,parent_population,population_size):
        #   define variables
        metrics = len(children_bag) # number of metrics
        joined_population = [list() for i in range(metrics)]
        new_population = [list() for i in range(metrics)]
        pareto_front=list()

        #   unify population
        for i in range(metrics):
            joined_population[i] = parent_population[i] + children_bag[i]
        
        n_fronts = 0
        population = copy.deepcopy(joined_population)

        #   apply FAST until front has {popualtion_size} elements
        while len(pareto_front) <= population_size:
            print(f'Number of front {n_fronts}, number of elements on pareto front {len(pareto_front)}')

            # call frontier normally (it expects list of lists)
            front = self.frontier(population, metrics)

            # temporarily convert to numpy to delete individuals (columns)
            pop_array = np.array(population)
            pop_array = np.delete(pop_array, front, axis=1)  # delete columns at indices in front
            population = pop_array.tolist()  # convert back to list of lists

            pareto_front += front
            n_fronts += 1
        
        #   chop population in case there was an overgrowth
        pareto_front = pareto_front[:population_size]

        #   integrate new population
        for index in pareto_front:
            for metric in range (metrics):
                new_population[metric].append(joined_population[index][metric])
        
        return new_population


if __name__== "__main__":
    pass