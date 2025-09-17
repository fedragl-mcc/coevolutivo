"""classifier module, uses models.py and preprocessing.py"""
# modulo_ml.py
import time
import csv

from preprocessing import Preprocessing
from models import Models

#   data handling
import pandas as pd
import numpy as np

#data processing libraries
from sklearn.model_selection import train_test_split

#metrics Libraries
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

class Classifier:
    def __init__(self,repository_path):
        """Inicializa la clase con el archivo de datos."""
        self.repo_Path = repository_path

        #   dataframe
        self.data=None
        self.features = None    #   number of features (int)
        self.df = None          #   dataset (dataframe)
        self.X = None           #   Features (dataframe)
        self.y = None           #   Target (Series)


        #   create instance
        self.Data_preprocess()

        #   model
        self.model = "KNN"  # Chosen ML model

        #   splits
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None

        #   metrics
        self.accuracy = None
        self.auc = None
        self.f1_score = None
        self.fitness = None

    def Data_preprocess(self):
        self.data = Preprocessing(self.repo_Path)
        self.data.Preprocess()
        self.df=self.data.df
        self.X=self.data.X
        self.y=self.data.y

    #   sample splits
    def TT_split(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2)
    
    #   chromosome split
    def Chromosome_split(self,chromosome):
        self.data.chromosome=chromosome
        self.data.Chromosome_FS()
        self.X=self.data.X_chromosome.copy()

    #   classifier
    def Training (self,chromosome):
        self.Chromosome_split(chromosome)
        #    train test split
        self.TT_split()
        classifier = Models(self.X_train,self.y_train,self.X_test)
        self.y_pred =classifier.Select_model(self.model)

    def Classif_evaluation(self):
        #   answer to the "ValueError: Classification metrics can't handle a mix of unknown and binary targets"
        #had to use astype bc self.y_test is dtype=object even after .to_numpy(), also had to save it to themselves again otherwise change does not happen
        self.y_pred = self.y_pred.astype(int)    
        self.y_test = self.y_test.astype(int).to_numpy()
        #_______________  

        self.accuracy = accuracy_score(self.y_test, self.y_pred)
        self.auc = roc_auc_score(self.y_test, self.y_pred)
        self.f1_score = f1_score(self.y_test, self.y_pred)
        
if __name__ == "__main__":
    print("Machinelearning starting...")
    test = Classifier('D:\Fedra\iCloudDrive\Mcc\Tesis\Resources\DS_breast+cancer+wisconsin+diagnostic\wdbc.csv')
    chromosome=[1,0,1,0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1]
    test.Training(chromosome)
    print(test.y_train)
    print(test.X_train)
    print(test.X_test)
    print(test.y_test)
    test.Classif_evaluation()
    print(test.accuracy)
    print(test.auc)
    print(test.f1_score)