from main import Species
from main import random_operators as randOperate
#   import modules part of the algoritthm
from genetic_algorithm import genetic_algorithm as ga
from ga_initial_population import initial_population
from topsis import topsis as topsis_ranking
from FAST import Dominance 

import random
import copy
import math
import numpy as np
import time
#   data handling
import csv
import datetime
import numpy as np

def capture_rate(prey_traits, predator_traits, a0=1.0, theta=5.0, weights=None):
    prey = np.array(prey_traits)
    pred = np.array(predator_traits)
    
    if weights is None:
        weights = np.ones_like(prey)
    else:
        weights = np.array(weights)
    
    # Performance advantage 
    S = np.sum(weights * (pred - prey))
    
    # Logistic transformation
    capture = a0 / (1 + np.exp(-theta * S))
    # print(round(S*100))
    # print(round(capture*100))

    winner = (1 if S > 0 else 0)    #send 1 if winner is predator
    
    return winner

if __name__ == "__main__":
    #   Declare path instance
    path = 'Instancias/DS_breast+cancer+wisconsin+diagnostic/wdbc.csv'
    #   ===============================================================
    #   Main variables
    generations=30
    timeSize = 2    #   population = timeSize*(number of features), timeSize default is 2
    numPredators = 1
    numPreys = 2

    #   INITIAL POPULATION:         create initial population, send dataset path, return population
    population = initial_population(path,timeSize) 
    popSize = len(population[0])   
    metrics = len(population)-1 #   number of metrics is always len(population)-1 as [0] is the vector
    
    #   Create instance of GA
    species=[]
    for specie in range (numPredators+numPreys):
        selectionT, crossoverT = randOperate("create")
        species.append(Species(path,("placeholder",population), selectionT, crossoverT,popSize,"fast"))
        #   output: print operators
        print(f'Selection type: {selectionT} | Cross type: {crossoverT}')

    speOperators=[]
    for specie in species:
        crossp,mutatep,model = randOperate("set")
        speOperators.append([crossp,mutatep,model])

    #   COEVOLUTIVE PROCESS
    #==========================================================================
    #competition variables
    predation = 0


    #   GENERATIONS
    for generation in range (1,generations):
        #print('generation {}'.format(_))

        #   genetic algorithm / generation of children  mutation prob, cross prob, ML model, fitness metric, weights (if required)
        #   Predator
        species[0].generation(speOperators[0],1)    #   focuses on acc
        #   Preys
        species[1].generation(speOperators[1],1)    #   focuses on auc
        species[2].generation(speOperators[2],3)    #   focuses on f1

        #   [MISSING] get growth rate from these

        #   Competition
        if generation%5 == 0:
            #   using prey/predator competition
            sampleSize = round(math.sqrt(popSize))

            #   predator/preys population
            popPredator = species[0].population
            popPrey1 = species[1].population
            popPrey2 = species[2].population


            #   currently  a prey population against samples of predator's population, 
            #   but i could also try a whole population agaisnts the other
            predWins=0
            preyWins=0
            for ind in range(popSize):
                indPrey = [metric[ind] for metric in popPrey1[1:]]  #   taking only the metrics from the individual
                samplePred = random.sample(range(0,popSize-1),k = sampleSize)
                for versus in samplePred:
                    indPred = [metric[versus] for metric in popPredator[1:]]    #   taking only the metrics from the individual
                    win = capture_rate(indPrey,indPred)
                    if win == 1:
                        predWins+=1
                    else:
                        preyWins+=1
            #   actual number of versus = sampleSize * len(preyPop[0]){preyPopSize}
            if preyWins > predWins:
                print(f'Prey 1 escapes {preyWins}/{sampleSize*popSize}')
                #print(species[1].evolution)
            else:
                print(f'Predator captures {predWins}/{sampleSize*popSize}')
                #print(species[0].evolution)
            #   second vs
            predBWins=0
            prey2Wins=0
            for ind in range(popSize):
                indPrey = [metric[ind] for metric in popPrey2[1:]]  #   taking only the metrics from the individual
                samplePred = random.sample(range(0,popSize-1),k = sampleSize)
                for versus in samplePred:
                    indPred = [metric[versus] for metric in popPredator[1:]]    #   taking only the metrics from the individual
                    win = capture_rate(indPrey,indPred)
                    if win == 1:
                        predBWins+=1
                    else:
                        prey2Wins+=1
            #   actual number of versus = sampleSize * len(preyPop[0]){preyPopSize}
            if prey2Wins > predBWins:
                print(f'prey 2 escapes {prey2Wins}/{sampleSize*popSize}')
                #print(species[2].evolution)
            else:
                print(f'Predator captures {predBWins}/{sampleSize*popSize}')
                #print(species[0].evolution)
            predation+=1

            #   retroalimentación
            #   how is the outcome of the competition going to affect the species?
