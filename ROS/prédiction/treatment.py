import generation
import numpy as np
import pandas as pd 
import seaborn as sns

def importData(nomFichier):
    try :
        return pd.read_csv(nomFichier, delimiter=',')
    except :
        print("no file named "+nomFichier+ " exists")
        g=input('Do you want generate file ? (y/n)')
        if(g.upper()='Y'):
            dataGen=generation.GenData(10000)
            dataGen.generateData()
            dataGen.simuleOutput()
            dataGen.saveCSV('simulateGenData')
        else :
            return None

class treatment:
    def __init__(self, data):
        self.data=data #de type pandas dataFrame

    def plot(self, colonne):
        
if __name__ == "__main__":
    data=importData('simulateGenData.csv')
    if(data!=None):
        treat=treatment(data)