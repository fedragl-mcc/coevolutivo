from main import Species
from main import random_operators as randOperate
from main import join_populations as joinPop
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

    winner = (1 if S > 0 else 0)    #send 1 if winner is predator
    
    return winner,capture

if __name__ == "__main__":
    #   Declare path instance
    # path = 'Instancias/DS_breast+cancer+wisconsin+diagnostic/wdbc.csv'
    path = 'D:\Fedra\coevolutivo\Instancias\\breast_cancer_uci\\breast_cancer.csv'
    #   ===============================================================
    #   Main variables
    timeSize = 2    #   population = timeSize*(number of features), default is 2
    numPredators = 1
    numPreys = 2

    numPredation = 1
    #   INITIAL POPULATION:         create initial population, send dataset path, return population
    population = initial_population(path,timeSize) 
    popSize = len(population[0])   
    metrics = len(population)-1 #   number of metrics is always len(population)-1 as [0] is the vector
    chromosomeSize = len(population[0][0])
    # generations=popSize*chromosomeSize
    generations=500
    competition = 10

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
    rePopPerc = 10  #percentage for repopulation
    start_time = time.time()
    
    #   GENERATIONS
    for generation in range (1,generations):
        print('generation {}'.format(generation))

        #   genetic algorithm / generation of children  mutation prob, cross prob, ML model, fitness metric, weights (if required)
        #   Predator
        species[0].generation(speOperators[0],1)    #   focuses on acc
        #   Preys
        species[1].generation(speOperators[1],2,)    #   focuses on auc
        species[2].generation(speOperators[2],2)    #   focuses on f1

        #   [MISSING] get growth rate from these

        #   Competition
        if generation%competition == 0:
            # print("predation:",numPredation)
            #   using prey/predator competition
            sampleSize = round(math.sqrt(popSize))

            #   predator/preys population
            popPredator = species[0].population
            popPrey1 = species[1].population
            popPrey2 = species[2].population

            #   currently  a prey population against samples of predator's population, 
            #   but i could also try a whole population agaisnts the other
            #   vs1: prey 1 vs predator
            predWins=0
            preyWins=0
            for ind in range(popSize):
                indPrey = [metric[ind] for metric in popPrey1[1:]]  #   taking only the metrics from the individual
                samplePred = random.sample(range(0,popSize-1),k = sampleSize)
                for versus in samplePred:
                    indPred = [metric[versus] for metric in popPredator[1:]]    #   taking only the metrics from the individual
                    win,capture = capture_rate(indPrey,indPred)
                    if win == 1:
                        predWins+=1
                    else:
                        preyWins+=1
            #   vs2: prey 2 vs predator
            predBWins=0
            prey2Wins=0
            for ind in range(popSize):
                indPrey = [metric[ind] for metric in popPrey2[1:]]  #   taking only the metrics from the individual
                samplePred = random.sample(range(0,popSize-1),k = sampleSize)
                for versus in samplePred:
                    indPred = [metric[versus] for metric in popPredator[1:]]    #   taking only the metrics from the individual
                    win,capture = capture_rate(indPrey,indPred)
                    if win == 1:
                        predBWins+=1
                    else:
                        prey2Wins+=1

            #   retroalimentación
            vs1out = preyWins < predWins
            vs2out = prey2Wins < predBWins 
            predWon = vs1out and vs2out

            if predWon:
                #he ought to give to both the preys
                # print("predator won")
                elitePop = species[0].elite_individuals(rePopPerc)
                species[1].repopulation(elitePop)
                species[2].repopulation(elitePop)
            else:
                if not vs1out and not vs2out:
                    # print("predator lost to preys")
                    half=(rePopPerc//2)
                    elitePop1 = species[1].elite_individuals(rePopPerc)
                    elitePop2 = species[2].elite_individuals(rePopPerc)
                    elitePop1 = [x[:half] for x in elitePop1]
                    elitePop2 = [x[:half] for x in elitePop2]
                    elitePop = joinPop(elitePop1,elitePop2)
                    species[0].repopulation(elitePop)
                elif vs1out:
                    # print("prey2 lost to pred")
                    elitePop = species[1].elite_individuals(rePopPerc)
                    species[2].repopulation(elitePop)
                elif vs2out:
                    # print("prey1 lost to pred")
                    elitePop = species[2].elite_individuals(rePopPerc)
                    species[1].repopulation(elitePop)

            if numPredation == (generations/competition/2):   
                equilibrium = ((sampleSize*popSize)/10)
                if (-equilibrium <= (preyWins - predWins)  <= equilibrium) and (-equilibrium <= (prey2Wins - predWins )  <= equilibrium):
                    break

            numPredation+=1
    end = time.time()
    elapsed=round(((end-start_time)/60),2)
    
    csv_=True
    if csv_:
        now = datetime.datetime.now()
        version = now.strftime("%m%d %H%M%S")
        eliteSize=round((rePopPerc/100)*popSize)

        route = f'Experimentacion\\UCI_1_{generations}_10.csv'

        with open(route, 'w', newline='') as csv_out:
            #   Create a CSV writer
            writer = csv.writer(csv_out)
            #   set time
            now = datetime.datetime.now()
            version = now.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([f' gen: {generations}, pop_size={popSize}, repopPercentage={rePopPerc}'])
            writer.writerow([f'generation it ended',generation])
            

            #   Headings
            heading = ['chromosome','acc','auc','f1']
            writer.writerow(heading)
            elite = round((rePopPerc/100)*popSize)
            for S in species:
                population = S.population
                for ind in range(elite):
                    individual = list()
                    for element in population:
                        individual.append(element[ind])
                    writer.writerow(individual)
            writer.writerow([elapsed])
    print(round((end - start_time)/60,2))