import generation

import numpy as np
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.metrics import mean_squared_error, r2_score

import operator

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

class planExp:
    def __init__(self, data):
        self.data=data
        self.size=len(data)
        self.nbParametres=[]
        self.col=['windSpd', 'windDir','swellFreq', 'swellAmpl', 'swellDir', 'streamSpd','streamDir','airT','airP','airH','waterT', 'waterS','time','sunUV','sunLux', 'sunOcta']

    def transform(self):
        for i in range(self.size):
            #on converti les données linéaire en un model par palier
            
            self.data['windSpd'].values[i]=int(self.data['windSpd'].values[i]/5) #par pas de 5
            self.data['windDir'].values[i]=int((self.data['windDir'].values[i]+180)/20) #par pas de 20 

            self.data['swellFreq'].values[i]=int(self.data['swellFreq'].values[i]/0.1) #pas de 0.1
            self.data['swellDir'].values[i]=int((self.data['swellDir'].values[i]+180)/20) #pas de 20
            self.data['swellAmpl'].values[i]=int(self.data['swellAmpl'].values[i]) #pas de 1

            self.data['streamSpd'].values[i]=int(self.data['streamSpd'].values[i]) #par pas de 1
            self.data['streamDir'].values[i]=int((self.data['streamDir'].values[i]+180)/20) #par pas de 20 

            self.data['airT'].values[i]=int(self.data['airT'].values[i]/5-1) #par pas de 5
            self.data['airP'].values[i]=int((self.data['airP'].values[i]-960)/10) #par pas de 10 
            self.data['airH'].values[i]=int((self.data['airH'].values[i])/20-1) #par pas de 20 

            self.data['waterT'].values[i]=int((self.data['waterT'].values[i])/5-1) #par pas de 5 
            self.data['waterS'].values[i]=int((self.data['waterS'].values[i])/10-2) #par pas de 10 

            self.data['time'].values[i]=int((self.data['time'].values[i])/5) #par pas de 5

            self.data['sunUV'].values[i]=int((self.data['sunUV'].values[i])/1) #par pas de 1
            self.data['sunLux'].values[i]=int((self.data['sunLux'].values[i])/300) #par pas de 100
            self.data['sunOcta'].values[i]=int((self.data['sunOcta'].values[i])/1-1) #par pas de 1

        for e in self.col:
            self.nbParametres.append(int(max(self.data[e].values)-min(self.data[e].values)))
        #print(self.nbParametres)

    def saveCSV(self, nomFichier):
        self.data.to_csv(nomFichier, index = None, header=True)

    def verifPlan(self):
        for i in range(len(self.col)-1):
            for j in range(i+1, len(self.col)):
                AB=np.zeros((self.nbParametres[i]+1,self.nbParametres[j]+1))
                print(self.col[i],self.col[j], self.nbParametres[i]+1,self.nbParametres[j]+1)
                for k in range(self.size):
                    x=int(self.data[self.col[i]].values[k])
                    y=int(self.data[self.col[j]].values[k])
                    AB[x,y]+=1


if __name__ == "__main__":
    #treat=treatment(importData('simulateGenData.csv'))
    exp=planExp(importData('simulateGenData.csv'))
    exp.transform()
    exp.saveCSV('planExp.csv')
    exp.verifPlan()
    #treat.linearRegression()
    #treat.plot(['spd'])
    #treat.polynomialRegression()