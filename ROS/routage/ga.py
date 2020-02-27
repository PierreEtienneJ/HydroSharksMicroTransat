import numpy as np
import random
import math
import matplotlib.pyplot as plt
import statistics
##source ALGORITHMES GENETIQUES Présenté par Souquet Amédée Radet Francois-Gérard

class Ga :
    def __init__(self, C:"depart reel", A:"depart th", B:"porte arrivee", largeurRoute:float):
        self.nbwaypoints=None                                  #nb de points par cellules
        self.nbCellules=None                                   #nb de cellules de l'algo
        self.nbGenerations=None                                #nb de génération
        self.generation=None
        self.A=A                                            #point initial théorique
        self.C=C    #pts initial
        self.B=B                                            #porte finale [[x1, y1],[x2, y2]]
        self.largeurRoute=largeurRoute                      #largeur de la route (évite que le bateau sorte)
        self.Bm=[(B[0][0]+B[1][0])/2, (B[0][1]+B[1][1])/2]  #centre de la porte
        
        self.listDistance=None       #listDistance[i]=distance en projection sur x1 du iem waypoints i=0 -> A, /!\ le dernier wayoints n'est pas dans la liste
        self.BestCout=[]
        self.meanCout=[]
    
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
                self.generation[i,k]=random.random()*2*self.largeurRoute-self.largeurRoute    #tire la 1er génération
                #self.generation[i,k]=0
            self.generation[self.nbwaypoints-1,k]=random.random()*math.sqrt(math.pow(self.B[0][0]-self.B[1][0],2)+math.pow(self.B[0][1]-self.B[1][1],2))-math.sqrt(math.pow(self.B[0][0]-self.B[1][0],2)+math.pow(self.B[0][1]-self.B[1][1],2))/2
            #le dernier waypoint
            
            self.fctCout(k) #la dernière case est le cout    
        element = lambda T: T[0]
        T=[[self.generation[self.nbwaypoints,i],i]  for i in range(self.nbCellules)]
        T=sorted(T,key=element,reverse=False) #on fait le trie sur le cout des cellules
        self.BestCout.append(T[0][0])
        self.meanCout.append(statistics.mean([T[i][0] for i in range(len(T))]))
        
        for g in range(self.nbGenerations-1):
            if(mEvol==1):
                #####################
                # reproduction      #
                #####################
                self.reproduction(1, mChoix) #croissement cellulaire
                self.reproduction(2) #mutation
            elif(mEvol==2):
                #############
                # Evolution # 
                #############
                c=self.choixCellules(self.nbCellules//2+1,mChoix)
                #on garde que les cellules choisi, les autres sont copier (ou reproduite ?)
                for j in range(self.nbwaypoints):
                    if(not j in c):
                        self.generation[:,j]=self.generation[:,random.choices(c,k=1)[0]]
                
                self.evolution(2)  #évolution avec une certaine méthode
                self.evolution(1)
            
            elif(mEvol==3):
                #####################
                # reproduction      #
                #####################
                #les enfants sont les cellules qu'on garde pas 
                choix=self.choixCellules(self.nbCellules//2+1,mChoix)
                pc=0.1 #proba de corssover
                co=2 #nb de points de crossover
                #croissement génétique
                #on prend (n-k)//2 couple qui font 2 enfants, si k est impaire la cellule est gardé 
                couples=[]
                while len(choix)>2:
                    c=random.choices(choix,k=1)
                    choix.remove(c[0])
                    d=random.choices(choix,k=1)
                    choix.remove(d[0])
                    couples.append([c[0], d[0]])

                for j in range(self.nbCellules):
                    if(not j in choix):
                        #on calcul les points de crossover : on inverse avant et après les points (cf source 1 p17)
                        C=random.choice(couples)
                        prs=0
                        for e in range(co):
                            t=random.sample([i for i in range(self.nbwaypoints-1)], co)
                            t.sort()
                            t.append(self.nbwaypoints)
                            for k in range(co-1):
                                if(random.random()>pc): #proba que les waypoints s'inversent
                                    e=random.randint(0,1)
                                    for i in range(t[k], t[k+1]):                                        
                                        self.generation[i, j]=self.generation[i, C[e]]
                self.reproduction(2)
                #self.evolution(1)
                
            #calcul du cout d# chaque cellules
            for j in range(self.nbCellules): 
                self.fctCout(j)             #mise à jour du cout
            
            element = lambda T: T[0]
            T=[[self.generation[self.nbwaypoints,i],i]  for i in range(self.nbCellules)]
            T=sorted(T,key=element,reverse=False) #on fait le trie sur le cout des cellules
            self.BestCout.append(T[0][0])
            self.meanCout.append(statistics.mean([T[i][0] for i in range(len(T))]))
             
    def setNbWaypoint(self)->"void":
        """Cela permet de set automatiquement le nb de waypoint. La distance en projection sur x1 entre 
        deux waypoints est une fonction croissante (type ln)
        Le dernier waypoint est sur l'axe B[0], B[1] donc la distance entre l'avant dernier waypoint et le suivant est variable suivant la cellule
        
        Il y a donc au moins un waypoint : celui sur l'axe B[0], B[1]"""
        a=0.05
        b=0.1
        c=1
        self.listDistance=[c]
        i=1
        while(self.listDistance[-1]<math.sqrt(math.pow(self.A[0]+self.Bm[0],2)+math.pow(self.A[1]+self.Bm[1],2))):
            self.listDistance.append(self.listDistance[-1]+a*i**2+b*i+c)
            i+=1
        self.nbwaypoints=i
        return True
        
    def R1ToR0(self, r:float, d:int)->list:
        """R1 : repère de la route
        R0 : repère terrestre
        r : largeur par rapport a la route
        d : indice de la perpendiculaire"""
        if(d<self.nbwaypoints-1): #les premiers points
            alpha=math.atan2(-self.A[1]+self.Bm[1],-self.A[0]+self.Bm[0])
            gama=math.atan2(r, self.listDistance[d])
            #return [self.listDistance[d]*math.cos(alpha)+r*math.cos(alpha+gama), self.listDistance[d]*math.sin(alpha)+r*math.sin(gama+alpha)]
            distance=math.sqrt(self.listDistance[d]**2+r**2)
            return [distance*math.cos(alpha+gama), distance*math.sin(alpha+gama)]
        elif(d==self.nbwaypoints-1): # le dernier est sur l'axe B1, B2
            alpha=math.atan2(-self.A[1]+self.Bm[1],-self.A[0]+self.Bm[0])
            beta=math.atan2(self.B[0][1]-self.B[1][1], self.B[0][0]-self.B[1][0])
            distanceRoute=math.sqrt(math.pow(self.A[0]+self.Bm[0],2)+math.pow(self.A[1]+self.Bm[1],2))
            return [distanceRoute*math.cos(alpha)+r*math.sin(beta),distanceRoute*math.sin(alpha)+r*math.sin(beta)]
        
        return None

    def fctCout(self, k:int):
        """k : indice de la cellule"""
        s=0 #longueur du chemin
        p=self.C
        for j in range(self.nbwaypoints):
            w=self.R1ToR0(self.generation[j,k], j)
            s+=math.sqrt((w[0]-p[0])**2+(w[1]-p[1])**2)
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
            while len(retour)<k:            #complexite nbCellule-k
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
            probaFusionWaypoint=50/100  #proba de fusion
            for i in range(0,self.nbCellules,2):
                for j in range(self.nbwaypoints):
                    if(probaFusionWaypoint>random.random()):
                        self.generation[j, i+1]=(self.generation[j,i]+self.generation[j,i+1])/2 #moyenne des waypoints
                        
    def reproduction(self, m:int, k:int=0):
        """Avec un départ de n cellules, on en a sélectionné k donc on complètent les n-k cellules manquante
        on prend la liste des indices des cellules qu'on garde et m la méthode de reproduction"""
        if(m==1):
            indice=self.choixCellules(self.nbCellules//2+1,k)
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
            pm=0.1
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
    
    def plot(self, show:bool=True):
        ###resultat
        r=self.R1ToR0List(self.resultat())
        rx=[self.C[0]]+[r[i][0] for i in range(self.nbwaypoints)]
        ry=[self.C[1]]+[r[i][1] for i in range(self.nbwaypoints)]
        
        plt.subplot(311)
        plt.plot(rx, ry, "-*r") #chemin
        plt.plot([self.C[0], self.Bm[0]],[self.C[1], self.Bm[1]], "m") #route direct reel
        plt.plot([self.A[0], self.Bm[0]],[self.A[1], self.Bm[1]], "b")  #centre de la route 
        plt.plot(self.C[0], self.C[1], "dm")    #pts de départ
        
        for i in range(self.nbwaypoints):
            d1=self.R1ToR0(self.largeurRoute, i)
            d2=self.R1ToR0(-self.largeurRoute, i)
            plt.plot([d1[0], d2[0]], [d1[1], d2[1]], 'y')
        
        d=self.R1ToR0List([0 for i in range(self.nbwaypoints)])
        dx=[d[i][0] for i in range(self.nbwaypoints)]
        dy=[d[i][1] for i in range(self.nbwaypoints)]
        plt.plot(dx,dy,"<y")    #projection des waypoints
        plt.plot([self.B[0][0], self.B[1][0]], [self.B[0][1], self.B[1][1]], "m")   #porte de sortie
        
        d1=self.R1ToR0(self.largeurRoute, 0)
        d2=self.R1ToR0(self.largeurRoute, self.nbwaypoints-2)
        d3=self.R1ToR0(-self.largeurRoute, 0)
        d4=self.R1ToR0(-self.largeurRoute, self.nbwaypoints-2)
        plt.plot([d1[0], d2[0]], [d1[1], d2[1]], "g")    #largeur route
        plt.plot([d3[0], d4[0]], [d3[1], d4[1]], "g")    #largeur route
        plt.title("Resultat routage pour "+ str(self.nbwaypoints)+" waypoints")
        
       
        
        plt.subplot(312)
        plt.plot([i for i in range(self.nbwaypoints+1)], [abs(self.C[0]-self.A[0])]+self.resultat(), "-ob")
        plt.title("distance par rapport à la route direct")
        
        plt.subplot(313)
        plt.plot([i for i in range(len(self.BestCout))], self.BestCout, "r")
        plt.plot([i for i in range(len(self.meanCout))], self.meanCout, "b")
        plt.plot([0, len(self.BestCout)], [math.sqrt(math.pow(self.C[0]-self.Bm[0],2)+math.pow(self.C[1]-self.Bm[1],2)), math.sqrt(math.pow(self.C[0]+self.Bm[0],2)+math.pow(self.C[1]+self.Bm[1],2))], "y")
        plt.title("évolution du cout -> cout cible :"+str(int(math.sqrt(math.pow(self.C[0]-self.Bm[0],2)+math.pow(self.C[1]-self.Bm[1],2))*100)/100))
        plt.legend(("best "+str(int(self.BestCout[-1]*10)/10),"mean "+str(int(self.meanCout[-1]*10)/10),"cible"))
        if(show):
            plt.show()
        
if __name__ == "__main__":
    ga=Ga([0,0],[0,0], [[-0.5, 30], [0.5,30]], 1)
    type(ga)
    ga.gen(100, 100, 3,1)   #pour le moment 3 1 best ou 3 3
    ga.plot()