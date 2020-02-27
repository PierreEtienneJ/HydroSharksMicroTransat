import generation
import pretreatment
from data import *

import numpy as np
import pandas as pd 
#import seaborn as sns
import tensorflow as tf #version 1.5 et non 2

import operator
###maybe a problem with python version and pip3 version => 3.6.9, (not 3.8.1) and pip3 => 9.0.1 (et not 19.3)
#tf just in 3.7 => python3.7 -m pip install ...

class treatment:
    def __init__(self, data:"panda or list"):
        try :
            self.df=data #de type pandas dataFrame
            self.X=self.df[['windSpd', 'windDir','swellFreq', 'swellAmpl', 'swellDir', 'streamSpd','streamDir','airT','airP','airH','waterT', 'waterS','time','sunUV','sunLux', 'sunOcta']]
            self.Y=self.df[['spd','drift','consumption','roll','production']] #'spd','drift','consumption','roll','production
        except : #si data est de type [X,Y]
            self.X=data[0]
            self.Y=data[1]
    
   # def plot(self, nameCols): 
   #     """ self.plot(['spd']) : density of spd
   #         treat.plot(['spd','windSpd]') spd fonction of windSpd
   #     """
   #     if(len(nameCols)==1):
   #         sns.distplot(self.df[[nameCols[0]]], kde=True)

   #     elif(len(nameCols)==2):
   #         plt.scatter(treat.df[[nameCols[0]]], treat.df[[nameCols[1]]])
   #         plt.title(nameCols[0]+" en fonction de "+nameCols[1]) 
   #         plt.xlabel(nameCols[0]) 
   #         plt.ylabel(nameCols[1]) 
   #     plt.show() 

    def neuronalNetwork(self):
        model=tf.keras.models.Sequential()
        #model.add(tf.keras.layers.Dense(32, activation="relu")) #16 neurones en entrée
        #model.add(tf.keras.layers.Dense(32,activation="relu")) #12 neurones suivant
        #model.add(tf.keras.layers.Dense(32, activation="relu")) # dernier neuroens
        #model.compile(loss='sparse_categorical_crossentropy', optimizer='sgd')#, metrics=["accuracy"]) #fct couts, Stokastique gradient descent, //
        model.add(tf.keras.layers.Dense(units=16, input_shape=[16]))
        model.add(tf.keras.layers.Dense(units=5, input_shape=[16]))
        model.compile(optimizer='sgd', loss='mean_squared_error')
        history=model.fit(self.X, self.Y, epochs=10) #X, Y, nb d'itération
        print(history)
        modelOutput=model.predict(pre.dataXVector)
        model.summary()
        print(modelOutput, pre.dataYVector)
        



if __name__ == "__main__":
    pretreat=pretreatment(importData('simulateGenData.csv'))
    pretreat.shape()
    pretreat.normalize()
    treat=treatment([pretreat.dataXVector,pretreat.dataYVector])
    treat.neuronalNetwork()
    
    #treat.linearRegression()
    #treat.plot(['windSpd', 'spd'])
    #treat.plot(['windSpd'])
    #treat.polynomialRegression()

