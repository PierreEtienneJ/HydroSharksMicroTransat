import numpy as np 
import time 

#algorithme de colonies de fourmis 

 

class Gf: 
    def __init__(self, graf:np.array, A:list, B:list): 
        self.graf=graf 
        #initialisation 
        self.Tmax=0 
        self.A=A #pt coordonnee depart ij 
        self.B=B #pt coordonnee arrive ij 
        self.t0=time.time()
        self.nbfourmis=0 
        self.nbfourmisE=0 #fourmis elististes 


    def generation(self, Tmax:int,nbfourmis:int, nbfourmisElitiste:int): 
        self.Tmax=Tmax 
        self.nbfourmis=nbfourmis 
        self.nbfourmisE=nbfourmisElitiste 

        self.t0=time.time() 

        while((time.time()-self.t0)<self.Tmax): 
            for i in range(self.nbfourmis): 
                passage=[] #liste des pts de passages de chaque fourmis 
                passage.append(self.A) 
                #on choisi une des cases autour 
                while passage[-1][0] != self.B[0] and passage[-1][1] != self.B[1]: #si on arrive a la fin
                    passage.append(choixCellule(passage[-1]))
                
                self.posePheromones(passage,10)
            self.evaporation(1)

    def choixCellule(self, T:list, m:int)->list:
        """T : current cellule
        m : methode de choix de cellule
                1 : la meillieur
                2 : tirage aléatoire entre les meillieurs"""
        I=[[T[-1][0]+1,T[-1][1]],[T[-1][0]+1,T[-1][1]+1],[T[-1][0],T[-1][1]+1],
           [T[-1][0]-1,T[-1][1]+1],[T[-1][0]-1,T[-1][1]],[T[-1][0]-1,T[-1][1]-1],
           [T[-1][0],T[-1][1]-1],[T[-1][0]+1,T[-1][1]-1]] 
        #I : coordonnées de la case autour 
        Q=[self.graf[1,I[i][0],I[i][1]] for i in range(8)]
        
        if(m==1):
            Q=[[Q[i],i] for i in range(8)] 
            element = lambda T : T[0] 
            Q=sorted(Q, key=element) 
            #on prend la case la plus haute en terme de pheromones 
            #si plusieurs cases ont le meme nombre de pheromones 
            i=1 
            while(Q[i-1][0]==Q[i][0] or i<len(Q)): 
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

    def fctCout(self, T): 
        s=0 
        for e in T: 
            s=self.graf[0,e[0],e[1]] 
        return s 

    def posePheromones(self, I:list, p:float)->None:
        """I : liste des points de passage de A à B
        p coef de phéromone"""
        cout=self.fctCout(I)
        if(cout<1):
            cout=1
        for e in I:
            self.graf[1,e[0],e[1]]+=p/cout
    
    def evaporation(self, evap:float):
        (a,b,c)=self.graf.shape
        for i in range(b):
            for j in range(c):
                self.graf[1,i,j]-=evap
                if self.graf[1,i,j]<0:
                    self.graf[1,i,j]=0

if __name__ == "__main__":
    graf=np.random.rand(2,100,100)
    for i in range(100): 
        for j in range(100): 
            graf[1,i,j]=0 

    gf=Gf(graf,[50,0],[50,100]) 
    #le graf est une matrice mn où le premier plan est la piste de phéromone et le deuxième la caratéristique de la route
    
 

 

 

 

 

 