import pandas as pd 
import tensorflow as tf 
import numpy as np
from data import *
###maybe a problem with python version and pip3 version => 3.6.9, (not 3.8.1) and pip3 => 9.0.1 (et not 19.3)
#tf just in 3.7 => python3.7 -m pip install ...
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
    #print(len(pre.dataYVector[:,0]))
    #print(len(pre.dataXVector[:,0]))
    #tf
    assert hasattr(tf, "function")
    model=tf.keras.models.Sequential()
    #model.add(tf.keras.layers.Dense(32, activation="relu")) #16 neurones en entrée
    #model.add(tf.keras.layers.Dense(32,activation="relu")) #12 neurones suivant
    #model.add(tf.keras.layers.Dense(32, activation="relu")) # dernier neuroens
    #model.compile(loss='sparse_categorical_crossentropy', optimizer='sgd')#, metrics=["accuracy"]) #fct couts, Stokastique gradient descent, //
    model.add(tf.keras.layers.Dense(units=16, input_shape=[16]))
    model.add(tf.keras.layers.Dense(units=5, input_shape=[16]))
    model.compile(optimizer='sgd', loss='mean_squared_error')
    history=model.fit(pre.dataXVector, pre.dataYVector, epochs=10) #X, Y, nb d'itération
    print(history)
    modelOutput=model.predict(pre.dataXVector)
    model.summary()
    print(modelOutput, pre.dataYVector)