import pandas as pd 
import numpy as np 
from data import *

class pretreatment:
    def __init__(self,data:"panda", X:int, Y:int):
        self.nomColonnes=('windSpd', 'windDir','swellFreq', 'swellAmpl', 'swellDir', 'streamSpd','streamDir','airT','airP','airH','waterT', 'waterS','time','sunUV','sunLux', 'sunOcta', 
            'spd','drift','consumption','roll','production')
        self.data=data
        self.datasize=len(data)
        self.X=X
        self.Y=Y
        self.dataXVector=np.zeros((self.datasize, self.X))
        self.dataYVector=np.zeros((self.datasize, self.Y))
        
    def importXY(self, X:list, Y:list):
        self.dataXVector=X
        self.dataYVector=Y

    def shape(self):
        """On change la taille du model, on transforme le tableau en une suite de vecteur ligne"""
        for i in range(self.datasize):
            for j in range(self.X):
                self.dataXVector[i,j]=self.data.iloc[i].values[j]
            for k in range(self.Y):
                self.dataYVector[i,k]=self.data.iloc[i].values[self.X+k]

    def normalize(self):
        moyenne=np.zeros(self.X+self.Y)
        ecartType=np.zeros(self.X+self.Y)
       
        for k in range(self.X+self.Y):
            moyenne[k]=np.mean(self.data[self.nomColonnes[k]].values)
            ecartType[k]=np.std(self.data[self.nomColonnes[k]].values)
        for i in range(self.datasize):
            for j in range(self.X):
                self.dataXVector[i,j]=(self.dataXVector[i,j]-moyenne[j])/ecartType[j]

            for j in range(self.Y):
                self.dataYVector[i,j]=(self.dataYVector[i,j]-moyenne[self.X+j])/ecartType[self.X+j]

class planExp:
    def __init__(self, data:"panda"):
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
            self.nbParametres.append(int(max(self.data[e].values)-min(self.data[e].values)+1))
        #print(self.nbParametres)
    

    def verifPlan(self):
        print("Starting experience plan verification ")
        for i in range(len(self.col)-1):
            for j in range(i+1, len(self.col)):
                AB=np.zeros((self.nbParametres[i],self.nbParametres[j]))
                print(self.col[i],self.col[j], self.nbParametres[i],self.nbParametres[j])
                for k in range(self.size):
                    x=int(self.data[self.col[i]].values[k])
                    y=int(self.data[self.col[j]].values[k])
                    AB[x,y]+=1

        
if __name__ == "__main__":
    pre=pretreatment(importData('simulateGenData.csv'), 16,5)
    pre.shape()
    pre.normalize()
    #exp=planExp(importData('simulateGenData.csv'))
    #exp.transform()
    #saveCSV(exp.data, 'planExp.csv')
    #exp.verifPlan()
    