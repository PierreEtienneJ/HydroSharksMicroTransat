import generation
import numpy as np
import pandas as pd 

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.metrics import mean_squared_error, r2_score

import operator

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
    

    def plot(self, nameCols): 
        """ self.plot(['spd']) : density of spd
            treat.plot(['spd','windSpd]') spd fonction of windSpd
        """
        if(len(nameCols)==1):
            sns.distplot(self.df[[nameCols[0]]], kde=True)

        elif(len(nameCols)==2):
            plt.scatter(treat.df[[nameCols[0]]], treat.df[[nameCols[1]]])
            plt.title(nameCols[0]+" en fonction de "+nameCols[1]) 
            plt.xlabel(nameCols[0]) 
            plt.ylabel(nameCols[1]) 
        plt.show() 

    def polynomialRegression(self):
        poly = PolynomialFeatures(degree = 10) 
        X_poly = poly.fit_transform(self.X) 
        
        poly.fit(X_poly, self.Y) 
        lin2 = LinearRegression() 
        lin2.fit(X_poly, self.Y)

        y_poly_pred = lin2.predict(X_poly)
        rmse = np.sqrt(mean_squared_error(self.Y,y_poly_pred))
        r2 = r2_score(self.Y,y_poly_pred)
        print(rmse)
        print(r2)
        plt.scatter(self.X, self.Y, color = 'blue', s=10) 
  
        plt.plot(self.X, y_poly_pred, color = 'red') 
        plt.title('Plynomial Regression') 
        plt.xlabel('WindSpeed') 
        plt.ylabel('BoatSpeed') 
        plt.show() 

if __name__ == "__main__":
    treat=treatment(importData('simulateGenData.csv'))
    #treat.linearRegression()
    treat.plot(['spd'])
    #treat.polynomialRegression()
