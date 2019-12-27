import pandas as pd 
import tensorflow as tf 
import numpy as np
from data import *

class pretreatment:
    def __init__(self,data, X, Y):
        self.nomColonnes=('windSpd', 'windDir','swellFreq', 'swellAmpl', 'swellDir', 'streamSpd','streamDir','airT','airP','airH','waterT', 'waterS','time','sunUV','sunLux', 'sunOcta', 
            'spd','drift','consumption','roll','production')
        self.data=data
        self.datasize=len(data)
        self.X=X
        self.Y=Y
        self.dataXVector=np.zeros((self.datasize, self.X))
        self.dataYVector=np.zeros((self.datasize, self.Y))
        
    def importXY(self, X, Y):
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


        

if __name__ == "__main__":
    pre=pretreatment(importData('simulateGenData.csv'), 16,5)
    pre.shape()
    pre.normalize()
    print(pre.dataXVector[0,:])
    #tf
    assert hasattr(tf, "function")
    model=tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(20, activation="relu")) #20 neurones en entrée
    model.add(tf.keras.layers.Dense(12,activation="relu")) #12 neurones suivant
    model.add(tf.keras.layers.Dense(1, activation="relu")) # dernier neuroens
    modelOutput=model.predict(pre.dataXVector[0,:])
    #print(modelOutput, pre.dataYVector[0,:])