import copy
import numpy as np

class Dominance:
    def __init__(self):
        pass
    
    def isNonDominated(self,ind1,ind2):
        NonDominated=False
        equal=False
        better = 0
        e_metrics=0

        metrics=len(ind1)
        for i in range (metrics):
            if ind1[i] >= ind2[i]:
                e_metrics += 1
                if ind1[i]>ind2[i]:
                    better += 1
            else:
                break

        if e_metrics==metrics:
            equal = True
            if better >= 1:
                NonDominated = True

        return NonDominated, equal
    #   creates the front, receives population, # of metrics
    def frontier(self, population,metrics):
        #   define variables
        front = list()
        lenght_pop = len(population[0]) #  number of individuals
        
        #   outer for
        for i in range(lenght_pop):
            #   define individual = [[chromosome],acc,auc,f1...metrics...]
            individual = [population[metric][i] for metric in range(1,metrics)]
            Dominates = list()
            #   inner for
            for ii in range(lenght_pop):
                if i != ii:
                    individual2 = [population[i][ii] for i in range(1,metrics)]
                    nonDominated, equal = self.isNonDominated(individual,individual2)
                    if equal:
                        if nonDominated:
                            Dominates.append(ii)
                    else:
                        break
            if nonDominated == True and len(Dominates) > 0:
                front.append(i) #   adds the index
            # elif nonDominated == False:
            #     print(f'{i} dominated by {ii}')
        return front

    def FAST(self,joined_population,population_size):
        #   define variables
        metrics = len(joined_population) # number of elements in the list
        new_population = [list() for i in range(metrics)]
        population_left = [list() for i in range(metrics)]
        pareto_front = list()
        n_fronts = list()
        
        population = copy.deepcopy(joined_population)

        #   apply FAST until front has {popualtion_size} elements
        while sum(n_fronts) <= population_size:
            # call frontier normally (it expects list of lists)
            front = self.frontier(population, metrics)
            if len(front) == 0:
                print("everyone is on the pareto front")
                break
            else:
                #   store elements 
                for index in front:
                    pareto_front.append(index)
                #   save new population
                for i,col in enumerate(population):
                    for element in range(len(population[0])):
                        if element not in front:
                            population_left[i].append(col[element])
                #   update population
                population = population_left.copy()
                [col.clear() for col in population_left]
                #   add number of elements per front
                n_fronts.append(len(front))
                #   flag
                print(f'Front {len(n_fronts)-1}, number of elements on pareto front {len(front)}')

        #   integrate new population
        for index in pareto_front:
            for i,metric in enumerate(new_population):
                metric.append(joined_population[i][index])
        
        element=0
        while len(new_population[0]) < population_size:
            for i,metric in enumerate(new_population):
                if element not in pareto_front:
                        metric.append(joined_population[i][element])
            element+=1
        
        return new_population


if __name__== "__main__":
    pass