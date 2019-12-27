# vim: set fileencoding=utf-8 :
import numpy as np
import random
import math
import csv

##le but est de générer des données aléatoires sur lequelles ont peut travailler 
class GenData :
    def __init__(self, nbData):
        self.nbData=nbData
        #imput
        self.wind=np.zeros((nbData, 2)) #vent : spd dir
        self.swell=np.zeros((nbData, 3)) #houle : freq, Amplitude, direction
        self.stream=np.zeros((nbData, 2)) #courant : spd dir
        self.air=np.zeros((nbData, 3)) # temperature pressure humidity
        self.water=np.zeros((nbData, 2)) # temperature salinity
        self.time=np.zeros(nbData) #UTC
        self.sun=np.zeros((nbData, 3)) #UV, lux, octa
    
        #output
        self.speed=np.zeros(nbData)
        self.drift=np.zeros(nbData) #dérive
        self.consuption=np.zeros(nbData) 
        self.roll=np.zeros(nbData)
        self.production=np.zeros(nbData)
    
    def generateData(self, aleatoire):
        print('Generate Data...')
        print("Chargement :")
        if(aleatoire==True or aleatoire==1):
            for i in range(self.nbData):
                if(100*i/self.nbData%10==0):
                    print(str(100*i/self.nbData)+"%  ")

                ###Vent la direction est aléatoire 
                self.wind[i,0]=np.random.exponential(scale=10, size=None) # vitesse doit être entre [0,40] qui suit une loi exponentiel, f(x, 1/B)=1/B exp(-x/B) scale=B
                self.wind[i,1]=360*random.random()-180 #direction aléatoire
                
                ###houle 
                self.swell[i,0]=1/((50-1)*random.random()+1) #freq T entre 1s et 50s
                self.swell[i,1]=10*random.random() #amlitude aléatoire entre [0, 10]
                self.swell[i,2]=360*random.random()-180 #direction aléatoire

                # courant
                self.stream[i,0]=2*random.random() #vitesse entre [0,2]
                self.stream[i,1]=360*random.random()-180 #direction aléatoire

                #air
                self.air[i,0]=(25-5)*random.random()+5# temperature en C entre 5 et 25
                self.air[i,2]=(90-30)*random.random()+30 #humidité entre 30% et 90%
                self.air[i,1]=10*np.random.randn()+1000 #pression en hPa loi normal centré en 1000 de variance 1

                #eau
                self.water[i,0]=(15-5)*random.random()+5 # temperature en C entre 5 et 15
                self.water[i,1]=0.2*np.random.randn()+30 #en PSU g/kg loi normal centré en 30 de variance 0.2

                #time 
                self.time[i]=24*random.random() #heure entre 0 et 24

                #soleil
                self.sun[i,2]=int(8*random.random()+1)

                if(not -1<self.time[i]-12<1):   #on invente une loi de génération 
                    self.sun[i,0]=1/abs(self.time[i]-12)*(4*random.random()+1)
                    self.sun[i,1]=1/abs(self.time[i]-12)*(self.sun[i][2]+1)*(700/8*random.random()+100)
                else :
                    self.sun[i,0]=(3*random.random()+1)
                    self.sun[i,1]=(self.sun[i,2]+1)*(700/8*random.random()+300)
        
        else :
            #on génère des données en fonction de courbe
            for i in range(self.nbData):
                if(100*i/self.nbData%10==0):
                    print(str(100*i/self.nbData)+"%  ")

                self.time[i]=i%24

                ###Vent
                self.wind[i,0]=abs(4*np.random.randn()+15)
                self.wind[i,1]=180*math.sin(i/5)

                 ###houle 
                self.swell[i,0]=1/((50-1)*random.random()+1) 
                self.swell[i,1]=5*math.sin(i/2)+5 
                self.swell[i,2]=180*math.sin(i/5) 

                # courant
                self.stream[i,0]=2*math.cos(i/10)+1
                self.stream[i,1]=180*math.sin(-i/5) 

                #air
                self.air[i,0]=5*math.sin(i/24) + 10
                self.air[i,2]=30*math.cos(i/24) + 60 #humidité entre 30% et 90%
                self.air[i,1]=10*np.random.randn()+1000 #pression en hPa loi normal centré en 1000 de variance 1

                #eau
                self.water[i,0]=5*math.cos(i/200) + 10 #humidité entre 30% et 90%
                self.water[i,1]=0.1*np.random.randn()+30 #en PSU g/kg loi normal centré en 30 de variance 0.2

                #soleil
                self.sun[i,2]=int(8*random.random()+1)

                if(not -1<self.time[i]-12<1):   #on invente une loi de génération 
                    self.sun[i,0]=1/abs(self.time[i]-12)*(4*random.random()+1)
                    self.sun[i,1]=1/abs(self.time[i]-12)*(self.sun[i][2]+1)*(700/8*random.random()+100)
                else :
                    self.sun[i,0]=(3*random.random()+1)
                    self.sun[i,1]=(self.sun[i,2]+1)*(700/8*random.random()+300)

        print("end generation !")

    def simuleOutput(self):
        self.__simuleSpeed()
        self.__simuleDrift()
        self.__simulateConsuption()
        self.__simulateRoll()
        self.__simulateProduction()

    def __simuleSpeed(self):
        for i in range(self.nbData):
            if(self.wind[i][0]<15) :
                self.speed[i]=1/4*self.wind[i,0]
            else :
                self.speed[i]=-1*self.wind[i,0]+15*(1/4+1)
                
            """ if(abs(self.wind[i][1])<30):
                self.speed[i]*=abs(self.wind[i,1])*1/30
            elif(abs(self.wind[i][1])<180-30):
                self.speed[i]*=abs(self.wind[i,1])*1/(150)*1.3
            else:
                self.speed[i]*=abs(self.wind[i,1])*1/180*0.9 """
    
    def __simuleDrift(self):
        for i in range(self.nbData):
            self.drift[i]=math.atan2(self.stream[i,0]*math.sin(self.stream[i,1]*np.pi/180)+self.speed[i], self.stream[i,0]*math.cos(self.stream[i,1]*np.pi/180))

    def __simulateConsuption(self):
        for i in range(self.nbData):
            self.consuption[i]=self.speed[i]+self.wind[i,0]
    
    def __simulateRoll(self):
        for i in range(self.nbData):
            self.roll[i]= -self.wind[i,1]*3/18

    def __simulateProduction(self):
        for i in range(self.nbData):
            if(self.time[i]<6 or self.time[i]>24-6):
                self.production[i]=0
            else :
                self.production[i]=self.sun[i,2]*self.sun[i,1]*self.sun[i,0]*3/100

    def saveCSV(self, nomFichier):
        with open(nomFichier+'.csv','w') as csvfile:
            csv.writer(csvfile).writerow(('windSpd', 'windDir','swellFreq', 'swellAmpl', 'swellDir', 'streamSpd','streamDir','airT','airP','airH','waterT', 'waterS','time','sunUV','sunLux', 'sunOcta', 
            'spd','drift','consumption','roll','production'))
            for i in range(self.nbData):
                csv.writer(csvfile).writerow((self.wind[i,0], self.wind[i,1], self.swell[i,0], self.swell[i,1], self.swell[i,2], self.stream[i,0], self.stream[i,1], self.air[i,0], self.air[i,1], self.air[i,2], self.water[i,0], 
                self.water[i,1], self.time[i], self.sun[i,0], self.sun[i,1], self.sun[i,2], 
                self.speed[i], self.drift[i], self.consuption[i], self.roll[i], self.production[i]))
        print('Saving Data...')

if __name__ == "__main__":
    dataGen=GenData(100)
    dataGen.generateData(False)
    dataGen.simuleOutput()
    dataGen.saveCSV('simulateGenData')

