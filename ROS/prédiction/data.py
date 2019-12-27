import generation
import pandas as pd 
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

def saveCSV(data, nomFichier):
        try : 
            data.to_csv(nomFichier, index = None, header=True)
        except :
            print("data not in pandas ")

