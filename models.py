#   module where prediction is done, other classifiers can be add
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

class Models:
    def __init__(self,X_train,y_train,X_test):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        
        
    def Select_model(self,model):
        #   wbcd (diagnostic)
        self.y_train = self.y_train.astype(int)
        #______________________________________
        if model == "SVM":
            y_pred=self.SVM()

        elif model == "RF":
            y_pred=self.RF()

        if model == "KNN":
            y_pred=self.KNN()
        
        return y_pred
    
    def SVM(self):
        try:
            modelo_svm = SVC() #   revisar aqui la hiperparametrizacion
            modelo_svm.fit(self.X_train, self.y_train)
        except ValueError:
            return 'null'
        y_pred = modelo_svm.predict(self.X_test)

        return y_pred
    
    def RF(self):
        try:
            modelo_RF = RandomForestClassifier() #   revisar aqui la hiperparametrizacion
            modelo_RF.fit(self.X_train, self.y_train)
        except ValueError:
            return 'null'
        y_pred = modelo_RF.predict(self.X_test)

        return y_pred
        
    def KNN(self):
        try:
            modelo_KNN = KNeighborsClassifier() #   revisar aqui la hiperparametrizacion
            modelo_KNN.fit(self.X_train, self.y_train)
        except ValueError:
            return 'null'
        y_pred = modelo_KNN.predict(self.X_test)

        return y_pred