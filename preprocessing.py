"""
    module where preprocessing is done
    none of the functions return anything
"""
import csv
import copy
import pandas as pd
import numpy as np

#data processing libraries
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

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
        self.df = pd.read_csv(self.path, header=None)

    #   target & feature split
    def TF_Split(self):
        #   WBC
        self.df.iloc[:,1] = self.df.iloc[:,1].map({'M': 1, 'B': 0}) #   Convertir la columna 'Diagnóstico' a valores numéricos
        self.y=self.df.iloc[:,1].copy() # set target column into its own df
        
        self.X=self.df.drop(self.df.columns[[0,1]], axis=1).copy() #dropping id[0] and target[1]
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
        self.y = self.y.loc[self.X.index] #Leave indexes needed and drop the rest
        #__________________________

    #   standarization
    def Standardization(self):
        #   Seleccionar columnas categoricas
        num_cols = self.X.select_dtypes(include=['number']).columns  # Solo numéricos

        #   label encoder
        le = LabelEncoder()
        for col in self.X.select_dtypes(exclude=['number']).columns:
            self.X[col] = le.fit_transform(self.X[col])

        #   standard scalation
        escalador = StandardScaler()
        self.X[num_cols] = escalador.fit_transform(self.X[num_cols])
    
    def Preprocess(self):
        self.ReadCSV()
        self.TF_Split()
        self.Missing_values()
        self.Outlier_detection()
        self.Standardization()

if __name__ == "__main__":
    print("Preprocessing starting...")
    test = Preprocessing(path='D:\Fedra\iCloudDrive\Mcc\Tesis\Resources\DS_breast+cancer+wisconsin+diagnostic\wdbc.csv')
    test.chromosome=[1,0,1,0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1]
    test.ReadCSV()
    test.TF_Split()
    print(test.df)
    test.Missing_values()
    print(test.df)
    print(test.X)
    test.Outlier_detection()
    print(test.X)
    test.Standardization()
    print(test.X)
    test.Chromosome_FS()
    print(test.X_chromosome)