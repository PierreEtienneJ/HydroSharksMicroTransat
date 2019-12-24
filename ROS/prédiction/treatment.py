import generation
import numpy as np
import pandas as pd 
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures 

import seaborn as sns
import matplotlib.pyplot as plt

def importData(nomFichier):
    try :
        return pd.read_csv(nomFichier, delimiter=',')
    except :
        print("no file named "+nomFichier+ " exists")
        g=input('Do you want generate file ? (y/n)')
        if(g.upper()=='Y'):
            dataGen=generation.GenData(10000)
            dataGen.generateData()
            dataGen.simuleOutput()
            dataGen.saveCSV('simulateGenData')
        else :
            return None

class treatment:
    def __init__(self, data):
        self.df=data #de type pandas dataFrame
        #self.X=self.df[['windSpd', 'windDir','swellFreq', 'swellAmpl', 'swellDir', 'streamSpd','streamDir','airT','airP','airH','waterT', 'waterS','time','sunUV','sunLux', 'sunOcta']]
        self.X=self.df[['windSpd']]
        #self.Y=self.df[['spd','drift','consumption','roll','production']] #'spd','drift','consumption','roll','production'
        self.Y=self.df[['spd']]
    
    def linearRegression(self):
        modeleReg=LinearRegression()
        modeleReg.fit(self.X, self.Y)

        print(modeleReg.intercept_)
        print(modeleReg.coef_)

        #calcul du R²
        R=modeleReg.score(self.X,self.Y)
        print(R)
        RMSE=np.sqrt(((self.Y-modeleReg.predict(self.X))**2).sum()/len(self.Y))

        plt.plot(self.Y, modeleReg.predict(self.X),'.')
        #plt.show()

        plt.plot(self.Y, self.Y-modeleReg.predict(self.X),'.')
        plt.show()
    
    def polynomialRegression(self):
        poly = PolynomialFeatures(degree = 10) 
        X_poly = poly.fit_transform(self.X) 
        
        poly.fit(X_poly, self.Y) 
        lin2 = LinearRegression() 
        lin2.fit(X_poly, self.Y) 

        plt.scatter(self.X, self.Y, color = 'blue') 
  
        plt.plot(self.X, lin2.predict(poly.fit_transform(self.X)), color = 'red') 
        plt.title('Plynomial Regression') 
        plt.xlabel('WindSpeed') 
        plt.ylabel('BoatSpeed') 
        plt.show() 

if __name__ == "__main__":
    treat=treatment(importData('simulateGenData.csv'))
    #treat.linearRegression()
    treat.polynomialRegression()
