"""
    module where preprocessing is done
    none of the functions return anything
    _______
    wbdc: D:\Fedra\iCloudDrive\Mcc\Tesis\Instancias\DS_breast+cancer+wisconsin+diagnostic\wdbc.csv
    bcuci: D:\Fedra\iCloudDrive\Mcc\Tesis\Instancias\\bcuci_yugos\\breast-cancer.csv
    coimbria: D:\Fedra\iCloudDrive\Mcc\Tesis\Instancias\\breast_cancer_coimbra\dataR2.csv [1,0,1,0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1]
    seer: D:\Fedra\iCloudDrive\Mcc\Tesis\Instancias\seer_breast\SEER_excelEDIT.csv

    _______________________
    edit 28/09/2025: previous versions of this only work for wisconsin breast cancer 
"""
import csv
import copy
import pandas as pd
import numpy as np

#data processing libraries
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

class Preprocessing:
    def __init__(self, path):
        self.path = path #  path to the csv 

        self.df = None  #   data frame for the unprocess data
        self.X = None
        self.features = None    #   int, number of features

        self.chromosome = None  #   features
        self.X_chromosome = None #  selected features

    #   read CSV and turn into a dataframe
    def ReadCSV(self):
        #wisconsin
        self.df = pd.read_csv(self.path, header=None) #0: bc_coimbra,seer   |   None: wbdc, bc_uci

    #   target & feature split 
    # # (WBCD)
    # def TF_Split(self):
    #     #   WBC
    #     self.df.iloc[:,1] = self.df.iloc[:,1].map({'M': 1, 'B': 0}) #   Convertir la columna 'Diagnóstico' a valores numéricos
    #     self.y=self.df.iloc[:,1].copy() # set target column into its own df
        
    #     self.X=self.df.drop(self.df.columns[[0,1]], axis=1).copy() #dropping id[0] and target[1]
    #     self.features = len(self.X.columns)

    # # (bc coimbra)
    # def TF_Split(self):
    #     self.y=self.df.iloc[:,-1].copy() # set target column into its own df
        
    #     self.X=self.df.drop(self.df.columns[[-1]], axis=1).copy() #dropping id[0] and target[1]
    #     self.features = len(self.X.columns)
    
    # (SEER)
    # def TF_Split(self):
    #     self.y=self.df.iloc[:,-1].copy() # set target column into its own df
        
    #     self.X=self.df.drop(self.df.columns[[-1]], axis=1).copy() #dropping id[0] and target[1]
    #     self.features = len(self.X.columns)
    
    #bcuci_yugos
    def TF_Split(self):
        #mid point for range characteristics
        for age,tumor,node,i in zip(self.df[1],self.df[3],self.df[4],range(len(self.df[3]))):
            start, end = map(int, age.split('-'))
            self.df.iloc[i,1] = (start + end) / 2
            start, end = map(int, tumor.split('-'))
            self.df.iloc[i,3] = (start + end) / 2
            start, end = map(int, node.split('-'))
            self.df.iloc[i,4] = (start + end) / 2
        
        # set target column into its own df, and apply label encoder
        self.y=self.df.iloc[:,0].copy() 
        
        #dropping  target at [0] 
        self.X=self.df.drop(self.df.columns[0], axis=1).copy() 
        self.features = len(self.X.columns)

    #   chromosome feature selection    
    def Chromosome_FS(self):
            chromosome = np.array(self.chromosome)
            features=self.X.columns[chromosome.astype(bool)]
            self.X_chromosome=self.X[features].copy()
        
    #   treat missing values, this is assuming there are no missing values on the target column
    def Missing_values(self):
        #   Treat missing values
        for col in self.X.columns:
            if self.X[col].isnull().sum() == 0:# Verifica si hay NaN en la columna, si no hay continua con la siguiente
                continue  
            else: #si hay nan, lo evalua y rellena
                if self.X[col].dtype == 'object':  # Para columnas categóricas
                        self.X[col].fillna(self.X[col].mode()[0], inplace=True)  # Rellenar con la moda
                else: #columnas númericas
                    self.X[col].fillna(self.X[col].mean(), inplace=True)  # Rellenar con la media
    
    #   Outlier detection with IQR
    def Outlier_detection(self):
        Q1 = self.X.select_dtypes(include=['number']).quantile(0.25)
        Q3 = self.X.select_dtypes(include=['number']).quantile(0.75)
        IQR = Q3 - Q1

        # Alinear los DataFrames antes de la comparación
        left, right = self.X.align(Q1 - 1.5 * IQR, axis=1, copy=False)
        lower_outliers = left < right  # Outliers por debajo del umbral

        left, right = self.X.align(Q3 + 1.5 * IQR, axis=1, copy=False)
        upper_outliers = left > right  # Outliers por encima del umbral

        # Filtrar los datos para eliminar los outliers
        self.X = self.X[~(lower_outliers | upper_outliers).any(axis=1)]
        #self.y = self.y.loc[self.X.index] #Leave indexes needed and drop the rest
        self.y = self.y[self.X.index] #for BC_coimbria
        #__________________________

    #   standarization
    #   wbdc
    # def Standardization(self):
        # #   Seleccionar columnas categoricas
        # num_cols = self.X.select_dtypes(include=['number']).columns  # Solo numéricos

        # #   label encoder
        # le = LabelEncoder()
        # for col in self.X.select_dtypes(exclude=['number']).columns:
        #     self.X[col] = le.fit_transform(self.X[col])

        # #   standard scalation
        # escalador = StandardScaler()
        # self.X[num_cols] = escalador.fit_transform(self.X[num_cols])
        
    #   bc_uci
    def Standardization(self):
        #   Seleccionar columnas 
        obj_cols = self.X.columns

        #   label encoder
        le = LabelEncoder()
        for col in obj_cols:
            self.X[col] = le.fit_transform(self.X[col])
        self.y = le.fit_transform(self.y)

    
    def Preprocess(self):
        self.ReadCSV()
        self.TF_Split()
        self.Missing_values()
        self.Standardization()
        # self.Outlier_detection() #    uncomment: wbdc,bc_coimbria,seer  |    comment for bc_uci

if __name__ == "__main__":
    print("Preprocessing starting...")
    test = Preprocessing(path='D:\Fedra\iCloudDrive\Mcc\Tesis\Instancias\\breast_cancer_uci\\breast_cancer.csv') #double bacl slash bc of the letter b? \\b
    # test.chromosome=[1,0,1,0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1]
    test.ReadCSV()
    test.TF_Split()
    print(test.df)
    test.Missing_values()
    print(test.df)
    print(test.X)
    test.Standardization()
    print(test.X)
    test.Outlier_detection()
    print(test.X)
    # test.Chromosome_FS()
    # print(test.X_chromosome)