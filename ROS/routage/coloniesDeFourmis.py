import numpy as np
import random
import matplotlib.pyplot as plt
import graf
#algorithme de colonies de fourmis 
#comme le nom l'indique, le but est d'imiter le comportement d'une colonie de formis.Les fourmis se déplacent 
#sur la graf et laisse une quantité de phéromone sur le chemin inversement propotionel au cout du chemin. 

class Cf: 
    def __init__(self, graf:np.array, A:list, B:list): 
        self.graf=graf 
        #initialisation 
        self.A=A #pt coordonnee depart ij 
        self.B=B #pt coordonnee arrive ij 
        self.nbfourmis=0
        self.best=[]

    def generation(self, T:int,nbfourmis:int): 
        self.nbfourmis=nbfourmis
        for l in range(T): 
            for i in range(self.nbfourmis): 
                passage=[] #liste des pts de passages de chaque fourmis 
                passage.append(self.A) 
                #on choisi une des cases autour 
                #print(passage[-1][0] != self.B[0] or passage[-1][1] != self.B[1])
                while (passage[-1][0] != self.B[0] or passage[-1][1] != self.B[1]): #si on arrive a la fin
                    #print(passage[-1], self.B)
                    try :
                        passage.append(self.choixCellule(passage[-1],1))
                    #    print("how ? ")
                    except:
                        passage.pop(-1)
                        passage.append(self.choixCellule(passage[-1],1))
                    if(passage[-1][0]<0 or passage[-1][1]<0):
                        passage.pop(-1)
                self.posePheromones(passage,10)
                self.best=passage
                #print("YES", len(passage))
            self.evaporation(0.01)

    def choixCellule(self, T:list, m:int)->list:
        """T : current cellule
        m : methode de choix de cellule
                1 : la meillieur
                2 : tirage aléatoire entre les meillieurs"""
        #I=[[T[-1][0]+1,T[-1][1]],[T[-1][0]+1,T[-1][1]+1],[T[-1][0],T[-1][1]+1],
        #   [T[-1][0]-1,T[-1][1]+1],[T[-1][0]-1,T[-1][1]],[T[-1][0]-1,T[-1][1]-1],
        #   [T[-1][0],T[-1][1]-1],[T[-1][0]+1,T[-1][1]-1]] 
        
        Ii=self.graf.voisin
        I=[[T[0]+Ii[i][0],T[1]+Ii[i][1]] for i in range(8)]
        #I : coordonnées de la case autour 
        Q=[self.graf.CoutVoisin(T,I[i]) for i in range(8)]
        
        if(m==1):
            Q=[[Q[i],i] for i in range(8)] 
            element = lambda T : T[0] 
            Q=sorted(Q, key=element) 
            #on prend la case la plus haute en terme de pheromones 
            #si plusieurs cases ont le meme nombre de pheromones 
            i=1
            while i<len(Q):
                if Q[i-1][0]!=Q[i][0]: 
                    break
                i+=1
            #on en prend une au hasard 
            Q=[Q[j][1] for j in range(i)] 
            return I[random.choice(Q)] 
        elif(m==2):
            s=sum(Q)
            if(s!=0):
                Q=[Q[i]/s for i in range(len(Q))] #liste des couts prépondéré 
                for i in range(1,len(Q)):
                    Q[i]+=Q[i-1]
                Q[0]=0
                #Q devient une liste croisante entre 0 et 1-Q[-1] 

                r=random.random()
                l=0
                while T[l]<r: #vérifier l'inégalité
                    l+=1
                return I[l-1]
            
            else:
                return I[random.randint(0,len(I))]

    def posePheromones(self, I:list, p:float)->None:
        """I : liste des points de passage de A à B
        p coef de phéromone"""
        cout=self.graf.CoutTot(I)
        if(cout<1):
            cout=1
        for i in range(len(I)-1):
            self.graf.addCoefVoisin(I[i],I[i+1],p/cout)
    
    def evaporation(self, evap:float):
        for i in range(self.graf.size[0]):
            for j in range(self.graf.size[1]):
                for e in self.graf.voisin:
                    self.graf.removeCoefVoisin([i,j],[i+e[0],j+e[1]] ,evap, True)

    def print(self):
        print(self.best)
        x=[self.best[i][0] for i in range(len(self.best))]
        y=[self.best[i][1] for i in range(len(self.best))]
        plt.plot(y, x)
        plt.show()
        
if __name__ == "__main__":
    graf=graf.Graf(100,100, 1)
    gf=Cf(graf,[50,0],[50,10]) 
    #le graf est une matrice mn où le premier plan est la piste de phéromone et le deuxième la caratéristique de la route
    gf.generation(1,1,0)
    gf.print()
 

 

 

 

 

 