import generation
import numpy as np
import pandas as pd 
from sklearn.preprocessing import StandardScaler
import seaborn as sns

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
        self.X=self.df[['windSpd', 'windDir','swellFreq', 'swellAmpl', 'swellDir', 'streamSpd','streamDir','airT','airP','airH','waterT', 'waterS','time','sunUV','sunLux', 'sunOcta']]
        self.Y=self.df[['spd','drift','consumption','roll','production']] #'spd','drift','consumption','roll','production'

if __name__ == "__main__":
    data=importData('simulateGenData.csv')
    
    treat=treatment(data)
    treat.scaler()