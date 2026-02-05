# #rank populations for each individual
# #competencia aqui (diversity tells me how many times a better child was not created (maximum 2 by generation))
#         d1=s1.diversity.copy()
#         d2=s2.diversity.copy()
# #this one goes inside the if _//5==0 : 
#             if (d1[-5:].count(False))>=3 or (d2[-5:].count(False))>=3:
#                 population1 = s1.topsis()
#                 population2 = s2.topsis()

#                 #determine how many individuals are the 10%
#                 percent=size//10
                
#                 # add best individuals of each species into a pool population
#                 for c,acc,auc,f1 in zip(population1[0][:percent],population1[1][:percent],population1[2][:percent],population1[3][:percent]):
#                     shared_population[0].append(c)
#                     shared_population[1].append(acc)
#                     shared_population[2].append(auc)
#                     shared_population[3].append(f1)
#                     shared_population[4].append(1)
#                 for c,acc,auc,f1 in zip(population2[0][:percent],population2[1][:percent],population2[2][:percent],population2[3][:percent]):
#                     shared_population[0].append(c)
#                     shared_population[1].append(acc)
#                     shared_population[2].append(auc)
#                     shared_population[3].append(f1)
#                     shared_population[4].append(2)
                
#                 #apply ranking to the pool population
#                 shared_population = topsis_ranking(population=shared_population,shared=True) #they chop the part where i say who is the winner species
                
#                 #log of which species had the most contribution
#                 if shared_population[-1][:percent//2].count(1) > shared_population[-1][:percent//2].count(2):
#                     winners.append(1)
#                 else:
#                     winners.append(2)

#                 #delete the last column for the "species" as i already kept the log 
#                 del shared_population[-1]

#                 # chop shared population to only the 10% best, store it in "elite population" by individual of the form (chromosome, acc,auc,f1), this log is reloaded each time the competition criteria is met
#                 elite_population=[]
#                 for i in range (percent):
#                     elite_population.append([])
#                     elite_population[i]=[shared_population[_][i] for _ in range (len(shared_population))]
                
#                 #mix population, call update population
#                 for individual in elite_population:
#                     s1.repopulate(individual)
#                     s2.repopulate(individual)