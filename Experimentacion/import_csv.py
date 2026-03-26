import csv
from os import listdir
from os.path import isfile, join
import math
import pandas as pd


def dominates(a, b):
    return all(x >= y for x, y in zip(a, b)) and any(x > y for x, y in zip(a, b))


def get_pareto_front(fitness_list):
    pareto_indices = []

    for i, fit_i in enumerate(fitness_list):
        dominated = False

        for j, fit_j in enumerate(fitness_list):
            if i == j:
                continue

            if dominates(fit_j, fit_i):
                dominated = True
                break

        if not dominated:
            pareto_indices.append(i)

    return pareto_indices



start = 3   #   line where it starts
timeend=9  #   line where time is stored
path='D:\Fedra\coevolutivo\Experimentacion\\uci500\\'
#uci/bcc 9
#bcc csv 1 = 8
#wdbc 21

# Source - https://stackoverflow.com/a/3207973
onlyfiles = [path+f for f in listdir(path) if isfile(join(path, f))]

metricsSize=3
acc=1
auc=2
f1=3

table=list()
experiments=list()
time=list()
metrics=[acc,auc,f1]
outputs = [list() for i in range(metricsSize)]

files = list()



for item,file in enumerate(onlyfiles):
    if item == (len(onlyfiles)): #-1 for bcc100
        break
    else:
        with open(file, 'r', newline='') as analysis:
            reader = csv.reader(analysis, delimiter=',')
            #   get them in their own "table"
            currentFile = [list() for i in range(metricsSize)]
            for line,row in enumerate(reader):
                if line < timeend and line >= start:
                    # table.append(row)
                    for m,out in zip(metrics,outputs):
                        try:
                            out.append(float(row[m]))
                        except IndexError:
                            print(row)

                    for m, metric in zip(metrics,currentFile):
                        try:
                            metric.append(float(row[m]))
                        except IndexError:
                            print(row)
                            print(m)

                if line == timeend:
                    time.append(float(row[0]))
                
            files.append(currentFile)
    # experiments.append(table)

metricas = [list() for i in range(3)]
for num,file in enumerate(files):
    #reshape
    metrics=3
    chromosomes = list()
    for i in range(len(file[0])-1):
        currentChromosome = list()
        for metric in range(3):
            currentChromosome.append(file[metric][i])
        chromosomes.append(currentChromosome)
    #pareto dominance, getting the 3 top for each file 3*30 = 90
    pareto_idx = get_pareto_front(chromosomes)
    top3_idx = pareto_idx[:3]
    top3 = [chromosomes[i] for i in top3_idx]
    for item in top3:
        for x,met in zip(item,metricas):
            met.append(x)
    #transpose data again


for item in outputs:
    meanMetric=round(sum(item)/len(item),4)
    print(meanMetric)
finalatime=round((sum(time))/len(time),2)
print(finalatime)

for item in metricas:
    meanMetric=round(sum(item)/len(item),4)
    print(meanMetric)
finalatime=round((sum(time))/len(time),2)
print(finalatime)

