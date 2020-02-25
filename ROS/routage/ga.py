import numpy as np
import random
import math
import matplotlib.pyplot as plt
##source ALGORITHMES GENETIQUES Présenté par Souquet Amédée Radet Francois-Gérard

class Ga :
    def __init__(self, A:"depart", B:"porte arrivee", largeurRoute:float):
        self.nbwaypoints=None                                  #nb de points par cellules
        self.nbCellules=None                                   #nb de cellules de l'algo
        self.nbGenerations=None                                #nb de génération
        self.generation=None
        self.A=A                                            #point initial 
        self.B=B                                            #porte finale [[x1, y1],[x2, y2]]
        self.largeurRoute=largeurRoute                      #largeur de la route (évite que le bateau sorte)
        self.Bm=[(B[0][0]+B[1][0])/2, (B[0][1]+B[1][1])/2]  #centre de la porte
        
        self.listDistance=None       #listDistance[i]=distance en projection sur x1 du iem waypoints i=0 -> A, /!\ le dernier wayoints n'est pas dans la liste
        self.BestCout=[]
    
    def gen(self,nbCellules:int, nbGenerations:int, mEvol:int, mChoix:int):
        self.setNbWaypoint()   #nb de waypoint générer pour tracer la route                
        self.nbCellules=nbCellules
        self.nbGenerations=nbGenerations
        self.generation=np.zeros((self.nbwaypoints+1,self.nbCellules)) #on travaille en 1D dans le repère de la route le dernier élément est le cout de la cellule
        
        #################
        # Initilisation #
        #################
        for k in range(self.nbCellules):                               #on crée les premières cellules                                
            for i in range(0,self.nbwaypoints-1):
                self.generation[i,k]=random.random()*self.largeurRoute-self.largeurRoute/2;    #tire la 1er génération
            self.generation[i,k]=random.random()*math.sqrt(math.pow(self.B[0][0]-self.B[1][0],2)+math.pow(self.B[0][1]-self.B[1][1],2))-math.sqrt(math.pow(self.B[0][0]-self.B[1][0],2)+math.pow(self.B[0][1]-self.B[1][1],2))/2
            #le dernier waypoint
            self.fctCout(k) #la dernière case est le cout
        self.BestCout.append(self.generation[self.nbwaypoints, 0])
        
        for g in range(self.nbGenerations-1):
            #####################
            # reproduction      #
            #####################
            self.reproduction(1, self.choixCellules(self.nbCellules//2+1,mChoix)) #croissement cellulaire
            #self.reproduction(2) #mutation
            
            
            #############
            # Evolution # 
            #############
            #self.evolution(mEvol)  #évolution avec une certaine méthode

            #calcul du cout de chaque cellules
            for j in range(self.nbCellules): 
                self.fctCout(j)             #mise à jour du cout
            
            element = lambda T: T[0]
            T=[[self.generation[self.nbwaypoints,i],i]  for i in range(self.nbCellules)]
            T=sorted(T,key=element,reverse=False) #on fait le trie sur le cout des cellules
            self.BestCout.append(T[0][0])
             
    def setNbWaypoint(self)->"void":
        """Cela permet de set automatiquement le nb de waypoint. La distance en projection sur x1 entre 
        deux waypoints est une fonction croissante (type ln)
        Le dernier waypoint est sur l'axe B[0], B[1] donc la distance entre l'avant dernier waypoint et le suivant est variable suivant la cellule
        
        Il y a donc au moins un waypoint : celui sur l'axe B[0], B[1]"""
        self.listDistance=[0]
        A=1
        B=2
        C=1
        i=1
        while(self.listDistance[-1]<math.sqrt(math.pow(self.A[0]+self.Bm[0],2)+math.pow(self.A[1]+self.Bm[1],2))):
            self.listDistance.append(self.listDistance[-1]+C*math.log(A*i+B))
            i+=1
        self.nbwaypoints=i
        return True
        
    def R1ToR0(self, r:float, d:int)->list:
        """R1 : repère de la route
        R0 : repère terrestre
        r : largeur par rapport a la route
        d : indice de la perpendiculaire"""
        if(d!=self.nbwaypoints-1):
            alpha=math.atan2(self.A[1]-self.Bm[1],self.A[0]-self.Bm[0])
            gama=math.atan2(r, self.listDistance[d])
            return [self.listDistance[d]*math.cos(alpha)+r*math.cos(gama), self.listDistance[d]*math.sin(alpha)+r*math.sin(gama)]
        elif(d==self.nbwaypoints-1):
            alpha=math.atan2(self.A[1]-self.Bm[1],self.A[0]-self.Bm[0])
            gama=math.atan2(self.B[0][1]-self.B[1][1], self.B[0][0]-self.B[1][0])
            return [math.sqrt(math.pow(self.A[0]+self.Bm[0],2)+math.pow(self.A[1]+self.Bm[1],2))*math.cos(alpha)+math.sqrt(math.pow(self.B[0][1]-self.B[1][1],2)+math.pow(self.B[0][0]-self.B[1][0],2))*math.cos(gama), math.sqrt(math.pow(self.A[0]+self.Bm[0],2)+math.pow(self.A[1]+self.Bm[1],2))*math.sin(alpha)+math.sqrt(math.pow(self.B[0][1]-self.B[1][1],2)+math.pow(self.B[0][0]-self.B[1][0],2))*math.sin(gama)]
        
        return None

    def fctCout(self, k:int):
        """k : indice de la cellule"""
        s=0 #longueur du chemin
        p=self.A
        for j in range(self.nbwaypoints):
            w=self.R1ToR0(self.generation[j,k], j)
            s+=math.sqrt((w[0]-p[0])**2+(w[1]-p[0])**2)
            p=w    
        self.generation[self.nbwaypoints, k]=s
    
    def choixCellules(self, k:int, m:int)->list:
        """choisi les numéros des k cellules à garder 
        en utilisant la methode m:
        1 : Sélection par rang (on prend les k meilleurs)
        2 : Probabilité de sélection proportionnelle à l'adaptation (on en prend k aléatoirement prépondérant a sa fct cout)
        3 : Sélection par tournoi 1vs1 jusqu'a ce qu'il en reste k
        4 : Sélection uniforme
        """
        T=[self.generation[self.nbwaypoints,i] for i in range(self.nbCellules)] #liste des couts
        
        if(m==1):#trie sur les indices
            T=[[T[i],i] for i in range(self.nbCellules)] #liste des couts avec indice
            element = lambda T: T[0]
            T=sorted(T,key=element,reverse=False) #on fait le trie sur la 1er colone de la matrice
            indice=[T[i][1] for i in range(len(T))] #on sort les indices
            return indice[0:k-1] #on en garde que k

        elif(m==2):
            somme=sum(T)
            T=[T[i]/somme for i in range(self.nbCellules)] #liste des couts prépondéré 
            for i in range(1,len(T)):
                T[i]+=T[i-1]
            T[0]=0
            #T devient une liste croisante entre 0 et 1-T[-1] 
            retour=[]
            for i in range(k):
                r=random.random()
                l=0
                while T[l]<r: #vérifier l'inégalité
                    l+=1
                retour.append(l-1)
            return retour
            
        elif(m==3):
            indice=[i for i in range(self.nbCellules)]
            retour=[]
            proba=0.7
            while len(proba)<k:            #complexite nbCellule-k
                t=random.choices(indice,k=2) #prend 2 cellules
                if(T[t[0]]<T[t[1]] and random.random()<proba): #regarde la plus forte (forte=cout plus petit) avec une proba >0.5
                    retour.append(t[0])    #la plus forte reste 
                else:
                    retour.append(t[1])
            return retour

        else:  
            return random.choices([i for i in range(self.nbCellules)],k=k) #choix alléatoire
    
    def evolution(self,m:int):
        """igen : numéro de la génération en cours
        m : méthode d'évolution
        1: translation aléatoire
        2: fusion cellulaire
        """
        coef=0.1
        if(m==1): #on deplace chaque point de [-coef; coef]
            for i in range(self.nbCellules):
                for j in range(self.nbwaypoints):
                    self.generation[j, i]+=random.random()*2*coef-coef      #essayer avec la méthode du recuit simulé 
        
        elif(m==2): #fusion cellulaire : on prend deux cellules et on mixe certaine cellules dans les deux cellules
            probaFusionWaypoint=10/100  #proba de fusion
            for i in range(0,self.nbCellules,2):
                for j in range(self.nbwaypoints):
                    if(probaFusionWaypoint<random.random()):
                        self.generation[j, i+1]=(self.generation[j,i]+self.generation[j,i+1])/2 #moyenne des waypoints
                        
    def reproduction(self, m:int, indice:list=[]):
        """Avec un départ de n cellules, on en a sélectionné k donc on complètent les n-k cellules manquante
        on prend la liste des indices des cellules qu'on garde et m la méthode de reproduction"""
        if(m==1 and len(indice)>0):
            pc=0.5 #proba de corssover
            co=2 #nb de points de crossover
            #croissement génétique
            #on prend (n-k)//2 couple qui font 2 enfants, si k est impaire la cellule est gardé 
            couples=[]
            while len(indice)>2:
                c=random.choices(indice,k=1)
                indice.remove(c[0])
                d=random.choices(indice,k=1)
                indice.remove(d[0])
                couples.append([c[0], d[0]])

                
            for C in couples:
                #on calcul les points de crossover : on inverse avant et après les points (cf source 1 p17)
                prs=0
                for e in range(co):
                    t=random.sample([i for i in range(self.nbwaypoints-1)], co)
                    t.sort()
                    t.append(self.nbwaypoints)
                    for k in range(co-1):
                        if(random.random()>pc): #proba que les waypoints s'inversent
                            for i in range(t[k], t[k+1]):
                                self.generation[i, C[0]],self.generation[i, C[1]]=self.generation[i, C[1]],self.generation[i, C[0]]
        
        elif(m==2):
            ##mutation
            pm=0.01
            coef=0.01 #coef de mutation
            for j in range(self.nbCellules):
                for i in range(self.nbwaypoints):
                    if(pm>random.random()):
                        self.generation[i,j]+=random.random()*coef-coef/2
                        
                        #on vérifie qu'on sort pas de la route
                        if(self.generation[i,j]>self.largeurRoute):
                            self.generation[i,j]=self.largeurRoute
                        elif(self.generation[i,j]<-self.largeurRoute):
                            self.generation[i,j]=-self.largeurRoute
            
        #elif(m==3):
        ## on copie les première cellules cela permet de mieux suivre l'évolution
        #    for j in range(self.nbCellules):   #on complète l'algo
        #        for i in range(self.nbwaypoints):   
        #            if(j not in c):
        #                l=random.choices([i for i in range(self.nbCellules)],k=1)
        #                self.generation[i,j]=self.generation[i,l[0]]
        #        self.fctCout(j)
        
    def resultat(self):
        element = lambda T: T[0]
        T=[[self.generation[self.nbwaypoints,i],i]  for i in range(self.nbCellules)]
        T=sorted(T,key=element,reverse=False) #on fait le trie sur le cout des cellules
        return [self.generation[j,T[0][1]] for j in range(self.nbwaypoints)]

    def R1ToR0List(self, list:list)->list:
        r=[]
        for i in range(len(list)):
            r.append(self.R1ToR0(list[i],i))
        return r
        
if __name__ == "__main__":
    ga=Ga([0,0], [[0, 1000], [0,1100]], 1)
    type(ga)
    ga.gen(100, 1, 1,1)
    print(ga.nbwaypoints)
    print(ga.nbGenerations)
    r=ga.R1ToR0List(ga.resultat())
    rx=[r[i][0] for i in range(ga.nbwaypoints)]
    ry=[r[i][1] for i in range(ga.nbwaypoints)]
    #plt.plot(rx, ry, "r", [ga.A[0], ga.Bm[0]], [ga.A[1], ga.Bm[1]], "b")
    #plt.show()
    print(len(ga.BestCout))
    #plt.plot([i for i in range(len(ga.BestCout))], ga.BestCout, "r")
    #plt.show()
    #plt.plot([i for i in range(len(ga.listDistance))], ga.listDistance, "r")
    #plt.show()
    #A=[ga.listDistance[i]-ga.listDistance[i-1] for i in range(1, len(ga.listDistance))]
    A=[math.log(i) for i in range(1, 100)]
    B=[0]
    for i in range(1, len(A)):
        B.append(B[-1]+A[i])
    C=[2*i-5 for i in range(1,11)]
    plt.plot([i for i in range(1,len(A)+1)], A, "r")
    plt.plot([i for i in range(1,len(B)+1)], B, "b")
    plt.plot([i for i in range(1,11)], C, "g")
    plt.show()
    pass