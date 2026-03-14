import csv
from os import listdir
from os.path import isfile, join

#   line where it starts
start = 3
path='D:\Fedra\coevolutivo\Experimentacion\\100'

# Source - https://stackoverflow.com/a/3207973
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

for file in onlyfiles:
    with open(file, 'r', newline='') as analysis:
        reader = csv.reader(file,"csv",",")
        print(reader)